"""
export_qti.py — Export approved questions from veriqa.db as QTI 1.2 packages
for Canvas LMS import. One zip file per chapter.

Usage:
    python export_qti.py --module 1
    python export_qti.py --module 1 --chapter 2
    python export_qti.py --module 1 --status approved
    python export_qti.py --module 1 --type prelecture   (questions tagged 'prelecture')
    python export_qti.py --module 1 --type postlecture  (questions tagged 'postlecture')
    python export_qti.py --module 1 --type final        (questions tagged 'final')

When --type is given, questions are filtered by the question_tags table
(populated by the trigger in schema.sql, or by migrate_add_tags.py for
pre-existing rows). When --type is omitted, every question with the
requested status is exported regardless of tag.
"""

import sqlite3
import json
import zipfile
import os
import re
import argparse
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "veriqa.db"))
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "exports")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text):
    """Lowercase, spaces→underscores, strip non-alphanumeric/underscore chars."""
    text = text.lower().strip()
    text = re.sub(r"[\s\-]+", "_", text)
    text = re.sub(r"[^\w]", "", text)
    return text


def fix_unicode_escapes(text):
    """Replace literal \\uXXXX escape sequences with their actual Unicode characters.

    LLM-generated text is sometimes stored with JSON-style Unicode escapes
    (e.g. the 6-char sequence \\u2014) rather than the real character (—).
    This ensures they render correctly in exported HTML/XML.
    """
    if not text:
        return text
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)


def xml_attr(text):
    """Escape a string for safe use in an XML attribute value (double-quoted)."""
    if not text:
        return text
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


# XML 1.0 forbids control characters other than tab (9), LF (10), CR (13)
_INVALID_XML_CHARS = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


def sanitize_xml_text(text):
    """Remove control characters that are illegal in XML 1.0."""
    if not text:
        return text
    return _INVALID_XML_CHARS.sub('', text)


def assessment_identifier(module_number, chapter_number):
    """e.g. module1_chapter0_bank"""
    return f"module{module_number}_chapter{chapter_number}_bank"


def output_filename(module_number, chapter_number, chapter_title):
    """e.g. module_01_chapter_0_preamble.zip"""
    slug = slugify(chapter_title)
    return f"module_{int(module_number):02d}_chapter_{chapter_number}_{slug}.zip"


# ---------------------------------------------------------------------------
# XML Builders (string templates to preserve CDATA blocks exactly)
# ---------------------------------------------------------------------------

def build_manifest(ident):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{ident}_manifest"
  xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
  xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1
    http://www.imsglobal.org/xsd/imscp_v1p1.xsd">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.1.3</schemaversion>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="{ident}"
              type="imsqti_xmlv1p2/imscc_xmlv1p2/assessment"
              href="{ident}.xml">
      <file href="{ident}.xml"/>
    </resource>
  </resources>
</manifest>"""


def build_feedback_blocks(qid, feedback_correct, feedback_incorrect):
    return f"""  <itemfeedback ident="q{qid}_correct">
    <flow_mat>
      <material>
        <mattext texttype="text/html"><![CDATA[{feedback_correct}]]></mattext>
      </material>
    </flow_mat>
  </itemfeedback>
  <itemfeedback ident="q{qid}_incorrect">
    <flow_mat>
      <material>
        <mattext texttype="text/html"><![CDATA[{feedback_incorrect}]]></mattext>
      </material>
    </flow_mat>
  </itemfeedback>"""


def build_resprocessing(qid, points, correct_ident):
    return f"""  <resprocessing>
    <outcomes>
      <decvar maxvalue="{points}" minvalue="0" varname="SCORE" vartype="Decimal"/>
    </outcomes>
    <respcondition continue="No">
      <conditionvar>
        <varequal respident="response1">{correct_ident}</varequal>
      </conditionvar>
      <setvar action="Set" varname="SCORE">{points}</setvar>
      <displayfeedback feedbacktype="Response" linkrefid="q{qid}_correct"/>
    </respcondition>
    <respcondition continue="No">
      <conditionvar><other/></conditionvar>
      <setvar action="Set" varname="SCORE">0</setvar>
      <displayfeedback feedbacktype="Response" linkrefid="q{qid}_incorrect"/>
    </respcondition>
  </resprocessing>"""


def build_item_multiple_choice(q):
    qid = q["id"]
    title = q["title"]
    points = q["points"]
    question_text = q["question_text"]
    choices = json.loads(q["choices"])
    correct_idx = q["correct_answer_index"]
    feedback_correct = q["feedback_correct"]
    feedback_incorrect = q["feedback_incorrect"]
    qtype = q["type"]  # multiple_choice or true_false

    question_type_entry = (
        "true_false_question" if qtype == "true_false" else "multiple_choice_question"
    )

    # Build response labels
    labels = ""
    for i, choice_text in enumerate(choices):
        labels += f"""        <response_label ident="answer_{i}">
          <material><mattext texttype="text/html"><![CDATA[{choice_text}]]></mattext></material>
        </response_label>\n"""

    resprocessing = build_resprocessing(qid, points, f"answer_{correct_idx}")
    feedback = build_feedback_blocks(qid, feedback_correct, feedback_incorrect)

    return f"""<item ident="question_{qid}" title="{xml_attr(title)}">
  <itemmetadata>
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>question_type</fieldlabel>
        <fieldentry>{question_type_entry}</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>points_possible</fieldlabel>
        <fieldentry>{points}</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
  </itemmetadata>
  <presentation>
    <material>
      <mattext texttype="text/html"><![CDATA[{question_text}]]></mattext>
    </material>
    <response_lid ident="response1" rcardinality="Single">
      <render_choice>
{labels}      </render_choice>
    </response_lid>
  </presentation>
{resprocessing}
{feedback}
</item>"""


def build_item_numeric(q):
    qid = q["id"]
    title = q["title"]
    points = q["points"]
    question_text = q["question_text"]
    choices = json.loads(q["choices"])
    correct_idx = q["correct_answer_index"]
    correct_value = choices[correct_idx]
    tolerance = q["tolerance"]
    feedback_correct = q["feedback_correct"]
    feedback_incorrect = q["feedback_incorrect"]

    resprocessing = build_resprocessing(qid, points, correct_value)
    feedback = build_feedback_blocks(qid, feedback_correct, feedback_incorrect)

    return f"""<item ident="question_{qid}" title="{xml_attr(title)}">
  <!-- tolerance: {tolerance} (fractional) — Canvas handles via import processing -->
  <itemmetadata>
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>question_type</fieldlabel>
        <fieldentry>numerical_question</fieldentry>
      </qtimetadatafield>
      <qtimetadatafield>
        <fieldlabel>points_possible</fieldlabel>
        <fieldentry>{points}</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
  </itemmetadata>
  <presentation>
    <material>
      <mattext texttype="text/html"><![CDATA[{question_text}]]></mattext>
    </material>
    <response_num ident="response1" rcardinality="Single">
      <render_fib fibtype="Decimal"/>
    </response_num>
  </presentation>
{resprocessing}
{feedback}
</item>"""


def build_item(q):
    qtype = q["type"]
    if qtype in ("multiple_choice", "true_false"):
        return build_item_multiple_choice(q)
    elif qtype == "numeric":
        return build_item_numeric(q)
    else:
        raise ValueError(f"Unknown question type: {qtype!r} (question id={q['id']})")


def build_assessment_xml(ident, title, items_xml):
    items_block = "\n".join(f"      {line}" if not line.startswith("      ") else line
                            for item in items_xml for line in item.split("\n"))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2
    http://www.imsglobal.org/xsd/ims_qtiasiv1p2.xsd">
  <assessment ident="{ident}"
              title="{title}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>1</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
{items_block}
    </section>
  </assessment>
</questestinterop>"""


# ---------------------------------------------------------------------------
# Main export logic
# ---------------------------------------------------------------------------

def export_module(module_number, chapter_filter=None, status="approved", quiz_type=None):
    os.makedirs(EXPORTS_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        # Look up the module row
        mod_row = conn.execute(
            "SELECT id, number, title FROM modules WHERE number = ?",
            (module_number,)
        ).fetchone()
        if mod_row is None:
            print(f"[ERROR] Module {module_number} not found in database.")
            return

        module_id = mod_row["id"]
        module_num = mod_row["number"]  # integer stored in DB

        # Fetch chapters for this module (optionally filtered by chapter number)
        if chapter_filter is not None:
            chapters = conn.execute(
                "SELECT id, number, title FROM chapters WHERE module_id = ? AND number = ? ORDER BY CAST(number AS INTEGER)",
                (module_id, str(chapter_filter))
            ).fetchall()
        else:
            chapters = conn.execute(
                "SELECT id, number, title FROM chapters WHERE module_id = ? ORDER BY CAST(number AS INTEGER)",
                (module_id,)
            ).fetchall()

        if not chapters:
            print(f"[ERROR] No chapters found for module {module_number}.")
            return

        for chapter in chapters:
            chapter_id = chapter["id"]
            chapter_number = chapter["number"]
            chapter_title = chapter["title"]

            # Fetch questions. When quiz_type is given, JOIN question_tags
            # so the tag column in the DB drives selection (post-migration);
            # otherwise return everything matching status.
            if quiz_type in ("prelecture", "postlecture", "final"):
                questions = conn.execute(
                    """
                    SELECT q.id, q.title, q.type, q.question_text, q.choices,
                           q.correct_answer_index, q.points, q.tolerance,
                           q.feedback_correct, q.feedback_incorrect
                    FROM questions q
                    JOIN topics t ON q.topic_id = t.id
                    JOIN question_tags qt ON qt.question_id = q.id
                    WHERE t.chapter_id = ? AND q.status = ? AND qt.tag = ?
                    ORDER BY q.id
                    """,
                    (chapter_id, status, quiz_type),
                ).fetchall()
            else:
                questions = conn.execute(
                    """
                    SELECT q.id, q.title, q.type, q.question_text, q.choices,
                           q.correct_answer_index, q.points, q.tolerance,
                           q.feedback_correct, q.feedback_incorrect
                    FROM questions q
                    JOIN topics t ON q.topic_id = t.id
                    WHERE t.chapter_id = ? AND q.status = ?
                    ORDER BY q.id
                    """,
                    (chapter_id, status),
                ).fetchall()

            base_fname = output_filename(module_num, chapter_number, chapter_title)
            if quiz_type is not None:
                fname = base_fname[:-4] + f"_{quiz_type}.zip"
            else:
                fname = base_fname
            fpath = os.path.join(EXPORTS_DIR, fname)

            if not questions:
                print(f"[SKIP] {fname} — 0 {status} questions")
                continue

            # Build XML content
            ident = assessment_identifier(module_num, chapter_number)
            assessment_title = f"Module {module_num} \u2014 Chapter {chapter_number}: {chapter_title}"
            if quiz_type == "prelecture":
                assessment_title += " \u2014 Pre-Lecture Quiz"
            elif quiz_type == "postlecture":
                assessment_title += " \u2014 Post-Lecture Quiz"
            elif quiz_type == "final":
                assessment_title += " \u2014 Final Exam"

            items_xml = []
            for q in questions:
                q = dict(q)
                # Sanitize any literal \uXXXX escape sequences in plain text fields
                for field in ("question_text", "feedback_correct",
                              "feedback_incorrect", "title"):
                    if q.get(field):
                        q[field] = sanitize_xml_text(fix_unicode_escapes(q[field]))
                # choices is JSON: parse → fix each element → re-serialize
                # This handles both \u2014 (json.loads resolves) and \\u2014
                # (json.loads gives literal \u2014 → fix_unicode_escapes resolves)
                if q.get("choices"):
                    try:
                        parsed = json.loads(q["choices"])
                        q["choices"] = json.dumps(
                            [sanitize_xml_text(fix_unicode_escapes(c)) if isinstance(c, str) else c
                             for c in parsed],
                            ensure_ascii=False
                        )
                    except (json.JSONDecodeError, TypeError):
                        pass  # leave malformed JSON as-is
                items_xml.append(build_item(q))

            # Indent each item under <section>
            indented_items = []
            for item_xml in items_xml:
                indented = "\n".join("      " + line for line in item_xml.split("\n"))
                indented_items.append(indented)

            items_block = "\n".join(indented_items)

            assessment_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2
    http://www.imsglobal.org/xsd/ims_qtiasiv1p2.xsd">
  <assessment ident="{ident}"
              title="{xml_attr(assessment_title)}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>1</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
{items_block}
    </section>
  </assessment>
</questestinterop>"""

            manifest_xml = build_manifest(ident)

            # Write zip
            with zipfile.ZipFile(fpath, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("imsmanifest.xml", manifest_xml.encode("utf-8"))
                zf.writestr(f"{ident}.xml", assessment_xml.encode("utf-8"))

            # Validate zip contents
            with zipfile.ZipFile(fpath, "r") as zf:
                names = zf.namelist()
            assert len(names) == 2, f"Expected 2 files in zip, got {len(names)}: {names}"
            assert "imsmanifest.xml" in names
            assert f"{ident}.xml" in names

            print(f"[OK] {fname} — {len(questions)} questions")

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Export approved questions as QTI 1.2 packages.")
    parser.add_argument("--module", type=int, required=True, help="Module number to export")
    parser.add_argument("--chapter", type=int, default=None, help="Export single chapter only (chapters.number value)")
    parser.add_argument("--status", default="approved", help="Question status to export (default: approved)")
    parser.add_argument("--type", choices=["prelecture", "postlecture", "final"],
                        default=None, dest="quiz_type",
                        help="Filter by question_tags.tag (default: no tag filter)")
    args = parser.parse_args()

    export_module(args.module, chapter_filter=args.chapter, status=args.status, quiz_type=args.quiz_type)


if __name__ == "__main__":
    main()
