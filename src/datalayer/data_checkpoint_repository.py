# src/datalayer/data_checkpoint_repository.py
from typing import Optional
from src.datalayer.base_repository import BaseRepository


class DataCheckpointRepository(BaseRepository):
    """Repository for persisting latest processed IDs for any data source."""

    def get_last_id(self, source_name: str) -> Optional[str]:
        row = self.fetch_one(
            "SELECT last_id FROM DataCheckpoint WHERE source_name = ?",
            (source_name,),
        )
        return str(row[0]) if row else None

    def update_last_id(self, source_name: str, last_id: str):
        self.execute(
            """
            MERGE DataCheckpoint AS target
            USING (SELECT ? AS source_name, ? AS last_id) AS src
            ON target.source_name = src.source_name
            WHEN MATCHED THEN
                UPDATE SET target.last_id = src.last_id, updated_at = GETDATE()
            WHEN NOT MATCHED THEN
                INSERT (source_name, last_id) VALUES (src.source_name, src.last_id);
            """,
            (source_name, last_id),
        )
