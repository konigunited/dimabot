import dotenv from 'dotenv';

dotenv.config();

export const config = {
  botToken: process.env.BOT_TOKEN || '',
  yukassa: {
    shopId: process.env.YUKASSA_SHOP_ID || '',
    secretKey: process.env.YUKASSA_SECRET_KEY || '',
  },
  webhookUrl: process.env.WEBHOOK_URL || '',
  // Временный режим мок-оплаты (пока настраиваются ключи ЮKassa)
  useMockPayments: process.env.USE_MOCK_PAYMENTS === 'true',
};

if (!config.botToken) {
  throw new Error('BOT_TOKEN is not defined in .env file');
}

// Проверяем ключи ЮKassa только если не используем мок-оплату
if (!config.useMockPayments && (!config.yukassa.shopId || !config.yukassa.secretKey)) {
  console.warn('⚠️  YUKASSA ключи не настроены. Используйте USE_MOCK_PAYMENTS=true для тестирования');
}
