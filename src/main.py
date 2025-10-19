"""
main.py

Entry point for testing the logger.
"""

import sys
from pathlib import Path
import os
from dotenv import load_dotenv
from src.services.company_parser_service import CompanyParserService
from src.services.discord_bot_service import DiscordBotService
from src.services.news_service import NewsService
from src.utilities.constants import COMPANIES
from src.datalayer.connection import Database

# Not too sure of the following
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

sys.path.append(str(Path(__file__).parent))

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(str(os.getenv("DISCORD_CHANNEL_ID")))

SQL_SERVER = str(os.getenv("SQL_SERVER"))
SQL_DATABASE = str(os.getenv("SQL_DATABASE"))
SQL_USERNAME = str(os.getenv("SQL_USERNAME"))
SQL_PASSWORD = str(os.getenv("SQL_PASSWORD"))


def main():
    """entry point"""

    db = Database(
        server=SQL_SERVER,
        database=SQL_DATABASE,
        username=SQL_USERNAME,
        password=SQL_PASSWORD,
    )
    company_parser = CompanyParserService(companies=COMPANIES)

    bot = DiscordBotService(db=db, channel_id=CHANNEL_ID)
    bot.run(str(TOKEN))

    service = NewsService(interval=30, max_items=10, company_parser=company_parser)
    service.run()


if __name__ == "__main__":
    main()
