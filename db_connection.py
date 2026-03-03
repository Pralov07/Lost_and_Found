import sqlite3

def get_db_connection():
    conn = sqlite3.connect('lost_and_found.db')
    # Ensure tables exist
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lost_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            date_lost TEXT,
            location_lost TEXT,
            description TEXT,
            contact_info TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS found_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            date_found TEXT,
            location_found TEXT,
            description TEXT,
            contact_info TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claimed_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            date_claimed TEXT,
            location_claimed TEXT,
            description TEXT,
            contact_info TEXT
        )
    ''')
    conn.commit()
    return conn
