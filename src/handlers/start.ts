import { Context } from 'grammy';
import { getMainMenuKeyboard } from '../keyboards';
import { saveUser } from '../database';
import { WELCOME_MESSAGE } from '../prompts';

export async function handleStart(ctx: Context) {
  const user = ctx.from;
  if (!user) return;

  // Сохраняем пользователя в БД
  saveUser(user.id, user.username, user.first_name, user.last_name);

  await ctx.reply(WELCOME_MESSAGE, {
    reply_markup: getMainMenuKeyboard(),
    parse_mode: 'Markdown',
  });
}
