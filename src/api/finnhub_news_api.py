"""
Finnhub API wrapper for fetching news.
"""

from typing import Optional, List, Dict
import requests
from src.logger import Logger

logger = Logger.get("FinnhubAPI")

BASE_URL = "https://finnhub.io/api/v1/news"


def fetch_news(
    api_key: Optional[str], category: str = "general", max_items: int = 3
) -> List[Dict]:
    """
    Fetch the latest news from Finnhub.

    :param api_key: Finnhub API key
    :param category: News category
    :param max_items: Maximum number of news items to return
    :return: List of news items (dictionaries)
    """
    if not api_key:
        logger.warning("API key not provided. Skipping news fetch.")
        return []

    params = {"category": category, "token": api_key}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        news = response.json()[:max_items]
        logger.info("Fetched %d news items.", len(news))
        for item in news:
            logger.info(
                "News: %s | URL: %s",
                item.get("headline", "No title"),
                item.get("url", "No URL"),
            )
        return news
    except requests.Timeout:
        logger.warning("Request to Finnhub timed out.")
        return []
    except requests.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return []
    except Exception as e:
        logger.error("Unexpected error fetching news: %s", e)
        return []
