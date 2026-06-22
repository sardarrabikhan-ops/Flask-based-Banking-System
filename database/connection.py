#database/connection.py

import sqlite3
import os

def get_db_connection():
    db_path = os.getenv("DB_PATH")

    if not db_path:
        raise ValueError("DB_PATH is missing")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn