from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from src.core.config import Config

setting = Config()

Base = declarative_base()
db_engine = create_engine(setting.DB_URL, pool_pre_ping=True)
db_session = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = None
    try:
        db = db_session()
        yield db

    finally:
        db.close()
