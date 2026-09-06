from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# 2. Фабрика сессий — штампует новые сессии для каждого запроса
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Указываем, что функция генерирует AsyncSession и ничего не возвращает в конце (None)
# 3. Функция выдачи сессии (Dependency для роутеров FastAPI)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session