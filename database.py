# database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "bank.db"

def get_connection():
    """Returns a SQLite connection to the shared database."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Creates tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Customers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0
    )
    """)

    # Transactions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        balance_after REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    conn.commit()
    conn.close()

# Auto-create tables when this file is first imported
init_db()
