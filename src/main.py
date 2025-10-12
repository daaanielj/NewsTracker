"""
main.py

Entry point for testing the logger.
"""

from logger import Logger

logger = Logger.get("Main")

def main():
    """Entry point"""
    logger.info("Hello, world!")

if __name__ == "__main__":
    main()
