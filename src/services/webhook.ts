import express, { Request, Response } from 'express';
import { Bot } from 'grammy';
import { updateOrderStatus } from '../database';
import { getPromptById, getAllPromptsContent } from '../prompts';
import { getAfterPaymentKeyboard } from '../keyboards';

const app = express();
app.use(express.json());

let bot: Bot;

/**
 * Инициализация webhook сервера
 */
export function initWebhookServer(telegramBot: Bot, port: number = 3000) {
  bot = telegramBot;

  // Webhook endpoint для уведомлений от ЮKassa
  app.post('/webhook', handleYuKassaWebhook);

  // Health check endpoint
  app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'ok' });
  });

  app.listen(port, () => {
    console.log(`🌐 Webhook сервер запущен на порту ${port}`);
  });

  return app;
}

/**
 * Обработчик webhook от ЮKassa
 */
async function handleYuKassaWebhook(req: Request, res: Response) {
  try {
    const notification = req.body;

    console.log('Получено уведомление от ЮKassa:', JSON.stringify(notification, null, 2));

    // Проверяем тип события
    if (notification.event === 'payment.succeeded') {
      const payment = notification.object;
      const { orderId, userId, promptId } = payment.metadata;

      // Обновляем статус заказа в БД
      updateOrderStatus(orderId, 'paid', payment.id);

      // Отправляем промпт пользователю
      await sendPromptToUser(userId, promptId);
    }

    // Возвращаем 200 OK
    res.status(200).send('OK');
  } catch (error) {
    console.error('Ошибка обработки webhook:', error);
    res.status(500).send('Internal Server Error');
  }
}

/**
 * Отправка промпта пользователю после успешной оплаты
 */
async function sendPromptToUser(userId: number, promptId: string) {
  try {
    let content: string;
    let title: string;

    if (promptId === 'all') {
      content = getAllPromptsContent();
      title = 'Все промпты';
    } else {
      const prompt = getPromptById(promptId);
      if (!prompt) {
        console.error(`Промпт с ID ${promptId} не найден`);
        return;
      }
      content = prompt.content;
      title = prompt.title;
    }

    const successMessage = `🎉 Готово! Платёж получен.

Вот твой промпт 👇`;

    await bot.api.sendMessage(userId, successMessage, {
      reply_markup: getAfterPaymentKeyboard(),
    });

    // Отправляем промпт отдельным сообщением
    // Разбиваем на части, если текст слишком длинный (лимит Telegram - 4096 символов)
    const MAX_LENGTH = 4000;
    if (content.length <= MAX_LENGTH) {
      await bot.api.sendMessage(userId, content);
    } else {
      // Разбиваем на части
      const parts = [];
      for (let i = 0; i < content.length; i += MAX_LENGTH) {
        parts.push(content.substring(i, i + MAX_LENGTH));
      }

      for (const part of parts) {
        await bot.api.sendMessage(userId, part);
      }
    }

    // Инструкция
    const instructionMessage = `📘 Как пользоваться:

1️⃣ Скопируй весь текст промпта выше
2️⃣ Вставь в ChatGPT
3️⃣ Начинай тренировку 🔥

Если хочешь больше таких промптов — нажми кнопку ниже 👇`;

    await bot.api.sendMessage(userId, instructionMessage, {
      reply_markup: getAfterPaymentKeyboard(),
    });

    console.log(`✅ Промпт успешно отправлен пользователю ${userId}`);
  } catch (error) {
    console.error('Ошибка отправки промпта пользователю:', error);
  }
}
