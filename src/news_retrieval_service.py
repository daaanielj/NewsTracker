"""
news_retrieval_service.py

Defines the NewsRetrievalService class, which fetches news from Finnhub periodically.
"""

import os
import time
from typing import Optional, List, Dict
import requests
from src.logger import Logger

logger = Logger.get("NewsRetrievalService")


class NewsRetrievalService:
    """Service that periodically fetches news from Finnhub."""

    def __init__(self, api_key: Optional[str] = None, interval: int = 30, max_items: int = 3):
        """
        Initialize the service.
        
        :param interval: Polling interval in seconds
        :param max_items: Maximum number of news items to fetch each interval
        """
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        self.interval = interval
        self.max_items = max_items
        self.base_url = "https://finnhub.io/api/v1/news"
        if not self.api_key:
            logger.warning("FINNHUB_API_KEY not set. News fetching will be disabled.")

    def fetch_news(self) -> List[Dict]:
        """Fetch the latest news from Finnhub, limited to max_items."""
        if not self.api_key:
            return []

        params = {"category": "general", "token": self.api_key}
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            news = response.json()[:self.max_items]
            logger.info("Fetched %d news items.", len(news))
            
            for item in news:
                logger.info("News: %s | URL: %s", item.get("headline", "No title"), item.get("url", "No URL"))
            return news
        except requests.Timeout:
            logger.warning("Request to Finnhub timed out.")
            return []
        except requests.RequestException as e:
            logger.error("Error fetching news: %s", e)
            return []
        except Exception as e:
            logger.error("Error fetching news: %s", e)
            return []

    def run(self):
        """Run the service indefinitely, fetching news every `interval` seconds."""
        logger.info("News Retrieval Service started. Running indefinitely...")
        try:
            while True:
                news_items = self.fetch_news()
                logger.info("Next fetch in %d seconds...", self.interval)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("News Retrieval Service stopped by user.")
