# Указываем базовый образ

FROM python:3.13

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер

COPY . .

# Открываем порт 8000 для взаимодействия с приложением

EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
