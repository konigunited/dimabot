"""Configuration helpers for the bot."""
from __future__ import annotations

import os

MINI_COURSE_PLACES_URL: str = os.getenv(
    "MINI_COURSE_PLACES_URL",
    "https://dima.one/mini-course-places",
)
"""Ссылка на лендинг мини-курса «Места».

При необходимости её можно переопределить через одноимённую переменную окружения,
что упрощает настройку разных окружений (разработка, предпросмотр, продакшен).
"""
