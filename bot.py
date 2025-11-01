import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

WELCOME_TEXT = (
    "Привет! Я Димабот — твой проводник по гайду. "
    "Помогу тебе разобраться в процессе и пройти каждый шаг."
)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message) -> None:
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="📘 Получить гайд", callback_data="get_guide")
    )
    await message.answer(WELCOME_TEXT, reply_markup=keyboard)


@dp.callback_query_handler(text="get_guide")
async def process_get_guide(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()
    await callback_query.message.answer("Следующий шаг сценария будет добавлен позже.")


if __name__ == "__main__":
    executor.start_polling(dp)
