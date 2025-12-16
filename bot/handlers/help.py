from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.inline import get_back_to_menu_keyboard, get_courses_keyboard, get_prompts_keyboard
import os

router = Router()


@router.callback_query(F.data == "courses")
async def show_courses(callback: CallbackQuery):
    """Показать раздел Курсы"""
    courses_text = """🎓 <b>Курсы</b>

Выбери, что тебе интересно:

🏆 <b>Онлайн-курс</b> - полноценное обучение английскому с живым преподавателем

🎓 <b>Мини-урок "Места"</b> - компактный урок с практикой, который научит тебя обходить забытые слова через контекст"""

    await callback.message.edit_text(
        courses_text,
        reply_markup=get_courses_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "prompts")
async def show_prompts(callback: CallbackQuery):
    """Показать раздел Промпты"""
    prompts_text = """📚 <b>Промпты для ChatGPT</b>

Выбери промпт для тренировки:

🔵🟢🟣 <b>Вопросы в SIMPLE</b> - научись строить вопросы с to be, WHO и глаголами

🔵🟢🟣 <b>Вопросы в CONTINUOUS</b> - тренировка вопросов в Present, Past, Future Continuous

🎁 <b>КОМБО-наборы</b> - несколько промптов со скидкой

💎 <b>ВСЕ ПРОМПТЫ РАЗОМ</b> - максимальная выгода!"""

    await callback.message.edit_text(
        prompts_text,
        reply_markup=get_prompts_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    """Показать помощь"""
    help_text = """❓ <b>Помощь</b>

<b>Как пользоваться ботом:</b>

1️⃣ <b>Курсы</b> - для полноценного обучения с преподавателем
2️⃣ <b>Промпты</b> - готовые инструкции для тренировки с ChatGPT
3️⃣ <b>Помощь</b> - ты здесь 😊
4️⃣ <b>Контакт поддержки</b> - если возникли вопросы

<b>Как работают промпты:</b>
• Выбираешь нужный промпт
• Покупаешь его (оплата через бота)
• Получаешь PDF с промптом
• Копируешь текст и вставляешь в ChatGPT
• Начинаешь тренировку!

Если остались вопросы — напиши в поддержку: @dima_lingvist"""

    await callback.message.edit_text(
        help_text,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "support")
async def show_support(callback: CallbackQuery):
    """Показать контакт поддержки"""
    support_text = """💬 <b>Контакт поддержки</b>

Есть вопросы или предложения?

Напиши мне напрямую: @dima_lingvist

Отвечу как можно скорее! 😊"""

    await callback.message.edit_text(
        support_text,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


