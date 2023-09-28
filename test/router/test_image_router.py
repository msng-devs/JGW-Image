import io

from fastapi import FastAPI
from starlette.testclient import TestClient

from src.db.model import ImageMeta


def test_get_img_by_id(
        app: FastAPI,
        client: TestClient,
        test_img,
        test_datetime,
        setup_test_db,
        mocker
):

    mocker.patch("src.router.image_router.find_by_id", return_value=ImageMeta(
        IMAGE_META_PK=1,
        IMAGE_META_ORIGIN_TYPE="PNG",
        IMAGE_META_ORIGIN_NM="test_img",
        IMAGE_META_ORIGIN_FILE_SIZE=1898,
        IMAGE_META_FILE_PATH="/test/data",
        IMAGE_META_UPLOAD_BY="test_user",
        IMAGE_META_CONVERTED_NM="2023-09-27_2d0b7c5b-9a9e-46cb-8d69-4cf28a67ceae.jgwimg",
        IMAGE_META_CREATED_AT=test_datetime
    ))

    mocker.patch("src.router.image_router.load_img", return_value=test_img.read())

    response = client.get("/api/v1/image/1")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/PNG"
    # TODO : 결과 이미지 비교 추가
