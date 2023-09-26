import json
from datetime import datetime

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.schema.response import ErrorResponse


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == 'POST':
            if 'content-length' not in request.headers:
                response = ErrorResponse(
                    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    status="LENGTH_REQUIRED",
                    error="LENGTH_REQUIRED",
                    message="파일 크기 헤더가 없습니다.",
                    errorCode="IG-M-001",
                    path=request.url.path
                )
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED,
                                content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                                   ensure_ascii=False),
                                media_type="application/json")
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                response = ErrorResponse(
                    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    status="ENTITY_TOO_LARGE",
                    error="ENTITY_TOO_LARGE",
                    message="파일 크기가 너무 큽니다.",
                    errorCode="IG-M-002",
                    path=request.url.path
                )
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                                   ensure_ascii=False),
                                media_type="application/json")
        return await call_next(request)


class LimitFileType(BaseHTTPMiddleware):
    def __init__(self, app, allowed_extensions):
        super().__init__(app)
        self.allowed_extensions = allowed_extensions

    async def dispatch(self, request: Request, call_next):
        if request.method == 'POST':
            content_type = request.headers.get('content-type')
            if content_type is None:
                response = ErrorResponse(
                    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    status="BAD_REQUEST",
                    error="BAD_REQUEST",
                    message="파일을 찾을 수 없습니다.",
                    errorCode="IG-M-003",
                    path=request.url.path
                )
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                                   ensure_ascii=False),
                                media_type="application/json")

            file_extension = content_type.split("/")[-1]
            if not self.is_allowed_extension(file_extension):
                response = ErrorResponse(
                    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    status="BAD_REQUEST",
                    error="BAD_REQUEST",
                    message="지원하지 않는 파일 확장자 입니다.",
                    errorCode="IG-M-004",
                    path=request.url.path
                )
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                                   ensure_ascii=False),
                                media_type="application/json")

        return await call_next(request)

    def is_allowed_extension(self, extension):
        return extension.lower() in self.allowed_extensions
