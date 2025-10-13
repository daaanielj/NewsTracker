# src/cache/redis_cache.py
from typing import Optional
import os
import redis
from src.logger import Logger

logger = Logger.get("RedisCache")


class RedisCache:
    """Wrapper around Redis for storing namespaced items."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: Optional[int] = None,
        namespace: str = "default",
    ):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db or int(os.getenv("REDIS_DB", 0))
        self.namespace = namespace
        try:
            self.client = redis.Redis(
                host=self.host, port=self.port, db=self.db, decode_responses=True
            )
            self.client.ping()
            logger.info(
                "Connected to Redis at %s:%d [%s]", self.host, self.port, self.namespace
            )
        except redis.RedisError as e:
            logger.error("Could not connect to Redis: %s", e)
            self.client = None

    def _key(self, key: str) -> str:
        """Prefix key with namespace."""
        return f"{self.namespace}:{key}"

    def is_seen(self, key: str) -> bool:
        if not self.client:
            return False
        return bool(self.client.sismember(self._key("seen"), key))

    def mark_seen(self, key: str):
        if not self.client:
            return
        self.client.sadd(self._key("seen"), key)

    def get(self, key: str) -> Optional[str]:
        if not self.client:
            return None
        return str(self.client.get(self._key(key)))

    def set(self, key: str, value: str, ex: Optional[int] = None):
        if not self.client:
            return
        self.client.set(self._key(key), value, ex=ex)
