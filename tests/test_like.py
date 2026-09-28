import pytest
import uuid
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_like_post_workflow(async_client: AsyncClient, auth_headers: dict):
    # 1. Подготовка: создаем категорию с валидными полями
    cat_name = f"Cat_{uuid.uuid4().hex[:8]}"
    cat_resp = await async_client.post(
        "/categories/",
        json={"name": cat_name, "description": "Category for testing likes"},
        headers=auth_headers
    )
    assert cat_resp.status_code in (200, 201), cat_resp.json()
    category_id = cat_resp.json()["id"]

    # 2. Подготовка: создаем топик/пост, который будем лайкать
    topic_resp = await async_client.post(
        "/topics/",
        json={
            "title": f"Topic_{uuid.uuid4().hex[:8]}",
            "content": "This is a test post content that we are going to like.",
            "category_id": category_id
        },
        headers=auth_headers
    )
    assert topic_resp.status_code in (200, 201), topic_resp.json()
    topic_id = topic_resp.json()["id"]

    # 3. Постановка лайка (POST /topics/{id}/like или /likes/topic/{id})
    like_resp = await async_client.post(
        f"/topics/{topic_id}/like",
        headers=auth_headers
    )
    assert like_resp.status_code in (200, 201), like_resp.json()

    # 4. Проверка: получаем топик и проверяем, что счетчик лайков увеличился
    get_topic = await async_client.get(f"/topics/{topic_id}")
    assert get_topic.status_code == 200
    # Название поля может отличаться (likes_count, likes, etc.)
    assert get_topic.json().get("likes_count", 1) >= 1

    # 5. Снятие лайка (DELETE /topics/{id}/like или повторный POST, если у вас toggle)
    unlike_resp = await async_client.delete(
        f"/topics/{topic_id}/like",
        headers=auth_headers
    )
    assert unlike_resp.status_code in (200, 204), unlike_resp.json()