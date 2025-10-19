# seed_companies.py
from src.datalayer.connection import Database
from src.datalayer.company_repository import CompanyRepository
from src.utilities.constants import COMPANIES


def seed_companies(db: Database):
    repo = CompanyRepository(db)
    repo.bulk_insert(COMPANIES)
    print(f"Inserted {len(COMPANIES)} companies successfully!")
