# db/base.py

def get_or_create_id(conn, table: str, name: str) -> int:
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid



from flask import g
import sqlite3
from config import DB_NAME

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
    return db
