from fastapi import FastAPI
from app.routers import forum # 1. Импортируем наш файл роутера

app = FastAPI(
    title="Mini-forum",  # название проекта 
    description="Учебный проект для Junior Python Developer",  #для чего проект 
    version="1.0.0"
)

# 2. Подключаем роутер к главному приложению
app.include_router(forum.router)

# Создаем тот самый тестовый маршрут (эндпоинт)
@app.get("/health")
async def health_check():
    return {"status": "ok"}