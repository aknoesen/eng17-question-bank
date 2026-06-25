"""
fix_unicode_escapes.py — Find and fix literal \\uXXXX escape sequences in veriqa.db.

These appear when LLM-generated text containing Unicode escapes (e.g. \\u2014 for —)
is stored in the database without being fully decoded.

Two storage patterns are handled:
  - Plain text fields (question_text, feedback_*): literal \\uXXXX in the string
  - choices JSON field: parsed first, each element fixed, then re-serialized with
    ensure_ascii=False.  This correctly handles both \\u2014 (JSON escape) and
    \\\\u2014 (escaped backslash + literal u-digits) inside the stored JSON.

This script:
  1. Creates a timestamped backup of veriqa.db before making any changes
  2. Scans all text fields in the questions table
  3. Replaces literal \\uXXXX sequences with their actual Unicode characters
  4. Reports every change made

Usage:
    python fix_unicode_escapes.py [--dry-run]
"""

import sqlite3
import shutil
import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone

# Ensure stdout can handle full Unicode on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_PATH = os.path.join(os.path.dirname(__file__), "veriqa.db")

# Plain text fields (stored as-is, not JSON)
TEXT_FIELDS = ["title", "question_text", "feedback_correct", "feedback_incorrect"]

# JSON array field — needs parse/fix/re-serialize treatment
JSON_FIELDS = ["choices"]


def decode_unicode_escapes(text: str) -> tuple[str, int]:
    """
    Replace all literal \\uXXXX sequences in `text` with their Unicode characters.
    Returns (fixed_text, count_of_replacements).
    """
    count = 0

    def replacer(m):
        nonlocal count
        count += 1
        return chr(int(m.group(1), 16))

    fixed = re.sub(r'\\u([0-9a-fA-F]{4})', replacer, text)
    return fixed, count


def fix_choices_json(raw: str) -> tuple[str, int]:
    """
    Fix \\uXXXX sequences inside a choices JSON array.

    Strategy: parse the JSON (so \\u2014 → — and \\\\u2014 → literal \\u2014
    are both fully decoded into Python strings), then apply decode_unicode_escapes
    to each element (catches the \\\\u2014 → \\u2014 → — case), then re-serialize
    with ensure_ascii=False so real Unicode characters are stored directly.
    """
    if not raw:
        return raw, 0
    try:
        choices = json.loads(raw)
    except json.JSONDecodeError:
        # Malformed JSON: fall back to plain-text fix
        return decode_unicode_escapes(raw)

    total = 0
    fixed_choices = []
    for item in choices:
        if isinstance(item, str):
            fixed_item, n = decode_unicode_escapes(item)
            total += n
            fixed_choices.append(fixed_item)
        else:
            fixed_choices.append(item)

    if total > 0:
        # Re-serialize: separators keep compact form, ensure_ascii=False stores real chars
        return json.dumps(fixed_choices, ensure_ascii=False, separators=(", ", ": ")), total
    else:
        return raw, 0


def backup_database(db_path: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = db_path + f".backup_{ts}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def first_occurrence_context(text: str, width: int = 40) -> str | None:
    """Return a short snippet around the first \\uXXXX in text, or None."""
    m = re.search(r'\\u[0-9a-fA-F]{4}', text)
    if not m:
        return None
    start = max(0, m.start() - width)
    end = min(len(text), m.end() + width)
    return text[start:end]


def main():
    parser = argparse.ArgumentParser(description="Fix literal Unicode escapes in veriqa.db")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report changes without writing to the database")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found: {DB_PATH}")
        return

    # --- Backup first ---
    if not args.dry_run:
        backup_path = backup_database(DB_PATH)
        print(f"[BACKUP] {backup_path}")
    else:
        print("[DRY-RUN] No changes will be written.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    total_fields_fixed = 0
    total_rows_fixed = 0

    try:
        rows = conn.execute("SELECT id FROM questions ORDER BY id").fetchall()
        print(f"\nScanning {len(rows)} questions ...\n")

        for row in rows:
            qid = row["id"]
            q = conn.execute(
                "SELECT id, title, question_text, choices, feedback_correct, feedback_incorrect "
                "FROM questions WHERE id = ?", (qid,)
            ).fetchone()

            updates = {}      # field_name -> new_value
            field_report = []

            # --- Plain text fields ---
            for field in TEXT_FIELDS:
                raw = q[field]
                if not raw:
                    continue
                snippet_before = first_occurrence_context(raw)
                if snippet_before is None:
                    continue  # no escapes
                fixed, n = decode_unicode_escapes(raw)
                snippet_after = first_occurrence_context(fixed) or fixed[
                    max(0, fixed.find("—") - 40): fixed.find("—") + 40
                ]
                updates[field] = fixed
                field_report.append(f"  {field}: {n} replacement(s)")
                field_report.append(f"    before: ...{snippet_before}...")
                field_report.append(f"    after:  ...{snippet_after}...")

            # --- JSON choices field ---
            raw_choices = q["choices"]
            if raw_choices:
                # Check if there are any \\uXXXX patterns at all before doing work
                if re.search(r'\\u[0-9a-fA-F]{4}', raw_choices):
                    fixed_choices, n = fix_choices_json(raw_choices)
                    if n > 0:
                        updates["choices"] = fixed_choices
                        # For reporting, show the first problem in the raw JSON
                        snippet_before = first_occurrence_context(raw_choices)
                        # And what it looks like after fixing (search for any char we introduced)
                        # Just show the same window position in the fixed string
                        m = re.search(r'\\u[0-9a-fA-F]{4}', raw_choices)
                        if m:
                            start = max(0, m.start() - 40)
                            end = min(len(fixed_choices), m.start() + 80)
                            snippet_after = fixed_choices[start:end]
                        else:
                            snippet_after = "(no further escapes)"
                        field_report.append(f"  choices: {n} replacement(s)")
                        field_report.append(f"    before: ...{snippet_before}...")
                        field_report.append(f"    after:  ...{snippet_after}...")

            if updates:
                total_rows_fixed += 1
                total_fields_fixed += len(updates)
                set_clause = ", ".join(f"{f} = ?" for f in updates)
                values = list(updates.values()) + [qid]
                print(f"[FIX] question id={qid}")
                for line in field_report:
                    print(line)
                if not args.dry_run:
                    conn.execute(
                        f"UPDATE questions SET {set_clause} WHERE id = ?", values
                    )

        if not args.dry_run:
            conn.commit()
            print(f"\n[DONE] Fixed {total_fields_fixed} field(s) across "
                  f"{total_rows_fixed} question(s). Changes committed.")
        else:
            print(f"\n[DRY-RUN DONE] Would fix {total_fields_fixed} field(s) across "
                  f"{total_rows_fixed} question(s). No changes written.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
