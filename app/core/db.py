from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

dbname = settings.DB_NAME
username = settings.DB_USERNAME
password = settings.DB_PASSWORD
host = settings.DB_HOST
port = settings.DB_PORT

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{username}:{password}@{host}:{port}/{dbname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
