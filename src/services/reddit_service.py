import asyncio
import logging
from typing import List, Dict
import requests
from datetime import datetime

from src.api.reddit_dd_api import fetch_dd_posts
from src.datalayer.connection import Database
from src.datalayer.data_checkpoint_repository import DataCheckpointRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RedditService:
    """Service to continuously fetch new posts"""

    BASE_URL = "https://www.reddit.com/r/wallstreetbets/search.json"

    def __init__(
        self,
        db: Database,
        discord_bot,
        interval: int = 60,
    ):
        self.checkpoint_repo = DataCheckpointRepository(db)
        self.discord_bot = discord_bot
        self.source_name = "reddit_wsb"
        self.interval = interval
        self.running = True

    def get_new_posts(self) -> List[Dict]:
        """Filter posts that are newer than the last checkpoint."""
        # Get last seen timestamp from DB
        last_timestamp_str = self.checkpoint_repo.get_last_id(self.source_name)
        last_timestamp = float(last_timestamp_str) if last_timestamp_str else 0

        posts = fetch_dd_posts(limit=5)
        new_posts = []

        for post in posts:
            created_utc = post.get("created_utc", 0)
            if created_utc <= last_timestamp:
                continue
            new_posts.append(post)

        if new_posts:
            newest_timestamp = max(p["created_utc"] for p in new_posts)
            self.checkpoint_repo.update_last_id(self.source_name, str(newest_timestamp))

        return list(reversed(new_posts))

    async def run_async(self):
        """Continuously fetch new posts and ping Discord."""
        while self.running:
            try:
                new_posts = self.get_new_posts()
                for post in new_posts:
                    title = post.get("title", "")
                    permalink = post.get("permalink", "")
                    reddit_url = f"https://reddit.com{permalink}"
                    message = f"New DD post: {title} - {reddit_url}"
                    await self.discord_bot.ping_users(message)
                    logger.info("Pinged Discord for new Reddit post")
            except Exception as e:
                logger.error("Error in RedditService run loop: %s", e)

            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False
