"""
main.py

Entry point for testing the logger.
"""

import sys
import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv
import discord
from src.services.company_parser_service import CompanyParserService
from src.services.discord_bot_service import DiscordBotService
from src.services.reddit_service import RedditService
from src.services.news_service import NewsService
from src.datalayer.connection import Database
from src.cogs.subscriber_cog import SubscriberCog

# Not too sure of the following
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

sys.path.append(str(Path(__file__).parent))

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(str(os.getenv("DISCORD_CHANNEL_ID")))
SERVER_ID = int(str(os.getenv("DISCORD_SERVER_ID")))

SQL_SERVER = str(os.getenv("SQL_SERVER"))
SQL_DATABASE = str(os.getenv("SQL_DATABASE"))
SQL_USERNAME = str(os.getenv("SQL_USERNAME"))
SQL_PASSWORD = str(os.getenv("SQL_PASSWORD"))


async def main():
    """entry point"""

    db = Database(
        server=SQL_SERVER,
        database=SQL_DATABASE,
        username=SQL_USERNAME,
        password=SQL_PASSWORD,
    )

    company_parser = CompanyParserService(db)

    bot = DiscordBotService(db=db, channel_id=CHANNEL_ID)
    # await bot.add_cog(SubscriberCog(bot, db))

    # @bot.event
    # async def on_ready():
    #     print("Bot ready, syncing commands...")
    #     guild = discord.Object(id=SERVER_ID)
    #     await bot.tree.sync(guild=guild)
    #     print("Commands synced!")

    service = NewsService(
        interval=30, bot=bot, max_items=10, company_parser=company_parser, db=db
    )

    reddit_service = RedditService(
        db=db,
        discord_bot=bot,
        interval=30,
    )
    await asyncio.gather(
        bot.start(str(TOKEN)), service.run_async(), reddit_service.run_async()
    )


if __name__ == "__main__":
    asyncio.run(main())
