# Используем минималистичный официальный образ Python
FROM python:3.12-slim

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Копируем исходный код LeakFinder
COPY . /app

# Отключаем буферизацию вывода для удобного логирования
ENV PYTHONUNBUFFERED=1

# Запускаем LeakFinder с поддержкой передачи аргументов
ENTRYPOINT ["python", "leakfinder.py"]
