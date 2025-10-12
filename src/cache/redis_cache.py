"""
RedisCache class for tracking seen news articles.
"""

import os
import redis
from typing import Optional
from src.logger import Logger


logger = Logger.get("RedisCache")


class RedisCache:
    """Wrapper around Redis for storing seen items."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: Optional[int] = None,
    ):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db or int(os.getenv("REDIS_DB", 0))
        try:
            self.client = redis.Redis(
                host=self.host, port=self.port, db=self.db, decode_responses=True
            )
            self.client.ping()
            logger.info("Connected to Redis at %s:%d", self.host, self.port)
        except redis.RedisError as e:
            logger.error("Could not connect to Redis: %s", e)
            self.client = None

    def is_seen(self, key: str) -> bool:
        """Check if the key is in the seen set."""
        if not self.client:
            return False
        return bool(self.client.sismember("seen_news", key))

    def mark_seen(self, key: str):
        """Mark a key as seen."""
        if not self.client:
            return
        self.client.sadd("seen_news", key)

    def mark_seen_with_expiry(self, key: str, ttl_seconds: int):
        """Mark key as seen and set expiration (optional)."""
        if not self.client:
            return
        self.client.sadd("seen_news", key)
        self.client.expire("seen_news", ttl_seconds)
