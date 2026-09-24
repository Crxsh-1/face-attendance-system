import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "attendance.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            consent_given INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            embedding BLOB NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (participant_id) REFERENCES participants(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (participant_id) REFERENCES participants(id)
                ON DELETE CASCADE
        );
        """)


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DB_PATH}")