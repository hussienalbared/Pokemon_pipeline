# db/base.py
from flask import g
import sqlite3
from config import DB_NAME

def get_or_create_id(conn, table: str, name: str) -> int:
    """
    Retrieves the ID of a row with the specified name from the given table, or inserts a new row if it does not exist.

    Args:
        conn: A SQLite database connection object.
        table (str): The name of the table to query or insert into.
        name (str): The value to search for in the 'name' column.

    Returns:
        int: The ID of the existing or newly inserted row.

    Note:
        This function assumes the table has columns 'id' (primary key) and 'name' (unique or indexed).
        SQL injection is possible if 'table' is not validated; ensure 'table' is a trusted value.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid





def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
    return db
