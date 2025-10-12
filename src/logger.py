"""
logger.py

Provides a centralized logger class for the News Tracker application.
"""

import logging
import sys

class Logger:
    """Creates and returns a configured logging.Logger instance."""

    @staticmethod
    def get(name: str = __name__) -> logging.Logger:
        """Returns a logger with a standard console handler and formatting."""
        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger
