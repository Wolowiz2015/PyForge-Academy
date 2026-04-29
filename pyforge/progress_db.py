"""
Lightweight progress store backed by SQLite.

Tracks:
  - lessons:       progress per lesson (status, last_seen, exercise_passed)
  - app_meta:      app-level kv (user name, current model, etc.)
  - run_history:   last N successful runs (for quick re-open)

Local-first by design. The file lives in ~/.pyforge/progress.db. Safe to
delete to reset progress.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


DB_DIR  = Path(os.path.expanduser("~")) / ".pyforge"
DB_PATH = DB_DIR / "progress.db"


@dataclass
class LessonProgress:
    lesson_id: str
    status: str = "new"          # new | viewed | completed
    exercise_passed: bool = False
    attempts: int = 0
    last_seen_iso: str = ""


SCHEMA = """
CREATE TABLE IF NOT EXISTS lessons (
    lesson_id        TEXT PRIMARY KEY,
    status           TEXT NOT NULL DEFAULT 'new',
    exercise_passed  INTEGER NOT NULL DEFAULT 0,
    attempts         INTEGER NOT NULL DEFAULT 0,
    last_seen_iso    TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS app_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS run_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id   TEXT,
    source      TEXT,
    duration_ms REAL,
    ok          INTEGER,
    created_iso TEXT
);
"""


class ProgressStore:
    def __init__(self, path: Path = DB_PATH):
        DB_DIR.mkdir(parents=True, exist_ok=True)
        self._path = path
        with self._conn() as c:
            c.executescript(SCHEMA)
            c.commit()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)

    # ---------------------------------------------------------------- lessons
    def upsert_lesson(self, p: LessonProgress) -> None:
        with closing(self._conn()) as c:
            c.execute(
                """
                INSERT INTO lessons(lesson_id, status, exercise_passed, attempts, last_seen_iso)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    status          = excluded.status,
                    exercise_passed = excluded.exercise_passed,
                    attempts        = excluded.attempts,
                    last_seen_iso   = excluded.last_seen_iso
                """,
                (p.lesson_id, p.status, int(p.exercise_passed),
                 p.attempts, p.last_seen_iso),
            )
            c.commit()

    def get_lesson(self, lesson_id: str) -> Optional[LessonProgress]:
        with closing(self._conn()) as c:
            row = c.execute("SELECT * FROM lessons WHERE lesson_id = ?",
                            (lesson_id,)).fetchone()
        if not row:
            return None
        return LessonProgress(
            lesson_id=row[0],
            status=row[1],
            exercise_passed=bool(row[2]),
            attempts=row[3],
            last_seen_iso=row[4],
        )

    def all_progress(self) -> Dict[str, LessonProgress]:
        with closing(self._conn()) as c:
            rows = c.execute("SELECT * FROM lessons").fetchall()
        return {
            r[0]: LessonProgress(r[0], r[1], bool(r[2]), r[3], r[4])
            for r in rows
        }

    def completion_summary(self, total: int) -> Dict[str, int]:
        with closing(self._conn()) as c:
            row = c.execute(
                "SELECT "
                "  SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END), "
                "  SUM(CASE WHEN exercise_passed=1 THEN 1 ELSE 0 END), "
                "  COUNT(*) "
                "FROM lessons"
            ).fetchone()
        completed = row[0] or 0
        passed    = row[1] or 0
        seen      = row[2] or 0
        return {
            "completed": completed,
            "passed_exercise": passed,
            "viewed": seen,
            "total": total,
        }

    # ---------------------------------------------------------------- meta
    def set_meta(self, key: str, value: str) -> None:
        with closing(self._conn()) as c:
            c.execute(
                "INSERT INTO app_meta(key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )
            c.commit()

    def get_meta(self, key: str, default: str = "") -> str:
        with closing(self._conn()) as c:
            row = c.execute("SELECT value FROM app_meta WHERE key = ?",
                            (key,)).fetchone()
        return row[0] if row else default

    # ---------------------------------------------------------------- runs
    def log_run(self, lesson_id: str, source: str, duration_ms: float,
                ok: bool, created_iso: str) -> None:
        with closing(self._conn()) as c:
            c.execute(
                "INSERT INTO run_history(lesson_id, source, duration_ms, ok, created_iso) "
                "VALUES (?, ?, ?, ?, ?)",
                (lesson_id, source, duration_ms, int(ok), created_iso),
            )
            # Keep only the most recent 200 runs to stay light.
            c.execute(
                "DELETE FROM run_history WHERE id NOT IN ("
                "  SELECT id FROM run_history ORDER BY id DESC LIMIT 200"
                ")"
            )
            c.commit()
