"""Bot entry point."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from .config import load_settings
from .handlers import router


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


async def main() -> None:
    """Start the bot polling loop."""

    setup_logging()
    settings = load_settings()

    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    bot["guide_path"] = str(settings.guide_path)
    if settings.mini_lesson_url:
        bot["mini_lesson_url"] = settings.mini_lesson_url

    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
