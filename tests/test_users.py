import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.database import user_collection
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    await user_collection.delete_many({})
    yield
    await user_collection.delete_many({})


@pytest.mark.asyncio
async def test_create_and_get_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={"name": "Sujai Gupta", "email": "Sujai@example.com", "age": 30},
        )
        assert response.status_code == 201
        user = response.json()
        assert user["email"] == "Sujai@example.com"
        user_id = user["_id"]

        response = await ac.get(f"/users/{user_id}")
        assert response.status_code == 200
        fetched_user = response.json()
        assert fetched_user["email"] == "Sujai@example.com"


@pytest.mark.asyncio
async def test_list_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for i in range(15):
            await ac.post(
                "/users/",
                json={
                    "name": f"User{i}",
                    "email": f"user{i}@example.com",
                    "age": 20 + i,
                },
            )
        response = await ac.get("/users/", params={"page": 2, "size": 10})
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 5


@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={"name": "suresh Gupta", "email": "suresh@example.com", "age": 25},
        )
        user = response.json()
        user_id = user["_id"]

        response = await ac.put(
            f"/users/{user_id}", json={"name": "suresh Smith", "age": 26}
        )
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "suresh Smith"
        assert updated_user["age"] == 26


@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={"name": "Delete Me", "email": "deleteme@example.com", "age": 40},
        )
        user = response.json()
        user_id = user["_id"]

        response = await ac.delete(f"/users/{user_id}")
        assert response.status_code == 204

        response = await ac.get(f"/users/{user_id}")
        assert response.status_code == 404
