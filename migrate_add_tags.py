"""
migrate_add_tags.py — One-shot migration: add the question_tags table and
backfill 'prelecture'/'postlecture' tags from existing questions.

Run once, from the question_bank/ directory:
    python migrate_add_tags.py

Safe to re-run — every step is idempotent. Backs up the database to
question_bank/backups/ before touching it.

After this migration:
- Every existing question has a 'prelecture' or 'postlecture' tag based
  on the same difficulty rule the exporter previously used at runtime
  (diff 1-2 -> prelecture, diff 3+ -> postlecture).
- Newly inserted questions are auto-tagged by the trigger in schema.sql.
- 'final' tags are NOT set here; populate them when authoring final
  questions in a future module.
"""

import os
import shutil
import sqlite3
import sys
from datetime import datetime

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DB_PATH     = os.environ.get("DB_PATH", os.path.join(SCRIPT_DIR, "veriqa.db"))
BACKUPS_DIR = os.path.join(SCRIPT_DIR, "backups")


def backup_db():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found: {DB_PATH}")
        sys.exit(1)
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(BACKUPS_DIR, f"veriqa_pre_migrate_tags_{ts}.db")
    shutil.copy2(DB_PATH, dst)
    print(f"[OK] Backup written: {os.path.relpath(dst, SCRIPT_DIR)}")


def ensure_schema(conn):
    """Create question_tags + index + trigger if they don't already exist."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS question_tags (
            question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
            tag         TEXT NOT NULL,
            PRIMARY KEY (question_id, tag)
        );
        CREATE INDEX IF NOT EXISTS idx_question_tags_tag ON question_tags(tag);

        CREATE TRIGGER IF NOT EXISTS question_tags_auto_difficulty
        AFTER INSERT ON questions
        BEGIN
            INSERT OR IGNORE INTO question_tags (question_id, tag)
            VALUES (
                NEW.id,
                CASE WHEN NEW.difficulty IN (1, 2) THEN 'prelecture' ELSE 'postlecture' END
            );
        END;
        """
    )
    conn.commit()
    print("[OK] question_tags table, index, and trigger ensured.")


def backfill_tags(conn):
    """Apply the historical difficulty-based rule to every existing question."""
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO question_tags (question_id, tag)
        SELECT id, 'prelecture' FROM questions WHERE difficulty IN (1, 2)
        """
    )
    pre_inserted = cur.rowcount

    cur.execute(
        """
        INSERT OR IGNORE INTO question_tags (question_id, tag)
        SELECT id, 'postlecture' FROM questions WHERE difficulty >= 3
        """
    )
    post_inserted = cur.rowcount

    conn.commit()
    print(f"[OK] Backfill: prelecture +{pre_inserted}, postlecture +{post_inserted}")


def report_counts(conn, label):
    cur = conn.cursor()
    total_q = cur.execute("SELECT COUNT(*) FROM questions").fetchone()[0]

    counts = dict(
        cur.execute(
            "SELECT tag, COUNT(*) FROM question_tags GROUP BY tag"
        ).fetchall()
    )

    untagged = cur.execute(
        """
        SELECT COUNT(*) FROM questions q
        WHERE NOT EXISTS (SELECT 1 FROM question_tags t WHERE t.question_id = q.id)
        """
    ).fetchone()[0]

    print(f"--- {label} ---")
    print(f"  questions total : {total_q}")
    print(f"  prelecture      : {counts.get('prelecture', 0)}")
    print(f"  postlecture     : {counts.get('postlecture', 0)}")
    print(f"  final           : {counts.get('final', 0)}")
    print(f"  untagged        : {untagged}")


def main():
    print(f"DB: {DB_PATH}")
    backup_db()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        # Counts before — table may not exist yet on first run; be defensive.
        try:
            report_counts(conn, "BEFORE")
        except sqlite3.OperationalError:
            print("--- BEFORE ---")
            print("  question_tags table does not exist yet")

        ensure_schema(conn)
        backfill_tags(conn)
        report_counts(conn, "AFTER")
    finally:
        conn.close()

    print("\n[DONE] Migration complete. Re-run any time; it's idempotent.")


if __name__ == "__main__":
    main()
