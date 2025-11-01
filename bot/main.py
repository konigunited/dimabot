"""Runtime entry point and handlers for the Telegram onboarding bot."""

from __future__ import annotations

import asyncio
import logging
from typing import Final

from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from .config import BotConfig, load_config

try:  # pragma: no cover - optional dependency is always available in runtime
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - only triggered if dependency missing
    load_dotenv = None  # type: ignore[assignment]
from .conversation import ConversationFlow, Step, build_default_flow

LOGGER = logging.getLogger(__name__)
STEP_INDEX_KEY: Final[str] = "step_index"
FLOW_KEY: Final[str] = "flow"


def _render_step(step: Step) -> str:
    return f"<b>{step.title}</b>\n\n{step.body}"


def _build_keyboard(is_last_step: bool) -> InlineKeyboardMarkup:
    button_text = "Получить ссылку" if is_last_step else "Далее"
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(button_text, callback_data="advance")]]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""

    if not update.message:
        return

    flow: ConversationFlow = context.application.bot_data[FLOW_KEY]
    context.user_data[STEP_INDEX_KEY] = 0

    first_step = flow.first()
    await update.message.reply_html(
        _render_step(first_step),
        reply_markup=_build_keyboard(flow.is_last(0)),
    )


async def advance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Advance to the next step when the inline button is pressed."""

    if not update.callback_query:
        return

    query = update.callback_query
    await query.answer()

    flow: ConversationFlow = context.application.bot_data[FLOW_KEY]
    current_index = context.user_data.get(STEP_INDEX_KEY, 0)

    if flow.is_last(current_index):
        await _send_final_link(query, flow)
        context.user_data[STEP_INDEX_KEY] = 0
        return

    next_step = flow.next_step(current_index)
    if next_step is None:
        # Safety net in case the flow definition changes at runtime.
        await _send_final_link(query, flow)
        context.user_data[STEP_INDEX_KEY] = 0
        return

    new_index = current_index + 1
    context.user_data[STEP_INDEX_KEY] = new_index

    await query.edit_message_text(
        _render_step(next_step),
        reply_markup=_build_keyboard(flow.is_last(new_index)),
        parse_mode=ParseMode.HTML,
    )


async def _send_final_link(query: CallbackQuery, flow: ConversationFlow) -> None:
    """Send the final link message and log the event."""

    message = query.message
    if not message:
        return

    final_text = (
        "🎉 Вы прошли все шаги! Ниже находится финальная ссылка."
        " Возвращайтесь к /start, если нужно пройти путь заново."
    )

    await query.edit_message_text(
        _render_step(flow.steps[-1]),
        reply_markup=None,
        parse_mode=ParseMode.HTML,
    )

    await message.reply_html(
        final_text + f"\n\n<a href=\"{flow.final_link}\">Открыть ресурс</a>",
        disable_web_page_preview=True,
    )
    LOGGER.info("Final link sent to chat_id=%s", message.chat_id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "Используйте /start, чтобы начать прохождение. Кнопка в сообщениях"
        " поможет переходить между шагами."
    )


async def _on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.exception("Unhandled error while processing update: %s", update)
    config: BotConfig = context.application.bot_data["config"]
    if config.admin_chat_id:
        try:
            await context.bot.send_message(
                chat_id=config.admin_chat_id,
                text=(
                    "⚠️ В работе бота произошла ошибка. Проверьте логи приложения."
                ),
            )
        except Exception:  # pragma: no cover - best effort notification
            LOGGER.exception("Failed to notify admin about an error")


async def build_application(config: BotConfig) -> Application:
    """Create a configured Application instance."""

    flow = build_default_flow(config.final_link)
    app = (
        ApplicationBuilder()
        .token(config.token)
        .rate_limiter(AIORateLimiter())
        .build()
    )

    app.bot_data["config"] = config
    app.bot_data[FLOW_KEY] = flow

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(advance, pattern="^advance$"))
    app.add_error_handler(_on_error)

    return app


async def run() -> None:
    """Entry point used by ``python -m bot.main`` and scripts."""

    logging.basicConfig(level=logging.INFO)
    if load_dotenv is not None:
        load_dotenv()
    config = load_config()
    app = await build_application(config)

    LOGGER.info("Starting bot with final link %s", config.final_link)
    await app.initialize()
    await app.start()
    if app.updater is None:  # pragma: no cover - should not happen in normal use
        raise RuntimeError("Updater is not available")
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        if app.updater:
            await app.updater.stop()
        await app.stop()
        await app.shutdown()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
