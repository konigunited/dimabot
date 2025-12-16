import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from database.db import init_db
from bot.handlers import start, products, help, mini_lesson

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    # Инициализация бота
    # Если нужен прокси, раскомментируйте и настройте:
    # from aiogram.client.session.aiohttp import AiohttpSession
    # from aiohttp import BasicAuth
    # session = AiohttpSession(proxy="http://proxy.server:port")
    # или для SOCKS5: session = AiohttpSession(proxy="socks5://proxy.server:port")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Инициализация диспетчера
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(products.router)
    dp.include_router(help.router)
    dp.include_router(mini_lesson.router)

    # Инициализация БД
    logger.info("Инициализация базы данных...")
    await init_db()
    logger.info("База данных инициализирована!")

    # Запуск бота
    logger.info("Бот запущен!")
    if settings.MOCK_PAYMENTS:
        logger.warning("⚠️ МОК-РЕЖИМ ОПЛАТЫ ВКЛЮЧЕН! Все платежи проходят автоматически.")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен!")
