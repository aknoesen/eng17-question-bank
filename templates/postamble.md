# Output Format — Required JSON Structure

Return ONLY a JSON object with this EXACT structure and field names.
Generate exactly the number of questions specified in the config.

```
{
  "questions": [
    {
      "type": "multiple_choice",
      "title": "Clear descriptive title (not the question itself)",
      "question_text": "Complete question using KaTeX: \\( V = IR \\)",
      "choices": [
        "Choice A text",
        "Choice B text",
        "Choice C text",
        "Choice D text"
      ],
      "correct_answer_index": 0,
      "points": 1,
      "tolerance": 0.0,
      "feedback_correct": "Explanation of why this is correct, with KaTeX where needed",
      "feedback_incorrect": "Guidance that helps student understand their error",
      "bloom_level": "Apply",
      "difficulty": 3,
      "katex_present": true,
      "topic": "Main topic area from table",
      "subtopic": "Specific subtopic from table",
      "learning_objective": "Full learning objective text from table",
      "module_id": 1,
      "chapter_id": 1,
      "topic_row": 5
    }
  ]
}
```

## CRITICAL FIELD REQUIREMENTS
- `correct_answer_index`: integer 0-3 matching the index of the correct item in `choices`
- `choices`: exactly 4 items for multiple_choice; exactly 2 items ["True", "False"] for true_false
- `tolerance`: 0.0 for non-numeric; fractional tolerance (e.g. 0.05) for numeric answer types
- `katex_present`: true if any KaTeX appears in question_text or choices, false otherwise
- `bloom_level`: must match the level specified in the generation config exactly
- `difficulty`: integer 1-4 matching the topic table
- `topic_row`: integer matching the row number from topics.md (for DB linking)

## JSON BACKSLASH RULE (CRITICAL)
In JSON, ALL backslashes must be doubled. This is standard JSON encoding.
After JSON parsing, doubled backslashes become single — which is what KaTeX requires.

CORRECT — doubled backslashes in JSON output:
  "question_text": "Apply \\( V = IR \\) to find the current."
  "feedback_correct": "Using \\( R_{th} = \\frac{v_{oc}}{i_{sc}} \\) gives..."

WRONG — single backslashes will cause corruption on parsing:
  "question_text": "Apply \( V = IR \) to find the current."

Common sequences that CORRUPT if not doubled (single → parsed as):
  \t  -> tab character       affects: \text, \times, \theta, \tau, \tan
  \f  -> form feed           affects: \frac, \forall
  \b  -> backspace           affects: \beta, \bf, \bar
  \r  -> carriage return     affects: \rho, \right
  \n  -> newline             affects: \nabla, \nu, \neq, \not

Every KaTeX command must have its backslash doubled in JSON:
  \\( \\frac{a}{b} \\)          not  \( \frac{a}{b} \)
  \\( \\text{V} \\)             not  \( \text{V} \)
  \\( \\alpha \\)               not  \( \alpha \)
  \\( \\omega_d \\)             not  \( \omega_d \)
  \\( v_C(t) \\)               not  \( v_C(t) \)

The example template above already uses correct doubled backslashes — follow it exactly.

## JSON COMPLETENESS
- Ensure the JSON is complete and valid — no truncated arrays or objects
- No trailing commas
