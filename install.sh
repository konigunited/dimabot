#!/bin/bash
set -e

echo "🚀 Установка English Telegram Bot..."

# Проверка что мы в правильной директории
if [ ! -f "bot.py" ]; then
    echo "❌ Ошибка: bot.py не найден. Запустите скрипт из директории проекта."
    exit 1
fi

# Установка зависимостей системы
echo "📦 Установка системных зависимостей..."
apt update
apt install -y python3-venv python3-pip

# Создание виртуального окружения
echo "🐍 Создание виртуального окружения..."
python3 -m venv venv

# Установка Python зависимостей
echo "📚 Установка Python пакетов..."
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Копирование systemd сервиса
echo "⚙️ Настройка systemd сервиса..."
cp english-bot.service /etc/systemd/system/

# Перезагрузка systemd
systemctl daemon-reload

# Включение автозапуска
systemctl enable english-bot.service

# Запуск сервиса
echo "▶️ Запуск бота..."
systemctl restart english-bot.service

# Проверка статуса
echo ""
echo "✅ Установка завершена!"
echo ""
echo "Статус бота:"
systemctl status english-bot.service --no-pager

echo ""
echo "📋 Полезные команды:"
echo "  systemctl status english-bot.service   - статус бота"
echo "  systemctl restart english-bot.service  - перезапуск бота"
echo "  systemctl stop english-bot.service     - остановка бота"
echo "  journalctl -u english-bot.service -f  - просмотр логов"
