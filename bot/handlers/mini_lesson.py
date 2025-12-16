from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.inline import get_back_to_menu_keyboard
import os

router = Router()


class MiniLessonStates(StatesGroup):
    task1 = State()
    task2 = State()
    task3 = State()
    task4 = State()


@router.callback_query(F.data == "mini_lesson")
async def start_mini_lesson(callback: CallbackQuery, state: FSMContext):
    """Начать мини-урок - Задание 1"""
    await callback.answer()

    # Задание 1
    text = """🍀 <b>Задание 1 -- Куда ты идешь?</b>

You go to cook dinner.

Где ты находишься?"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) kitchen", callback_data="task1_kitchen")],
        [InlineKeyboardButton(text="b) bedroom", callback_data="task1_bedroom")],
        [InlineKeyboardButton(text="c) bathroom", callback_data="task1_bathroom")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])

    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(MiniLessonStates.task1)


@router.callback_query(F.data.startswith("task1_") & ~F.data.in_(["task1_retry"]))
async def handle_task1(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа на задание 1"""
    answer = callback.data.split("_")[1]

    if answer == "kitchen":
        await callback.answer("✅ Правильно!")
        text = """✅ <b>Отлично!</b>

Теперь ты понимаешь, как обходить комнаты дома. Вот предложение "I went to the kitchen."

Забыл kitchen? Будешь вспоминать? Потратишь время. Просто скажи, что там делают: <b>I went to cook dinner.</b>

Ты скажешь, что ужин не готовил там? И вообще не готовишь? Ну так скажи, что там делаешь? Ешь, пьешь, посуду моешь? Понимаешь?"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Да, давай еще примеры", callback_data="task2_start")],
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
        ])

        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(MiniLessonStates.task2)
    else:
        await callback.answer("❌ Неправильно")

        keyboard_retry = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Попробовать еще раз", callback_data="task1_retry")],
            [InlineKeyboardButton(text="➡️ Продолжить", callback_data="task2_start")],
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
        ])

        await callback.message.answer(
            "❌ <b>Не совсем...</b>\n\nПодумай, где обычно готовят ужин (cook dinner)?",
            reply_markup=keyboard_retry,
            parse_mode="HTML"
        )


@router.callback_query(F.data == "task1_retry")
async def retry_task1(callback: CallbackQuery, state: FSMContext):
    """Повторить задание 1"""
    await start_mini_lesson(callback, state)


@router.callback_query(F.data == "task2_start")
async def start_task2(callback: CallbackQuery, state: FSMContext):
    """Задание 2 - множественный выбор"""
    await callback.answer()

    text = """💼 <b>Да пожалуйста. Задание 2</b>

Ты забыл слово "airport".

Часто, мы не можем сказать иначе, потому что не думаем о том, что находится в забытом месте.

<b>Выбери предметы, которые напрямую относятся к аэропорту:</b>

(Выбери все подходящие варианты)"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✈️ a plane", callback_data="task2_plane")],
        [InlineKeyboardButton(text="🪜 a ladder", callback_data="task2_ladder")],
        [InlineKeyboardButton(text="🧳 a suitcase", callback_data="task2_suitcase")],
        [InlineKeyboardButton(text="🐱 a cat", callback_data="task2_cat")],
        [InlineKeyboardButton(text="🎫 a flight ticket", callback_data="task2_ticket")],
        [InlineKeyboardButton(text="🚪 a gate", callback_data="task2_gate")],
        [InlineKeyboardButton(text="✅ Готово, продолжить", callback_data="task2_finish")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])

    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(selected=[])


@router.callback_query(F.data.startswith("task2_") & ~F.data.in_(["task2_start", "task2_finish", "task2_retry"]))
async def handle_task2_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора вариантов в задании 2"""
    data = await state.get_data()
    selected = data.get("selected", [])

    choice = callback.data.split("_")[1]

    if choice in selected:
        selected.remove(choice)
        await callback.answer("❌ Убрано")
    else:
        selected.append(choice)
        await callback.answer("✅ Добавлено")

    await state.update_data(selected=selected)


@router.callback_query(F.data == "task2_finish")
async def finish_task2(callback: CallbackQuery, state: FSMContext):
    """Завершение задания 2"""
    data = await state.get_data()
    selected = data.get("selected", [])

    # Правильные ответы
    correct_answers = {"plane", "suitcase", "ticket", "gate"}

    # Проверяем, выбраны ли хотя бы некоторые правильные ответы
    if len(set(selected) & correct_answers) >= 2:  # Минимум 2 правильных
        await callback.answer("✅ Отлично!")

        text = """👍 <b>Вывод:</b>

Намного проще передать смысл места, зная что там находится:

<i>"I came to a place with planes and I had a flight ticket"</i>

-- Я пришел в место с самолетами и у меня был билет.

Правильные ответы: plane, suitcase, flight ticket, gate."""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Логику улавливаю. Давай закрепим", callback_data="task3_start")],
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
        ])

        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(MiniLessonStates.task3)
    else:
        await callback.answer("❌ Попробуй выбрать правильные варианты")

        keyboard_retry = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Попробовать еще раз", callback_data="task2_retry")],
            [InlineKeyboardButton(text="➡️ Продолжить", callback_data="task3_start")],
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
        ])

        await callback.message.answer(
            "❌ <b>Подумай ещё!</b>\n\nЧто действительно связано с аэропортом? (самолеты, багаж, билеты...)",
            reply_markup=keyboard_retry,
            parse_mode="HTML"
        )


@router.callback_query(F.data == "task2_retry")
async def retry_task2(callback: CallbackQuery, state: FSMContext):
    """Повторить задание 2"""
    await start_task2(callback, state)


@router.callback_query(F.data == "task3_start")
async def start_task3(callback: CallbackQuery, state: FSMContext):
    """Задание 3 - аудио + вопрос"""
    await callback.answer()

    text = """🎧 <b>Давай. Задание 3</b>

Послушаем этого господина. Он сейчас расскажет, где находится, но место не назовет. Выбери его место."""

    await callback.message.answer(text, parse_mode="HTML")

    # Отправляем аудио
    mp3_path = os.path.join("assets", "BOT.mp3")
    if os.path.exists(mp3_path):
        mp3_file = FSInputFile(mp3_path)
        await callback.message.answer_audio(mp3_file)

    # Вопрос
    question_text = """🎤 <i>"I sit, drink coffee, and watch people walking outside."</i>

<b>Где он?</b>"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) café", callback_data="task3_cafe")],
        [InlineKeyboardButton(text="b) gym", callback_data="task3_gym")],
        [InlineKeyboardButton(text="c) post office", callback_data="task3_post")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])

    await callback.message.answer(question_text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("task3_") & ~F.data.in_(["task3_retry", "task3_start"]))
async def handle_task3(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа на задание 3"""
    answer = callback.data.split("_")[1]

    if answer == "cafe":
        await callback.answer("✅ Правильно!")
        text = """✅ <b>Видишь?</b>

Есть закон: <b>Мысль одна — слова разные.</b>

Любое слово можно передать другими словами и не молчать во время общения 😊"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Понял!", callback_data="task4_start")],
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
        ])

        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(MiniLessonStates.task4)
    else:
        await callback.answer("❌ Неправильно")

        keyboard_retry = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Попробовать еще раз", callback_data="task3_retry")],
            [InlineKeyboardButton(text="➡️ Продолжить", callback_data="task4_start")],
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
        ])

        await callback.message.answer(
            "❌ <b>Не совсем...</b>\n\nОн сидит, пьет кофе и смотрит на людей. Где обычно делают такое?",
            reply_markup=keyboard_retry,
            parse_mode="HTML"
        )


@router.callback_query(F.data == "task3_retry")
async def retry_task3(callback: CallbackQuery, state: FSMContext):
    """Повторить задание 3"""
    # Показываем снова вопрос с аудио
    text = """🎧 <b>Давай еще раз!</b>

Послушай внимательно и выбери правильный ответ."""

    await callback.message.answer(text, parse_mode="HTML")

    # Отправляем аудио
    mp3_path = os.path.join("assets", "BOT.mp3")
    if os.path.exists(mp3_path):
        mp3_file = FSInputFile(mp3_path)
        await callback.message.answer_audio(mp3_file)

    # Вопрос
    question_text = """🎤 <i>"I sit, drink coffee, and watch people walking outside."</i>

<b>Где он?</b>"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="a) café", callback_data="task3_cafe")],
        [InlineKeyboardButton(text="b) gym", callback_data="task3_gym")],
        [InlineKeyboardButton(text="c) post office", callback_data="task3_post")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])

    await callback.message.answer(question_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "task4_start")
async def start_task4(callback: CallbackQuery, state: FSMContext):
    """Задание 4 - мотивация и продажа"""
    await callback.answer()

    text = """🔥 <b>Просто, да?</b>

Ты уже передаёшь смысл, даже не вспоминая слово.

Хочешь продолжить и освоить это в реальных ситуациях?"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Пройти мини-курс 'Места'", callback_data="finish_lesson")],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])

    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "finish_lesson")
async def finish_lesson(callback: CallbackQuery, state: FSMContext):
    """Завершение урока - продажа"""
    await callback.answer()

    text = """🎯 <b>В полном мини-уроке ты научишься обходить забытые слова через смысл, не через зубрёжку.</b>

Аудио, интерактив, игры - все это обучит тебя тут 👇

🔗 <a href="https://speakbysteps.ru/tariff-mini/">Перейти к мини-курсу на сайте</a>"""

    await callback.message.answer(text, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
    await state.clear()
