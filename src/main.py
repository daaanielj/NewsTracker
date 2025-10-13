"""
main.py

Entry point for testing the logger.
"""

from pathlib import Path
from dotenv import load_dotenv
from src.services.company_parser_service import CompanyParserService
from src.services.news_service import NewsService
from src.utilities.constants import COMPANIES

# Load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def main():
    """entry point"""
    company_parser = CompanyParserService(companies=COMPANIES)

    service = NewsService(interval=30, max_items=10, company_parser=company_parser)
    service.run()


if __name__ == "__main__":
    main()
