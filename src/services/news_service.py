"""
news_service.py

Handles periodic news retrieval using the Finnhub API and Redis-based caching.
"""

import os
import time
from typing import Optional, List, Dict
from src.logger import Logger
from src.cache.redis_cache import RedisCache
from src.api.finnhub_news_api import fetch_news
from src.api.finnhub_company_api import fetch_company_profile
from src.services.company_parser_service import CompanyParserService

logger = Logger.get("NewsService")


class NewsService:
    """Service that periodically fetches news from Finnhub and caches seen ones."""

    def __init__(
        self,
        company_parser: CompanyParserService,
        interval: int = 30,
        max_items: int = 10,
        api_key: Optional[str] = None,
        news_cache: Optional[RedisCache] = None,
        company_cache: Optional[RedisCache] = None,
    ):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        self.interval = interval
        self.max_items = max_items
        self.news_cache = news_cache or RedisCache(namespace="news")
        self.company_cache = company_cache or RedisCache(namespace="company")
        self.company_parser = company_parser

        if not self.api_key:
            logger.warning("FINNHUB_API_KEY not set. News fetching will be disabled.")

    def validate_news(self, news: List[Dict]) -> List[Dict]:
        """
        Filter out already-seen news articles and mark new ones as seen.
        """
        new_items = []
        for item in news:
            key = item.get("id")
            if not key:
                continue

            if self.news_cache.is_seen(key):
                continue

            self.news_cache.mark_seen(key)
            new_items.append(item)
            logger.info("New article: %s", item.get("headline", "No title"))

        return new_items

    def validate_company(self, news: List[Dict]):
        """Process the news by getting the ticker in the related field"""
        # TODO: Cannot rely on the related field from the api because it
        #       doesn't seem to be populated most of the time.
        #      Instead, just use flashtext and parse the headline and summary for the company name

        return True

    def fetch_news(self) -> List[Dict]:
        """Fetch and process news once."""
        if not self.api_key:
            logger.warning("Skipping fetch — no API key configured.")
            return []

        # call the api to get the most recent news
        news = fetch_news(api_key=self.api_key, max_items=self.max_items)
        new_items = self.validate_news(news)
        self.validate_company(new_items)

        logger.info("Fetched %d new items out of %d total.", len(new_items), len(news))
        return new_items

    def run(self):
        """Continuously fetch news at an interval."""
        logger.info("News Service started. Running indefinitely...")
        try:
            while True:
                self.fetch_news()
                logger.info("Next fetch in %d seconds...", self.interval)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("News Service stopped by user.")
