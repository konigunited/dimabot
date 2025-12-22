# Настройка интеграции с ЮKassa

## Что было сделано

1. **Добавлены учетные данные в .env**
   - `YUKASSA_SHOP_ID=390517924621`
   - `YUKASSA_SECRET_KEY=live_XdalYS1_Of-6agxvffAx7kuNPm9oNTeVr4PK8bczx8w`
   - `WEBHOOK_URL=https://your-domain.com/webhook` (необходимо обновить!)

2. **Обновлен config.ts**
   - Добавлена конфигурация для ЮKassa
   - Добавлена проверка наличия учетных данных при запуске

3. **Создан сервис yukassa.ts** (`src/services/yukassa.ts`)
   - `createPayment()` - создание платежа
   - `getPayment()` - получение информации о платеже
   - `cancelPayment()` - отмена платежа

4. **Создан webhook handler** (`src/services/webhook.ts`)
   - Express сервер на порту 3000
   - Endpoint `/webhook` для уведомлений от ЮKassa
   - Автоматическая отправка промпта после успешной оплаты

5. **Обновлена БД**
   - Добавлено поле `payment_id` в таблицу orders
   - Добавлено поле `updated_at` для отслеживания изменений
   - Добавлена функция `getOrderById()`

6. **Интегрирована оплата в бот**
   - Обработчик `handleBuyPrompt` теперь создает настоящий платеж в ЮKassa
   - Пользователь получает кнопку с URL для оплаты
   - После оплаты webhook автоматически отправляет промпт

## Что нужно сделать для запуска

### 1. Настроить публичный URL

Вам нужен публичный URL для получения webhook от ЮKassa. Варианты:

**Вариант A: Использовать ngrok (для тестирования)**
```bash
# Установите ngrok
npm install -g ngrok

# Запустите туннель
ngrok http 3000

# Скопируйте URL вида https://xxxx-xx-xx-xxx-xxx.ngrok-free.app
```

**Вариант B: Развернуть на сервере**
- VPS (DigitalOcean, AWS, etc.)
- Heroku
- Railway
- Render

### 2. Обновить WEBHOOK_URL в .env

Замените в файле `.env`:
```env
WEBHOOK_URL=https://your-actual-domain.com/webhook
```

### 3. Настроить webhook в личном кабинете ЮKassa

1. Войдите в личный кабинет ЮKassa: https://yookassa.ru/my
2. Перейдите в "Настройки" → "Уведомления"
3. Добавьте URL: `https://your-domain.com/webhook`
4. Выберите события: `payment.succeeded`, `payment.canceled`
5. Сохраните

### 4. Обновить return_url в yukassa.ts

В файле `src/services/yukassa.ts` замените:
```typescript
return_url: 'https://t.me/your_bot'
```

На ссылку на ваш реальный бот, например:
```typescript
return_url: 'https://t.me/your_actual_bot_username'
```

### 5. Запустить бота

```bash
# Разработка
npm run dev

# Продакшн
npm run build
npm start
```

## Как это работает

1. **Пользователь выбирает промпт** → нажимает "Оплатить"
2. **Бот создает заказ в БД** и вызывает `createPayment()` в ЮKassa
3. **ЮKassa возвращает URL** для оплаты
4. **Бот отправляет кнопку** с URL для оплаты пользователю
5. **Пользователь переходит** и оплачивает
6. **ЮKassa отправляет webhook** на `/webhook` endpoint
7. **Webhook handler обрабатывает** уведомление и отправляет промпт
8. **Пользователь получает промпт** автоматически в Telegram

## Тестирование

### Тестовые карты ЮKassa

Для тестирования используйте тестовые карты:

**Успешная оплата:**
- Номер: `1111 1111 1111 1026`
- Срок: любая будущая дата
- CVC: любые 3 цифры
- 3-D Secure: `12345`

**Отклоненная оплата:**
- Номер: `1111 1111 1111 1027`

### Проверка webhook

Тестовые уведомления можно отправить через личный кабинет ЮKassa или с помощью curl:

```bash
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "payment.succeeded",
    "object": {
      "id": "test-payment-id",
      "status": "succeeded",
      "metadata": {
        "orderId": "1",
        "userId": 123456789,
        "promptId": "grammar"
      }
    }
  }'
```

## Безопасность

⚠️ **Важно:**

1. **Никогда не коммитьте .env** в git
2. **Проверяйте подпись webhook** от ЮKassa (можно добавить позже)
3. **Используйте HTTPS** для webhook endpoint
4. **Храните секретный ключ** в безопасности

## Дополнительные возможности

Что можно добавить:

- ✅ Проверка подписи webhook от ЮKassa
- ✅ Возврат платежей (refunds)
- ✅ История платежей для пользователя
- ✅ Уведомления администратору о новых платежах
- ✅ Автоматическая отмена неоплаченных заказов через N времени
- ✅ Аналитика продаж

## Поддержка

Документация ЮKassa: https://yookassa.ru/developers/api

Если возникают вопросы:
- Проверьте логи бота
- Проверьте логи webhook (должны выводиться в консоль)
- Проверьте настройки webhook в личном кабинете ЮKassa
