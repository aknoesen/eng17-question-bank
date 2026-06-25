import argparse
import sqlite3
import os
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument('--module', type=int, required=True)
parser.add_argument('--questions-per-topic', type=int, default=3,
                    dest='questions_per_topic')
args = parser.parse_args()
MODULE_ID = args.module
QUESTIONS_PER_TOPIC = args.questions_per_topic

DB_PATH = os.environ.get(
    'DB_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "veriqa.db")
)

module_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    f"module_{MODULE_ID:02d}"
)
os.makedirs(module_dir, exist_ok=True)
REPORT_PATH = os.path.join(module_dir, "review_summary.md")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def q(sql, *args):
    cur.execute(sql, args)
    return cur.fetchall()

def q1(sql, *args):
    cur.execute(sql, args)
    row = cur.fetchone()
    return row[0] if row else 0

# ── 1. Overall counts ─────────────────────────────────────────────────────────

approved_total = q1(
    "SELECT COUNT(*) FROM questions WHERE module_id=? AND status='approved'", MODULE_ID
)
rejected_total = q1(
    "SELECT COUNT(*) FROM questions WHERE module_id=? AND status='failed'", MODULE_ID
)
grand_total = approved_total + rejected_total

# ── 2. Per-chapter / per-topic breakdown ──────────────────────────────────────

chapters = q(
    "SELECT id, number, title FROM chapters WHERE module_id=? ORDER BY id", MODULE_ID
)

chapter_sections = []
global_row_num = 0
topic_row_map = {}

for ch in chapters:
    ch_id, ch_num, ch_title = ch["id"], ch["number"], ch["title"]
    ch_title_clean = ch_title.encode("utf-8", "replace").decode("utf-8")

    topics = q(
        "SELECT id, row_number, subtopic FROM topics WHERE chapter_id=? ORDER BY row_number",
        ch_id,
    )

    lines = [f"## Chapter {ch_num} — {ch_title_clean}\n"]
    lines.append("| Row | Subtopic | Approved | Rejected |")
    lines.append("|-----|----------|----------|----------|")

    ch_approved = 0
    ch_rejected = 0
    for t in topics:
        global_row_num += 1
        topic_row_map[t["id"]] = global_row_num
        subtopic = (t["subtopic"] or "").encode("utf-8", "replace").decode("utf-8")
        ta = q1("SELECT COUNT(*) FROM questions WHERE topic_id=? AND status='approved'", t["id"])
        tr = q1("SELECT COUNT(*) FROM questions WHERE topic_id=? AND status='failed'", t["id"])
        ch_approved += ta
        ch_rejected += tr
        lines.append(f"| {global_row_num} | {subtopic} | {ta} | {tr} |")

    lines.append(f"\nChapter total: {ch_approved} approved, {ch_rejected} rejected\n")
    chapter_sections.append("\n".join(lines))

# ── 3. Bloom level distribution ───────────────────────────────────────────────

bloom_levels = ["Remember", "Understand", "Apply", "Analyze"]
bloom_rows = []
for bl in bloom_levels:
    ba = q1(
        "SELECT COUNT(*) FROM questions WHERE module_id=? AND status='approved' AND bloom_level=?",
        MODULE_ID, bl,
    )
    br = q1(
        "SELECT COUNT(*) FROM questions WHERE module_id=? AND status='failed' AND bloom_level=?",
        MODULE_ID, bl,
    )
    bloom_rows.append((bl, ba, br))

# ── 4. Difficulty distribution ────────────────────────────────────────────────

diff_rows = []
for d in range(1, 5):
    da = q1(
        "SELECT COUNT(*) FROM questions WHERE module_id=? AND status='approved' AND difficulty=?",
        MODULE_ID, d,
    )
    dr = q1(
        "SELECT COUNT(*) FROM questions WHERE module_id=? AND status='failed' AND difficulty=?",
        MODULE_ID, d,
    )
    diff_rows.append((d, da, dr))

# ── 5. Topics needing attention ───────────────────────────────────────────────

all_topics = q(
    """
    SELECT t.id, t.subtopic, t.chapter_id
    FROM topics t
    JOIN chapters c ON t.chapter_id = c.id
    WHERE c.module_id=?
    ORDER BY t.chapter_id, t.row_number
    """,
    MODULE_ID,
)

need_attention = []
for t in all_topics:
    tid = t["id"]
    subtopic = (t["subtopic"] or "").encode("utf-8", "replace").decode("utf-8")
    rn = topic_row_map.get(tid, "?")
    ta = q1("SELECT COUNT(*) FROM questions WHERE topic_id=? AND status='approved'", tid)
    tr = q1("SELECT COUNT(*) FROM questions WHERE topic_id=? AND status='failed'", tid)
    if ta < QUESTIONS_PER_TOPIC:
        needed = QUESTIONS_PER_TOPIC - ta
        need_attention.append((rn, subtopic, ta, tr, f"Regenerate {needed}"))

# ── 6. Rejected questions detail ─────────────────────────────────────────────

rejected_qs = q(
    """
    SELECT t.id AS topic_id, t.subtopic, q.id AS question_id, q.question_number
    FROM questions q
    JOIN topics t ON q.topic_id = t.id
    WHERE q.module_id=? AND q.status='failed'
    ORDER BY t.chapter_id, t.row_number, q.question_number
    """,
    MODULE_ID,
)

# ── Assemble report ───────────────────────────────────────────────────────────

lines = []
lines.append(f"# Module {MODULE_ID} Question Bank — Review Summary")
lines.append("Course: ENG17")
lines.append(f"Generated: {date.today().isoformat()}")
lines.append(f"Questions per topic target: {QUESTIONS_PER_TOPIC}")
lines.append("")

# 1
lines.append("---")
lines.append("")
lines.append("## 1. Overall Counts")
lines.append("")
lines.append("| Status   | Count |")
lines.append("|----------|-------|")
lines.append(f"| Approved | {approved_total} |")
lines.append(f"| Rejected | {rejected_total} |")
lines.append(f"| Total    | {grand_total} |")
lines.append("")

# 2
lines.append("---")
lines.append("")
lines.append("## 2. Results by Chapter")
lines.append("")
for sec in chapter_sections:
    lines.append(sec)

# 3
lines.append("---")
lines.append("")
lines.append("## 3. Bloom Level Distribution")
lines.append("")
lines.append("| Bloom Level | Approved | Rejected |")
lines.append("|-------------|----------|----------|")
for bl, ba, br in bloom_rows:
    lines.append(f"| {bl} | {ba} | {br} |")
lines.append("")

# 4
lines.append("---")
lines.append("")
lines.append("## 4. Difficulty Distribution")
lines.append("")
lines.append("| Difficulty | Approved | Rejected |")
lines.append("|------------|----------|----------|")
for d, da, dr in diff_rows:
    lines.append(f"| {d} | {da} | {dr} |")
lines.append("")

# 5
lines.append("---")
lines.append("")
lines.append("## 5. Topics Needing Attention")
lines.append("")
if need_attention:
    lines.append("| Row | Subtopic | Approved | Rejected | Action Needed |")
    lines.append("|----|----------|----------|----------|---------------|")
    for rn, subtopic, ta, tr, action in need_attention:
        lines.append(f"| {rn} | {subtopic} | {ta} | {tr} | {action} |")
else:
    lines.append(f"All topics have {QUESTIONS_PER_TOPIC} approved questions. No regeneration needed.")
lines.append("")

# 6
lines.append("---")
lines.append("")
lines.append("## 6. Rejected Questions Detail")
lines.append("")
if rejected_qs:
    lines.append("| Row | Subtopic | Q# | Rejection Reason |")
    lines.append("|----|----------|----|-----------------|")
    for rq in rejected_qs:
        tid = rq["topic_id"]
        subtopic = (rq["subtopic"] or "").encode("utf-8", "replace").decode("utf-8")
        rn = topic_row_map.get(tid, "?")
        qnum = rq["question_number"]
        lines.append(f"| {rn} | {subtopic} | {qnum} | Marked failed during review |")
else:
    lines.append("No questions were rejected.")
lines.append("")

report = "\n".join(lines)

# ── Write file ────────────────────────────────────────────────────────────────

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)

line_count = report.count("\n") + 1
print(f"\nReport written to: {os.path.abspath(REPORT_PATH)}")
print(f"Total lines: {line_count}")
print("\n" + "=" * 70)
print(report)

conn.close()
