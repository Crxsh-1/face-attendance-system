import numpy as np

from app.storage.database import initialize_database
from app.storage.participants import add_participant


def test_add_participant(tmp_path, monkeypatch):
    import app.storage.database as database

    db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", db)

    initialize_database()

    embedding = np.zeros(128, dtype=np.float32)
    participant_id = add_participant("Test Person", embedding)

    assert participant_id == 1