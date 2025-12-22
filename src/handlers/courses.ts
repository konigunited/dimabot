import { Context, InlineKeyboard } from 'grammy';
import { getCourseById } from '../courses';
import {
  getCoursesMenuKeyboard,
  getCourseWelcomeKeyboard,
  getAfterGuideKeyboard,
  getNextLessonKeyboard,
  getBuyCourseKeyboard,
} from '../keyboards';
import path from 'path';
import fs from 'fs';
import { InputFile } from 'grammy';

// Хранилище прогресса пользователя (в памяти, для MVP)
// В продакшне нужно использовать БД
const userProgress = new Map<string, { courseId: string; currentLessonIndex: number }>();

// Обработчик меню курсов
export async function handleCoursesMenu(ctx: Context) {
  const message = `🎓 **Интерактивные курсы**

Учись передавать смысл, не зубря слова!
Каждый курс включает тесты и практику.

Выбери курс 👇`;

  await ctx.answerCallbackQuery();
  await ctx.reply(message, {
    reply_markup: getCoursesMenuKeyboard(),
    parse_mode: 'Markdown',
  });
}

// Обработчик выбора курса
export async function handleCourseSelection(ctx: Context) {
  if (!ctx.callbackQuery?.data || !ctx.from) return;

  const courseId = ctx.callbackQuery.data.split(':')[1];
  const course = getCourseById(courseId);

  if (!course) {
    await ctx.answerCallbackQuery('Курс не найден');
    return;
  }

  const message = `${course.emoji} **${course.title}**

👋 **Привет!**

Здесь ты научишься передавать смысл, даже если слово вылетело из головы.

Получай гайд и применяй знания уже сегодня!`;

  await ctx.answerCallbackQuery();
  await ctx.reply(message, {
    reply_markup: getCourseWelcomeKeyboard(courseId),
    parse_mode: 'Markdown',
  });
}

// Обработчик получения гайда
export async function handleGetGuide(ctx: Context) {
  if (!ctx.callbackQuery?.data || !ctx.from) return;

  const courseId = ctx.callbackQuery.data.split(':')[1];
  const course = getCourseById(courseId);

  if (!course) {
    await ctx.answerCallbackQuery('Курс не найден');
    return;
  }

  await ctx.answerCallbackQuery('📎 Отправляю гайд...');

  // Отправляем сообщение
  await ctx.reply(`✅ **Отлично!**

Вот твой мини-гайд *"Как не забывать слова и говорить свободно"* 👇`, {
    parse_mode: 'Markdown',
  });

  // Проверяем существование файла
  const guidePath = path.join(process.cwd(), course.guideUrl || 'assets/guide.pdf');

  if (fs.existsSync(guidePath)) {
    // Отправляем PDF
    await ctx.replyWithDocument(new InputFile(guidePath));
  } else {
    // Если файла нет, отправляем заглушку
    await ctx.reply(`📄 [ЗДЕСЬ БУДЕТ PDF-ГАЙД]

⚠️ Для MVP: добавь файл по пути: ${course.guideUrl}
Или замени guideUrl в courses.ts на реальный путь.`);
  }

  // Предложение пройти урок
  const message = `🎯 **А теперь хочешь попробовать это на практике?**

Бесплатно пройди короткий пробный мини-урок:
⏱ Займет всего 3 минуты
✅ Сразу поймешь, что это работает`;

  await ctx.reply(message, {
    reply_markup: getAfterGuideKeyboard(courseId),
    parse_mode: 'Markdown',
  });
}

// Обработчик старта демо-урока
export async function handleStartDemo(ctx: Context) {
  if (!ctx.callbackQuery?.data || !ctx.from) return;

  const courseId = ctx.callbackQuery.data.split(':')[1];
  const course = getCourseById(courseId);

  if (!course || !course.lessons.length) {
    await ctx.answerCallbackQuery('Уроки не найдены');
    return;
  }

  // Сохраняем прогресс пользователя
  const progressKey = `${ctx.from.id}:${courseId}`;
  userProgress.set(progressKey, { courseId, currentLessonIndex: 0 });

  await ctx.answerCallbackQuery('🚀 Начинаем!');

  // Показываем первый урок
  await showLesson(ctx, courseId, 0);
}

// Обработчик следующего урока
export async function handleNextLesson(ctx: Context) {
  if (!ctx.callbackQuery?.data || !ctx.from) return;

  const parts = ctx.callbackQuery.data.split(':');
  const courseId = parts[1];
  const currentIndex = parseInt(parts[2]);

  await ctx.answerCallbackQuery();

  // Переходим к следующему уроку
  const nextIndex = currentIndex + 1;
  const progressKey = `${ctx.from.id}:${courseId}`;
  userProgress.set(progressKey, { courseId, currentLessonIndex: nextIndex });

  await showLesson(ctx, courseId, nextIndex);
}

// Функция отображения урока
async function showLesson(ctx: Context, courseId: string, lessonIndex: number) {
  const course = getCourseById(courseId);

  if (!course) return;

  // Если уроки закончились, показываем финал
  if (lessonIndex >= course.lessons.length) {
    const message = `🎯 **Готов продолжить обучение?**

В полном мини-курсе ты научишься обходить забытые слова через смысл, не через зубрёжку.

🎧 Аудио
🎮 Интерактив
🎲 Игры
✨ Всё это обучит тебя!`;

    await ctx.reply(message, {
      reply_markup: getBuyCourseKeyboard(courseId, course.purchaseUrl),
      parse_mode: 'Markdown',
    });
    return;
  }

  const lesson = course.lessons[lessonIndex];

  // В зависимости от типа урока показываем разный контент
  if (lesson.type === 'quiz') {
    await showQuiz(ctx, courseId, lessonIndex, lesson);
  } else if (lesson.type === 'poll') {
    await showPoll(ctx, courseId, lessonIndex, lesson);
  } else if (lesson.type === 'audio_quiz') {
    await showAudioQuiz(ctx, courseId, lessonIndex, lesson);
  } else if (lesson.type === 'message') {
    await showMessage(ctx, courseId, lessonIndex, lesson);
  }
}

// Показать quiz (одиночный выбор)
async function showQuiz(ctx: Context, courseId: string, lessonIndex: number, lesson: any) {
  const course = getCourseById(courseId);
  const totalLessons = course?.lessons.length || 0;
  const currentLesson = lessonIndex + 1;

  const keyboard = new InlineKeyboard();

  lesson.options?.forEach((option: string, index: number) => {
    keyboard.text(option, `quiz_answer:${courseId}:${lessonIndex}:${index}`).row();
  });

  const progressBar = `☂️ ${currentLesson}/${totalLessons}`;
  const message = `${progressBar}

${lesson.question || ''}`;

  await ctx.reply(message, {
    reply_markup: keyboard,
    parse_mode: 'Markdown',
  });
}

// Показать poll (множественный выбор)
async function showPoll(ctx: Context, courseId: string, lessonIndex: number, lesson: any) {
  const course = getCourseById(courseId);
  const totalLessons = course?.lessons.length || 0;
  const currentLesson = lessonIndex + 1;

  const keyboard = new InlineKeyboard();

  lesson.options?.forEach((option: string, index: number) => {
    keyboard.text(option, `poll_answer:${courseId}:${lessonIndex}:${index}`).row();
  });

  keyboard.text('✅ Проверить ответ', `poll_check:${courseId}:${lessonIndex}`);

  const progressBar = `☂️ ${currentLesson}/${totalLessons}`;
  const message = `${progressBar}

${lesson.question || ''}`;

  await ctx.reply(message, {
    reply_markup: keyboard,
    parse_mode: 'Markdown',
  });
}

// Показать audio quiz
async function showAudioQuiz(ctx: Context, courseId: string, lessonIndex: number, lesson: any) {
  const course = getCourseById(courseId);
  const totalLessons = course?.lessons.length || 0;
  const currentLesson = lessonIndex + 1;

  // Отправляем аудио (если есть)
  const audioPath = path.join(process.cwd(), lesson.audioUrl || '');

  if (fs.existsSync(audioPath)) {
    await ctx.replyWithAudio(new InputFile(audioPath));
  } else {
    await ctx.reply(`🎧 [ЗДЕСЬ БУДЕТ АУДИО]

⚠️ Для MVP: добавь аудиофайл по пути: ${lesson.audioUrl}`);
  }

  // Показываем вопрос с вариантами
  const keyboard = new InlineKeyboard();

  lesson.options?.forEach((option: string, index: number) => {
    keyboard.text(option, `audio_answer:${courseId}:${lessonIndex}:${index}`).row();
  });

  const progressBar = `☂️ ${currentLesson}/${totalLessons}`;
  const message = `${progressBar}

${lesson.question || ''}`;

  await ctx.reply(message, {
    reply_markup: keyboard,
    parse_mode: 'Markdown',
  });
}

// Показать простое сообщение
async function showMessage(ctx: Context, courseId: string, lessonIndex: number, lesson: any) {
  const course = getCourseById(courseId);
  const totalLessons = course?.lessons.length || 0;
  const currentLesson = lessonIndex + 1;

  const progressBar = `☂️ ${currentLesson}/${totalLessons}`;
  const message = `${progressBar}

${lesson.question || ''}`;

  await ctx.reply(message, {
    reply_markup: getNextLessonKeyboard(courseId, lessonIndex),
    parse_mode: 'Markdown',
  });
}

// Обработчик ответа на quiz
export async function handleQuizAnswer(ctx: Context) {
  if (!ctx.callbackQuery?.data) return;

  const parts = ctx.callbackQuery.data.split(':');
  const courseId = parts[1];
  const lessonIndex = parseInt(parts[2]);
  const answerIndex = parseInt(parts[3]);

  const course = getCourseById(courseId);
  if (!course) return;

  const lesson = course.lessons[lessonIndex];
  const isCorrect = lesson.correctAnswer === answerIndex;

  if (isCorrect) {
    await ctx.answerCallbackQuery('✅ Правильно!');

    // Показываем объяснение и кнопку далее
    const message = `✅ **Правильно!**

${lesson.explanation || ''}`;

    await ctx.reply(message, {
      reply_markup: getNextLessonKeyboard(courseId, lessonIndex),
      parse_mode: 'Markdown',
    });
  } else {
    await ctx.answerCallbackQuery('❌ Не то, попробуй ещё раз!');
  }
}

// Обработчики для poll и audio_quiz (упрощённые для MVP)
export async function handlePollAnswer(ctx: Context) {
  await ctx.answerCallbackQuery('Выбрано!');
}

export async function handlePollCheck(ctx: Context) {
  if (!ctx.callbackQuery?.data) return;

  const parts = ctx.callbackQuery.data.split(':');
  const courseId = parts[1];
  const lessonIndex = parseInt(parts[2]);

  const course = getCourseById(courseId);
  if (!course) return;

  const lesson = course.lessons[lessonIndex];

  // Для MVP просто показываем правильный ответ
  await ctx.answerCallbackQuery('✅ Проверено!');

  const message = `✅ **Проверено!**

${lesson.explanation || ''}`;

  await ctx.reply(message, {
    reply_markup: getNextLessonKeyboard(courseId, lessonIndex),
    parse_mode: 'Markdown',
  });
}

export async function handleAudioAnswer(ctx: Context) {
  // Аналогично handleQuizAnswer
  await handleQuizAnswer(ctx);
}
