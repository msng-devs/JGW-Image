from sqlalchemy import Column, Integer, String, INTEGER, BIGINT, VARCHAR, CHAR, DATETIME

from src.db.database import Base
from src.helper.repr import repr_create


class ImageMeta(Base):
    __tablename__ = "IMAGE_META"

    IMAGE_META_PK = Column(BIGINT, primary_key=True, autoincrement=True)
    IMAGE_META_ORIGIN_NM = Column(VARCHAR(260), nullable=False)
    IMAGE_META_ORIGIN_TYPE = Column(VARCHAR(5), nullable=False)
    IMAGE_META_FILE_PATH = Column(VARCHAR(1024), nullable=False)
    IMAGE_META_ORIGIN_FILE_SIZE = Column(INTEGER, nullable=False)
    IMAGE_META_CONVERTED_NM = Column(VARCHAR(260), nullable=False)
    IMAGE_META_UPLOAD_BY = Column(CHAR(28), nullable=False)
    IMAGE_META_CREATED_AT = Column(DATETIME, nullable=False)

    def __repr__(self):
        return repr_create(class_name="ImageMeta",
                           table_list=["IMAGE_META_PK", "IMAGE_META_ORIGIN_NM", "IMAGE_META_ORIGIN_TYPE",
                                       "IMAGE_META_FILE_PATH", "IMAGE_META_ORIGIN_FILE_SIZE",
                                       "IMAGE_META_CONVERTED_NM", "IMAGE_META_UPLOAD_BY", "IMAGE_META_CREATED_AT"]) \
            .format(self=self)
