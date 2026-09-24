import numpy as np

from app.storage.database import initialize_database
from app.storage.participants import add_participant, get_embeddings


def test_load_embedding(tmp_path, monkeypatch):
    import app.storage.database as database

    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    initialize_database()

    original = np.ones(128, dtype=np.float32)
    add_participant("Test Person", original)

    rows = get_embeddings()

    assert len(rows) == 1
    assert rows[0][0] == 1
    assert np.array_equal(rows[0][1], original)
