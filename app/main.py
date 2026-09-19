from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# 1. ИМПОРТИРУЕМ ВСЕ МОДЕЛИ (Это решение ошибки с 'Post')
# SQLAlchemy должна загрузить все классы в память при старте сервера
from app.models.user import User
from app.models.topic import Topic
from app.models.post import Post
from app.models.like import Like
# Если есть файл категории, также импортируй его:
# from app.models.category import Category

# 2. Импортируем роутеры
from app.routers import forum, categories, auth, users, topics
from app.core.config import settings
from app.db.database import get_session

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

# 3. Подключаем роутеры к главному приложению
app.include_router(forum.router)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(topics.router)
# app.include_router(posts.router)  # ⬅️ ДОБАВЛЕНО: раньше роутер posts был импортирован, но не подключен


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """Универсальный эндпоинт проверки работы сервера и базы данных."""
    try:
        await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status,
    }