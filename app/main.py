from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers import forum # 1. Импортируем наш файл роутера
from app.routers import categories
from app.routers import auth
from app.routers import users
from app.core.config import settings
from app.db.database import get_session

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

# 2. Подключаем роутер к главному приложению
app.include_router(forum.router)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(users.router)

# Создаем тот самый тестовый маршрут (эндпоинт)
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
  
