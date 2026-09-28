import pytest
from httpx import AsyncClient
    
async def get_token(async_client: AsyncClient, username: str, email: str) -> str:
    user_data = {"username": username, "email": email, "password": "password123"}
    # Игнорируем ошибку 400, если юзер уже есть в базе (для тестов, где база не очищается)
    await async_client.post("/auth/register", json=user_data)
    resp = await async_client.post("/auth/login",
                                   data={
                                       'username': email,
                                       "password": "password123"
                                   }
                                )
    return resp.json()["access_token"]

@pytest.mark.asyncio
async def test_get_nonexistent_topic(async_client: AsyncClient):
    """Получение несуществующей темы."""
    response = await async_client.get("/topics/999999")
    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_create_topic_without_token(async_client: AsyncClient):
    """Создание темы без токена."""
    response = await async_client.post("/topics/", json={"title": "No Token Topic", "category_id": 1})
    assert response.status_code == 401
    
@pytest.mark.asyncio
async def test_create_topic(async_client: AsyncClient):
    """Успешное создание темы."""
    token = await get_token(async_client, "author1", "author1@mail.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    cat_resp = await async_client.post(
        "/categories/", 
        json={"name": "General News", "description": "Some description"}, 
        headers=headers
    )
    category_id = cat_resp.json()["id"]

    # 2. Передаем полученный category_id в тему
    response = await async_client.post(
        "/topics/",
        json={"title": "My First Topic", "category_id": category_id},
        headers=headers
    )
    
    assert response.status_code in (200, 201)
    assert response.json()["title"] == "My First Topic"
    assert "id" in response.json()
    
@pytest.mark.asyncio
async def test_edit_own_topic(async_client: AsyncClient):
    """Редактирование своей темы."""
    token = await get_token(async_client, 'owner', "owner@mail.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Создаем
    topic_resp = await async_client.post("/topics/", json={"title": "Old Title", "category_id": 1}, headers=headers)
    topic_id = topic_resp.json()["id"]
    
    # Редактируем (своим токеном)
    patch_resp = await async_client.patch(f"/token/{topic_id}", json={"title": "New Title"}, headers=headers)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["title"] == "New Title"
    
@pytest.mark.asyncio
async def test_edit_others_topic(async_client: AsyncClient):
    """Редактирование чужого сообщения."""
    token_a = await get_token(async_client, 'user_c', "userc@mail.com")
    token_b = await get_token(async_client, 'user_b', "userb@mail.com")
    
    # User A создает тему и пост
    topic_resp = await async_client.post("/topics/", json={"title": "T", "category_id": 1}, headers={"Authorization": f"Bearer {token_a}"})
    post_resp = await async_client.post("/posts/", json={"content": "My Post", "topic_id": topic_resp.json()["id"]}, headers={"Authorization": f"Bearer {token_a}"})
    post_id = post_resp.json()["id"]
    
    # User B пытается изменить пост User A
    patch_resp = await async_client.patch(
        f"/token/{post_id}", json={"content": "Hacked Post!"},
        headers={"Authorization": f"Bearer {token_b}"}
    )
    
    assert patch_resp.status_code in (403, 400)
    
@pytest.mark.asyncio
async def test_pagination(async_client: AsyncClient):
    """Пагинация (limit и offset)."""
    token = await get_token(async_client, 'pagi_user', "pagiuser@mail.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Создаем 3 темы
    for i in range(3):
        await async_client.post("/topics/", json={'title': f"Topic {i}", 'category_id': 1}, headers=headers)
        
    response = await async_client.get("/topics/?limit=2&offset=0")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2