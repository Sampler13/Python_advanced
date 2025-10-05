import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# USERS_FILE = os.path.join(BASE_DIR, 'users.json')
DB_DIR = os.path.join(BASE_DIR, 'database')

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    DB_PATH = os.path.join(DB_DIR, 'db_quiz.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    # USERS_FILE = USERS_FILE

