"""
finnhub_company_api.py

Provides functions for interacting with Finnhub company profile endpoints.
"""

import requests
from src.logger import Logger

logger = Logger.get("FinnhubCompanyAPI")


def fetch_company_profile(symbol: str, api_key: str):
    """Fetch company profile info for a given stock symbol."""
    url = "https://finnhub.io/api/v1/stock/profile2"
    params = {"symbol": symbol, "token": api_key}
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        if not data or "name" not in data:
            logger.warning("No company profile found for symbol: %s", symbol)
        return data
    except requests.Timeout:
        logger.warning("Timeout while fetching profile for %s", symbol)
        return {}
    except requests.RequestException as e:
        logger.error("Error fetching company profile for %s: %s", symbol, e)
        return {}
