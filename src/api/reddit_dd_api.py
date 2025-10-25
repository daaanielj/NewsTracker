import requests
from typing import List, Dict

BASE_URL = "https://www.reddit.com/r/wallstreetbets/search.json"


def fetch_dd_posts(limit: int = 5) -> List[Dict]:
    """
    Fetch the latest posts with flair 'DD' from r/wallstreetbets.

    Args:
        limit: Maximum number of posts to fetch (default 5)

    Returns:
        List of posts as dictionaries (each is post['data'])
    """
    params = {
        "q": "flair:DD",
        "restrict_sr": "on",
        "sort": "new",
        "limit": limit,
    }
    headers = {"User-Agent": "Mozilla/5.0 (RedditServiceBot)"}

    try:
        resp = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [p["data"] for p in data["data"]["children"]]
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return []
