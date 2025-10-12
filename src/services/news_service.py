"""
news_service.py

Handles periodic news retrieval using the Finnhub API and Redis-based caching.
"""

import os
import time
from typing import Optional, List, Dict
from src.logger import Logger
from src.cache.redis_cache import RedisCache
from src.api.finnhub_api import fetch_news

logger = Logger.get("NewsService")


class NewsService:
    """Service that periodically fetches news from Finnhub and caches seen ones."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        interval: int = 30,
        max_items: int = 3,
        cache: Optional[RedisCache] = None,
    ):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        self.interval = interval
        self.max_items = max_items
        self.cache = cache or RedisCache()

        if not self.api_key:
            logger.warning("FINNHUB_API_KEY not set. News fetching will be disabled.")

    def process_news(self, news: List[Dict]) -> List[Dict]:
        """
        Filter out already-seen news articles and mark new ones as seen.
        """
        new_items = []
        for item in news:
            # key = item.get("id") or item.get("url")
            # if not key:
            #     continue

            # if self.cache.is_seen(key):
            #     continue

            # self.cache.mark_seen(key)
            new_items.append(item)
            logger.info("New article: %s", item.get("headline", "No title"))

        return new_items

    def run_once(self) -> List[Dict]:
        """Fetch and process news once."""
        if not self.api_key:
            logger.warning("Skipping fetch — no API key configured.")
            return []

        news = fetch_news(api_key=self.api_key, max_items=self.max_items)
        new_items = self.process_news(news)
        logger.info("Fetched %d new items out of %d total.", len(new_items), len(news))
        return new_items

    def run(self):
        """Continuously fetch news at an interval."""
        logger.info("News Service started. Running indefinitely...")
        try:
            while True:
                self.run_once()
                logger.info("Next fetch in %d seconds...", self.interval)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("News Service stopped by user.")
