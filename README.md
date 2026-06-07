# Herzen Schedule Bot

> Дипломная работа: Разработка телеграм-бота для составления расписания ВУЗов

---

## ⚙️ Переменные окружения

| Переменная            | Описание                         | Пример                              |
|-----------------------|----------------------------------|-------------------------------------|
| TELEGRAM_TOKEN        | Токен Telegram-бота              | 123:ABC                             |
| ADMIN_TELEGRAM_ID     | ID администратора                | 123456789                           |
| WEBHOOK_HOST          | URL для вебхука                  | https://example.com                 |
| WEBAPP_PORT           | Порт веб-сервера (по умолчанию)  | 5000                                |
| DONATE_URL            | Ссылка на донат                  | https://pay.cloudtips.ru/p/0a19cb8e |
| SUBSCRIBE_URL         | Ссылка на подписку               | https://boosty.to/dant4ick          |
| TIMEZONE              | IANA-таймзона бота               | Europe/Moscow                       |
| REDIS_URL             | URL Redis для кеша API           | redis://redis:6379/0                |

---

## 🐍 Запуск в debug-режиме (локально)

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/Harder322/Schedule-Bot-of-Herzen
   ```
2. Создайте виртуальное окружение и активируйте:
   ```sh
   python3.10 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Отредактируйте значения
   ```
3. Запустите:
   ```sh
   python3 run.py --debug
   ```
   или
   ```sh
   sh start.sh
   ```

---

## 🛠️ Сборка и запуск своего Docker-образа (опционально)

1. Соберите образ:
   ```sh
   docker build -t herzen_schedule_bot:local .
   ```
2. Запустите:
   ```sh
   docker run --env-file .env -p 5000:5000 -v /var/lib/herzen_schedule_bot:/app/storage herzen_schedule_bot:local
   ```

---

## 🧩 Docker Compose

1. Пример `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     redis:
       image: redis:7-alpine
       container_name: herzen-schedule-redis
       restart: always
       command: ["redis-server", "--appendonly", "yes"]
       volumes:
         - ./dockerdata/redis:/data

     bot:
       image: ghcr.io/dant4ick/herzen_schedule_bot:latest
       container_name: herzen-schedule-bot
       restart: always
       environment:
         TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
         ADMIN_TELEGRAM_ID: ${ADMIN_TELEGRAM_ID}
         WEBHOOK_HOST: ${WEBHOOK_HOST}
         WEBAPP_HOST: 0.0.0.0
         WEBAPP_PORT: ${WEBAPP_PORT:-5000}
         TIMEZONE: ${TIMEZONE:-Europe/Moscow}
         REDIS_URL: redis://redis:6379/0
       volumes:
         - /var/lib/herzen_schedule_bot:/app/storage
       ports:
         - "5000:5000"
   ```
2. Запуск:
   ```sh
   docker compose up -d
   ```

---

## 🔄 Автообновление через Watchtower (опционально)

Запустите Watchtower отдельно, чтобы обновлять все контейнеры:
```sh
docker run -d --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e WATCHTOWER_POLL_INTERVAL=900 \
  -e WATCHTOWER_CLEANUP=true \
  containrrr/watchtower:latest --include-restarting --revive-stopped
```
