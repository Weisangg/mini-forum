import pytest
import uuid
from httpx import AsyncClient

def get_test_user():
    unique_id = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "strongpassword123",
    }

@pytest.mark.asyncio
async def test_successful_registration(async_client: AsyncClient):
    """Успешная регистрация и проверка, что пароль не возвращается."""
    user = get_test_user()
    response = await async_client.post("/auth/register", json=user)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user["email"]
    assert data["username"] == user["username"]
    
    assert "password" not in data
    
@pytest.mark.asyncio
async def test_registration_existing_email(async_client: AsyncClient):
    """Регистрация с занятым email."""
    user = get_test_user()

    # Первый запрос - создаем юзера
    await async_client.post("/auth/register", json=user)
    response = await async_client.post("/auth/register",json=user)
    
    assert response.status_code == 409
    assert "уже существует" in response.json()["detail"].lower()
    
@pytest.mark.asyncio
async def test_successful_login(async_client: AsyncClient):
    """Успешный вход."""
    user = get_test_user()
    await async_client.post("/auth/register", json=user)
    
    response = await async_client.post("/auth/login" ,data={
        "username": user["email"],
        "password": user["password"]
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
@pytest.mark.asyncio
async def test_wrong_passwort_login(async_client: AsyncClient):
    """Неправильный пароль при входе."""
    user = get_test_user()
    await async_client.post("/auth/register", json=user)
    
    response = await async_client.post("/auth/login", data={
        "username": user["email"],
        "password": "wrongpassword!"
    })
    
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_get_users_me(async_client: AsyncClient):
    """Получение /users/me с правильным JWT."""
    user = get_test_user()
    await async_client.post("/auth/register", json=user)
    login_resp = await async_client.post("/auth/login", data={
        "username": user["email"],
        "password": user["password"]
    })
    token = login_resp.json()['access_token']
    
    # Делаем запрос с токеном в заголовке
    response = await async_client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == user["email"]
    
@pytest.mark.asyncio
async def test_access_without_jwt(async_client: AsyncClient):
    """Доступ к /users/me без JWT."""
    response = await async_client.get("/users/me")
    assert response.status_code == 401, response.text
    
@pytest.mark.asyncio
async def test_access_with_invalid_jwt(async_client: AsyncClient):
    """Доступ с недействительным/истёкшим JWT."""
    response = await async_client.get("/users/me", headers={
        "Authorization": "Bearer fake.jwt.token"
    })
    assert response.status_code == 401