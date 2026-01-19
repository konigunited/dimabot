from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    """Клавиатура для приветствия"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Курсы", callback_data="show_courses")],
        [InlineKeyboardButton(text="💡 Промты", callback_data="show_prompts")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="show_help")]
    ])
    return keyboard

def get_course_keyboard(course_url):
    """Клавиатура с ссылкой на курс"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Перейти к курсам на сайте", url=course_url)]
    ])
    return keyboard

def get_courses_menu():
    """Меню курсов"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Получить мини-урок", callback_data="get_guide")],
        [InlineKeyboardButton(text="🎓 Обучи себя говорить на английском языке", callback_data="online_course")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")]
    ])
    return keyboard

def get_online_course_keyboard():
    """Клавиатура для онлайн курса"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить курс", callback_data="buy_online_course")],
        [InlineKeyboardButton(text="◀️ Назад к курсам", callback_data="show_courses")]
    ])
    return keyboard

def get_after_guide_keyboard():
    """Клавиатура после получения мини-урока"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад к курсам", callback_data="show_courses")]
    ])
    return keyboard
