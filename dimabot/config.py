"""Application configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """Container for runtime configuration."""

    bot_token: str
    guide_path: Path
    mini_lesson_url: str | None = None


def load_settings() -> Settings:
    """Load runtime configuration from environment variables.

    BOT_TOKEN is mandatory. GUIDE_PATH and MINI_LESSON_URL are optional and
    fall back to sensible defaults if not provided.
    """

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is not set")

    guide_path_value = os.getenv("GUIDE_PATH")
    if guide_path_value:
        guide_path = Path(guide_path_value).expanduser()
    else:
        guide_path = Path(__file__).resolve().parent.parent / "guide_assets" / "guide.pdf"

    mini_lesson_url = os.getenv("MINI_LESSON_URL")

    return Settings(bot_token=token, guide_path=guide_path, mini_lesson_url=mini_lesson_url)


__all__ = ["Settings", "load_settings"]
