"""
company_parser_service.py

Service for extracting company mentions from text using a keyword processor.
"""

from typing import List
from flashtext import KeywordProcessor
from src.logger import Logger
from src.datalayer.company_repository import CompanyRepository

logger = Logger.get("CompanyParserService")


class CompanyParserService:
    """Parses text for company mentions based on data from the Companies table."""

    def __init__(self, db):
        """
        Initialize the parser by loading companies from the database.
        :param db: Database instance
        """
        self.db = db
        self.repo = CompanyRepository(db)
        self.processor = KeywordProcessor(case_sensitive=False)

        self._load_companies()

    def _load_companies(self):
        """Load companies from the database into the keyword processor."""
        companies = self.repo.get_all()

        for company in companies:
            name = company["company_name"]
            ticker = company["ticker_symbol"]

            # Add both name and ticker as keywords
            if name:
                self.processor.add_keyword(name, ticker)
            if ticker:
                self.processor.add_keyword(ticker, ticker)

        logger.info("Loaded %d companies into parser", len(companies))

    def extract_companies(self, text: str) -> List[str]:
        """
        Extract ticker symbols mentioned in the given text.

        :param text: Text to parse (headline + summary)
        :return: List of ticker symbols found
        """
        if not text:
            return []
        symbols = self.processor.extract_keywords(text)
        logger.debug("Extracted companies: %s", symbols)
        return symbols
