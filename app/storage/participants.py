import sqlite3
from datetime import datetime, timezone

from app.storage.database import get_connection


def add_participant(name: str, embedding) -> int:
    data = embedding.astype("float32").tobytes()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO participants (name, consent_given, created_at)
            VALUES (?, 1, ?)
            """,
            (name.strip(), datetime.now(timezone.utc).isoformat()),
        )

        participant_id = cursor.lastrowid

        conn.execute(
            """
            INSERT INTO embeddings (participant_id, embedding, created_at)
            VALUES (?, ?, ?)
            """,
            (
                participant_id,
                data,
                datetime.now(timezone.utc).isoformat(),
            ),
        )

        return participant_id