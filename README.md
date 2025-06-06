# Онлайн-школа

Проект для покупки курсов.

## 🚀 Технологии

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery + Celery Beat
- Docker

## ⚙️ Установка и запуск

### Предварительные требования

1. Установите [Docker](https://www.docker.com/get-started)
2. Установите [Docker Compose](https://docs.docker.com/compose/install/)
3. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/AnikanovAleksei/online_school-.git
   cd online_school-
   ```

### Настройка окружения

1. Создайте файл `.env` в корне проекта на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Заполните переменные окружения в `.env` файле

### Запуск проекта
```bash
  docker-compose up --build
```

После запуска проект будет доступен по адресу: [http://localhost:8000](http://localhost:8000)

## 🛠 Команды

- Запуск в фоновом режиме:
  ```bash
  docker-compose up -d
  ```
- Остановка:
  ```bash
  docker-compose down
  ```
- Просмотр логов:
  ```bash
  docker-compose logs -f
  ```
- Создание миграций:
  ```bash
  docker-compose exec web python manage.py makemigrations
  ```
- Применение миграций:
  ```bash
  docker-compose exec web python manage.py migrate
  ```
- Создание суперпользователя:
  ```bash
  docker-compose exec web python manage.py createsuperuser
  ```

## 📦 Структура сервисов

- Web: [http://localhost:8000](http://localhost:8000)
- PostgreSQL: `postgres://db:5432`
- Redis: `redis://redis:6379`

## 🌱 Примеры переменных окружения

```ini
# Django
SECRET_KEY=your_secret-key
DEBUG=
NAME=namedb
USER=user_name_db
PASSWORD=your_password
HOST=your_host
PORT=your_port

# PostgreSQL
POSTGRES_DB=yourdb
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
```

## 📄 Лицензия

Укажите вашу лицензию (MIT, Apache и т.д.)