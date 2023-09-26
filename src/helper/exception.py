from enum import Enum


class ErrorCode(Enum):
    NOT_FOUND = ("NOT_FOUND", "IG-001", 404)
    UNKNOWN_ERROR = ("UNKNOWN_ERROR", "IG-002", 500)
    INVALID_FILE_TYPE = ("INVALID_FILE_TYPE", "IG-003", 400)
    LIMIT_FILE_SIZE = ("LIMIT_FILE_SIZE", "IG-004", 400)


class InternalException(Exception):
    def __init__(self, message: str, error_code: ErrorCode):
        self.message = message
        self.error_code = error_code


class ImgProcessException(Exception):
    def __init__(self, message: str):
        self.message = message
