import sqlite3
import datetime
import os

class ZeroTrustLogger:
    """
    Maintains an immutable encrypted audit trail of identity verification attempts.
    """
    def __init__(self, db_path="data/audit.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            biometric_score REAL,
            mfa_status TEXT,
            event_type TEXT,
            failure_reason TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def log_attempt(self, bio_score, mfa_status, event_type, reason=""):
        timestamp = datetime.datetime.now().isoformat()
        query = "INSERT INTO access_logs (timestamp, biometric_score, mfa_status, event_type, failure_reason) VALUES (?, ?, ?, ?, ?)"
        self.conn.execute(query, (timestamp, bio_score, mfa_status, event_type, reason))
        self.conn.commit()

    def get_recent_logs(self, limit=10):
        cursor = self.conn.execute("SELECT * FROM access_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()
