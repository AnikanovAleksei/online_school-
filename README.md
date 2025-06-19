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

# 🚀 Инструкция по развертыванию

## 1. Настройка удаленного сервера

### 📋 Требования
- Сервер с ОС Ubuntu 20.04/22.04
- Открытые порты: `80 (HTTP)`, `22 (SSH)`
- Доступ по SSH с правами `sudo`

### 🛠 Шаги установки

#### 1. Установите Docker и Docker Compose
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
#### 2. Настройте фаервол
```bash
sudo ufw allow 80
sudo ufw allow 22
sudo ufw allow 443/tcp
sudo ufw enable
```
#### 3. Добавьте пользователя в группу docker
```bash
sudo usermod -aG docker $USER
newgrp docker
```
#### 4. 🔍 Проверка установки
```bash
docker --version
docker-compose --version
```
## 2. Настройка GitHub Secrets
```commandline
Необходимые секреты

Название	              Описание
DOCKER_HUB_USERNAME	      Ваш логин Docker Hub
DOCKER_HUB_TOKEN	      Токен доступа Docker Hub
SSH_KEY	                  Приватный SSH-ключ сервера
SERVER_IP	              IP-адрес вашего сервера
```

## 3. Запуск приложения
```commandline
Сборка образа
docker build -t your_app_name .

Запуск контейнера
docker run -d -p 80:8000 --name app_container your_app_name
```
## 🌐 Доступ к приложению
```commandline
Откройте в браузере:
http://ваш_сервер_ip
```

## 📄 Лицензия

Укажите вашу лицензию (MIT, Apache и т.д.)