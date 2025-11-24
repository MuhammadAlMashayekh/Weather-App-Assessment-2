import sqlite3

def connect():
    x = sqlite3.connect("weather_database.db")
    x.row_factory = sqlite3.Row
    return x
def create_table():
    x = connect()
    cursor = x.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        temperature_data TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    x.commit()
    x.close()
    
def insert(location, start_date, end_date, temperature_data):
    x = connect()
    cursor = x.cursor()
    cursor.execute("INSERT INTO weather_records (location, start_date, end_date, temperature_data) VALUES (?, ?, ?, ?)",
        (location, start_date, end_date, temperature_data))
    x.commit()
    x.close()
    
def fetch_all():
    x = connect()
    cursor = x.cursor()
    cursor.execute("SELECT * FROM weather_records")
    rows = cursor.fetchall()
    x.close()
    return rows
    
def fetch_one(record_id):
    x = connect()
    cursor = x.cursor()
    cursor.execute("SELECT * FROM weather_records WHERE id = ?", (record_id,))
    rows = cursor.fetchone()
    x.close()
    return rows
    
def update(location, start_date, end_date, temperature_data, record_id):
    x = connect()
    cursor = x.cursor()
    cursor.execute("UPDATE weather_records SET location=?, start_date=?, end_date=?, temperature_data=? WHERE id=?",
        (location, start_date, end_date, temperature_data, record_id))
    x.commit()
    x.close()

def delete(record_id):
    x = connect()
    cursor = x.cursor()
    cursor.execute("DELETE FROM weather_records WHERE id=?", (record_id,))
    x.commit()
    x.close()