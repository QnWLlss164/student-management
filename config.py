import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = "super-secret-change-me"
    DB_PATH = os.path.join(BASE_DIR, "students.db")
