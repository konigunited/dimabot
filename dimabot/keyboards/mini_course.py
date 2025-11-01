"""Inline keyboard for the mini-course call to action."""
from __future__ import annotations

from typing import Any

from dimabot.settings import MINI_COURSE_PLACES_URL

MINI_COURSE_URL_BUTTON_TEXT: str = "Открыть мини-курс"
"""Подпись для кнопки-перехода на лендинг мини-курса «Места»."""


def mini_course_cta_keyboard(url: str | None = None) -> Any:
    """Return inline keyboard markup that opens the mini-course website.

    The function tries to build настоящий :class:`aiogram.types.InlineKeyboardMarkup`
    при наличии Aiogram в окружении. Если библиотека недоступна (например, во время
    unit-тестов), возвращается простая словарная структура с теми же данными.
    """
    final_url = url or MINI_COURSE_PLACES_URL

    try:  # pragma: no cover - ветка выполняется только при наличии aiogram
        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    except ModuleNotFoundError:
        return {
            "inline_keyboard": [
                [
                    {
                        "text": MINI_COURSE_URL_BUTTON_TEXT,
                        "url": final_url,
                    }
                ]
            ]
        }

    button = InlineKeyboardButton(text=MINI_COURSE_URL_BUTTON_TEXT, url=final_url)
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
