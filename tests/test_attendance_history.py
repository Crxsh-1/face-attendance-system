from app.storage import database
from app.storage.database import get_connection, initialize_database
from app.attendance.history import get_attendance


def test_get_attendance(tmp_path, monkeypatch):
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
            INSERT INTO attendance (participant_id, timestamp)
            VALUES (?, ?)
            """,
            (participant_id, "2026-09-24T10:00:00+00:00"),
        )

    records = get_attendance()

    assert records == [
        ("Test Person", "2026-09-24T10:00:00+00:00")
    ]