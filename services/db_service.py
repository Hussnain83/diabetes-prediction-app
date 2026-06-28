import sqlite3
import hashlib
import json

DB_PATH = "diabetes_checks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS checks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            data_hash TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
'''
    )
    conn.commit()
    conn.close()

def generate_hash(data: dict) -> str:
    # Name + all data combine karke hash banao
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_string.encode()).hexdigest()

def is_duplicate(data: dict) -> bool:
    data_hash = generate_hash(data)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM checks WHERE data_hash = ?", (data_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_check(data: dict):
    data_hash = generate_hash(data)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO checks (name, data_hash) VALUES (?, ?)",
        (data['name'], data_hash)
    )
    conn.commit()
    conn.close()
