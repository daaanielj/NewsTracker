"""
main.py

Entry point for testing the logger.
"""
from pathlib import Path
from dotenv import load_dotenv
from src.news_retrieval_service import NewsRetrievalService

# Load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def main():
    """entry point"""
    service = NewsRetrievalService(interval=30, max_items=3)
    service.run()

if __name__ == "__main__":
    main()
