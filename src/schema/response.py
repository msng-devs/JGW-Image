from pydantic import BaseModel


class ErrorResponse(BaseModel):
    timestamp: str
    status: str
    error: str
    message: str
    errorCode: str
    path: str


class ImageMetaResponse(BaseModel):
    id: int
    origin_type: str
    origin_nm: str
    origin_file_size: int
    upload_by: str
    created_at: str
