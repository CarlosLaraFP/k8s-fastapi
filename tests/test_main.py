"""
Uses fakeredis to mock Redis in-memory instead of requiring a real Redis instance.
app.dependency_overrides[get_redis] = lambda: redis_mock injects a fake Redis instance.
Uses pytest.mark.asyncio because FastAPI's Redis functions are asynchronous.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fakeredis.aioredis import FakeRedis
from app.main import app, get_redis


# Use fakeredis instead of a real Redis
@pytest_asyncio.fixture
async def redis_mock():
    redis_client = await FakeRedis(decode_responses=True)
    await redis_client.flushdb()  # Ensure it's empty before tests
    yield redis_client  # Yield the client for testing
    await redis_client.flushdb()  # Cleanup after test


# Override the get_redis dependency in tests
@pytest_asyncio.fixture
async def override_redis(redis_mock):
    async def _override_get_redis():
        return redis_mock
    app.dependency_overrides[get_redis] = _override_get_redis
    yield
    app.dependency_overrides.pop(get_redis, None)


# Create an ASGITransport and use it to instantiate AsyncClient
@pytest_asyncio.fixture
async def test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_read_main(test_client):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI running with Redis!"}


@pytest.mark.asyncio
async def test_set_and_get_key(test_client, override_redis):
    response = await test_client.post(
        "/set/", params={"key": "username", "value": "JohnDoe"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Key 'username' set successfully"}

    response = await test_client.get("/get/username")
    assert response.status_code == 200
    assert response.json() == {"key": "username", "value": "JohnDoe"}


@pytest.mark.asyncio
async def test_get_nonexistent_key(test_client, override_redis):
    response = await test_client.get("/get/nonexistent")
    assert response.status_code == 200
    assert response.json() == {"error": "Key not found"}
