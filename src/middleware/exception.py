import json
from datetime import datetime

from starlette.requests import Request
from starlette.responses import Response

from src.helper.exception import InternalException, ImgProcessException
from logging import getLogger

log = getLogger(__name__)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except InternalException as e:
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "status": e.error_code.value[2],
            "error": e.error_code.value[0],
            "message": e.message,
            "errorCode": e.error_code.value[1],
            "path": request.url.path
        }
        return Response(status_code=e.error_code.value[2],
                        content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                           ensure_ascii=False),
                        media_type="application/json")
    except ImgProcessException as e:
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "status": "INTERNAL_SERVER_ERROR",
            "error": "INTERNAL_SERVER_ERROR",
            "message": e.message,
            "errorCode": "IG-100",
            "path": request.url.path
        }
        return Response(status_code=500,
                        content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                           ensure_ascii=False),
                        media_type="application/json")
    except Exception as e:
        log.error(e.__class__.__name__ + " : " + str(e))
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "status": "INTERNAL_SERVER_ERROR",
            "error": "INTERNAL_SERVER_ERROR",
            "message": "알 수 없는 오류가 발생했습니다.",
            "errorCode": "IG-200",
            "path": request.url.path
        }
        return Response(status_code=500,
                        content=json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4,
                                           ensure_ascii=False),
                        media_type="application/json")
