from src.db.model import ImageMeta
from src.helper.exception import InternalException, ErrorCode
from logging import getLogger

log = getLogger(__name__)


def find_by_id(db, id: int) -> ImageMeta:
    result = db.query(ImageMeta).filter(ImageMeta.IMAGE_META_PK == id).first()
    if result is None:
        raise InternalException(message="해당 ID로 이미지를 조회할 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
    return result


def find_all_by_converted_names(db, converted_names: list) -> list:
    result = db.query(ImageMeta).filter(ImageMeta.IMAGE_META_CONVERTED_NM.in_(converted_names)).all()
    if result is None:
        return []
    return result


def create(db, image_meta: ImageMeta) -> ImageMeta:
    try:
        db.add(image_meta)
        db.commit()
        db.refresh(image_meta)
    except Exception as e:
        db.rollback()
        log.debug(str(e))
        raise InternalException(message="이미지를 데이터베이스에 저장하는 중 오류가 발생했습니다.", error_code=ErrorCode.UNKNOWN_ERROR)
    return image_meta


def delete_by_id(db, id: int) -> ImageMeta:
    try:
        result = db.query(ImageMeta).filter(ImageMeta.IMAGE_META_PK == id).first()
        assert result is not None
        db.delete(result)
        db.commit()
    except AssertionError as e:
        log.debug(str(e))
        raise InternalException(message="해당 ID로 이미지를 조회할 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
    except Exception as e:
        db.rollback()
        log.debug(str(e))
        raise InternalException(message="이미지를 데이터베이스에서 삭제하는 중 오류가 발생했습니다.", error_code=ErrorCode.UNKNOWN_ERROR)
    return result
