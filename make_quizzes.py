"""
make_quizzes.py — Generate per-tag QTI packages for a module.

Wraps export_qti.py and places output files in the correct subdirectory:
    exports/module_N/prelecture/
    exports/module_N/postlecture/
    exports/module_N/final/

Selection is driven by the question_tags table (see schema.sql).

Usage:
    python make_quizzes.py --module 1                     # both pre and post
    python make_quizzes.py --module 1 --type prelecture   # pre only
    python make_quizzes.py --module 1 --type postlecture  # post only
    python make_quizzes.py --module 1 --type final        # final only
    python make_quizzes.py --module 1 --chapter 2         # chapter 2 only, both pre+post
"""

import argparse
import os
import sys

# Allow importing export_qti from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_qti


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run(module, quiz_types, chapter_filter=None):
    for qt in quiz_types:
        out_dir = os.path.join(SCRIPT_DIR, "exports", f"module_{module}", qt)
        os.makedirs(out_dir, exist_ok=True)

        # Redirect the output directory used by export_qti
        original_dir = export_qti.EXPORTS_DIR
        export_qti.EXPORTS_DIR = out_dir
        try:
            export_qti.export_module(module, chapter_filter=chapter_filter, quiz_type=qt)
        finally:
            export_qti.EXPORTS_DIR = original_dir


def main():
    parser = argparse.ArgumentParser(
        description="Export pre/post-lecture QTI packages for a module."
    )
    parser.add_argument("--module", type=int, required=True, help="Module number")
    parser.add_argument(
        "--type",
        choices=["prelecture", "postlecture", "final", "both"],
        default="both",
        help="Which tag to export. 'both' = prelecture + postlecture. "
             "'final' must be requested explicitly. (default: both)",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Export a single chapter only (chapter number, e.g. 2)",
    )
    args = parser.parse_args()

    quiz_types = ["prelecture", "postlecture"] if args.type == "both" else [args.type]
    run(args.module, quiz_types, chapter_filter=args.chapter)


if __name__ == "__main__":
    main()
