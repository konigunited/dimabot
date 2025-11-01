"""Handlers for bot interactions."""

from __future__ import annotations

import logging
from pathlib import Path

from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message

from . import keyboards

logger = logging.getLogger(__name__)

router = Router(name=__name__)


def _guide_path_from_bot(bot: Bot) -> Path:
    guide_path = bot.get("guide_path")
    if not guide_path:
        raise RuntimeError("Guide path is not configured on the bot instance")
    return Path(guide_path)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Send welcome message with the guide button."""

    await message.answer(
        "Привет! Я пришлю тебе гайд по Dimabot. Нажми кнопку ниже, чтобы получить его.",
        reply_markup=keyboards.main_menu_keyboard(),
    )


@router.callback_query(lambda c: c.data == keyboards.GUIDE_CALLBACK)
async def handle_get_guide(callback: CallbackQuery) -> None:
    """Send the PDF guide and invite to the mini-lesson."""

    bot = callback.bot
    guide_path = _guide_path_from_bot(bot)

    if not guide_path.exists():
        logger.error("Guide file does not exist at %s", guide_path)
        await callback.answer("Не удалось найти файл с гайдом.", show_alert=True)
        return

    document = FSInputFile(guide_path)
    caption = (
        "Держи гайд по Dimabot! Внутри ты найдёшь краткие инструкции по основным функциям."
    )

    await callback.message.answer_document(document=document, caption=caption)

    mini_lesson_url = bot.get("mini_lesson_url")
    invite_text = (
        "Готов продолжить? Пройди мини-урок, чтобы закрепить знания!"
    )
    await callback.message.answer(
        invite_text,
        reply_markup=keyboards.mini_lesson_keyboard(mini_lesson_url),
    )

    await callback.answer()


@router.callback_query(lambda c: c.data == keyboards.MINI_LESSON_CALLBACK)
async def handle_mini_lesson(callback: CallbackQuery) -> None:
    """Fallback handler when the mini-lesson button triggers a callback."""

    await callback.message.answer(
        "Мини-урок скоро будет готов. Следи за обновлениями!"
    )
    await callback.answer()


__all__ = ["router"]
