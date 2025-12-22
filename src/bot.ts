import { Bot } from 'grammy';
import { config } from './config';
import { initDatabase } from './database';
import { initWebhookServer } from './services/webhook';
import { handleStart } from './handlers/start';
import {
  handlePromptSelection,
  handleAllPrompts,
  handleBuyPrompt,
  handleMockPayment,
  handleCheckPayment,
  handleMainMenu,
  handlePromptsMenu,
  handleHelp,
  handleSupport,
} from './handlers/callbacks';
import {
  handleCoursesMenu,
  handleCourseSelection,
  handleGetGuide,
  handleStartDemo,
  handleNextLesson,
  handleQuizAnswer,
  handlePollAnswer,
  handlePollCheck,
  handleAudioAnswer,
} from './handlers/courses';
import { CallbackAction } from './types';

// Инициализация бота
const bot = new Bot(config.botToken);

// Инициализация базы данных
initDatabase();

// Инициализация webhook сервера для приема уведомлений от ЮKassa
initWebhookServer(bot, 3000);

// ==================== КОМАНДЫ ====================

// Команда /start
bot.command('start', handleStart);

// ==================== ГЛАВНОЕ МЕНЮ ====================

// Кнопка "Главное меню"
bot.callbackQuery(CallbackAction.MAIN_MENU, handleMainMenu);

// Кнопка "Промпты"
bot.callbackQuery(CallbackAction.PROMPTS_MENU, handlePromptsMenu);

// Кнопка "Курсы"
bot.callbackQuery(CallbackAction.COURSES_MENU, handleCoursesMenu);

// Кнопка "Помощь"
bot.callbackQuery(CallbackAction.HELP, handleHelp);

// Кнопка "Поддержка"
bot.callbackQuery(CallbackAction.SUPPORT, handleSupport);

// ==================== ОБРАБОТЧИКИ ПРОМПТОВ ====================

// Выбор конкретного промпта
bot.callbackQuery(new RegExp(`^${CallbackAction.PROMPT}:`), handlePromptSelection);

// Кнопка "Все промпты разом"
bot.callbackQuery(CallbackAction.ALL_PROMPTS, handleAllPrompts);

// Кнопка "Оплатить"
bot.callbackQuery(new RegExp(`^${CallbackAction.BUY}:`), handleBuyPrompt);

// Мок-оплата
bot.callbackQuery(new RegExp(`^${CallbackAction.PAY}:`), handleMockPayment);

// Проверка реальной оплаты (БЕЗ webhook)
bot.callbackQuery(new RegExp(`^${CallbackAction.CHECK_PAYMENT}:`), handleCheckPayment);

// ==================== ОБРАБОТЧИКИ КУРСОВ ====================

// Выбор курса
bot.callbackQuery(new RegExp(`^${CallbackAction.COURSE}:`), handleCourseSelection);

// Получить гайд
bot.callbackQuery(new RegExp(`^${CallbackAction.GET_GUIDE}:`), handleGetGuide);

// Начать демо
bot.callbackQuery(new RegExp(`^${CallbackAction.START_DEMO}:`), handleStartDemo);

// Следующий урок
bot.callbackQuery(new RegExp(`^${CallbackAction.NEXT_LESSON}:`), handleNextLesson);

// Ответы на quiz
bot.callbackQuery(/^quiz_answer:/, handleQuizAnswer);

// Ответы на poll
bot.callbackQuery(/^poll_answer:/, handlePollAnswer);
bot.callbackQuery(/^poll_check:/, handlePollCheck);

// Ответы на audio quiz
bot.callbackQuery(/^audio_answer:/, handleAudioAnswer);

// ==================== ОБРАБОТКА ОШИБОК ====================

bot.catch((err) => {
  console.error('Ошибка в боте:', err);
});

// ==================== ЗАПУСК ====================

bot.start({
  onStart: () => {
    console.log('✅ Бот запущен успешно!');
    console.log('🚀 Отправь /start боту в Telegram');
  },
});

// Graceful shutdown
process.once('SIGINT', () => {
  console.log('\n⏹️  Остановка бота...');
  bot.stop();
});

process.once('SIGTERM', () => {
  console.log('\n⏹️  Остановка бота...');
  bot.stop();
});
