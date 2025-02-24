import os
import redis
from fastapi import FastAPI

app = FastAPI()

# Get Redis connection details from environment variables
# FastAPI connects to Redis using the redis-service name, which CoreDNS resolves to a ClusterIP.
# Then, kube-proxy in each worker node routes requests to an available Redis pod IP (based on Selector rules).
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # Default to localhost for local dev
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI running with Redis!"}

@app.post("/set/")
def set_key(key: str, value: str):
    redis_client.set(key, value)
    return {"message": f"Key '{key}' set successfully"}

@app.get("/get/{key}")
def get_key(key: str):
    value = redis_client.get(key)
    if value is None:
        return {"error": "Key not found"}
    return {"key": key, "value": value}
