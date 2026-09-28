import pytest
import uuid
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_categories(async_client: AsyncClient):
    token = await get_token(async_client, "cat_user", "cat_user@mail.com")
    headers = {"Authorization": f"Bearer {token}"}

    cat_name = f"Cat_{uuid.uuid4().hex[:8]}"

    response = await async_client.post(
        "/categories/",
        json={
            "name": cat_name,
            "description": "Valid description text over 10 chars",
        },
        headers=headers,  # Добавлен заголовок
    )
    assert response.status_code == 200
    