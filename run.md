# Памятка по запуску проекта (Docker + FastAPI + Frontend)

## 1. База данных (PostgreSQL в Docker)
> Перед выполнением убедись, что **Docker Desktop** запущен в Windows.

```powershell
# Запуск уже созданного контейнера
docker start pg-container

# Проверка статуса (в колонке STATUS должно быть Up)
docker ps
```

---

## 2. Бэкенд (FastAPI)
*Терминал 1 (папка проекта):*

```powershell
# 1. Переход в папку бэкенда
cd todo-app-backend

# 2. Активация виртуального окружения
venv\Scripts\activate

# 3. Запуск сервера с автоперезагрузкой
uvicorn main:app --port 8080 --reload
```

---

## 3. Фронтенд (React / Vite)
*Терминал 2:*

```powershell
# 1. Переход в папку фронтенда
cd todo-app-frontend

# 2. Запуск dev-сервера
npm run dev
# (или npm start, если проект на Create React App)
```

---

## Адреса и ссылки

| Сервис | Адрес | Описание |
| :--- | :--- | :--- |
| **Фронтенд** | `http://localhost:5173` *(или `:3000`)* | Интерфейс приложения |
| **Бэкенд** | `http://127.0.0.1:8080` | API сервер |
| **Swagger UI** | `http://127.0.0.1:8080/docs` | Документация и тестирование эндпоинтов |
| **ReDoc** | `http://127.0.0.1:8080/redoc` | Альтернативная документация |
| **PostgreSQL** | `localhost:5432` | Порт базы данных |

---

## Остановка работы

* **Бэкенд / Фронтенд:** нажать `Ctrl + C` в соответствующем окне терминала.
* **База данных:**
```powershell
docker stop pg-container
```

---

## Полезные команды

```powershell
# Вход в консоль PostgreSQL внутри контейнера
docker exec -it pg-container psql -U postgres -d postgres

# Создание контейнера с нуля (если удалил)
docker run --name pg-container -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres

docker start pg-container
```