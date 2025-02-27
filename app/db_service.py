import redis.asyncio as redis
import os


class RedisService:
    def __init__(self):
        """
        Get Redis connection details from environment variables.
        FastAPI connects to Redis using the redis-service name, which CoreDNS resolves to a ClusterIP.
        Then, kube-proxy in each worker node routes requests to an available Redis pod IP (based on Selector rules).
        """
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))


    async def get_redis(self):
        """
        Dependency to get a Redis client.
        Using dependency injection (Depends(get_redis)) allows us to inject mock Redis instances in tests.
        """
        client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
        try:
            yield client
        finally:
            await client.close()

    