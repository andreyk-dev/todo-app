# Инструкция по установке и запуску проекта

Пошаговое руководство по локальному развёртыванию бэкенд-сервиса **To-Do & Categories API** с нуля.

---

## Системные требования

* **Python 3.12+**
* **Git**
* **Docker Desktop** (должен быть запущен)

---

## Пошаговый запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/andreyk-dev/todo-app.git
cd todo-app-backend
```

### 2. Создание и активация виртуального окружения
* **Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
*(Если скрипты заблокированы: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

* **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей и pre-commit
```bash
pip install --upgrade pip
pip install -r requirements.txt
pre-commit install
```

### 4. Запуск базы данных в Docker
```bash
docker compose up -d
```

### 5. Применение миграций Alembic
```bash
alembic upgrade head
```

### 6. Запуск сервера разработки
```bash
uvicorn app.main:app --reload
```
API начнёт принимать запросы по адресу: `http://127.0.0.1:8000`

---

## Документация API

После запуска веб-сервера интерактивная документация доступна в браузере:
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Запуск тестов и проверок качества
```bash
pytest -v                   # запуск 13 модульных тестов
mypy app                    # проверка статической типизации
ruff check app --fix        # проверка стиля и линтинг
pre-commit run --all-files  # комплексный запуск всех хуков
```

---

## Остановка проекта
* **Остановить базу данных:**
```bash
docker compose down
```