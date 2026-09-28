import pytest
import uuid
from httpx import AsyncClient

# --- Вспомогательная функция (Senior Trick) ---
# Чтобы не писать регистрацию и логин в каждом тесте, выносим это сюда.
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
async def test_create_post(async_client: AsyncClient):
    """Создание сообщения в теме."""
    token = await get_token(async_client, "author2", "author2@mail.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Сначала динамически создаем категорию (с уникальным именем)
    cat_resp = await async_client.post(
        "/categories/", 
        json={"name": f"Cat_{uuid.uuid4()}", "description": "Desc"}, 
        headers=headers
    )
    assert cat_resp.status_code in (201, 200), cat_resp.json()
    category_id = cat_resp.json()["id"]
    
    # 1. Создаем тему
    topic_resp = await async_client.post("/topics/", json={"title": "Topic for Post", "category_id": 1}, headers=headers)
    topic_id = topic_resp.json()["id"]
    
    # 2. Пишем сообщение
    post_resp = await async_client.post(
        "/posts/", 
        json={"content": "Hello World!", "topic_id": topic_id}, 
        headers=headers
    )
    assert post_resp.status_code in (200, 201)
    assert post_resp.json()["topic_id"] == topic_id
    
@pytest.mark.asyncio
async def test_edit_others_post(async_client: AsyncClient):
    """Редактирование чужого сообщения."""
    token_a = await get_token(async_client, "user_c", "userc@mail.com")
    token_b = await get_token(async_client, "user_d", "userd@mail.com")
    
    # User A создает тему и пост
    topic_resp = await async_client.post("/topics/", json={"title": "T", "category_id": 1}, headers={"Authorization": f"Bearer {token_a}"})
    post_resp = await async_client.post("/posts/", json={"content": "My Post", "topic_id": topic_resp.json()["id"]}, headers={"Authorization": f"Bearer {token_a}"})
    post_id = post_resp.json()["id"]
    
    # User B пытается изменить пост User A
    patch_resp = await async_client.patch(
        f"/posts/{post_id}", json={"content": "Hacked Post!"}, 
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert patch_resp.status_code in (403, 400)