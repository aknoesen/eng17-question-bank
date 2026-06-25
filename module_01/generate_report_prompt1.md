# Generate Review Summary Report — Module 1

Run the following command from the question_bank/ directory:

    python generate_report.py --module 1 --questions-per-topic 3

This will:
- Query veriqa.db for module 1 results
- Write the report to module_01/review_summary.md
- Print the full report to terminal

Run this after all questions for module 1 have been reviewed in the
review UI and status set to approved or failed.
