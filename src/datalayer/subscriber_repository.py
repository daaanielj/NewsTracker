class SubscriberRepository:
    """Repository for accessing the subscribers table."""

    def __init__(self, db):
        self.db = db

    def get_all(self) -> list[int]:
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT user_id FROM subscribers")
        return [row[0] for row in cursor.fetchall()]

    def add(self, user_id: int):
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO subscribers (id) VALUES (?)", user_id)
        self.db.connection.commit()

    def remove(self, user_id: int):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM subscribers WHERE id = ?", user_id)
        self.db.connection.commit()
