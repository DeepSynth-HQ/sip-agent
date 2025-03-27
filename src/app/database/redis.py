import redis
from settings import config


class RedisService:
    def __init__(self, uri: str = None):
        self.client = redis.Redis.from_url(uri or config.REDIS_URI)

    def get_client(self):
        return self.client
