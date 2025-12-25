# Инструкция по деплою бота на сервер

## Шаг 1: Подключитесь к серверу

```bash
ssh root@109.69.23.108
```

## Шаг 2: Установите необходимые зависимости

```bash
# Обновите систему
apt update && apt upgrade -y

# Установите Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Установите Git
apt install -y git

# Установите build-tools (для native модулей типа better-sqlite3)
apt install -y build-essential python3

# Проверьте версии
node --version
npm --version
git --version
```

## Шаг 3: Склонируйте репозиторий

```bash
# Создайте директорию для приложения
mkdir -p /opt/english-prompts-bot
cd /opt/english-prompts-bot

# Склонируйте репозиторий
git clone https://github.com/konigunited/dimabot.git .
```

## Шаг 4: Настройте переменные окружения

```bash
# Создайте файл .env
nano .env
```

Добавьте в файл:
```
BOT_TOKEN=ваш_токен_бота_от_BotFather
COURSE_URL=https://ваш-сайт-курса.com
YUKASSA_SHOP_ID=ваш_shop_id
YUKASSA_SECRET_KEY=ваш_secret_key
```

Сохраните (Ctrl+O, Enter, Ctrl+X)

## Шаг 5: Установите зависимости и соберите проект

```bash
# Установите зависимости
npm install --production

# Соберите TypeScript в JavaScript
npm run build
```

## Шаг 6: Создайте systemd service для автозапуска

```bash
# Создайте файл сервиса
nano /etc/systemd/system/english-bot.service
```

Вставьте содержимое:
```ini
[Unit]
Description=English Prompts Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/english-prompts-bot
ExecStart=/usr/bin/node /opt/english-prompts-bot/dist/bot.js
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=english-bot

Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Сохраните (Ctrl+O, Enter, Ctrl+X)

## Шаг 7: Запустите бота

```bash
# Перезагрузите systemd
systemctl daemon-reload

# Включите автозапуск
systemctl enable english-bot

# Запустите бота
systemctl start english-bot

# Проверьте статус
systemctl status english-bot

# Посмотрите логи
journalctl -u english-bot -f
```

## Полезные команды

### Управление ботом
```bash
systemctl start english-bot      # Запустить
systemctl stop english-bot       # Остановить
systemctl restart english-bot    # Перезапустить
systemctl status english-bot     # Статус
```

### Логи
```bash
journalctl -u english-bot -f          # Следить за логами в реальном времени
journalctl -u english-bot -n 100      # Последние 100 строк
journalctl -u english-bot --since "1 hour ago"  # За последний час
```

### Обновление кода
```bash
cd /opt/english-prompts-bot
git pull origin main
npm install --production
npm run build
systemctl restart english-bot
```

## Готово!

Ваш бот должен быть запущен и работать. Проверьте его в Telegram!
