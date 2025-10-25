import asyncio
import os
from typing import Optional, List, Dict
from src.logger import Logger
from src.cache.redis_cache import RedisCache
from src.api.finnhub_news_api import fetch_news
from src.services.company_parser_service import CompanyParserService
from src.datalayer.connection import Database
from src.datalayer.data_checkpoint_repository import DataCheckpointRepository

logger = Logger.get("NewsService")


class NewsService:
    """Service that periodically fetches news from Finnhub and notifies Discord subscribers."""

    def __init__(
        self,
        company_parser: CompanyParserService,
        db: Database,
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
        self.news_checkpoint_repo = DataCheckpointRepository(db)

        if not self.api_key:
            logger.warning("FINNHUB_API_KEY not set. News fetching will be disabled.")

    def validate_news(self, news: List[Dict]) -> List[Dict]:
        """Filter out already-seen news articles using persisted checkpoint."""
        source_name = "finnhub"
        new_items = []

        last_seen_id = int(self.news_checkpoint_repo.get_last_id(source_name) or "0")
        max_seen_id = last_seen_id

        for item in news:
            news_id = item.get("id")
            if not news_id:
                continue
            if news_id <= last_seen_id:
                continue

            self.news_cache.mark_seen(news_id)
            new_items.append(item)
            max_seen_id = max(max_seen_id, news_id)

        if max_seen_id > last_seen_id:
            self.news_checkpoint_repo.update_last_id(source_name, str(max_seen_id))

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
