import os
import shutil
from datetime import datetime
from typing import Generator, Any

import pytest
from fastapi import FastAPI
from sqlalchemy import text
from starlette.testclient import TestClient
from main import create_app
from src.helper.path import get_absolute_path, get_relative_path
from src.db.database import db_session, create_schema, drop_schema


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    _app = create_app()
    yield _app


@pytest.fixture(autouse=True)
def setup_test_db():
    print("setup_test_db")
    if os.path.isfile(get_relative_path(["test", "test.db"])):
        os.remove(get_relative_path(["test", "test.db"]))
    shutil.copyfile(get_relative_path(["test", "resource", "test.db"]), get_relative_path(["test", "test.db"]))
    yield
    print("clear_test_db")
    os.remove(get_relative_path(["test", "test.db"]))


@pytest.fixture()
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def test_img():
    test_img = open(get_relative_path(["test", "resource", "test_img.png"]), "rb")
    return test_img


@pytest.fixture()
def test_img_conv():
    test_img = open(get_relative_path(["test", "resource", "test_img_conv.png"]), "rb")
    return test_img


@pytest.fixture()
def test_img_pdf():
    test_img = open(get_relative_path(["test", "resource", "test_img.pdf"]), "rb")
    return test_img

@pytest.fixture()
def test_img_fake_png():
    test_img = open(get_relative_path(["test", "resource", "LOL_THIS_IS_NOT_PNG.png"]), "rb")
    return test_img

@pytest.fixture()
def test_datetime():
    date_string = "2023-09-27 18:57:09"
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(date_string, date_format)


@pytest.fixture()
def converted_file_restore():
    yield
    print("converted_file_restore")
    if os.path.isfile(get_relative_path(["test", "data", "2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg"])):
        return
    shutil.copyfile(get_relative_path(["test", "resource", "2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg"]),
                    get_relative_path(["test", "data", "2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg"]))


@pytest.fixture()
def clear_data_file():
    yield
    print("clear_data_file")
    file_list = os.listdir(get_relative_path(["test", "data"]))
    file_list.remove("2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg")
    target = file_list[-1]
    os.remove(get_relative_path(["test", "data", target]))
