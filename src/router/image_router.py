import shutil
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.db.database import get_db
from src.db.model import ImageMeta
from src.helper.decorator import AuthMode, auth_mode
from src.helper.exception import ImgProcessException, InternalException, ErrorCode
from src.helper.image import optimize_image, move_image, load_img, delete_img
import uuid
from src.core.config import Config
from src.helper.path import get_absolute_path
import src.crud.image_crud as img_crud
from src.schema.response import ImageMetaResponse
from logging import getLogger
from src.helper.validation import validate_file_extension, validate_file_signature

log = getLogger(__name__)
img_router = APIRouter(prefix="/image")

config = Config()


@auth_mode(mode=AuthMode.NO_AUTH)
@img_router.get("/{id}", response_class=Response)
async def get_img_by_id(id: int, db: Session = Depends(get_db)):
    img_meta = img_crud.find_by_id(db, id)
    loaded_img = load_img(get_absolute_path([img_meta.IMAGE_META_FILE_PATH, img_meta.IMAGE_META_CONVERTED_NM]))
    return Response(content=loaded_img, media_type=f"image/{img_meta.IMAGE_META_ORIGIN_TYPE}")


@auth_mode(mode=AuthMode.AUTH)
@img_router.delete("/{id}", response_model=ImageMetaResponse)
async def delete_img_by_id(id: int,user_pk: Annotated[str | None, Header()] = None,role_pk: Annotated[int | None, Header()] = None  ,db: Session = Depends(get_db)):
    delete_option = False if role_pk < 4 else True
    img_meta = img_crud.delete_by_id(db, id, user_pk, delete_option)
    delete_img(get_absolute_path([img_meta.IMAGE_META_FILE_PATH, img_meta.IMAGE_META_CONVERTED_NM]))
    return {
        "id": img_meta.IMAGE_META_PK,
        "origin_type": img_meta.IMAGE_META_ORIGIN_TYPE,
        "origin_nm": img_meta.IMAGE_META_ORIGIN_NM,
        "origin_file_size": img_meta.IMAGE_META_ORIGIN_FILE_SIZE,
        "file_path": img_meta.IMAGE_META_FILE_PATH,
        "upload_by": img_meta.IMAGE_META_UPLOAD_BY,
        "converted_nm": img_meta.IMAGE_META_CONVERTED_NM,
        "created_at": img_meta.IMAGE_META_CREATED_AT.strftime("%Y-%m-%d %H:%M:%S")
    }


@auth_mode(mode=AuthMode.AUTH)
@img_router.post("", response_model=ImageMetaResponse)
async def create_img(file: UploadFile,user_pk: Annotated[str | None, Header()] = None ,db: Session = Depends(get_db)):
    detected_type = validate_file_extension(file)
    await validate_file_signature(file, detected_type)

    new_file_name = convert_img(file)
    img_meta = ImageMeta(
        IMAGE_META_ORIGIN_TYPE=file.filename.split(".")[-1],
        IMAGE_META_ORIGIN_NM=file.filename.split(".")[0],
        IMAGE_META_ORIGIN_FILE_SIZE=file.size,
        IMAGE_META_FILE_PATH=config.FILE_PATH,
        IMAGE_META_UPLOAD_BY=user_pk,
        IMAGE_META_CONVERTED_NM=new_file_name,
        IMAGE_META_CREATED_AT=datetime.now()
    )

    new_img_meta = img_crud.create(db, img_meta)

    return {
        "id": new_img_meta.IMAGE_META_PK,
        "origin_type": new_img_meta.IMAGE_META_ORIGIN_TYPE,
        "origin_nm": new_img_meta.IMAGE_META_ORIGIN_NM,
        "origin_file_size": new_img_meta.IMAGE_META_ORIGIN_FILE_SIZE,
        "file_path": new_img_meta.IMAGE_META_FILE_PATH,
        "upload_by": new_img_meta.IMAGE_META_UPLOAD_BY,
        "converted_nm": new_img_meta.IMAGE_META_CONVERTED_NM,
        "created_at": new_img_meta.IMAGE_META_CREATED_AT.strftime("%Y-%m-%d %H:%M:%S")
    }


def convert_img(file: UploadFile):
    try:
        tmp_new_file_name = datetime.now().strftime("%Y-%m-%d") + "_" + str(uuid.uuid4()) + "." + \
                            file.filename.split(".")[-1]
        new_file_name = datetime.now().strftime("%Y-%m-%d") + "_" + str(uuid.uuid4()) + "." + config.FILE_CONVERTED_TYPE

        # gif일 경우 최적화 제외
        if file.filename.split(".")[-1] != "gif":
            optimize_image(file.file, get_absolute_path([config.TMP_FILE_PATH, tmp_new_file_name]),
                           config.IMG_QUALITY)

            move_image(get_absolute_path([config.TMP_FILE_PATH, tmp_new_file_name]),
                       get_absolute_path([config.FILE_PATH, new_file_name]))
        else:
            log.debug("gif 파일이므로 최적화를 건너뜁니다.")
            with open(get_absolute_path([config.FILE_PATH, new_file_name]), "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    except ImgProcessException as e:
        log.error(str(e))
        raise e

    except InternalException as e:
        log.error(str(e))
        raise e

    except Exception as e:
        log.error(str(e))
        raise InternalException(message="서버에 알 수 없는 에러가 발생했습니다.", error_code=ErrorCode.UNKNOWN_ERROR)

    return new_file_name
