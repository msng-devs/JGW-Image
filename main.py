from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.core.config import Config
from src.middleware.upload import LimitUploadSize
from src.router.router import router
from src.helper.log import setup_logging

config = Config()
setup_logging()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LimitUploadSize, max_upload_size=config.MAX_FILE_SIZE)
# app.add_middleware(LimitFileType, allowed_extensions=config.ALLOWED_FILE_TYPE)
app.include_router(router)
