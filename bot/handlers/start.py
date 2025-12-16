from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import get_main_menu_keyboard
from database.db import async_session_maker
from database.crud import get_or_create_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    async with async_session_maker() as session:
        await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )

    welcome_text = """👋 Привет!

Я помогу тебе быстро прокачать английский!

**Что я умею:**

🎓 **Курсы** - обучение с живым преподавателем
📚 **Промпты** - готовые инструкции для ChatGPT
❓ **Помощь** - инструкции по использованию
💬 **Поддержка** - связь с преподавателем

Выбери нужный раздел 👇"""

    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    welcome_text = """👋 Привет!

Я помогу тебе быстро прокачать английский!

**Что я умею:**

🎓 **Курсы** - обучение с живым преподавателем
📚 **Промпты** - готовые инструкции для ChatGPT
❓ **Помощь** - инструкции по использованию
💬 **Поддержка** - связь с преподавателем

Выбери нужный раздел 👇"""

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()
