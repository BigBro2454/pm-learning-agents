import sqlite3
import json
import os
from datetime import datetime

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory.db')

def init_db():
    """
    Initializes the SQLite database for storing episodic memory of research runs.
    Creates the 'runs' table if it doesn't already exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create a table to store each research run
    # Storing plan, findings, and final_report as JSON or text
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            plan TEXT,
            findings TEXT,
            final_report TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_run(query: str, plan: list, findings: dict, final_report: str):
    """
    Logs the entire research run to episodic memory.
    
    Args:
        query: The original user query.
        plan: The final list of subtasks and their statuses.
        findings: The accumulated knowledge dictionary.
        final_report: The generated markdown report.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    plan_json = json.dumps(plan)
    findings_json = json.dumps(findings)
    
    cursor.execute('''
        INSERT INTO runs (timestamp, query, plan, findings, final_report)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, query, plan_json, findings_json, final_report))
    
    conn.commit()
    conn.close()
    print(f"Run logged to episodic memory (query: '{query}')")

# Initialize database when this module is imported
init_db()
