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
    get_lesson_start_keyboard,
    get_task1_keyboard,
    get_task1_next_keyboard,
    get_task2_keyboard,
    get_task2_next_keyboard,
    get_task3_keyboard,
    get_task3_next_keyboard,
    get_task4_keyboard,
    get_final_keyboard
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
            caption="📘 Мини-гайд 'Как не забывать слова и говорить свободно'"
        )
    else:
        # Если файла нет, отправляем заглушку
        await callback.message.answer(
            "📘 Мини-гайд 'Как не забывать слова и говорить свободно'\n"
            "(PDF файл будет прикреплен позже)"
        )

    await callback.message.answer(
        text=config.GUIDE_SENT_TEXT,
        reply_markup=get_lesson_start_keyboard()
    )


# Обработчик начала мини-урока
@dp.callback_query(F.data == "start_lesson")
async def process_start_lesson(callback: CallbackQuery):
    """Начало мини-урока - Задание 1"""
    await callback.answer()
    await callback.message.answer(
        text=config.TASK1_TEXT,
        reply_markup=get_task1_keyboard()
    )


# Обработчики ответов на задание 1
@dp.callback_query(F.data.in_(["task1_a", "task1_b", "task1_c"]))
async def process_task1_answer(callback: CallbackQuery):
    """Обработка ответа на задание 1"""
    await callback.answer()

    if callback.data == "task1_a":
        response = "✅ Правильно!\n\n" + config.TASK1_EXPLANATION
    else:
        response = "❌ Неправильно. Правильный ответ: a) kitchen\n\n" + config.TASK1_EXPLANATION

    await callback.message.answer(
        text=response,
        reply_markup=get_task1_next_keyboard()
    )


# Переход к заданию 2
@dp.callback_query(F.data == "task2")
async def process_task2(callback: CallbackQuery):
    """Задание 2"""
    await callback.answer()
    await callback.message.answer(
        text=config.TASK2_TEXT,
        reply_markup=get_task2_keyboard()
    )


# Обработчик задания 2 (любой клик ведет дальше)
@dp.callback_query(F.data == "task2_done")
async def process_task2_done(callback: CallbackQuery):
    """Завершение задания 2"""
    await callback.answer()
    await callback.message.answer(
        text=config.TASK2_EXPLANATION,
        reply_markup=get_task2_next_keyboard()
    )


# Переход к заданию 3
@dp.callback_query(F.data == "task3")
async def process_task3(callback: CallbackQuery):
    """Задание 3 с аудио"""
    await callback.answer()

    # Отправляем аудио, если файл существует
    if os.path.exists(config.AUDIO_TASK3_PATH):
        audio_file = FSInputFile(config.AUDIO_TASK3_PATH)
        await callback.message.answer_audio(audio_file)
    else:
        # Заглушка для аудио
        await callback.message.answer(
            "🎧 (Здесь будет аудио: 'I sit, drink coffee, and watch people walking outside.')"
        )

    await callback.message.answer(
        text=config.TASK3_TEXT,
        reply_markup=get_task3_keyboard()
    )


# Обработчики ответов на задание 3
@dp.callback_query(F.data.in_(["task3_a", "task3_b", "task3_c"]))
async def process_task3_answer(callback: CallbackQuery):
    """Обработка ответа на задание 3"""
    await callback.answer()

    if callback.data == "task3_a":
        response = "✅ Правильно!\n\n" + config.TASK3_EXPLANATION
    else:
        response = "❌ Неправильно. Правильный ответ: a) café\n\n" + config.TASK3_EXPLANATION

    await callback.message.answer(
        text=response,
        reply_markup=get_task3_next_keyboard()
    )


# Переход к заданию 4 (мотивация)
@dp.callback_query(F.data == "task4")
async def process_task4(callback: CallbackQuery):
    """Задание 4 - мотивация"""
    await callback.answer()
    await callback.message.answer(
        text=config.TASK4_TEXT,
        reply_markup=get_task4_keyboard()
    )


# Финальное сообщение
@dp.callback_query(F.data == "final")
async def process_final(callback: CallbackQuery):
    """Финальное сообщение с переходом на курс"""
    await callback.answer()
    await callback.message.answer(
        text=config.FINAL_TEXT,
        reply_markup=get_final_keyboard(config.COURSE_URL)
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
