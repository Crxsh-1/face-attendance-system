from app.storage import database
from app.storage.database import get_connection, initialize_database
from app.attendance.service import record_attendance


def test_attendance_records_once_per_day(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database,
        "DB_PATH",
        tmp_path / "attendance.db",
    )

    initialize_database()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO participants (name, consent_given, created_at)
            VALUES (?, ?, ?)
            """,
            ("Test Person", 1, "2026-09-24T00:00:00+00:00"),
        )
        participant_id = cursor.lastrowid

    assert record_attendance(participant_id) is True
    assert record_attendance(participant_id) is False

    with get_connection() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM attendance WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()[0]

    assert count == 1