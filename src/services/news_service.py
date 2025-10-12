"""
NewsService that periodically fetches news using Finnhub API.
"""

import os
import time
from typing import Optional
from src.api.finnhub_api import fetch_news
from src.logger import Logger

logger = Logger.get("NewsService")

class NewsService:
    """Service that periodically fetches news from Finnhub."""

    def __init__(self, api_key: Optional[str] = None, interval: int = 30, max_items: int = 3):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        self.interval = interval
        self.max_items = max_items
        if not self.api_key:
            logger.warning("FINNHUB_API_KEY not set. News fetching will be disabled.")

    def fetch_news(self):
        """Fetch the latest news using the Finnhub API wrapper."""
        return fetch_news(api_key=self.api_key, max_items=self.max_items)

    def run(self):
        """Run the service indefinitely, fetching news every `interval` seconds."""
        logger.info("News Service started. Running indefinitely...")
        try:
            while True:
                self.fetch_news()
                logger.info("Next fetch in %d seconds...", self.interval)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("News Service stopped by user.")
