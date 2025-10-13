"""
parser_service.py

Service for extracting company mentions from text using a keyword processor.
"""

from typing import List, Dict
from flashtext import KeywordProcessor
from src.logger import Logger

logger = Logger.get("CompanyParserService")


class CompanyParserService:
    """Parses text for company mentions based on a predefined company list."""

    def __init__(self, companies: Dict[str, str]):
        """
        Initialize the parser with a list of companies.

        :param companies: List of dicts with "name" and "symbol" keys
        """
        self.processor = KeywordProcessor(case_sensitive=False)
        for company in companies.items():
            name = company[0]
            ticker = company[1]
            if name:
                self.processor.add_keyword(name, ticker)
            if ticker:
                self.processor.add_keyword(ticker, ticker)

        logger.info(
            "CompanyParserService initialized with %d companies", len(companies)
        )

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
