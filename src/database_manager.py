import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='data/maintenance.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        sensor_id TEXT,
        temperature REAL,
        vibration REAL,
        preasure REAL,
        failure_label INTEGER DEFAULT 0 
    );
    """
        with self.get_connection() as conn:
            conn.execute(query)
        print(f'Database initialized at {self.db_path}')

    def insert_record(self, sensor_id, temp, vib, press, failure):
        query = """INSERT INTO telemetry (sensor_id, temperature, vibration, preasure, failure_label)
        VALUES(?,?,?,?,?)
        """
        with self.get_connection() as conn:
            conn.execute(query, (sensor_id, temp, vib, press, failure))

        