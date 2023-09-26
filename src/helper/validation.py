import fleep
from fastapi import UploadFile

from src.core.config import Config
from src.helper.exception import ImgProcessException, ErrorCode, InternalException

config = Config()


def validate_file_extension(file: UploadFile):
    file_type = file.filename.split(".")[-1]
    if f"image/{file_type}" in config.ALLOWED_FILE_TYPE:
        return f"image/{file_type}"
    else:
        raise InternalException("업로드가 불가능한 타입입니다.", ErrorCode.INVALID_FILE_TYPE)


async def validate_file_signature(file: UploadFile,detect_type: str):
    file_content = await file.read(128)

    info = fleep.get(file_content)

    # MIME 타입 확인
    mime_type = info.mime[0] if info.mime else None

    # 기대한 MIME 타입과 비교
    if mime_type == detect_type:
        return True
    else:
        raise InternalException("파일의 시그니처가 잘못되었습니다.", ErrorCode.INVALID_FILE_TYPE)
