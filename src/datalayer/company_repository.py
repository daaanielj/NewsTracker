# src/datalayer/company_repository.py
from typing import Optional, Dict, List
from src.datalayer.base_repository import BaseRepository


class CompanyRepository(BaseRepository):
    """Repository for accessing and managing the Companies table."""

    def get_all(self) -> List[Dict[str, str]]:
        """Return all companies."""
        rows = self.fetch_all("SELECT company_name, ticker_symbol FROM Companies")
        return [{"company_name": r[0], "ticker_symbol": r[1]} for r in rows]

    def get_ticker_by_name(self, company_name: str) -> Optional[str]:
        """Fetch ticker symbol for a given company name."""
        row = self.fetch_one(
            "SELECT ticker_symbol FROM Companies WHERE company_name = ?",
            (company_name,),
        )
        return row[0] if row else None

    def insert(self, company_name: str, ticker_symbol: str):
        """Insert a new company if it doesn't exist."""
        self.execute(
            """
            IF NOT EXISTS (SELECT 1 FROM Companies WHERE company_name = ?)
            INSERT INTO Companies (company_name, ticker_symbol)
            VALUES (?, ?)
            """,
            (company_name, company_name, ticker_symbol),
        )

    def bulk_insert(self, companies: Dict[str, str]):
        """Insert multiple companies (idempotent)."""
        for name, ticker in companies.items():
            self.execute(
                """
                IF NOT EXISTS (SELECT 1 FROM Companies WHERE company_name = ?)
                INSERT INTO Companies (company_name, ticker_symbol)
                VALUES (?, ?)
                """,
                (name, name, ticker),
                commit=False,
            )

        self.db.connection.commit()
