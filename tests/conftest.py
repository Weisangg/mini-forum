import sys
from pathlib import Path
import pytest_asyncio
from tests.test_posts import get_token
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.main import app 

TEST_DATABASE_URL = "postgresql+asyncpg://forum_admin:supersecret@localhost:5432/mini_forum"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass = NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

from app.db.database import get_session

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session
        
# Применяем переопределение в FastAPI
app.dependency_overrides[get_session] = override_get_db

@pytest_asyncio.fixture
async def async_client():
    """Фикстура для асинхронных запросов к FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
        
@pytest_asyncio.fixture
async def auth_headers(async_client):
    # Генерация токена/авторизация
    token = await get_token(async_client, "test_user", "test@mail.com")
    return {"Authorization": f"Bearer {token}"}