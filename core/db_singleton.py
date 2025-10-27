import sqlite3
from config import Config

class Database:
    _instance = None

    def __new__(cls):
        # Chỉ tạo đúng 1 instance cho toàn bộ chương trình
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(
                Config.DB_PATH,
                check_same_thread=False  # cho phép dùng trong Flask dev server
            )
            cls._instance.connection.row_factory = sqlite3.Row
        return cls._instance

    def get_connection(self):
        return self.connection

    def init_schema(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            name TEXT,
            classroom TEXT,
            midterm REAL,
            final REAL
        );
        """)
        conn.commit()
