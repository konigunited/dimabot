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
    get_course_keyboard,
    get_courses_menu,
    get_online_course_keyboard
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


# Обработчик кнопки "Курсы"
@dp.callback_query(F.data == "show_courses")
async def process_show_courses(callback: CallbackQuery):
    """Показать меню курсов"""
    await callback.answer()
    await callback.message.answer(
        text="📚 Выберите курс:",
        reply_markup=get_courses_menu()
    )


# Обработчик кнопки "Назад"
@dp.callback_query(F.data == "back_to_start")
async def process_back_to_start(callback: CallbackQuery):
    """Вернуться в начало"""
    await callback.answer()
    await callback.message.answer(
        text=config.WELCOME_TEXT,
        reply_markup=get_start_keyboard()
    )


# Обработчик онлайн курса
@dp.callback_query(F.data == "online_course")
async def process_online_course(callback: CallbackQuery):
    """Показать описание онлайн курса"""
    await callback.answer()
    await callback.message.answer(
        text=config.ONLINE_COURSE_DESCRIPTION,
        reply_markup=get_online_course_keyboard()
    )


# Обработчик покупки онлайн курса
@dp.callback_query(F.data == "buy_online_course")
async def process_buy_online_course(callback: CallbackQuery):
    """Обработка покупки онлайн курса"""
    await callback.answer()

    # TODO: Здесь будет интеграция с ЮКассой
    await callback.message.answer(
        "💳 Оплата курса\n\n"
        "Функционал оплаты будет добавлен в следующей версии."
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
