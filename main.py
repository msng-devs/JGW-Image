from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.core.config import config
from src.middleware.exception import catch_exceptions_middleware
from src.middleware.upload import LimitUploadSize
from src.router.router import router
from src.helper.log import setup_logging

setup_logging()
config.print_setting()


def create_app():
    tmp_app = FastAPI()

    tmp_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    tmp_app.add_middleware(LimitUploadSize, max_upload_size=config.MAX_FILE_SIZE)
    tmp_app.middleware('http')(catch_exceptions_middleware)
    tmp_app.include_router(router)

    return tmp_app


app = create_app()
