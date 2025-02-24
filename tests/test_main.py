import pytest
from httpx import AsyncClient
from fakeredis import FakeRedis
from app.main import app, get_redis
from fastapi.testclient import TestClient

@pytest.fixture
def test_client():
    return TestClient(app)

# tests the FastAPI / route
def test_read_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

"""
Uses fakeredis to mock Redis in-memory instead of requiring a real Redis instance.
app.dependency_overrides[get_redis] = lambda: redis_mock injects a fake Redis instance.
Uses pytest.mark.asyncio because FastAPI's Redis functions are asynchronous.
"""
# Use fakeredis instead of real Redis
@pytest.fixture
async def redis_mock():
    redis_client = FakeRedis(decode_responses=True)
    await redis_client.flushdb()  # Ensure it's empty before tests
    return redis_client


# Override the get_redis dependency in tests
@pytest.fixture
def override_redis(redis_mock):
    app.dependency_overrides[get_redis] = lambda: redis_mock


@pytest.mark.asyncio
async def test_set_and_get_key(test_client, override_redis):
    response = test_client.post("/set/", params={"key": "username", "value": "JohnDoe"})
    assert response.status_code == 200
    assert response.json() == {"message": "Key 'username' set successfully"}

    response = test_client.get("/get/username")
    assert response.status_code == 200
    assert response.json() == {"key": "username", "value": "JohnDoe"}


@pytest.mark.asyncio
async def test_get_nonexistent_key(test_client, override_redis):
    response = test_client.get("/get/nonexistent")
    assert response.status_code == 200
    assert response.json() == {"error": "Key not found"}
