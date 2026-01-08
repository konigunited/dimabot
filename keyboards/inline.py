from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    """Клавиатура для приветствия"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Получить мини-урок", callback_data="get_guide")]
    ])
    return keyboard

def get_course_keyboard(course_url):
    """Клавиатура с ссылкой на курс"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Перейти к курсам на сайте", url=course_url)]
    ])
    return keyboard
