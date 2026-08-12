from cryptography.fernet import Fernet
import sqlite3
import os
import json

class EncryptedVault:
    def __init__(self, db_path="assets/audit.db", key_path="assets/master.key"):
        self.db_path = db_path
        self.key_path = key_path
        self._load_key()
        self._init_db()

    def _load_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            dir_name = os.path.dirname(self.key_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(self.key_path, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                status TEXT,
                sent_count INTEGER DEFAULT 0,
                click_count INTEGER DEFAULT 0,
                compromised_count INTEGER DEFAULT 0,
                config_blob TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_campaign(self, name, config):
        conn = sqlite3.connect(self.db_path)
        blob = self.cipher.encrypt(json.dumps(config).encode()).decode()
        conn.execute("INSERT INTO campaigns (name, status, config_blob) VALUES (?, ?, ?)", 
                     (name, "Draft", blob))
        conn.commit()
        conn.close()

    def get_campaigns(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, status, sent_count, click_count, compromised_count FROM campaigns")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_stats(self, campaign_id, sent=0, click=0, compromised=0):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            UPDATE campaigns SET 
            sent_count = sent_count + ?, 
            click_count = click_count + ?, 
            compromised_count = compromised_count + ?
            WHERE id = ?
        """, (sent, click, compromised, campaign_id))
        conn.commit()
        conn.close()
