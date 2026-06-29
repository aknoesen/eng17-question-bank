#!/usr/bin/env python3
"""Reset question review status back to 'draft'.

Restores the review queue after questions have been approved or rejected
in review_ui/ — useful if you clicked through them by accident.

Usage:
    python reset_status.py               # reset ALL questions to draft
    python reset_status.py --chapter 3   # reset only chapter_id 3
    python reset_status.py --db path/to/veriqa.db
"""
import argparse
import os
import sqlite3

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veriqa.db")


def main():
    parser = argparse.ArgumentParser(description="Reset question status to 'draft'.")
    parser.add_argument("--chapter", type=int, help="Only reset this chapter_id")
    parser.add_argument("--db", default=DEFAULT_DB, help="Path to veriqa.db")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    try:
        if args.chapter is not None:
            cur = conn.execute(
                "UPDATE questions SET status = 'draft' "
                "WHERE chapter_id = ? AND status != 'draft'",
                (args.chapter,),
            )
            scope = f"chapter {args.chapter}"
        else:
            cur = conn.execute(
                "UPDATE questions SET status = 'draft' WHERE status != 'draft'"
            )
            scope = "all chapters"
        conn.commit()
        print(f"Reset {cur.rowcount} question(s) to draft ({scope}).")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
