import pytest
from app.entrypoints.api.dependencies import get_user_service
from httpx import AsyncClient
from app.main import app
from dataclasses import dataclass


@pytest.fixture(autouse=True)
def reset_overrides():
    yield
    app.dependency_overrides.clear()


@dataclass
class MockUser:
    id: int
    username: str
    email: str
    is_active: bool


class TestUserService:
    async def create_user(self, user):
        return MockUser(
            id=1, username=user.username, email=user.email, is_active=True
        )

    async def get_user_by_id(self, user_id):
        return MockUser(
            id=user_id,
            username="testuser",
            email="testuser@example.com",
            is_active=True,
        )

    async def get_user_by_username(self, username):
        return MockUser(
            id=1,
            username=username,
            email=f"{username}@example.com",
            is_active=True,
        )

    async def delete_user(self, user_id):
        return None


@pytest.mark.asyncio
async def test_create_user(async_client):
    app.dependency_overrides[get_user_service] = lambda: TestUserService()
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "is_active": True,
    }

    response = await async_client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_by_id(async_client):
    app.dependency_overrides[get_user_service] = lambda: TestUserService()
    test_user_id = 1

    response = await async_client.get(f"/users/{test_user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == test_user_id
    assert user["username"] == "testuser"
    assert user["email"] == "testuser@example.com"
