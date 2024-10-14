# Используем базовый образ Python
FROM python:3.12

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Создание папки для логов и установка прав
RUN mkdir -p logs && chmod -R 777 logs

# Копирование файла зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только необходимые файлы (например, код)
COPY src/ ./src

# Устанавливаем рабочую директорию для запуска приложения
WORKDIR /app

# Команда для запуска приложения
CMD ["python", "src/main.py"]
