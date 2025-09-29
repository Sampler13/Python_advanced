import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    USERS_FILE = USERS_FILE

