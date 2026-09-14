import sqlite3
import hashlib
from typing import Dict, Any, Optional

class MemoryDB:
    def __init__(self, db_path: str):
        """
        Initializes the SQLite database for agent memory.
        This provides episodic memory to remember what articles have already been processed.
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Creates the necessary tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Table to store seen articles and deduplicate them
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seen_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url_hash TEXT UNIQUE NOT NULL,
                    title TEXT,
                    url TEXT,
                    relevance_score REAL,
                    alerted BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def _generate_hash(self, url: str) -> str:
        """Generates a unique hash for a given URL to be used as a deduplication key."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def is_article_seen(self, url: str) -> bool:
        """
        Checks if an article has already been processed based on its URL.
        This prevents the agent from processing and alerting on the same article multiple times.
        """
        url_hash = self._generate_hash(url)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM seen_articles WHERE url_hash = ?", (url_hash,))
            result = cursor.fetchone()
            return result is not None

    def log_article(self, title: str, url: str, relevance_score: float, alerted: bool):
        """
        Logs an article into the database along with its relevance and alert status.
        Even if not alerted, logging helps in future analysis of the agent's perception.
        """
        url_hash = self._generate_hash(url)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO seen_articles (url_hash, title, url, relevance_score, alerted)
                    VALUES (?, ?, ?, ?, ?)
                ''', (url_hash, title, url, relevance_score, alerted))
                conn.commit()
        except sqlite3.IntegrityError:
            # Handle potential race conditions where the article is inserted between check and insert
            pass
