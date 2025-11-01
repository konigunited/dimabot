"""Handlers that promote the «Места» mini-course."""
from __future__ import annotations

import inspect
from typing import Any, Callable, Optional

from dimabot.keyboards.mini_course import mini_course_cta_keyboard
from dimabot.texts import MINI_COURSE_PLACES_TEXT

MINI_COURSE_BUTTON_TEXT: str = "🚀 Пройти мини-курс “Места”"
"""Текст кнопки в основном меню, нажатие на которую открывает мини-курс."""


async def handle_mini_course_button(message: Any) -> None:
    """Send motivation and CTA for the «Места» mini-course.

    Функция написана максимально универсально: она принимает любой объект,
    обладающий вызываемым атрибутом ``answer``. Это позволяет использовать её
    как с реальными объектами :class:`aiogram.types.Message`, так и с простыми
    тестовыми заглушками без дополнительных зависимостей.
    """
    answer: Optional[Callable[..., Any]] = getattr(message, "answer", None)
    if answer is None:
        raise AttributeError("message must provide an 'answer' method")

    response = answer(
        MINI_COURSE_PLACES_TEXT,
        reply_markup=mini_course_cta_keyboard(),
    )
    if inspect.isawaitable(response):
        await response  # type: ignore[func-returns-value]


def register_mini_course_handler(router: Any) -> None:
    """Register the handler in an Aiogram router.

    Регистрация вынесена в отдельную функцию, чтобы избежать обязательного
    импорта Aiogram при импорте всего модуля. Это также позволяет удобнее
    тестировать модуль в окружении без установленной библиотеки.
    """
    try:
        from aiogram import F
    except ModuleNotFoundError as exc:  # pragma: no cover - защитный код
        raise RuntimeError("Aiogram is required to register handlers") from exc

    router.message.register(handle_mini_course_button, F.text == MINI_COURSE_BUTTON_TEXT)
