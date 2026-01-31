from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    """Клавиатура для приветствия"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Курсы", callback_data="show_courses")],
        [InlineKeyboardButton(text="💡 Промты", callback_data="show_prompts")],
        [InlineKeyboardButton(text="📕 Гайды", callback_data="show_guides")],
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

def get_online_course_keyboard(course_url):
    """Клавиатура для онлайн курса"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить курс", url=course_url)],
        [InlineKeyboardButton(text="◀️ Назад к курсам", callback_data="show_courses")]
    ])
    return keyboard

# Клавиатуры для мини-урока
def get_lesson_task1_keyboard():
    """Клавиатура для задания 1"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) kitchen", callback_data="lesson_task1_a")],
        [InlineKeyboardButton(text="b) bedroom", callback_data="lesson_task1_b")],
        [InlineKeyboardButton(text="c) bathroom", callback_data="lesson_task1_c")]
    ])
    return keyboard

def get_lesson_task1_next():
    """Кнопка после задания 1"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, давай еще примеры", callback_data="lesson_task2")]
    ])
    return keyboard

def get_lesson_task2_next():
    """Кнопка после задания 2 (квиза)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Логику улавливаю. Давай закрепим", callback_data="lesson_task3")]
    ])
    return keyboard

def get_lesson_task3_keyboard():
    """Клавиатура для задания 3"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) café", callback_data="lesson_task3_a")],
        [InlineKeyboardButton(text="b) gym", callback_data="lesson_task3_b")],
        [InlineKeyboardButton(text="c) post office", callback_data="lesson_task3_c")]
    ])
    return keyboard

def get_lesson_task3_next():
    """Кнопка после задания 3"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Понятно", callback_data="lesson_task4")]
    ])
    return keyboard

def get_lesson_task4_keyboard(course_url):
    """Финальная клавиатура для задания 4"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Пройти мини-урок 'Места'", url=course_url)],
        [InlineKeyboardButton(text="◀️ Назад к курсам", callback_data="show_courses")]
    ])
    return keyboard

def get_prompts_menu(prompts):
    """Меню промптов"""
    buttons = []
    for prompt in prompts:
        buttons.append([InlineKeyboardButton(
            text=f"{prompt['emoji']} {prompt['title']}",
            callback_data=f"prompt_{prompt['id']}"
        )])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_prompt_detail_keyboard(prompt_id):
    """Клавиатура для деталей промпта"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить", callback_data=f"buy_prompt_{prompt_id}")],
        [InlineKeyboardButton(text="◀️ Назад к промптам", callback_data="show_prompts")]
    ])
    return keyboard

def get_help_keyboard():
    """Клавиатура для помощи"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Поддержка", callback_data="show_support")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")]
    ])
    return keyboard

def get_support_keyboard():
    """Клавиатура для поддержки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад к помощи", callback_data="show_help")]
    ])
    return keyboard
