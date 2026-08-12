import sqlite3
try:
    from pysqlcipher3 import dbapi2 as sqlite
except ImportError:
    import sqlite3 as sqlite
import os

class EncryptedDB:
    def __init__(self, db_path="assets/vault.db", password="TACTICAL_RED_SECURE_KEY"):
        self.db_path = db_path
        self.password = password
        self._init_db()

    def _init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        # Active Keywords to monitor
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT UNIQUE,
                type TEXT
            )
        """)
        # Breach History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS breaches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT,
                snippet TEXT,
                keyword TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_connection(self):
        conn = sqlite.connect(self.db_path)
        # Apply encryption if using sqlcipher
        if hasattr(sqlite, 'version'):
             cursor = conn.cursor()
             cursor.execute(f"PRAGMA key = '{self.password}'")
        return conn

    def add_keyword(self, value, ktype="email"):
        conn = self.get_connection()
        try:
            conn.execute("INSERT INTO keywords (value, type) VALUES (?, ?)", (value, ktype))
            conn.commit()
        except:
            pass
        finally:
            conn.close()

    def get_keywords(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value, type FROM keywords")
        data = cursor.fetchall()
        conn.close()
        return data

    def log_breach(self, source, snippet, keyword):
        conn = self.get_connection()
        conn.execute("INSERT INTO breaches (source, snippet, keyword) VALUES (?, ?, ?)", 
                     (source, snippet, keyword))
        conn.commit()
        conn.close()

    def get_breaches(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, source, snippet, keyword FROM breaches ORDER BY timestamp DESC")
        data = cursor.fetchall()
        conn.close()
        return data
