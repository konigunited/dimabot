import express, { Request, Response } from 'express';
import { Bot, InputFile } from 'grammy';
import { updateOrderStatus } from '../database';
import { getPromptById } from '../prompts';
import { getAfterPaymentKeyboard } from '../keyboards';
import path from 'path';
import fs from 'fs';

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
    const prompt = getPromptById(promptId);
    if (!prompt) {
      console.error(`Промпт с ID ${promptId} не найден`);
      return;
    }

    const successMessage = `🎉 Готово! Платёж получен

📥 Вот твой промпт 👇`;

    await bot.api.sendMessage(userId, successMessage);

    // Отправляем PDF файл
    const pdfPath = path.join(process.cwd(), prompt.content);

    if (fs.existsSync(pdfPath)) {
      await bot.api.sendDocument(userId, new InputFile(pdfPath), {
        caption: `📄 ${prompt.title}`,
      });
    } else {
      await bot.api.sendMessage(userId, `⚠️ Ошибка: PDF файл не найден`);
    }

    // Инструкция
    const instructionMessage = `📘 **Как пользоваться:**

1️⃣ Открой PDF файл выше
2️⃣ Скопируй текст промпта
3️⃣ Вставь в ChatGPT (или любую LLM: DeepSeek, Claude, Gemini)
4️⃣ Начинай тренировку 🔥

⚠️ **Внимательно читай инструкции!**

💡 Хочешь больше промптов? Нажми кнопку ниже 👇`;

    await bot.api.sendMessage(userId, instructionMessage, {
      reply_markup: getAfterPaymentKeyboard(),
      parse_mode: 'Markdown',
    });

    console.log(`✅ Промпт успешно отправлен пользователю ${userId}`);
  } catch (error) {
    console.error('Ошибка отправки промпта пользователю:', error);
  }
}
