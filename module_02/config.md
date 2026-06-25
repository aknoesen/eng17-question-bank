# Module 2 Generation Config — ENG17

## Module Info
module_id: 2
module_number: 2
module_title: "Thevenin & Norton Equivalence + Maximum Power Transfer"
course: "ENG17"

## Chapter Mapping
| Chapter | chapter_id | Title                                      | Topic Rows |
|---------|------------|--------------------------------------------|------------|
| 1       | 6          | Thevenin's Theorem                         | 1–7        |
| 2       | 7          | Norton Equivalence and Source Transformation | 8–9      |
| 3       | 8          | Maximum Power Transfer                     | 10–12      |

## Generation Parameters
questions_per_topic: 3
question_type: multiple_choice
bloom_level: Apply
points_per_question: 1

## Prior Modules
prior_modules: 1

## Run Instructions for Claude Code
1. veriqa.db already exists (created for Module 1)
2. Insert module record (id=2) if not present
3. Insert chapter records (ids=6,7,8) if not present
4. Insert topic records from module_02/topics.md if not present
5. For each topic: generate 3 questions, validate, insert with status='draft'
6. Run chapter by chapter — Chapter 6 through Chapter 8 in order

## Notes
- Source content is in module_02/context.md
- Prior module context is in module_02/prior_context.md
- Default Bloom level is Apply; individual topic rows override this
- chapter_ids start at 6 to continue from Module 1 (chapters 1–5)
