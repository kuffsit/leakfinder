Вот хороший вариант `README.md` для твоего **LeakFinder**.

---

# 🔍 LeakFinder  
**LeakFinder** – это инструмент для поиска утечек **API-ключей, токенов, паролей и других секретов** в коде.  
Работает с Python, JavaScript, Go, конфигурационными файлами и `.env`-файлами.

## 🚀 Возможности
✅ **Поддержка множества форматов файлов** (`.py`, `.js`, `.go`, `.env`, `.yaml`, `.ini`, `.json`)  
✅ **Гибкая настройка паттернов** в `patterns.yaml`  
✅ **Автоматическое сканирование в текущей директории**  
✅ **Интерактивный HTML-отчёт или JSON-вывод**  
✅ **Лёгкая интеграция в CI/CD**  
✅ **Поддержка Docker**  

---

## 📦 Установка и использование

### 🔹 1. Локальный запуск (без Docker)
#### **1️⃣ Установка зависимостей**
```bash
pip install -r requirements.txt
```

#### **2️⃣ Запуск сканирования**
Сканирование текущей директории:
```bash
python leakfinder.py .
```
Сканирование конкретной папки:
```bash
python leakfinder.py path/to/project
```
Вывод отчёта в JSON:
```bash
python leakfinder.py path/to/project --format json
```

---

### 🐳 2. Запуск в Docker
#### **1️⃣ Сборка Docker-образа**
```bash
docker build -t leakfinder .
```

#### **2️⃣ Сканирование директории**
```bash
docker run --rm -v $(pwd):/app leakfinder .
```
или, если сканируем `test_project`:
```bash
docker run --rm -v $(pwd)/test_project:/app leakfinder .
```

#### **3️⃣ JSON-отчёт**
```bash
docker run --rm -v $(pwd)/test_project:/app leakfinder . --format json
```

---

## ⚙️ **Как добавить новые паттерны?**
Все правила хранятся в файле `patterns.yaml`.  
Ты можешь добавить свой паттерн, например, для **Slack-токенов**:
```yaml
Slack Token: "xox[baprs]-[0-9a-zA-Z]{10,48}"
```
После этого LeakFinder начнёт находить Slack-токены в коде!

---

## 📌 **Примеры найденных утечек**
```bash
⚠️ API Key найден в config.py на строке 7: API_KEY = "sk_live_abcdef123456EXAMPLE"
⚠️ Hardcoded Password найден в database.py на строке 4: PASSWORD = "supersecretpassword"
⚠️ AWS Access Key найден в .env на строке 2: AKIAEXAMPLE123456789
```

---

## 🔄 **Интеграция в CI/CD**
LeakFinder можно встроить в **GitHub Actions, GitLab CI/CD, Jenkins** и другие системы.

**Пример для GitHub Actions:**
```yaml
name: LeakFinder Scan
on: [push]
jobs:
  leakfinder:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v2

      - name: Run LeakFinder
        run: docker run --rm -v $(pwd):/app leakfinder .
```
Если в коде найдутся секреты, сборка **упадёт**! 🔥

