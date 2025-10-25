# src/datalayer/subscriber_repository.py
from src.datalayer.base_repository import BaseRepository


class SubscriberRepository(BaseRepository):
    """Repository for accessing the subscribers table."""

    def get_all(self) -> list[int]:
        rows = self.fetch_all("SELECT user_id FROM subscribers")
        return [row[0] for row in rows]

    def add(self, user_id: int):
        self.execute("INSERT INTO subscribers (user_id) VALUES (?)", (user_id,))

    def remove(self, user_id: int):
        self.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
