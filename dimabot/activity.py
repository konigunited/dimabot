"""High level helpers for recording bot activity."""

from __future__ import annotations

import logging
from typing import Optional

from .storage import GUIDE_EVENT, LESSON_EVENT, UserStorage

LOGGER = logging.getLogger(__name__)


class UserActivityTracker:
    """Coordinates between bot handlers and the persistent storage."""

    def __init__(self, storage: Optional[UserStorage] = None) -> None:
        self.storage = storage or UserStorage()

    def handle_start(self, user_id: int, name: str) -> None:
        """Record that the user executed the /start command."""

        LOGGER.debug("Handling /start for user %s (%s)", user_id, name)
        self.storage.record_user(user_id, name)

    def guide_issued(
        self, user_id: int, guide_id: Optional[str] = None, title: Optional[str] = None
    ) -> None:
        """Log that a guide was sent to the user."""

        LOGGER.debug(
            "Logging guide issued: user_id=%s guide_id=%s title=%s",
            user_id,
            guide_id,
            title,
        )
        self.storage.log_guide_issued(user_id, guide_id, title)

    def lesson_completed(
        self,
        user_id: int,
        lesson_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        """Log that the user completed a lesson."""

        LOGGER.debug(
            "Logging lesson completion: user_id=%s lesson_id=%s status=%s",
            user_id,
            lesson_id,
            status,
        )
        self.storage.log_lesson_completed(user_id, lesson_id, status)


__all__ = ["UserActivityTracker", "GUIDE_EVENT", "LESSON_EVENT"]
