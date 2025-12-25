import { Context } from 'grammy';
import { CallbackAction } from '../types';
import { getPromptById, getAllPromptsContent, prompts, ALL_PROMPTS_PRICE, WELCOME_MESSAGE, HELP_MESSAGE, SUPPORT_MESSAGE } from '../prompts';
import {
  getProductKeyboard,
  getAllPromptsKeyboard,
  getMainMenuKeyboard,
  getPromptsMenuKeyboard,
  getAfterPaymentKeyboard,
} from '../keyboards';
import { createOrder, updateOrderStatus, getOrderByPaymentId, saveUser } from '../database';
import { createPayment, getPayment } from '../services/yukassa';
import { InlineKeyboard } from 'grammy';

// Обработчик выбора конкретного промпта
export async function handlePromptSelection(ctx: Context) {
  if (!ctx.callbackQuery?.data) return;

  const promptId = ctx.callbackQuery.data.split(':')[1];
  const prompt = getPromptById(promptId);

  if (!prompt) {
    await ctx.answerCallbackQuery('Промпт не найден');
    return;
  }

  const message = `${prompt.emoji} **${prompt.title}**

${prompt.description}

💰 **Цена:** ${prompt.price}₽`;

  await ctx.answerCallbackQuery();
  await ctx.reply(message, {
    reply_markup: getProductKeyboard(promptId, prompt.price),
    parse_mode: 'Markdown',
  });
}

// Обработчик "Все промпты разом"
export async function handleAllPrompts(ctx: Context) {
  const totalRegularPrice = prompts.reduce((sum, p) => sum + p.price, 0);
  const discount = totalRegularPrice - ALL_PROMPTS_PRICE;

  const message = `🎁 **Все промпты разом**

Получи все ${prompts.length} промптов по специальной цене!

📦 **Включает:**
${prompts.map(p => `  ${p.emoji} ${p.title}`).join('\n')}

💵 ~~${totalRegularPrice}₽~~ → **${ALL_PROMPTS_PRICE}₽**
💰 **Экономия:** ${discount}₽`;

  await ctx.answerCallbackQuery();
  await ctx.reply(message, {
    reply_markup: getAllPromptsKeyboard(),
    parse_mode: 'Markdown',
  });
}

// Обработчик нажатия кнопки "Оплатить"
export async function handleBuyPrompt(ctx: Context) {
  if (!ctx.callbackQuery?.data || !ctx.from) return;

  const promptId = ctx.callbackQuery.data.split(':')[1];

  // Сохраняем пользователя в БД (если его еще нет)
  saveUser(ctx.from.id, ctx.from.username, ctx.from.first_name, ctx.from.last_name);

  let price: number;
  let title: string;

  if (promptId === 'all') {
    price = ALL_PROMPTS_PRICE;
    title = 'Все промпты';
  } else {
    const prompt = getPromptById(promptId);
    if (!prompt) {
      await ctx.answerCallbackQuery('Промпт не найден');
      return;
    }
    price = prompt.price;
    title = prompt.title;
  }

  // Создаем заказ в БД
  const orderId = createOrder(ctx.from.id, promptId, price);

  try {
    // Создаем платеж в ЮKassa
    const payment = await createPayment({
      amount: price,
      description: `Оплата: ${title}`,
      orderId: orderId.toString(),
      metadata: {
        userId: ctx.from.id,
        promptId,
      },
    });

    // Сохраняем payment_id в БД
    updateOrderStatus(orderId, 'pending', payment.id);

    // Получаем URL для оплаты
    const paymentUrl = payment.confirmation?.confirmation_url;

    if (!paymentUrl) {
      throw new Error('Не удалось получить URL для оплаты');
    }

    const message = `💳 **Оплата**

📦 **Товар:** ${title}
💰 **Цена:** ${price}₽

**Как оплатить:**
1️⃣ Нажми "Оплатить" ниже
2️⃣ После оплаты вернись сюда
3️⃣ Нажми "Я оплатил ✅" для проверки`;

    const keyboard = new InlineKeyboard()
      .url('💳 Оплатить', paymentUrl)
      .row()
      .text('✅ Я оплатил', `${CallbackAction.CHECK_PAYMENT}:${payment.id}`)
      .row()
      .text('🏠 Главное меню', CallbackAction.MAIN_MENU);

    await ctx.answerCallbackQuery();
    await ctx.reply(message, {
      reply_markup: keyboard,
      parse_mode: 'Markdown',
    });
  } catch (error) {
    console.error('Ошибка создания платежа:', error);
    await ctx.answerCallbackQuery('Ошибка создания платежа. Попробуйте позже.');

    // Показываем сообщение с кнопкой возврата в меню
    await ctx.reply('Произошла ошибка при создании платежа. Пожалуйста, попробуйте позже.', {
      reply_markup: new InlineKeyboard().text('🏠 Главное меню', CallbackAction.MAIN_MENU),
    });
  }
}

// Обработчик кнопки "Главное меню"
export async function handleMainMenu(ctx: Context) {
  await ctx.answerCallbackQuery();
  await ctx.reply(WELCOME_MESSAGE, {
    reply_markup: getMainMenuKeyboard(),
    parse_mode: 'Markdown',
  });
}

// Обработчик кнопки "Меню промптов"
export async function handlePromptsMenu(ctx: Context) {
  const message = `📝 **Готовые ChatGPT-промпты для английского**

Выбери промпт, который хочешь получить 👇`;

  await ctx.answerCallbackQuery();
  await ctx.reply(message, {
    reply_markup: getPromptsMenuKeyboard(),
    parse_mode: 'Markdown',
  });
}

// Обработчик кнопки "Помощь"
export async function handleHelp(ctx: Context) {
  await ctx.answerCallbackQuery();
  await ctx.reply(HELP_MESSAGE, {
    reply_markup: getMainMenuKeyboard(),
    parse_mode: 'Markdown',
  });
}

// Обработчик кнопки "Поддержка"
export async function handleSupport(ctx: Context) {
  await ctx.answerCallbackQuery();
  await ctx.reply(SUPPORT_MESSAGE, {
    reply_markup: getMainMenuKeyboard(),
    parse_mode: 'Markdown',
  });
}

// Обработчик проверки платежа (БЕЗ webhook)
export async function handleCheckPayment(ctx: Context) {
  if (!ctx.callbackQuery?.data || !ctx.from) return;

  const paymentId = ctx.callbackQuery.data.split(':')[1];

  try {
    await ctx.answerCallbackQuery('Проверяем статус оплаты...');

    // Получаем информацию о платеже из ЮKassa
    const payment = await getPayment(paymentId);

    if (payment.status === 'succeeded') {
      // Платеж успешен! Обновляем БД и отправляем промпт
      const order: any = getOrderByPaymentId(paymentId);

      if (!order) {
        await ctx.reply('Ошибка: заказ не найден');
        return;
      }

      // Обновляем статус заказа
      updateOrderStatus(order.id, 'paid', paymentId);

      // Получаем контент промпта
      let content: string;
      let title: string;

      if (order.prompt_id === 'all') {
        content = getAllPromptsContent();
        title = 'Все промпты';
      } else {
        const prompt = getPromptById(order.prompt_id);
        if (!prompt) {
          await ctx.reply('Ошибка: промпт не найден');
          return;
        }
        content = prompt.content;
        title = prompt.title;
      }

      // Отправляем успешное сообщение
      const successMessage = `🎉 **Готово! Платёж получен**

📥 Вот твой промпт 👇`;

      await ctx.reply(successMessage, {
        reply_markup: getAfterPaymentKeyboard(),
        parse_mode: 'Markdown',
      });

      // Отправляем промпт
      const MAX_LENGTH = 4000;
      if (content.length <= MAX_LENGTH) {
        await ctx.reply(content);
      } else {
        const parts = [];
        for (let i = 0; i < content.length; i += MAX_LENGTH) {
          parts.push(content.substring(i, i + MAX_LENGTH));
        }
        for (const part of parts) {
          await ctx.reply(part);
        }
      }

      // Инструкция
      const instructionMessage = `📘 **Как пользоваться:**

1️⃣ Скопируй весь текст промпта выше
2️⃣ Вставь в ChatGPT
3️⃣ Начинай тренировку 🔥

💡 Хочешь больше промптов? Нажми кнопку ниже 👇`;

      await ctx.reply(instructionMessage, {
        reply_markup: getAfterPaymentKeyboard(),
        parse_mode: 'Markdown',
      });
    } else if (payment.status === 'pending' || payment.status === 'waiting_for_capture') {
      // Платеж еще в процессе
      await ctx.reply(`⏳ Платеж еще обрабатывается...

Статус: ${payment.status}

Подождите немного и нажмите "Я оплатил ✅" снова.`, {
        reply_markup: new InlineKeyboard()
          .text('✅ Проверить снова', `${CallbackAction.CHECK_PAYMENT}:${paymentId}`)
          .row()
          .text('🏠 Главное меню', CallbackAction.MAIN_MENU),
      });
    } else {
      // Платеж отменен или ошибка
      const order: any = getOrderByPaymentId(paymentId);
      const promptId = order?.prompt_id || 'all';

      await ctx.reply(`❌ Платеж не завершен

Статус: ${payment.status}

Попробуйте оплатить снова или обратитесь в поддержку.`, {
        reply_markup: new InlineKeyboard()
          .text('🔄 Попробовать снова', `${CallbackAction.BUY}:${promptId}`)
          .row()
          .text('🏠 Главное меню', CallbackAction.MAIN_MENU),
      });
    }
  } catch (error) {
    console.error('Ошибка проверки платежа:', error);
    await ctx.reply('Произошла ошибка при проверке платежа. Попробуйте позже.', {
      reply_markup: new InlineKeyboard()
        .text('✅ Проверить снова', `${CallbackAction.CHECK_PAYMENT}:${paymentId}`)
        .row()
        .text('🏠 Главное меню', CallbackAction.MAIN_MENU),
    });
  }
}
