import dotenv from 'dotenv';
import { YooCheckout, ICreatePayment } from '@a2seven/yoo-checkout';
import { v4 as uuidv4 } from 'uuid';

dotenv.config();

async function testPayment() {
  console.log('🧪 Тестирование создания платежа в ЮKassa...\n');

  // Проверяем учетные данные
  const shopId = process.env.YUKASSA_SHOP_ID;
  const secretKey = process.env.YUKASSA_SECRET_KEY;

  console.log('📋 Проверка учетных данных:');
  console.log('Shop ID:', shopId);
  console.log('Secret Key:', secretKey ? `${secretKey.substring(0, 10)}...` : 'не задан');
  console.log('');

  if (!shopId || !secretKey) {
    console.error('❌ Ошибка: учетные данные не найдены в .env');
    process.exit(1);
  }

  try {
    console.log('🔄 Создание клиента ЮKassa...');
    const checkout = new YooCheckout({
      shopId: shopId,
      secretKey: secretKey,
    });

    console.log('✅ Клиент создан');
    console.log('');

    const idempotenceKey = uuidv4();
    console.log('🔑 Idempotence Key:', idempotenceKey);
    console.log('');

    const createPayload: ICreatePayment = {
      amount: {
        value: '100.00',
        currency: 'RUB',
      },
      confirmation: {
        type: 'redirect',
        return_url: 'https://t.me/your_bot',
      },
      capture: true,
      description: 'Тестовый платеж',
      metadata: {
        orderId: 'test-order-123',
        userId: 123456789,
        promptId: 'test-prompt',
      },
    };

    console.log('📤 Отправка запроса в ЮKassa...');
    console.log('Сумма:', createPayload.amount.value, createPayload.amount.currency);
    console.log('');

    const payment = await checkout.createPayment(createPayload, idempotenceKey);

    console.log('✅ Платеж успешно создан!');
    console.log('');
    console.log('📋 Информация о платеже:');
    console.log('ID платежа:', payment.id);
    console.log('Статус:', payment.status);
    console.log('Сумма:', payment.amount.value, payment.amount.currency);
    console.log('');
    console.log('🔗 URL для оплаты:');
    console.log(payment.confirmation?.confirmation_url);
    console.log('');
    console.log('💡 Откройте эту ссылку в браузере для тестовой оплаты');
    console.log('');
    console.log('📌 Используйте тестовую карту:');
    console.log('Номер: 1111 1111 1111 1026');
    console.log('Срок: любая будущая дата (например, 12/25)');
    console.log('CVC: 123');
    console.log('3-D Secure: 12345');
  } catch (error: any) {
    console.error('');
    console.error('❌ Ошибка при создании платежа:');
    console.error('');
    if (error.response) {
      console.error('HTTP Status:', error.response.status);
      console.error('Response data:', JSON.stringify(error.response.data, null, 2));
    } else if (error.message) {
      console.error('Сообщение:', error.message);
    } else {
      console.error(error);
    }
  }
}

testPayment();
