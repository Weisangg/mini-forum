import pytest
from httpx import AsyncClient

TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "strongpassword123",
}

@pytest.mark.asyncio
async def test_successful_registration(async_client: AsyncClient):
    """Успешная регистрация и проверка, что пароль не возвращается."""
    response = await async_client.post("/auth/register",json=TEST_USER)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert data["username"] == TEST_USER["username"]
    
    assert "password" not in data
    
@pytest.mark.asyncio
async def test_registration_existing_email(async_client: AsyncClient):
    """Регистрация с занятым email."""
    # Первый запрос - создаем юзера
    await async_client.post("/auth/register", json=TEST_USER)
    response = await async_client.post("/auth/register",json=TEST_USER)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()
    
@pytest.mark.asyncio
async def test_successful_login(async_client: AsyncClient):
    """Успешный вход."""
    await async_client.post("/auth/register", json=TEST_USER)
    
    response = await async_client.post("/auth/login" ,json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
@pytest.mark.asyncio
async def test_wrong_passwort_login(async_client: AsyncClient):
    """Неправильный пароль при входе."""
    await async_client.post("/auth/register", json=TEST_USER)
    
    response = await async_client.post("/auht/login", json={
        "email": TEST_USER["email"],
        "username": "wrongpassword!"
    })
    
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_get_usets_me(async_client: AsyncClient):
    """Получение /users/me с правильным JWT."""
    await async_client.post("/auth/register", json=TEST_USER)
    login_resp = await async_client.post("/auth/register", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    token = login_resp.json()['access_token']
    
    # Делаем запрос с токеном в заголовке
    response = await async_client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == TEST_USER["email"]
    
@pytest.mark.asyncio
async def test_access_without_jwt(async_client: AsyncClient):
    """Доступ к /users/me без JWT."""
    response = await async_client.get("/users/me")
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_access_with_invalid_jwt(async_client: AsyncClient):
    """Доступ с недействительным/истёкшим JWT."""
    response = await async_client.get("/users/me", headers={
        "Authorization": "Bearer fake.jwt.token"
    })
    assert response.status_code == 401