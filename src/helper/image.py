import shutil

from PIL import Image

from src.helper.exception import ImgProcessException, InternalException, ErrorCode
import os
from logging import getLogger

log = getLogger(__name__)


def optimize_image(input_path, output_path, quality=85):
    try:

        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=quality)

    except Exception as e:
        raise ImgProcessException(str(e))


def move_image(tmp_file_path: str, file_path: str):
    try:
        shutil.move(tmp_file_path, file_path)
    except shutil.Error as e:
        log.debug(str(e))
        raise ImgProcessException(str(e))
    except Exception as e:
        log.debug(str(e))
        raise InternalException(message="이미지 처리중 알 수 없는 에러가 발생했습니다.", error_code=ErrorCode.UNKNOWN_ERROR)


def load_img(path):
    try:
        assert os.path.exists(path)
        with open(path, "rb") as f:
            return f.read()

    except AssertionError as e:
        log.debug(str(e))
        raise InternalException(message="해당 이미지가 존재하지 않습니다.", error_code=ErrorCode.NOT_FOUND)

    except Exception as e:
        log.debug(str(e))
        raise InternalException(message="이미지 처리중 알 수 없는 에러가 발생했습니다.", error_code=ErrorCode.UNKNOWN_ERROR)


def delete_img(path):
    try:
        assert os.path.exists(path)
        os.remove(path)

    except AssertionError as e:
        log.debug(str(e))
        raise InternalException(message="해당 이미지가 존재하지 않습니다.", error_code=ErrorCode.NOT_FOUND)

    except Exception as e:
        log.debug(str(e))
        raise InternalException(message="이미지 처리중 알 수 없는 에러가 발생했습니다.", error_code=ErrorCode.UNKNOWN_ERROR)
