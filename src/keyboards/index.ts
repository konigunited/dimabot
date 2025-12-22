import { InlineKeyboard } from 'grammy';
import { prompts, ALL_PROMPTS_PRICE } from '../prompts';
import { courses } from '../courses';
import { CallbackAction } from '../types';

// ========== ГЛАВНОЕ МЕНЮ ==========

// Главное меню при /start (выбор: Промпты / Курсы)
export function getMainMenuKeyboard() {
  return new InlineKeyboard()
    .text('📝 Промпты', CallbackAction.PROMPTS_MENU)
    .row()
    .text('🎓 Курсы', CallbackAction.COURSES_MENU)
    .row()
    .text('❓ Помощь', CallbackAction.HELP)
    .text('💬 Поддержка', CallbackAction.SUPPORT);
}

// ========== МЕНЮ ПРОМПТОВ ==========

// Меню выбора промптов
export function getPromptsMenuKeyboard() {
  const keyboard = new InlineKeyboard();

  // Добавляем кнопки для каждого промпта
  prompts.forEach(prompt => {
    keyboard
      .text(`${prompt.emoji} ${prompt.title}`, `${CallbackAction.PROMPT}:${prompt.id}`)
      .row();
  });

  // Кнопка "Все промпты разом"
  keyboard.text('🎁 Все промпты разом', CallbackAction.ALL_PROMPTS).row();

  // Кнопка "Назад"
  keyboard.text('⬅️ Главное меню', CallbackAction.MAIN_MENU);

  return keyboard;
}

// Клавиатура страницы товара (отдельный промпт)
export function getProductKeyboard(promptId: string, price: number) {
  return new InlineKeyboard()
    .text(`💳 Оплатить ${price}₽`, `${CallbackAction.BUY}:${promptId}`)
    .row()
    .text('⬅️ Все промпты', CallbackAction.PROMPTS_MENU);
}

// Клавиатура для всех промптов сразу
export function getAllPromptsKeyboard() {
  return new InlineKeyboard()
    .text(`💳 Оплатить ${ALL_PROMPTS_PRICE}₽`, `${CallbackAction.BUY}:all`)
    .row()
    .text('⬅️ Все промпты', CallbackAction.PROMPTS_MENU);
}

// Клавиатура после оплаты промпта
export function getAfterPaymentKeyboard() {
  return new InlineKeyboard()
    .text('📝 Другие промпты', CallbackAction.PROMPTS_MENU)
    .row()
    .text('🏠 Главное меню', CallbackAction.MAIN_MENU);
}

// Клавиатура мок-оплаты (для MVP)
export function getMockPaymentKeyboard(promptId: string) {
  return new InlineKeyboard()
    .text('🔐 Оплатить (мок)', `${CallbackAction.PAY}:${promptId}`)
    .row()
    .text('⬅️ Отменить', `${CallbackAction.PROMPT}:${promptId === 'all' ? prompts[0].id : promptId}`);
}

// ========== МЕНЮ КУРСОВ ==========

// Меню выбора курсов
export function getCoursesMenuKeyboard() {
  const keyboard = new InlineKeyboard();

  // Добавляем кнопки для каждого курса
  courses.forEach(course => {
    keyboard
      .text(`${course.emoji} ${course.title}`, `${CallbackAction.COURSE}:${course.id}`)
      .row();
  });

  // Кнопка "Назад"
  keyboard.text('⬅️ Главное меню', CallbackAction.MAIN_MENU);

  return keyboard;
}

// Клавиатура страницы курса (приветствие)
export function getCourseWelcomeKeyboard(courseId: string) {
  return new InlineKeyboard()
    .text('📘 Получить гайд', `${CallbackAction.GET_GUIDE}:${courseId}`)
    .row()
    .text('⬅️ Все курсы', CallbackAction.COURSES_MENU);
}

// Клавиатура после получения гайда
export function getAfterGuideKeyboard(courseId: string) {
  return new InlineKeyboard()
    .text('🎯 Пройти мини-урок', `${CallbackAction.START_DEMO}:${courseId}`)
    .row()
    .text('⬅️ Все курсы', CallbackAction.COURSES_MENU)
    .text('🏠 Главное меню', CallbackAction.MAIN_MENU);
}

// Клавиатура для продолжения урока
export function getNextLessonKeyboard(courseId: string, lessonIndex: number) {
  const course = courses.find(c => c.id === courseId);
  const lesson = course?.lessons[lessonIndex];

  if (!lesson) return new InlineKeyboard();

  return new InlineKeyboard()
    .text(lesson.buttonText || '➡️ Далее', `${CallbackAction.NEXT_LESSON}:${courseId}:${lessonIndex}`);
}

// Клавиатура завершения курса (покупка)
export function getBuyCourseKeyboard(courseId: string, purchaseUrl?: string) {
  const keyboard = new InlineKeyboard();

  if (purchaseUrl) {
    keyboard.url('🚀 Пройти полный курс', purchaseUrl).row();
  }

  keyboard
    .text('⬅️ Все курсы', CallbackAction.COURSES_MENU)
    .text('🏠 Главное меню', CallbackAction.MAIN_MENU);

  return keyboard;
}
