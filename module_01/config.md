# Module 1 Generation Config — ENG17

## Module Info
module_id: 1
module_number: 1
module_title: "Response of the Series RLC Circuit"
course: "ENG17"

## Chapter Mapping
| Chapter | chapter_id | Title                                    | Topic Rows |
|---------|------------|------------------------------------------|------------|
| 1       | 1          | Initial Conditions and ODE Derivation    | 1–5        |
| 2       | 2          | Transient and Steady-State Decomposition | 6–9        |
| 3       | 3          | Overdamped Response                      | 10–14      |
| 4       | 4          | Underdamped Response                     | 15–20      |
| 5       | 5          | Critically Damped Response and Comparison| 21–24      |

## Generation Parameters
questions_per_topic: 3
question_type: multiple_choice
bloom_level: Apply
points_per_question: 1

## Prior Modules
prior_modules: none

## Run Instructions for Claude Code
1. Initialize DB from schema.sql if veriqa.db does not exist
2. Insert module record (id=1) if not present
3. Insert chapter records (ids=1,2,3,4,5) if not present
4. Insert topic records from module_01/topics.md if not present
5. For each topic: generate 3 questions, validate, insert with status='draft'
6. Run chapter by chapter — Chapter 1 through Chapter 5 in order

## Notes
- Source content is in module_01/context.md (path to the lecture notes .tex file)
- No prior module context for Module 1
- Default Bloom level is Apply; individual topic rows override this
- Difficulty per question matches the difficulty column in topics.md
