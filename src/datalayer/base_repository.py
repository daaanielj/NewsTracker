# src/datalayer/base_repository.py
from typing import Any, Iterable, Optional
from src.datalayer.connection import Database


class BaseRepository:
    """Base repository that operates using a shared Database instance."""

    def __init__(self, db: Database):
        self.db = db

    def execute(
        self, query: str, params: Optional[Iterable[Any]] = None, commit: bool = True
    ):
        """Execute INSERT, UPDATE, or DELETE queries."""
        conn = self.db.connection
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()

    def fetch_all(self, query: str, params: Optional[Iterable[Any]] = None):
        """Run SELECT queries and fetch all results."""
        conn = self.db.connection
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Optional[Iterable[Any]] = None):
        """Run SELECT queries and fetch one result."""
        conn = self.db.connection
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
