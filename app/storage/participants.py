import numpy as np
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


def get_embeddings():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT participant_id, embedding FROM embeddings"
        ).fetchall()

    return [
        (participant_id, np.frombuffer(data, dtype=np.float32))
        for participant_id, data in rows
    ]

def get_participant_name(participant_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT name FROM participants WHERE id = ?",
            (participant_id,),
        ).fetchone()

    return row[0] if row else None