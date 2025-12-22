// Типы промптов
export interface Prompt {
  id: string;
  title: string;
  emoji: string;
  description: string;
  price: number;
  content: string;
}

// Типы курсов
export interface Course {
  id: string;
  title: string;
  emoji: string;
  description: string;
  price: number;
  guideUrl?: string; // Ссылка на PDF-гайд
  lessons: Lesson[];
  purchaseUrl?: string; // Ссылка на покупку полного курса
}

export interface Lesson {
  id: string;
  type: 'quiz' | 'poll' | 'audio_quiz' | 'message';
  question?: string;
  audioUrl?: string;
  options?: string[];
  correctAnswer?: number | number[]; // Индекс правильного ответа или массив индексов
  explanation?: string;
  buttonText?: string;
}

export interface UserProgress {
  userId: number;
  courseId: string;
  currentLessonIndex: number;
  completed: boolean;
}

// Типы для callback data
export enum CallbackAction {
  PROMPT = 'prompt',
  BUY = 'buy',
  PAY = 'pay',
  CHECK_PAYMENT = 'check_payment', // Проверка оплаты без webhook
  BACK = 'back',
  ALL_PROMPTS = 'all_prompts',

  // Новые действия для курсов и главного меню
  MAIN_MENU = 'main_menu',
  PROMPTS_MENU = 'prompts_menu',
  COURSES_MENU = 'courses_menu',

  // Действия для курсов
  COURSE = 'course',
  GET_GUIDE = 'get_guide',
  START_DEMO = 'start_demo',
  NEXT_LESSON = 'next_lesson',
  BUY_COURSE = 'buy_course',

  // Поддержка и помощь
  HELP = 'help',
  SUPPORT = 'support',
}
