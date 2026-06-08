import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "metrics.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT    NOT NULL UNIQUE,
                sleep_hours REAL,
                sleep_quality INTEGER,
                mood        INTEGER,
                water_ml    INTEGER,
                screen_min  INTEGER,
                weight_kg   REAL,
                notes       TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)


if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")
