# 📝 TaskManager

## 🚀 Возможности

- ✅ Создание, обновление, удаление задач
- 🏷 Привязка тегов к задачам
- 📆 Статусы задач: `new`, `in_progress`, `done`, `overdue`
- 🔎 Фильтрация задач по статусу
- ⏰ Автоматическая проверка и обновление статуса задач на `overdue` (если срок истёк)
- 🧩 JWT-авторизация (`<token>`)
- 📚 Логирование просроченных задач

---

## 📦 Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/daulethanov/TaskManager.git
cd TaskManager/
```


### ⚙️ Настройка

```bash
docker compose up -d 
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```


### 🚀 Запуск

```bash
uvicorn main:app
```

> 💡 Используется встроенная документация FastAPI (Swagger UI).
> http://127.0.0.1:8000/docs.
