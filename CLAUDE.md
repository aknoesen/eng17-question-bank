# Question Bank Generator — Claude Code Instructions
# ENG17: Circuits I

**This is the authoritative generation recipe.**

## Purpose
Generate autograded quiz questions from ENG17 module content and store them in a SQLite database.
This file tells Claude Code exactly how to execute a generation run.

## Git Repository
This directory is the root of a private git repo:
  https://github.com/aknoesen/eng17-question-bank

After any meaningful change (new questions, schema edits, config updates):
  git add -A && git commit -m "<message>" && git push

## Current State (as of 2026-06-28)
- Modules 1 and 2 are fully generated: 108 questions across 36 topics in veriqa.db
- Generation scripts: generate_m1_ch1to3.py, generate_m1_ch4to5.py, generate_m2_ch6to8.py
- All questions are status='draft' — pending human review in review_ui/
- Do NOT re-run generation scripts for existing topics (EXISTS check will skip them,
  but avoid unnecessary runs)

## Review State Recovery
The review UI writes each approve/reject decision to veriqa.db immediately, with no
undo. Approving (or clicking) through every question empties the draft queue, and the
UI then shows "all questions reviewed" — which looks like the questions are missing.

To put questions back into the review queue:
- In the UI: click "Reset all to draft" at the bottom of the sidebar, OR
- CLI: `python reset_status.py` (all) / `python reset_status.py --chapter N` (one chapter), OR
- For a clone with no other local changes: `git restore veriqa.db` (restores committed state)

Backend endpoint backing the button: `POST /api/reset` (optional `chapter_id`).

## Project Structure
```
question_bank/
  CLAUDE.md                    <- this file
  schema.sql                   <- database schema (do not modify)
  veriqa.db                    <- SQLite database (persistent across runs)
  sources/                     <- local copies of all lecture note inputs
    ENG17-series-RLC-derivation/main.tex
    ENG17-thevenin-norton-notes/main.tex      <- expanded typed notes (generated)
    ENG17-thevenin-norton-slides/main.tex     <- Anthony's original Beamer slides
    ENG17-series-RLC-learning-objectives.md
    ENG17-thevenin-norton-learning-objectives.md
  review_ui/                   <- self-contained question reviewer (FastAPI + React)
    start.sh / start.bat       <- one-click launcher
    backend/main.py            <- reads veriqa.db at ../../veriqa.db
    frontend/                  <- React + KaTeX + Tailwind
  templates/
    preamble.md                <- system prompt template
    postamble.md               <- output format template
  module_XX/
    config.md                  <- module metadata and generation parameters
    topics.md                  <- topic table for this module
    context.md                 <- reading content for this module (paths into sources/)
    prior_context.md           <- accumulated summaries from prior modules
```

## Bloom Level Rule (CRITICAL — do not ask for clarification on this)

Two sources specify Bloom level. The rule is always:

    per-row bloom_level in topics.md  >  bloom_level in config.md

The config.md bloom_level is the DEFAULT only. It applies to any topic row
that does not have an explicit Bloom Level value in topics.md.
If a topic row has a Bloom Level, use that value — never override it with config.

Example:
    config.md:          bloom_level: Apply
    topics.md row 7:    Bloom Level = Analyze
    topics.md row 10:   Bloom Level = Remember
    topics.md row 14:   (no override)
    Result:
        row 7  -> Analyze
        row 10 -> Remember
        row 14 -> Apply  (config default applies)

Store the resolved bloom_level (after applying this rule) in the DB questions table.

## Execution Workflow

When asked to run generation for a module:

1. Read `module_XX/config.md`
   - Extract: module_id, chapter assignments, default bloom_level, questions_per_topic

2. Read context files
   - `module_XX/prior_context.md` — prior module summaries (if present)
   - `module_XX/context.md` — current module reading content (file paths to source .tex or .md)

3. Read `module_XX/topics.md`
   - Parse all topic rows
   - Resolve bloom_level per row using the rule above

4. Read `templates/preamble.md` and `templates/postamble.md`

5. Initialize database
   - If veriqa.db does not exist: create it from schema.sql
   - Insert module record if not present (use module_id from config)
   - Insert chapter records if not present
   - Insert topic records if not present

6. For each topic row — ONE AT A TIME, in sequence:
   a. Check for existing questions in DB:
      SELECT COUNT(*) FROM questions WHERE topic_id = ? AND status != 'failed'
      If count >= questions_per_topic: log [EXISTS] Topic N — skipping
      and continue to next topic. Do not regenerate.

   b. Compose the full prompt:
      - preamble.md content
      - Prior module summaries (from prior_context.md)
      - Current module context (full context.md or relevant chapter section)
      - Topic details: topic, subtopic, learning_objective, bloom_level, difficulty
      - Instruction: generate exactly questions_per_topic questions for this topic
      - postamble.md content

   c. Call the LLM — generate questions_per_topic questions for this topic only

   d. Validate the JSON response (see Validation Rules below)

   e. Insert each question into veriqa.db immediately — do not wait for other topics

   f. Log: [OK] Topic N (row X) — bloom: [level] — Q questions inserted

7. On completion print summary:
   - Total questions inserted this run
   - Total [EXISTS] skips
   - Total [WARNING] retries
   - Total [ERROR] failures

## Error Handling
- Validation failure: log [WARNING] Topic N failed — retry once with same prompt
- Retry failure: log [ERROR] Topic N skipped — insert placeholder with status='failed'
- Never abort the full run due to a single topic failure
- A [WARN] or [ERROR] count > 0 in the summary means human review is needed

## Database Write Pattern
Use Python + sqlite3. Always INSERT with:
- status = 'draft'
- created_at = current UTC timestamp
- Resolve and store bloom_level using the precedence rule above
- Do NOT overwrite existing questions — the EXISTS check in step 6a handles this

CRITICAL — NEVER write a monolithic script that generates all topics first
and inserts later. Generate and insert ONE topic at a time. Each topic must
be inserted into the DB before moving to the next topic.

Do NOT create files named insert_questions.py, generate_moduleXX.py, or
any batch script that defers insertion. These are forbidden patterns.

## Question Tagging (prelecture / postlecture / final)

A `question_tags` side table records which assessment a question belongs to.
The export tool (`export_qti.py` / `make_quizzes.py`) filters by TAG.

The schema.sql trigger `question_tags_auto_difficulty` auto-tags every new
question on INSERT:

    difficulty IN (1, 2)  ->  'prelecture'
    difficulty >= 3       ->  'postlecture'

### Reading-check runs with mixed difficulty (the override case)

When the run is identified as pre-lecture in config.md, after inserting every
question for the module, ALSO run:

    INSERT OR IGNORE INTO question_tags (question_id, tag)
    SELECT id, 'prelecture' FROM questions WHERE module_id = ?;

### Final-exam runs

For a final-exam generation run, after INSERTing each question, ALSO:

    INSERT INTO question_tags (question_id, tag) VALUES (?, 'final')

## JSON Validation Rules
Before inserting, verify each question has:
- question_text (non-empty string)
- choices (array of exactly 4 strings for multiple_choice)
- correct_answer_index (integer 0-3)
- bloom_level (non-empty string, matches resolved level for this topic)
- feedback_correct (non-empty string)
- feedback_incorrect (non-empty string)
- topic_row (integer matching the row number from topics.md)

## Running a Generation
```
# Standard invocation
Generate questions for module 1 using module_01/config.md

# Single chapter only
Generate questions for module 1, chapter 2 only using module_01/config.md

# Retry failed topics only
Regenerate failed topics for module 1 (status='failed' in DB)
```
