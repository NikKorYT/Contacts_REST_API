from unittest.mock import patch

import pytest
from fastapi import BackgroundTasks
from httpx import ASGITransport, AsyncClient

from main import app
from tests.conftest import test_user, user_password


@pytest.mark.asyncio
async def test_register_user(faker):
    with patch.object(BackgroundTasks, "add_task") as mock_add_task:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            payload = {
                "email": faker.email(),
                "username": faker.user_name(),
                "password": faker.password(),
            }
            response = await ac.post("/auth/register", json=payload)
            assert response.status_code == 201
            data = response.json()
            assert data["email"] == payload["email"]
            assert data["username"] == payload["username"]
            assert data.get("password") is None
            assert data["id"] is not None
            
# @pytest.mark.asyncio          
# async def test_user_login(test_user, user_password):
#     with patch.object(BackgroundTasks, "add_task"):
#         async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#             response = await ac.post("/auth/token")
#             data = {
#                 "username": test_user.username,
#                 "password": user_password(),
#             }
            
#             assert response.status_code == 200
#             data = response.json()
#             assert data["access_token"] in data
#             assert data["refresh_token"] in data