from datetime import datetime
from typing import Generator, Any

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from main import create_app
from src.helper.path import get_absolute_path
from src.db.database import create_schema, drop_schema, db_session


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    _app = create_app()
    yield _app


@pytest.fixture(scope='function')
def setup_test_db():
    create_schema()
    db = db_session()
    db.execute("INSERT INTO IMAGE_META (IMAGE_META_PK, IMAGE_META_ORIGIN_TYPE, IMAGE_META_ORIGIN_NM, ")
    yield
    drop_schema()


@pytest.fixture()
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def test_img():
    test_img = open(get_absolute_path(["resource", "test_img.PNG"]), "rb")
    return test_img


@pytest.fixture()
def test_datetime():
    date_string = "2023-09-27 18:57:09"
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_string, date_format)
