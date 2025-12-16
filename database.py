"""
Database initialization and connection utilities
Compatible with both SQLite (development) and PostgreSQL (production)
"""
import os
import sqlite3
from pathlib import Path


def get_db_connection():
    """Get a connection to the database (SQLite or PostgreSQL)"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url and database_url.startswith('postgres'):
        # PostgreSQL para producción
        import psycopg2
        import psycopg2.extras
        
        # Render usa postgres:// pero psycopg2 necesita postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url)
        return conn
    else:
        # SQLite para desarrollo local
        db_path = Path(__file__).parent / 'lottery.db'
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    database_url = os.getenv('DATABASE_URL', '')
    is_postgres = database_url.startswith('postgres')
    
    c = conn.cursor()
    
    if is_postgres:
        # PostgreSQL syntax
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id SERIAL PRIMARY KEY,
                      username VARCHAR(255) UNIQUE NOT NULL,
                      password VARCHAR(255) NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Sorteos table
        c.execute('''CREATE TABLE IF NOT EXISTS sorteos
                     (id SERIAL PRIMARY KEY,
                      user_id INTEGER NOT NULL,
                      numbers TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        
        # Historical data table
        c.execute('''CREATE TABLE IF NOT EXISTS historical_data
                     (id SERIAL PRIMARY KEY,
                      balota1 INTEGER,
                      balota2 INTEGER,
                      balota3 INTEGER,
                      balota4 INTEGER,
                      balota5 INTEGER,
                      balota6 INTEGER,
                      date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    else:
        # SQLite syntax
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
    db_type = "PostgreSQL" if is_postgres else "SQLite"
    print(f"✅ Database initialized successfully ({db_type})")


def close_db_connection(conn):
    """Close database connection"""
    if conn:
        conn.close()
