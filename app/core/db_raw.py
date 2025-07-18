# Obsolete!!!
import psycopg
from app.core.config import settings


def get_connection():
    conn = psycopg.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )
    conn.row_factory = psycopg.rows.dict_row
    return conn
