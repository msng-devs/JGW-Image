from enum import Enum
from functools import wraps

from src.helper.exception import ErrorCode, InternalException


class AuthMode(Enum):
    NO_AUTH = 1
    AUTH = 2
    ONLY_TOKEN_AUTH = 3
    RBAC = 4
    AUTH_OPTIONAL = 5


def auth_mode(mode: AuthMode, arg: str = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            header = request.headers

            uid = header.get('user_pk') if header.get('user_pk') else None
            role = header.get('role_pk') if header.get('role_pk') else None

            if mode == mode.NO_AUTH:
                pass

            elif mode == mode.AUTH:
                if uid is None or role is None:
                    raise InternalException("인증 정보가 없습니다.", ErrorCode.UNKNOWN_ERROR)

            elif mode == mode.ONLY_TOKEN_AUTH:
                if uid is None:
                    raise InternalException("인증 정보가 없습니다.", ErrorCode.UNKNOWN_ERROR)

            elif mode == mode.RBAC:
                if uid is None or role is None:
                    raise InternalException("인증 정보가 없습니다.", ErrorCode.UNKNOWN_ERROR)
                if role < arg:
                    raise InternalException("권한이 없습니다.", ErrorCode.UNKNOWN_ERROR)

            elif mode == mode.AUTH_OPTIONAL:
                if not (uid is None and role is None) and (uid is None or role is None):
                    raise InternalException("인증 정보가 없습니다.", ErrorCode.UNKNOWN_ERROR)

            return wrapper

        return decorator
