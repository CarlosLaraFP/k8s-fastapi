import os
import redis.asyncio as redis
from fastapi import FastAPI, Depends

app = FastAPI()

# Get Redis connection details from environment variables.
# FastAPI connects to Redis using the redis-service name, which CoreDNS resolves to a ClusterIP.
# Then, kube-proxy in each worker node routes requests to an available Redis pod IP (based on Selector rules).
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


# Dependency to get a Redis client
# Using dependency injection (Depends(get_redis)) allows us to inject mock Redis instances in tests
async def get_redis():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI running with Redis!"}


@app.post("/set/")
async def set_key(key: str, value: str, redis_client: redis.Redis = Depends(get_redis)):
    await redis_client.set(key, value)
    return {"message": f"Key '{key}' set successfully"}


@app.get("/get/{key}")
async def get_key(key: str, redis_client: redis.Redis = Depends(get_redis)):
    value = await redis_client.get(key)
    if value is None:
        return {"error": "Key not found"}
    return {"key": key, "value": value}
