import { Context, InputFile } from 'grammy';
import { InlineKeyboard } from 'grammy';
import { CallbackAction } from '../types';
import path from 'path';
import fs from 'fs';

// Данные о гайдах
export interface Guide {
    id: string;
    emoji: string;
    title: string;
    description: string;
    fileUrl: string; // путь к PDF файлу
}

// Список доступных гайдов
export const guides: Guide[] = [
    {
        id: 'speak_english',
        emoji: '📖',
        title: 'Как начать говорить на английском',
        description: 'Научись передавать смысл, даже если слово вылетело из головы. Получай мини-урок и применяй знания уже сегодня!',
        fileUrl: 'assets/гайды/guide_speak_english.pdf'
    }
];

// Сообщение для меню гайдов
export const GUIDES_MENU_MESSAGE = `📕 **Бесплатные гайды**

Здесь ты найдёшь полезные материалы для изучения английского.

Выбери гайд 👇`;

// Сообщение, если гайдов пока нет
export const NO_GUIDES_MESSAGE = `📕 **Гайды**

Раздел с бесплатными гайдами скоро появится!

Следи за обновлениями 🔔`;

// Клавиатура меню гайдов
export function getGuidesMenuKeyboard() {
    const keyboard = new InlineKeyboard();

    if (guides.length > 0) {
        guides.forEach(guide => {
            keyboard
                .text(`${guide.emoji} ${guide.title}`, `guide:${guide.id}`)
                .row();
        });
    }

    keyboard.text('⬅️ Главное меню', CallbackAction.MAIN_MENU);

    return keyboard;
}

// Обработчик меню гайдов
export async function handleGuidesMenu(ctx: Context) {
    await ctx.answerCallbackQuery();

    const message = guides.length > 0 ? GUIDES_MENU_MESSAGE : NO_GUIDES_MESSAGE;

    await ctx.editMessageText(message, {
        parse_mode: 'Markdown',
        reply_markup: getGuidesMenuKeyboard(),
    });
}

// Обработчик выбора конкретного гайда
export async function handleGuideSelection(ctx: Context) {
    await ctx.answerCallbackQuery('📎 Отправляю гайд...');

    const data = ctx.callbackQuery?.data;
    if (!data) return;

    const guideId = data.split(':')[1];
    const guide = guides.find(g => g.id === guideId);

    if (!guide) {
        await ctx.reply('❌ Гайд не найден');
        return;
    }

    // Отправляем PDF файл
    try {
        const pdfPath = path.join(process.cwd(), guide.fileUrl);

        if (fs.existsSync(pdfPath)) {
            await ctx.replyWithDocument(new InputFile(pdfPath), {
                caption: `${guide.emoji} **${guide.title}**\n\n${guide.description}`,
                parse_mode: 'Markdown',
            });
        } else {
            console.error(`Файл гайда не найден: ${pdfPath}`);
            await ctx.reply('❌ Файл гайда не найден. Пожалуйста, свяжитесь с поддержкой.');
        }
    } catch (error) {
        console.error('Ошибка отправки гайда:', error);
        await ctx.reply('❌ Не удалось отправить гайд. Попробуйте позже.');
    }
}
