from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Product


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Курсы", callback_data="courses")],
        [InlineKeyboardButton(text="📚 Промпты", callback_data="prompts")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
        [InlineKeyboardButton(text="💬 Контакт поддержки", callback_data="support")]
    ])
    return keyboard


def get_courses_keyboard() -> InlineKeyboardMarkup:
    """Подменю Курсы"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Онлайн-курс", url="https://speakbysteps.ru/tariffs/")],
        [InlineKeyboardButton(text="🎓 Мини-урок 'Места'", callback_data="mini_lesson")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])
    return keyboard


def get_prompts_keyboard() -> InlineKeyboardMarkup:
    """Подменю Промпты"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # Вопросы в SIMPLE
        [InlineKeyboardButton(text="🔵 Вопросы в SIMPLE c to be", callback_data="product_simple_to_be")],
        [InlineKeyboardButton(text="🟢 Вопросы в SIMPLE c WHO", callback_data="product_simple_who")],
        [InlineKeyboardButton(text="🟣 Вопросы в SIMPLE с глаголами", callback_data="product_simple_verbs")],

        # Вопросы в CONTINUOUS
        [InlineKeyboardButton(text="🔵 Вопросы PRESENT CONTINUOUS", callback_data="product_present_cont")],
        [InlineKeyboardButton(text="🟢 Вопросы PAST CONTINUOUS", callback_data="product_past_cont")],
        [InlineKeyboardButton(text="🟣 Вопросы FUTURE CONTINUOUS", callback_data="product_future_cont")],

        # Комбо-наборы
        [InlineKeyboardButton(text="🎁 КОМБО: Вопросы в SIMPLE", callback_data="product_combo_simple")],
        [InlineKeyboardButton(text="🎁 КОМБО: Вопросы в CONTINUOUS", callback_data="product_combo_cont")],

        # Полный набор
        [InlineKeyboardButton(text="💎 ВСЕ ПРОМПТЫ РАЗОМ", callback_data="product_bundle")],

        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])
    return keyboard


def get_product_keyboard(product_key: str) -> InlineKeyboardMarkup:
    """Клавиатура для страницы товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить", callback_data=f"buy_{product_key}")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_menu")]
    ])
    return keyboard


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Другие промпты", callback_data="back_to_menu")]
    ])
    return keyboard
