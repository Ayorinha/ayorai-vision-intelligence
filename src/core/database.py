import sqlite3
from pathlib import Path

DB_PATH = Path("data/ayorai.db")

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY, filename TEXT NOT NULL, status TEXT NOT NULL,
            progress REAL DEFAULT 0, output_path TEXT, error TEXT,
            created_at TEXT NOT NULL, started_at TEXT, completed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
            frame INTEGER NOT NULL, track_id INTEGER, label TEXT NOT NULL, confidence REAL NOT NULL,
            x1 REAL NOT NULL, y1 REAL NOT NULL, x2 REAL NOT NULL, y2 REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_detections_job ON detections(job_id);
        CREATE INDEX IF NOT EXISTS idx_detections_track ON detections(track_id);
        CREATE INDEX IF NOT EXISTS idx_detections_conf ON detections(confidence);
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT, detection_id INTEGER NOT NULL REFERENCES detections(id) ON DELETE CASCADE,
            status TEXT NOT NULL, reason TEXT NOT NULL, decision TEXT, reviewer TEXT, final_label TEXT,
            created_at TEXT NOT NULL, reviewed_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_reviews_status ON reviews(status);
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
            event_type TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL
        );
        """)
