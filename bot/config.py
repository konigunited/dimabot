"""Configuration helpers for dimabot."""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional


class ConfigError(RuntimeError):
    """Raised when bot configuration is invalid."""


@dataclass(frozen=True)
class BotConfig:
    """Runtime configuration for the Telegram bot."""

    token: str
    final_link: str
    admin_chat_id: Optional[int] = None

    @classmethod
    def from_env(cls) -> "BotConfig":
        """Create configuration by reading environment variables.

        Expected variables:
            DIMABOT_TOKEN: Telegram bot token.
            DIMABOT_FINAL_LINK: URL that should be sent at the end of the flow.
            DIMABOT_ADMIN_CHAT_ID: optional chat id for diagnostic notifications.
        """

        token = os.getenv("DIMABOT_TOKEN")
        final_link = os.getenv("DIMABOT_FINAL_LINK")
        admin_chat_id_raw = os.getenv("DIMABOT_ADMIN_CHAT_ID")

        if not token:
            raise ConfigError("DIMABOT_TOKEN is not set")
        if not final_link:
            raise ConfigError("DIMABOT_FINAL_LINK is not set")

        admin_chat_id: Optional[int] = None
        if admin_chat_id_raw:
            try:
                admin_chat_id = int(admin_chat_id_raw)
            except ValueError as exc:  # pragma: no cover - defensive branch
                raise ConfigError(
                    "DIMABOT_ADMIN_CHAT_ID must be an integer"
                ) from exc

        return cls(token=token, final_link=final_link, admin_chat_id=admin_chat_id)


def load_config() -> BotConfig:
    """Helper used by runtime entrypoints."""

    return BotConfig.from_env()
