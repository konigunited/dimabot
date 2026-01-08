import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage

import config
from keyboards.inline import (
    get_start_keyboard,
    get_course_keyboard
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        text=config.WELCOME_TEXT,
        reply_markup=get_start_keyboard()
    )


# Обработчик кнопки "Получить гайд"
@dp.callback_query(F.data == "get_guide")
async def process_get_guide(callback: CallbackQuery):
    """Отправка PDF-гайда"""
    await callback.answer()

    # Проверяем наличие PDF файла
    if os.path.exists(config.GUIDE_PDF_PATH):
        pdf_file = FSInputFile(config.GUIDE_PDF_PATH)
        await callback.message.answer_document(
            document=pdf_file,
            caption="📘 Мини-урок 'Места'"
        )
    else:
        # Если файла нет, отправляем заглушку
        await callback.message.answer(
            "📘 Мини-урок 'Места'\n"
            "(PDF файл будет прикреплен позже)"
        )

    await callback.message.answer(
        text=config.GUIDE_SENT_TEXT,
        reply_markup=get_course_keyboard(config.COURSE_URL)
    )


async def main():
    """Запуск бота"""
    logger.info("Бот запускается...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
