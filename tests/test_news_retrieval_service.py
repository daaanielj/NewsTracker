"""
Testing the NewsRetrievalService class
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Add project root to sys.path so `src` can be imported
sys.path.append(str(Path(__file__).parent.parent))

from src.news_retrieval_service import NewsRetrievalService

@pytest.fixture
def news_service() -> NewsRetrievalService:
    """Return a NewsRetrievalService instance for testing."""
    return NewsRetrievalService(api_key="FAKE_KEY", max_items=3)

@patch("src.news_retrieval_service.requests.get")
def test_fetch_news_limits_to_max_items(mock_get, news_service: NewsRetrievalService):
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

@patch("src.news_retrieval_service.requests.get")
def test_fetch_news_handles_timeout(mock_get, news_service: NewsRetrievalService):
    """Test that fetch_news returns empty list on exception."""
    mock_get.side_effect = Exception("Timeout")
    news = news_service.fetch_news()
    assert news == []

@patch("src.news_retrieval_service.requests.get")
def test_fetch_news_handles_empty_response(mock_get, news_service: NewsRetrievalService):
    """Test that fetch_news returns empty list when API returns empty."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_v
