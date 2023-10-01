import io
import os.path

from fastapi import FastAPI
from starlette.testclient import TestClient
from src.helper.path import get_relative_path


def test_get_img_by_id(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        test_img_conv,
        test_datetime
):
    response = client.get("/api/v1/image/1")
    assert 200 == response.status_code
    assert "image/png" == response.headers["content-type"]
    assert test_img_conv.read() == response.content


def test_get_img_by_id_fail(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        test_img_conv,

        test_datetime
):
    response = client.get("/api/v1/image/2")
    assert 404 == response.status_code
    result = response.json()
    assert 'IG-001' == result['errorCode']


def test_delete_img_by_id(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        converted_file_restore
):
    response = client.delete("/api/v1/image/1", headers={"user_pk": "NjCENMSLQmLwb6pltp8A19Qf5bRv", "role_pk": "4"})
    assert 200 == response.status_code
    result = response.json()
    assert 1 == result['id']
    assert 'png' == result['origin_type']
    assert 'test_img' == result['origin_nm']

    assert not os.path.isfile(
        get_relative_path(["test", "data", "2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg"]))


def test_delete_img_by_id_fail_by_auth(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        converted_file_restore
):
    response = client.delete("/api/v1/image/1", headers={"user_pk": "NjCENMSLQmLwb6pltp8A19Qf5bRv", "role_pk": "2"})
    assert 403 == response.status_code

    assert os.path.isfile(get_relative_path(["test", "data", "2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg"]))


def test_delete_img_by_id_self(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        converted_file_restore
):
    # this uid is not real. just create for test
    response = client.delete("/api/v1/image/1", headers={"user_pk": "91Hz3As0A96tQmmR1mrJtO7IxwCC", "role_pk": "2"})
    assert 200 == response.status_code
    result = response.json()
    assert 1 == result['id']
    assert 'png' == result['origin_type']
    assert 'test_img' == result['origin_nm']

    assert not os.path.isfile(
        get_relative_path(["test", "data", "2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg"]))


def test_create_img(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        test_img_conv,
        test_img,
        clear_data_file,
        test_datetime
):
    files = {"file": ("test_img.png", test_img, "image/png")}
    response = client.post("/api/v1/image", files=files,
                           headers={"user_pk": "NjCENMSLQmLwb6pltp8A19Qf5bRv", "role_pk": "4"})
    assert 200 == response.status_code
    result = response.json()
    assert 2 == result['id']
    assert 'png' == result['origin_type']
    assert 'test_img' == result['origin_nm']

    file_list = os.listdir(get_relative_path(["test", "data"]))
    file_list.remove("2023-09-29_a6c21641-8aaf-4294-a261-2f04ae49264a.jgwimg")
    target = file_list[-1]

    assert os.path.isfile(get_relative_path(["test", "data", target]))

    img = open(get_relative_path(["test", "data", target]), "rb")
    assert test_img_conv.read() == img.read()


def test_create_img_fail_type(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        test_img_pdf
):
    files = {"file": ("test_img.pdf", test_img_pdf, "image/png")}
    response = client.post("/api/v1/image", files=files,
                           headers={"user_pk": "NjCENMSLQmLwb6pltp8A19Qf5bRv", "role_pk": "4"})
    assert 400 == response.status_code


def test_create_img_fail_sig(
        setup_test_db,
        app: FastAPI,
        client: TestClient,
        test_img_fake_png
):
    files = {"file": ("LOL_THIS_IS_NOT_PNG.png", test_img_fake_png, "image/png")}
    response = client.post("/api/v1/image", files=files,
                           headers={"user_pk": "NjCENMSLQmLwb6pltp8A19Qf5bRv", "role_pk": "4"})
    assert 400 == response.status_code
