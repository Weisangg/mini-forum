import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_like_and_duplicate_like(async_client: AsyncClient):
    """Лайк и повторный лайк."""
    # 1. Регистрация и логин
    user_data = {"username": "liker", "email": "liker@test.com", "password": "pass"}
    await async_client.post("/auth/register", json=user_data)
    
    login_resp = await async_client.post("/auth/login", json={"email": "liker@test.com", "password": "pass"})
    token = login_resp.json()["access_token"]
    headers = {'Authorization': f"Bearer {token}"}
    
    # 2. Создаем тему и пост (подставь свои эндпоинты, если они отличаются)
    topic_resp = await async_client.post("/topics", json={"title": "Test Topic", "category_id": 1}, headers=headers)
    topic_id = topic_resp.json()['id']
    
    post_resp = await async_client.post("/posts", json={"content": "Test Post", "topic_id": topic_id}, headers=headers)
    post_id = post_resp.json()['id']
    
    # 3. Успешный лайк
    like_resp = await async_client.post(f"/posts/{post_id}/like", headers=headers)
    
    # 4. Повторный лайк
    duplicate_like_resp = await async_client.post(f"/posts/{post_id}/like", headers=headers)
    
    assert duplicate_like_resp.status_code == 400
    assert "already liked" in duplicate_like_resp.json()["detail"].lower
    
    # Если логика форума выдает ошибку при повторном лайке: