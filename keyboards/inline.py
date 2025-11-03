from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_keyboard():
    """Клавиатура для приветствия"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Получить гайд", callback_data="get_guide")]
    ])
    return keyboard

def get_lesson_start_keyboard():
    """Клавиатура после получения гайда"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Пройти мини-урок", callback_data="start_lesson")]
    ])
    return keyboard

def get_task1_keyboard():
    """Клавиатура для задания 1"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) kitchen", callback_data="task1_a")],
        [InlineKeyboardButton(text="b) bedroom", callback_data="task1_b")],
        [InlineKeyboardButton(text="c) bathroom", callback_data="task1_c")]
    ])
    return keyboard

def get_task1_next_keyboard():
    """Кнопка 'Идем дальше' после задания 1"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Идем дальше", callback_data="task2")]
    ])
    return keyboard

def get_task2_keyboard():
    """Клавиатура для задания 2 (множественный выбор)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1) a plane ✓", callback_data="task2_done")],
        [InlineKeyboardButton(text="2) a latter", callback_data="task2_done")],
        [InlineKeyboardButton(text="3) a suitcase ✓", callback_data="task2_done")],
        [InlineKeyboardButton(text="4) a cat", callback_data="task2_done")],
        [InlineKeyboardButton(text="5) a flight ticket ✓", callback_data="task2_done")],
        [InlineKeyboardButton(text="6) a gate ✓", callback_data="task2_done")],
    ])
    return keyboard

def get_task2_next_keyboard():
    """Кнопка 'Погнали дальше!' после задания 2"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Погнали дальше!", callback_data="task3")]
    ])
    return keyboard

def get_task3_keyboard():
    """Клавиатура для задания 3"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) café", callback_data="task3_a")],
        [InlineKeyboardButton(text="b) gym", callback_data="task3_b")],
        [InlineKeyboardButton(text="c) post office", callback_data="task3_c")]
    ])
    return keyboard

def get_task3_next_keyboard():
    """Кнопка после задания 3"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="task4")]
    ])
    return keyboard

def get_task4_keyboard():
    """Клавиатура для задания 4 (мотивация)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🚀 Пройти мини-курс "Места"', callback_data="final")]
    ])
    return keyboard

def get_final_keyboard(course_url):
    """Финальная клавиатура с ссылкой на курс"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Перейти к мини-курсу на сайте", url=course_url)]
    ])
    return keyboard
