"""
Database initialization and connection utilities
"""
import sqlite3
from pathlib import Path


def get_db_connection():
    """Get a connection to the SQLite database"""
    db_path = Path(__file__).parent / 'lottery.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Sorteos table
    c.execute('''CREATE TABLE IF NOT EXISTS sorteos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  numbers TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Historical data table
    c.execute('''CREATE TABLE IF NOT EXISTS historical_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  balota1 INTEGER,
                  balota2 INTEGER,
                  balota3 INTEGER,
                  balota4 INTEGER,
                  balota5 INTEGER,
                  balota6 INTEGER,
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")


def close_db_connection(conn):
    """Close database connection"""
    if conn:
        conn.close()
