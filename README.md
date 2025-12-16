# Telegram English Bot - MVP

Telegram-бот для продажи ChatGPT-промптов для изучения английского языка.

## Возможности MVP

- ✅ Приветственное сообщение с выбором промптов
- ✅ 3 отдельных промпта + пакет со скидкой
- ✅ Интеграция с ЮKassa (мок-режим для тестирования)
- ✅ База данных PostgreSQL
- ✅ Отправка промптов в PDF формате
- ✅ Автоматическая выдача после "оплаты"

## Технологии

- **Python 3.11+**
- **aiogram 3.x** - фреймворк для Telegram-ботов
- **PostgreSQL** - база данных
- **SQLAlchemy 2.0** - ORM
- **YooKassa SDK** - платежи (мок-режим)
- **Docker** - контейнеризация БД

## Структура проекта

```
telegram-english-bot/
├── bot/
│   ├── handlers/       # Обработчики команд и callback
│   │   ├── start.py    # /start и возврат в меню
│   │   └── products.py # Выбор и покупка промптов
│   ├── keyboards/      # Клавиатуры
│   │   └── inline.py   # Inline-кнопки
│   └── main.py         # Точка входа
├── database/
│   ├── models.py       # Модели БД (User, Product, Order)
│   ├── crud.py         # Операции с БД
│   └── db.py           # Подключение к БД
├── services/
│   └── payment.py      # Интеграция с ЮKassa (мок)
├── prompts/
│   └── products.py     # Данные о промптах
├── assets/             # PDF-файлы с промптами
│   ├── questions.pdf
│   ├── past_simple.pdf
│   └── speaking.pdf
├── config.py           # Настройки из .env
├── requirements.txt    # Зависимости
├── docker-compose.yml  # PostgreSQL
├── .env                # Переменные окружения (не коммитить!)
└── .env.example        # Пример .env
```

## Быстрый старт

### 1. Установка зависимостей

```bash
# Создай виртуальное окружение
python -m venv venv

# Активируй его (Windows)
venv\Scripts\activate

# Установи зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Файл `.env` уже создан с твоим токеном. Убедись, что там правильные данные:

```env
BOT_TOKEN=8256682945:AAHIV558GPcLXBYCLR9B5E75Rxcxim1_3jU
DATABASE_URL=postgresql+asyncpg://botuser:botpassword@localhost:5432/english_bot
MOCK_PAYMENTS=True  # МОК-РЕЖИМ: все покупки проходят бесплатно
DEBUG=True
```

### 3. Запуск PostgreSQL

```bash
# Запусти базу данных через Docker
docker-compose up -d

# Проверь, что контейнер запущен
docker ps
```

### 4. Добавь PDF с промптами

Положи PDF-файлы в папку `assets/`:
- `assets/questions.pdf`
- `assets/past_simple.pdf`
- `assets/speaking.pdf`

**Важно**: Названия файлов должны совпадать с `key` в `prompts/products.py`!

### 5. Запуск бота

```bash
# Из корня проекта
python bot/main.py
```

Если всё ок, увидишь:
```
INFO - Инициализация базы данных...
INFO - База данных инициализирована!
INFO - Бот запущен!
WARNING - ⚠️ МОК-РЕЖИМ ОПЛАТЫ ВКЛЮЧЕН! Все платежи проходят автоматически.
```

### 6. Тестирование

1. Открой Telegram и найди своего бота
2. Отправь `/start`
3. Выбери любой промпт
4. Нажми "Купить" - оплата пройдёт автоматически (мок)
5. Получи PDF с промптом

## Команды бота

- `/start` - Главное меню

## Мок-режим оплаты

По умолчанию включен `MOCK_PAYMENTS=True` в `.env`.

Это значит:
- ✅ Все покупки проходят **бесплатно и мгновенно**
- ✅ Не нужны реальные ключи ЮKassa
- ✅ Идеально для тестирования

Когда будешь готов принимать реальные платежи:
1. Зарегистрируйся в [ЮKassa](https://yookassa.ru/)
2. Получи `YOOKASSA_SHOP_ID` и `YOOKASSA_SECRET_KEY`
3. В `.env` установи `MOCK_PAYMENTS=False`
4. Добавь реальные ключи ЮKassa в `.env`

## База данных

### Модели

**User**
- `telegram_id` - ID пользователя в Telegram
- `username`, `first_name` - данные пользователя
- `created_at` - дата регистрации

**Product**
- `name` - название промпта
- `price` - цена в рублях
- `prompt_text` - текст промпта
- `product_key` - уникальный ключ (questions, past_simple, speaking, bundle)

**Order**
- `user_id`, `product_id` - связи
- `status` - pending/paid/cancelled
- `payment_id` - ID платежа в ЮKassa
- `created_at`, `paid_at` - даты

### Подключение к БД

```bash
# Посмотреть логи PostgreSQL
docker-compose logs -f

# Зайти в PostgreSQL
docker exec -it english_bot_db psql -U botuser -d english_bot

# Посмотреть таблицы
\dt

# Посмотреть пользователей
SELECT * FROM users;
```

## Что дальше (V2)

После тестирования MVP можно добавить:

- [ ] Админ-панель (статистика, рассылки)
- [ ] История покупок пользователя
- [ ] Реальные платежи через ЮKassa
- [ ] Реферальная система
- [ ] Больше промптов
- [ ] A/B тесты текстов
- [ ] Деплой на сервер (Railway/Render/VPS)

## Проблемы?

**Бот не отвечает:**
- Проверь, что токен правильный в `.env`
- Проверь, что бот запущен (`python bot/main.py`)

**Ошибка подключения к БД:**
- Запусти PostgreSQL: `docker-compose up -d`
- Проверь порт 5432: `docker ps`

**PDF не отправляются:**
- Проверь, что файлы есть в папке `assets/`
- Проверь названия файлов (должны совпадать с `product_key`)

## Лицензия

MIT
