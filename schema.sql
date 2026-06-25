-- VeriQAI Question Bank Schema
-- Run once: sqlite3 veriqa.db < schema.sql

CREATE TABLE IF NOT EXISTS modules (
    id          INTEGER PRIMARY KEY,
    number      INTEGER NOT NULL,
    title       TEXT NOT NULL,
    course      TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chapters (
    id          INTEGER PRIMARY KEY,
    module_id   INTEGER NOT NULL REFERENCES modules(id),
    number      TEXT NOT NULL,        -- '0' for Preamble, '1', '2', etc.
    title       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS topics (
    id                  INTEGER PRIMARY KEY,
    chapter_id          INTEGER NOT NULL REFERENCES chapters(id),
    row_number          INTEGER NOT NULL,   -- original row # from topics.md table
    title               TEXT NOT NULL,
    subtopic            TEXT NOT NULL,
    learning_objective  TEXT NOT NULL,
    bloom_level         TEXT NOT NULL,      -- Remember/Understand/Apply/Analyze/Evaluate/Create
    difficulty          INTEGER NOT NULL    -- 1-4
);

CREATE TABLE IF NOT EXISTS questions (
    id                      INTEGER PRIMARY KEY,
    topic_id                INTEGER NOT NULL REFERENCES topics(id),
    question_number         INTEGER NOT NULL,   -- 1, 2, or 3 within topic
    type                    TEXT NOT NULL,      -- multiple_choice / true_false / numeric
    title                   TEXT NOT NULL,
    question_text           TEXT NOT NULL,
    choices                 TEXT NOT NULL,      -- JSON array of 4 strings
    correct_answer_index    INTEGER NOT NULL,   -- 0-3
    points                  INTEGER NOT NULL DEFAULT 1,
    tolerance               REAL NOT NULL DEFAULT 0.0,
    feedback_correct        TEXT NOT NULL,
    feedback_incorrect      TEXT NOT NULL,
    bloom_level             TEXT NOT NULL,
    difficulty              INTEGER NOT NULL,
    katex_present           INTEGER NOT NULL DEFAULT 0,  -- 0/1 boolean
    status                  TEXT NOT NULL DEFAULT 'draft',  -- draft/approved/failed
    created_at              TEXT NOT NULL,
    -- Denormalized for easy querying
    module_id               INTEGER NOT NULL REFERENCES modules(id),
    chapter_id              INTEGER NOT NULL REFERENCES chapters(id)
);

-- Useful indexes
CREATE INDEX IF NOT EXISTS idx_questions_chapter  ON questions(chapter_id);
CREATE INDEX IF NOT EXISTS idx_questions_topic    ON questions(topic_id);
CREATE INDEX IF NOT EXISTS idx_questions_status   ON questions(status);
CREATE INDEX IF NOT EXISTS idx_topics_chapter     ON topics(chapter_id);

-- Tag table — a question can carry multiple tags (e.g., 'postlecture'
-- and 'final' on the same row). 'prelecture'/'postlecture' are populated
-- automatically by the trigger below; 'final' is set deliberately when
-- generating final-exam questions.
CREATE TABLE IF NOT EXISTS question_tags (
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    tag         TEXT NOT NULL,    -- 'prelecture' | 'postlecture' | 'final'
    PRIMARY KEY (question_id, tag)
);
CREATE INDEX IF NOT EXISTS idx_question_tags_tag ON question_tags(tag);

-- Auto-tag on insert: every new question gets 'prelecture' (difficulty
-- 1-2) or 'postlecture' (difficulty 3+). Uses INSERT OR IGNORE so a
-- pre-existing manual tag (e.g., 'final') is preserved.
CREATE TRIGGER IF NOT EXISTS question_tags_auto_difficulty
AFTER INSERT ON questions
BEGIN
    INSERT OR IGNORE INTO question_tags (question_id, tag)
    VALUES (
        NEW.id,
        CASE WHEN NEW.difficulty IN (1, 2) THEN 'prelecture' ELSE 'postlecture' END
    );
END;
