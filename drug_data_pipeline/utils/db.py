import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

# Load environment variables from .env
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def parse_date(val):
    try:
        if val and len(val) == 8:
            return datetime.strptime(val, "%Y%m%d").date()
    except Exception:
        pass
    return None
