# src/datalayer/company_repository.py
from typing import Optional, Dict, List


class CompanyRepository:
    """Repository for accessing and managing the Companies table."""

    def __init__(self, db):
        self.db = db

    def get_all(self) -> List[Dict[str, str]]:
        """Return all companies."""
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT company_name, ticker_symbol FROM Companies")
        rows = cursor.fetchall()
        return [{"company_name": r[0], "ticker_symbol": r[1]} for r in rows]

    def get_ticker_by_name(self, company_name: str) -> Optional[str]:
        """Fetch ticker symbol for a given company name."""
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT ticker_symbol FROM Companies WHERE company_name = ?",
            (company_name,),
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def insert(self, company_name: str, ticker_symbol: str):
        """Insert a new company if it doesn't exist."""
        cursor = self.db.connection.cursor()
        cursor.execute(
            """
            IF NOT EXISTS (SELECT 1 FROM Companies WHERE company_name = ?)
            INSERT INTO Companies (company_name, ticker_symbol)
            VALUES (?, ?)
        """,
            (company_name, company_name, ticker_symbol),
        )
        self.db.connection.commit()

    def bulk_insert(self, companies: Dict[str, str]):
        """Insert multiple companies (idempotent)."""
        cursor = self.db.connection.cursor()
        for name, ticker in companies.items():
            cursor.execute(
                """
                IF NOT EXISTS (SELECT 1 FROM Companies WHERE company_name = ?)
                INSERT INTO Companies (company_name, ticker_symbol)
                VALUES (?, ?)
            """,
                (name, name, ticker),
            )
        self.db.connection.commit()
