"""Persistent storage for user records and activity logs."""

from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

LOGGER = logging.getLogger(__name__)

GUIDE_EVENT = "guide_issued"
LESSON_EVENT = "lesson_completed"


@dataclass(slots=True)
class EventRecord:
    """Represents a single event stored in the activity log."""

    id: int
    user_id: int
    event_type: str
    payload: Optional[dict]
    created_at: str


class UserStorage:
    """Storage backed by SQLite for users and events."""

    def __init__(self, db_path: str | Path = "data/dimabot.sqlite3") -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        LOGGER.debug("Initialising user storage at %s", self._path)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._migrate()

    # -- context manager protocol -------------------------------------------------
    def __enter__(self) -> "UserStorage":  # pragma: no cover - trivial
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # pragma: no cover - trivial
        self.close()

    # -- public API ----------------------------------------------------------------
    @property
    def path(self) -> Path:
        return self._path

    def close(self) -> None:
        LOGGER.debug("Closing connection to %s", self._path)
        self._conn.close()

    def record_user(self, user_id: int, name: str) -> None:
        """Insert or update information about a user."""

        LOGGER.info("Recording user: id=%s name=%s", user_id, name)
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO users (user_id, name)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    name = excluded.name,
                    last_seen = CURRENT_TIMESTAMP
                """,
                (user_id, name),
            )

    def log_event(
        self,
        user_id: int,
        event_type: str,
        payload: Optional[dict] = None,
    ) -> None:
        """Persist an event emitted by the bot."""

        json_payload = json.dumps(payload, ensure_ascii=False) if payload else None
        LOGGER.info(
            "Logging event: user_id=%s type=%s payload=%s", user_id, event_type, payload
        )
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO events (user_id, event_type, payload)
                VALUES (?, ?, ?)
                """,
                (user_id, event_type, json_payload),
            )

    def log_guide_issued(
        self, user_id: int, guide_id: Optional[str] = None, title: Optional[str] = None
    ) -> None:
        """Log that a guide was issued to the user."""

        payload: dict[str, str] = {}
        if guide_id is not None:
            payload["guide_id"] = guide_id
        if title is not None:
            payload["title"] = title
        self.log_event(user_id, GUIDE_EVENT, payload or None)

    def log_lesson_completed(
        self,
        user_id: int,
        lesson_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        """Log that a lesson was completed by the user."""

        payload: dict[str, str] = {}
        if lesson_id is not None:
            payload["lesson_id"] = lesson_id
        if status is not None:
            payload["status"] = status
        self.log_event(user_id, LESSON_EVENT, payload or None)

    def get_user(self, user_id: int) -> Optional[dict]:
        """Return a single user record, if present."""

        cursor = self._conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "user_id": row["user_id"],
            "name": row["name"],
            "first_seen": row["first_seen"],
            "last_seen": row["last_seen"],
        }

    def iter_events(
        self, user_id: Optional[int] = None, event_type: Optional[str] = None
    ) -> Iterator[EventRecord]:
        """Iterate over event records with optional filters."""

        query = "SELECT * FROM events"
        clauses: list[str] = []
        params: list[object] = []
        if user_id is not None:
            clauses.append("user_id = ?")
            params.append(user_id)
        if event_type is not None:
            clauses.append("event_type = ?")
            params.append(event_type)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at, id"

        cursor = self._conn.execute(query, params)
        for row in cursor.fetchall():
            payload = json.loads(row["payload"]) if row["payload"] else None
            yield EventRecord(
                id=row["id"],
                user_id=row["user_id"],
                event_type=row["event_type"],
                payload=payload,
                created_at=row["created_at"],
            )

    # -- private helpers -----------------------------------------------------------
    def _migrate(self) -> None:
        LOGGER.debug("Applying migrations for %s", self._path)
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    first_seen TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
                    last_seen TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    payload TEXT,
                    created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
                """
            )
