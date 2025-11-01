"""Inline keyboards used by the bot."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

GUIDE_CALLBACK = "get_guide"
MINI_LESSON_CALLBACK = "start_mini_lesson"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Keyboard with the guide button."""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📘 Получить гайд", callback_data=GUIDE_CALLBACK)]
        ]
    )


def mini_lesson_keyboard(url: str | None = None) -> InlineKeyboardMarkup:
    """Keyboard with the mini-lesson button.

    If *url* is provided, the button will open the link instead of sending a
    callback.
    """

    if url:
        button = InlineKeyboardButton(text="🎯 Пройти мини-урок", url=url)
    else:
        button = InlineKeyboardButton(text="🎯 Пройти мини-урок", callback_data=MINI_LESSON_CALLBACK)

    return InlineKeyboardMarkup(inline_keyboard=[[button]])


__all__ = [
    "GUIDE_CALLBACK",
    "MINI_LESSON_CALLBACK",
    "main_menu_keyboard",
    "mini_lesson_keyboard",
]
