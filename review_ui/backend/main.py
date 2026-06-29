import json
import os
import sqlite3
from contextlib import contextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

_here = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DB_PATH", os.path.join(_here, "..", "..", "veriqa.db"))

app = FastAPI(title="VeriQAI Review API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@app.get("/api/chapters")
def get_chapters():
    with get_db() as conn:
        chapters = conn.execute("""
            SELECT c.id AS chapter_id, c.title AS chapter_title,
                   m.id AS module_id, m.title AS module_title
            FROM chapters c
            JOIN modules m ON c.module_id = m.id
            ORDER BY m.number, CAST(c.number AS INTEGER)
        """).fetchall()

        result = []
        for ch in chapters:
            counts = conn.execute("""
                SELECT status, COUNT(*) AS cnt
                FROM questions
                WHERE chapter_id = ?
                GROUP BY status
            """, (ch["chapter_id"],)).fetchall()

            count_dict = {"draft": 0, "approved": 0, "failed": 0}
            for row in counts:
                count_dict[row["status"]] = row["cnt"]

            result.append({
                "chapter_id": ch["chapter_id"],
                "chapter_title": ch["chapter_title"],
                "module_id": ch["module_id"],
                "module_title": ch["module_title"],
                "counts": count_dict,
            })

        return result


@app.get("/api/questions")
def get_questions(chapter_id: int, status: Optional[str] = None):
    with get_db() as conn:
        if status:
            rows = conn.execute("""
                SELECT q.id, q.title, q.question_text, q.choices,
                       q.correct_answer_index, q.feedback_correct, q.feedback_incorrect,
                       q.bloom_level, q.difficulty, q.katex_present, q.status,
                       q.question_number,
                       t.title AS topic_title, t.subtopic, t.learning_objective
                FROM questions q
                JOIN topics t ON q.topic_id = t.id
                WHERE q.chapter_id = ? AND q.status = ?
                ORDER BY q.id
            """, (chapter_id, status)).fetchall()
        else:
            rows = conn.execute("""
                SELECT q.id, q.title, q.question_text, q.choices,
                       q.correct_answer_index, q.feedback_correct, q.feedback_incorrect,
                       q.bloom_level, q.difficulty, q.katex_present, q.status,
                       q.question_number,
                       t.title AS topic_title, t.subtopic, t.learning_objective
                FROM questions q
                JOIN topics t ON q.topic_id = t.id
                WHERE q.chapter_id = ?
                ORDER BY q.id
            """, (chapter_id,)).fetchall()

        result = []
        for row in rows:
            d = dict(row)
            d["choices"] = json.loads(d["choices"])
            d["katex_present"] = bool(d["katex_present"])
            result.append(d)

        return result


class StatusUpdate(BaseModel):
    status: str


@app.patch("/api/questions/{question_id}/status")
def update_status(question_id: int, body: StatusUpdate):
    if body.status not in ("approved", "failed"):
        raise HTTPException(status_code=400, detail="status must be 'approved' or 'failed'")

    with get_db() as conn:
        conn.execute(
            "UPDATE questions SET status = ? WHERE id = ?",
            (body.status, question_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, status FROM questions WHERE id = ?", (question_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Question not found")
        return dict(row)


@app.post("/api/reset")
def reset_to_draft(chapter_id: Optional[int] = None):
    """Reset review decisions back to 'draft'.

    With no chapter_id, resets every question; otherwise only that chapter.
    Restores the review queue after questions have been approved/rejected.
    """
    with get_db() as conn:
        if chapter_id is not None:
            cur = conn.execute(
                "UPDATE questions SET status = 'draft' "
                "WHERE chapter_id = ? AND status != 'draft'",
                (chapter_id,),
            )
        else:
            cur = conn.execute(
                "UPDATE questions SET status = 'draft' WHERE status != 'draft'"
            )
        conn.commit()
        return {"reset": cur.rowcount}


@app.get("/api/summary")
def get_summary():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT m.id AS module_id, m.title AS module_title,
                   q.status, COUNT(*) AS cnt
            FROM questions q
            JOIN modules m ON q.module_id = m.id
            GROUP BY m.id, q.status
            ORDER BY m.number
        """).fetchall()

        modules: dict = {}
        for row in rows:
            mid = row["module_id"]
            if mid not in modules:
                modules[mid] = {
                    "module_id": mid,
                    "module_title": row["module_title"],
                    "counts": {"draft": 0, "approved": 0, "failed": 0},
                }
            modules[mid]["counts"][row["status"]] = row["cnt"]

        totals_rows = conn.execute(
            "SELECT status, COUNT(*) AS cnt FROM questions GROUP BY status"
        ).fetchall()
        totals = {"draft": 0, "approved": 0, "failed": 0}
        for row in totals_rows:
            totals[row["status"]] = row["cnt"]

        return {"modules": list(modules.values()), "totals": totals}
