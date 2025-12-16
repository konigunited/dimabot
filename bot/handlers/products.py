from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from bot.keyboards.inline import get_product_keyboard, get_back_to_menu_keyboard
from prompts.products import PRODUCTS
from database.db import async_session_maker
from database.crud import create_order, update_order_paid, get_or_create_user
from services.payment import create_payment, check_payment
from config import settings
import os

router = Router()


@router.callback_query(F.data.startswith("product_"))
async def show_product(callback: CallbackQuery):
    """Показать страницу товара"""
    product_key = callback.data.replace("product_", "")

    if product_key not in PRODUCTS:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    product = PRODUCTS[product_key]

    await callback.message.edit_text(
        product["description"],
        reply_markup=get_product_keyboard(product_key),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def process_purchase(callback: CallbackQuery):
    """Обработка покупки"""
    product_key = callback.data.replace("buy_", "")

    if product_key not in PRODUCTS:
        await callback.answer("Товар не найден!", show_alert=True)
        return

    product = PRODUCTS[product_key]

    # Получаем или создаем пользователя
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name
        )

        # Создаем платёж
        payment = create_payment(
            amount=product["price"],
            description=f"Промпт: {product['name']}"
        )

        # Создаем заказ в БД
        order = await create_order(
            session,
            user_id=callback.from_user.id,
            product_id=hash(product_key),  # Временно используем hash, позже добавим product_id в БД
            amount=product["price"] * 100,  # в копейках
            payment_id=payment["payment_id"]
        )

        # Проверяем статус оплаты
        payment_status = check_payment(payment["payment_id"])

        if payment_status["paid"]:
            # Оплата прошла (мок-режим)
            await update_order_paid(session, payment["payment_id"])

            # Отправляем промпт(ы)
            if product_key == "bundle":
                # Для полного набора отправляем один большой PDF
                await callback.message.answer(
                    "🎉 Готово! Платёж получен.\n\n"
                    "💎 Вот полный набор всех промптов 👇"
                )

                await send_prompt_file(callback.message, product, product_key)

                await callback.message.answer(
                    "📘 Как пользоваться:\n"
                    "1. Открой PDF файл с промптом\n"
                    "2. Скопируй нужный текст промпта\n"
                    "3. Вставь в ChatGPT\n"
                    "4. Начинай тренировку 🔥\n\n"
                    "💡 В файле собраны все 8 промптов для удобства!\n\n"
                    "Если хочешь вернуться в меню — нажми кнопку ниже 👇",
                    reply_markup=get_back_to_menu_keyboard()
                )
            elif product_key in ["combo_simple", "combo_cont"]:
                # Для комбо отправляем один комбо-файл
                await callback.message.answer(
                    "🎉 Готово! Платёж получен.\n\n"
                    "🎁 Вот твой КОМБО-набор 👇"
                )

                await send_prompt_file(callback.message, product, product_key)

                await callback.message.answer(
                    "📘 Как пользоваться:\n"
                    "1. Открой PDF файл с промптом\n"
                    "2. Скопируй нужный текст\n"
                    "3. Вставь в ChatGPT\n"
                    "4. Начинай тренировку 🔥\n\n"
                    "Если хочешь больше промптов — нажми кнопку ниже 👇",
                    reply_markup=get_back_to_menu_keyboard()
                )
            else:
                # Один промпт
                success_text = f"""🎉 Готово! Платёж получен.

Вот твой промпт 👇"""

                await callback.message.answer(success_text)

                # Отправляем файл с промптом
                await send_prompt_file(callback.message, product, product_key)

                await callback.message.answer(
                    "📘 Как пользоваться:\n"
                    "1. Открой PDF файл\n"
                    "2. Скопируй весь текст промпта\n"
                    "3. Вставь в ChatGPT\n"
                    "4. Начинай тренировку 🔥\n\n"
                    "Если хочешь больше таких промптов — нажми кнопку ниже 👇",
                    reply_markup=get_back_to_menu_keyboard()
                )
        else:
            # Если вдруг оплата не прошла (не должно случиться в мок-режиме)
            await callback.message.answer(
                "❌ Ошибка оплаты. Попробуйте снова или напишите в поддержку."
            )

    await callback.answer()


async def send_prompt_file(message, product, product_key):
    """Отправить файл с промптом"""
    # Используем file_name из продукта
    file_name = product.get("file_name", f"{product_key}.pdf")
    file_path = os.path.join("assets", file_name)

    if os.path.exists(file_path):
        # Отправляем PDF файл
        document = FSInputFile(file_path)
        await message.answer_document(
            document,
            caption=f"📄 {product['name']}"
        )
    else:
        # Если файла нет, сообщаем об ошибке
        await message.answer(
            f"❌ Файл {file_name} не найден. Обратитесь в поддержку."
        )
