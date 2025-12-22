# Руководство по тестированию интеграции с ЮKassa

## Проблема: запросы к API ЮKassa зависают

Это может происходить по нескольким причинам:

### 1. Магазин не активирован для продакшена

Если у вас live-ключ (`live_XdalYS1...`), но магазин еще не прошел модерацию ЮKassa, API может не отвечать на запросы.

**Решение:**
- Зайдите в личный кабинет ЮKassa: https://yookassa.ru/my
- Проверьте статус магазина
- Если магазин не активирован, переключитесь на тестовый режим

### 2. Получение тестовых ключей

Для тестирования нужны **тестовые** ключи:

1. Войдите в личный кабинет ЮKassa
2. Перейдите в раздел "Интеграция"
3. Включите "Тестовый режим"
4. Скопируйте тестовые ключи:
   - Shop ID (тестовый)
   - Secret Key (тестовый, начинается с `test_`)

5. Обновите `.env`:
```env
YUKASSA_SHOP_ID=your_test_shop_id
YUKASSA_SECRET_KEY=test_xxxxxxxxxxxxxxxx
```

### 3. Проверка сетевого подключения

Проверьте, доступен ли API ЮKassa:

```bash
curl -u SHOP_ID:SECRET_KEY https://api.yookassa.ru/v3/payments
```

Замените `SHOP_ID:SECRET_KEY` на ваши учетные данные.

## Альтернатива: Тестирование без реальных платежей

Пока вы настраиваете ЮKassa, можете использовать мок-оплату, которая уже есть в боте.

### Временное переключение на мок-оплату

1. В файле `src/handlers/callbacks.ts` закомментируйте код с настоящими платежами
2. Используйте существующую функцию `handleMockPayment`

Или создайте простой переключатель в config:

```typescript
// src/config.ts
export const config = {
  // ...
  useMockPayments: process.env.USE_MOCK_PAYMENTS === 'true',
};
```

Добавьте в `.env`:
```env
USE_MOCK_PAYMENTS=true
```

И измените логику в `handleBuyPrompt`:

```typescript
if (config.useMockPayments) {
  // Показать кнопку мок-оплаты
  await ctx.reply(message, {
    reply_markup: getMockPaymentKeyboard(promptId),
  });
} else {
  // Настоящая интеграция с ЮKassa
  const payment = await createPayment(...)
  // ...
}
```

## Тестирование бота локально

Вы можете протестировать бота с мок-оплатой прямо сейчас:

```bash
npm run dev
```

Затем:
1. Откройте Telegram
2. Найдите своего бота
3. Отправьте `/start`
4. Выберите промпт
5. Нажмите "Оплатить"
6. Нажмите кнопку мок-оплаты
7. Получите промпт

## Следующие шаги

1. **Получите тестовые ключи** из личного кабинета ЮKassa
2. **Обновите .env** с тестовыми ключами
3. **Запустите тест** снова: `npx tsx test-payment.ts`
4. Если тест пройдет успешно:
   - Настройте ngrok
   - Настройте webhook в ЮKassa
   - Протестируйте полный цикл оплаты

## Полезные ссылки

- Личный кабинет ЮKassa: https://yookassa.ru/my
- Документация API: https://yookassa.ru/developers/api
- Тестовые данные: https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing
