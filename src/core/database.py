import sqlite3
from pathlib import Path

DB_PATH = Path("data/ayorai.db")

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame INTEGER NOT NULL,
            track_id INTEGER,
            label TEXT NOT NULL,
            confidence REAL NOT NULL,
            x1 REAL NOT NULL, y1 REAL NOT NULL, x2 REAL NOT NULL, y2 REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_detections_track ON detections(track_id);
        CREATE INDEX IF NOT EXISTS idx_detections_conf ON detections(confidence);
        """)
