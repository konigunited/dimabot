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
    get_online_course_keyboard,
    get_lesson_task1_keyboard,
    get_lesson_task1_next,
    get_lesson_task2_next,
    get_lesson_task3_keyboard,
    get_lesson_task3_next,
    get_lesson_task4_keyboard
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


# Обработчик начала мини-урока - Задание 1
@dp.callback_query(F.data == "get_guide")
async def process_lesson_start(callback: CallbackQuery):
    """Начало мини-урока - Задание 1"""
    await callback.answer()
    await callback.message.answer(
        text=config.LESSON_TASK1_TEXT,
        reply_markup=get_lesson_task1_keyboard()
    )


# Обработчики ответов на задание 1
@dp.callback_query(F.data.in_(["lesson_task1_a", "lesson_task1_b", "lesson_task1_c"]))
async def process_lesson_task1_answer(callback: CallbackQuery):
    """Обработка ответа на задание 1"""
    await callback.answer()

    if callback.data == "lesson_task1_a":
        response = "✅ Правильно!\n\n" + config.LESSON_TASK1_EXPLANATION
    else:
        response = "❌ Неправильно. Правильный ответ: a) kitchen\n\n" + config.LESSON_TASK1_EXPLANATION

    await callback.message.answer(
        text=response,
        reply_markup=get_lesson_task1_next()
    )


# Переход к заданию 2 - викторина с множественным выбором
@dp.callback_query(F.data == "lesson_task2")
async def process_lesson_task2(callback: CallbackQuery):
    """Задание 2 - викторина с множественным выбором"""
    await callback.answer()

    # Отправляем текст вступления
    intro_text = """💭 Задание 2

Ты забыл слово "airport".
Часто, мы не можем сказать иначе, потому что не думаем о том, что находится в забытом месте."""

    await callback.message.answer(text=intro_text)

    # Отправляем викторину с множественным выбором и сразу объяснение
    await callback.message.answer_poll(
        question="Выбери предметы, которые относятся к аэропорту:",
        options=[
            "a plane",
            "a latter",
            "a suitcase",
            "a cat",
            "a flight ticket",
            "a gate"
        ],
        type="regular",  # Обычный poll, не quiz
        allows_multiple_answers=True,  # Разрешаем выбор нескольких вариантов
        is_anonymous=False
    )

    # Отправляем объяснение и кнопку продолжения (правильные ответы под спойлером)
    await callback.message.answer(
        text=config.LESSON_TASK2_EXPLANATION,
        reply_markup=get_lesson_task2_next()
    )


# Переход к заданию 3
@dp.callback_query(F.data == "lesson_task3")
async def process_lesson_task3(callback: CallbackQuery):
    """Задание 3 с аудио"""
    await callback.answer()

    # Отправляем аудио
    if os.path.exists(config.AUDIO_TASK3_PATH):
        audio_file = FSInputFile(config.AUDIO_TASK3_PATH)
        await callback.message.answer_audio(audio_file)

    await callback.message.answer(
        text=config.LESSON_TASK3_TEXT,
        reply_markup=get_lesson_task3_keyboard()
    )


# Обработчики ответов на задание 3
@dp.callback_query(F.data.in_(["lesson_task3_a", "lesson_task3_b", "lesson_task3_c"]))
async def process_lesson_task3_answer(callback: CallbackQuery):
    """Обработка ответа на задание 3"""
    await callback.answer()

    if callback.data == "lesson_task3_a":
        response = "✅ Правильно!\n\n" + config.LESSON_TASK3_EXPLANATION
    else:
        response = "❌ Неправильно. Правильный ответ: a) café\n\n" + config.LESSON_TASK3_EXPLANATION

    await callback.message.answer(
        text=response,
        reply_markup=get_lesson_task3_next()
    )


# Переход к заданию 4 (финал с мотивацией и предложением курса)
@dp.callback_query(F.data == "lesson_task4")
async def process_lesson_task4(callback: CallbackQuery):
    """Задание 4 - финальное сообщение с предложением курса"""
    await callback.answer()
    await callback.message.answer(
        text=config.LESSON_TASK4_TEXT,
        reply_markup=get_lesson_task4_keyboard(config.MINI_LESSON_URL)
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


# Обработчик кнопки "Промты"
@dp.callback_query(F.data == "show_prompts")
async def process_show_prompts(callback: CallbackQuery):
    """Показать раздел промтов"""
    await callback.answer()
    await callback.message.answer(
        text=config.PROMPTS_TEXT,
        reply_markup=get_start_keyboard()
    )


# Обработчик кнопки "Помощь"
@dp.callback_query(F.data == "show_help")
async def process_show_help(callback: CallbackQuery):
    """Показать помощь"""
    await callback.answer()
    await callback.message.answer(
        text=config.HELP_TEXT,
        reply_markup=get_start_keyboard()
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
