from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from src.core.config import config
Base = declarative_base()
db_engine = create_engine(config.DB_URL, pool_pre_ping=True)
db_session = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = None
    try:
        db = db_session()
        yield db

    finally:
        db.close()


def create_schema():
    Base.metadata.create_all(bind=db_engine, checkfirst=True)


def drop_schema():
    Base.metadata.drop_all(bind=db_engine, checkfirst=True)
