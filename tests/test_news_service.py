"""
Testing the NewsService class
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unittest.mock import MagicMock, patch
from src.services.news_service import NewsService
from src.services.company_parser_service import CompanyParserService


@pytest.fixture
def news_service() -> NewsService:
    """Return a NewsService instance for testing."""
    company_parser = CompanyParserService(companies={})
    return NewsService(api_key="FAKE_KEY", max_items=3, company_parser=company_parser)


@patch("src.api.finnhub_api.requests.get")
def test_fetch_news_limits_to_max_items(mock_get, news_service: NewsService):
    """Test that fetch_news respects max_items limit."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"headline": "News 1", "url": "url1"},
        {"headline": "News 2", "url": "url2"},
        {"headline": "News 3", "url": "url3"},
        {"headline": "News 4", "url": "url4"},
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    news = news_service.fetch_news()
    # Ensure only max_items are returned
    assert len(news) == news_service.max_items
    headlines = [item["headline"] for item in news]
    assert headlines == ["News 1", "News 2", "News 3"]


@patch("src.api.finnhub_api.requests.get")
def test_fetch_news_handles_timeout(mock_get, news_service: NewsService):
    """Test that fetch_news returns empty list on exception."""
    mock_get.side_effect = Exception("Timeout")
    news = news_service.fetch_news()
    assert news == []


@patch("src.api.finnhub_api.requests.get")
def test_fetch_news_handles_empty_response(mock_get, news_service: NewsService):
    """Test that fetch_news returns empty list when API returns empty."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_v
