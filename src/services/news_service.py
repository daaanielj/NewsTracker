import asyncio
import os
from typing import Optional, List, Dict
from src.logger import Logger
from src.cache.redis_cache import RedisCache
from src.api.finnhub_news_api import fetch_news
from src.services.company_parser_service import CompanyParserService

logger = Logger.get("NewsService")


class NewsService:
    """Service that periodically fetches news from Finnhub and notifies Discord subscribers."""

    def __init__(
        self,
        company_parser: CompanyParserService,
        bot=None,
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
        self.bot = bot

        if not self.api_key:
            logger.warning("FINNHUB_API_KEY not set. News fetching will be disabled.")

    def validate_news(self, news: List[Dict]) -> List[Dict]:
        """Filter out already-seen news articles."""
        #  TODO: persist the id in a table in the db for cross sessions
        #  or if the server shuts down, the id of the news should just be in
        #  increasing order so there should be no reason to keep all the
        #  ids in memory.
        new_items = []
        for item in news:
            key = item.get("id")
            if not key:
                continue
            if self.news_cache.is_seen(key):
                continue
            self.news_cache.mark_seen(key)
            new_items.append(item)
        return new_items

    async def validate_company(self, news: List[Dict]) -> List[Dict]:
        """Extract companies from headline + summary."""
        processed = []
        for n in news:
            headline = n.get("headline", "") or ""
            summary = n.get("summary", "") or ""
            companies = set()
            companies |= set(self.company_parser.extract_companies(headline))
            companies |= set(self.company_parser.extract_companies(summary))
            if companies:
                n["companies"] = list(companies)
                processed.append(n)
        return processed

    async def fetch_news(self) -> List[Dict]:
        """Fetch, process, and notify new news."""
        if not self.api_key:
            return []

        news = await asyncio.to_thread(
            fetch_news, api_key=self.api_key, max_items=self.max_items
        )
        new_items = self.validate_news(news)
        processed = await self.validate_company(new_items)

        if processed:
            await self.notify_subscribers(processed)

        logger.info("Fetched %d new items out of %d total.", len(processed), len(news))
        return processed

    async def notify_subscribers(self, articles: List[Dict]):
        """Send new news articles to all subscribers via the Discord bot."""
        if not self.bot:
            logger.warning("No Discord bot attached; skipping notifications.")
            return

        for article in articles:
            headline = article.get("headline", "")
            url = article.get("url", "")
            companies = ", ".join(article.get("companies", []))

            message = f"**{headline}**\nCompanies: {companies}\n<{url}>"
            try:
                await self.bot.ping_users(message)
            except Exception as e:
                logger.error(f"Failed to broadcast article: {e}")

    async def run_async(self):
        """Run continuously."""
        logger.info("News Service started.")
        while True:
            await self.fetch_news()
            await asyncio.sleep(self.interval)
