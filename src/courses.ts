import { Course } from './types';

// Данные о курсах
export const courses: Course[] = [
  {
    id: 'demo_course',
    emoji: '📚',
    title: 'Демо-курс',
    description: `Это демонстрационный курс для тестирования функционала.`,
    price: 0,
    purchaseUrl: 'https://speakbysteps.ru/',
    lessons: [
      {
        id: 'demo_1',
        type: 'message',
        question: `👋 Добро пожаловать в демо-курс!

Это тестовый урок для проверки работы бота.`,
        buttonText: '➡️ Продолжить',
      },
    ],
  },
];

// Функция для получения курса по ID
export function getCourseById(id: string): Course | undefined {
  return courses.find(c => c.id === id);
}

// Тексты гайдов для курсов
export const courseGuides: Record<string, string> = {
  demo_course: `📘 **Демо-гайд**

Это демонстрационный гайд для тестирования.`,
};
