import { YooCheckout, ICreatePayment } from '@a2seven/yoo-checkout';
import { config } from '../config';
import { v4 as uuidv4 } from 'uuid';

// Инициализация клиента ЮKassa
const checkout = new YooCheckout({
  shopId: config.yukassa.shopId,
  secretKey: config.yukassa.secretKey,
});

export interface CreatePaymentParams {
  amount: number;
  description: string;
  orderId: string;
  metadata?: Record<string, any>;
}

/**
 * Создание платежа в ЮKassa
 */
export async function createPayment(params: CreatePaymentParams) {
  const { amount, description, orderId, metadata = {} } = params;

  const idempotenceKey = uuidv4(); // Уникальный ключ для идемпотентности

  const createPayload: ICreatePayment = {
    amount: {
      value: amount.toFixed(2),
      currency: 'RUB',
    },
    confirmation: {
      type: 'redirect',
      return_url: 'https://t.me/your_bot', // URL для возврата пользователя после оплаты
    },
    capture: true, // Автоматическое подтверждение платежа
    description,
    metadata: {
      orderId,
      ...metadata,
    },
  };

  try {
    const payment = await checkout.createPayment(createPayload, idempotenceKey);
    return payment;
  } catch (error) {
    console.error('Ошибка создания платежа:', error);
    throw error;
  }
}

/**
 * Получение информации о платеже
 */
export async function getPayment(paymentId: string) {
  try {
    const payment = await checkout.getPayment(paymentId);
    return payment;
  } catch (error) {
    console.error('Ошибка получения информации о платеже:', error);
    throw error;
  }
}

/**
 * Отмена платежа
 */
export async function cancelPayment(paymentId: string) {
  try {
    const idempotenceKey = uuidv4();
    const payment = await checkout.cancelPayment(paymentId, idempotenceKey);
    return payment;
  } catch (error) {
    console.error('Ошибка отмены платежа:', error);
    throw error;
  }
}
