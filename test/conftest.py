from typing import Generator, Any

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.db.database import Base, get_db
from main import create_app
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)  # Create the tables.
    _app = create_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
