"""Utility helpers for the Dima bot project."""

from dimabot.handlers import (
    MINI_COURSE_BUTTON_TEXT,
    handle_mini_course_button,
    register_mini_course_handler,
)
from dimabot.keyboards import MINI_COURSE_URL_BUTTON_TEXT, mini_course_cta_keyboard
from dimabot.texts import MINI_COURSE_PLACES_TEXT

__all__ = [
    "MINI_COURSE_BUTTON_TEXT",
    "MINI_COURSE_PLACES_TEXT",
    "MINI_COURSE_URL_BUTTON_TEXT",
    "handle_mini_course_button",
    "mini_course_cta_keyboard",
    "register_mini_course_handler",
]
