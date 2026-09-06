import os

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://forum_admin:supersecret@localhost:5432/mini_forum")

engine = create_async_engine(DATABASE_URL, echo=True)

# 2. Фабрика сессий — штампует новые сессии для каждого запроса
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 3. Базовый класс — от него мы будем наследовать таблицы (User, Topic)
class Base(DeclarativeBase):
    pass

# Указываем, что функция генерирует AsyncSession и ничего не возвращает в конце (None)
# 4. Функция выдачи сессии (будет использоваться в роутерах)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session