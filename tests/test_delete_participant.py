from app.storage import database
from app.storage.database import get_connection, initialize_database
from app.storage.participants import delete_participant


def test_delete_participant(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database,
        "DB_PATH",
        tmp_path / "attendance.db",
    )

    initialize_database()

    with get_connection() as conn:
        participant_id = conn.execute(
            """
            INSERT INTO participants (name, consent_given, created_at)
            VALUES (?, ?, ?)
            """,
            ("Test Person", 1, "2026-09-24T00:00:00+00:00"),
        ).lastrowid

        conn.execute(
            """
            INSERT INTO embeddings
                (participant_id, embedding, created_at)
            VALUES (?, ?, ?)
            """,
            (participant_id, b"test", "2026-09-24T00:00:00+00:00"),
        )

        conn.execute(
            """
            INSERT INTO attendance (participant_id, timestamp)
            VALUES (?, ?)
            """,
            (participant_id, "2026-09-24T10:00:00+00:00"),
        )

    assert delete_participant(participant_id) is True

    with get_connection() as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM participants WHERE id = ?",
            (participant_id,),
        ).fetchone()[0] == 0

        assert conn.execute(
            "SELECT COUNT(*) FROM embeddings WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()[0] == 0

        assert conn.execute(
            "SELECT COUNT(*) FROM attendance WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()[0] == 0