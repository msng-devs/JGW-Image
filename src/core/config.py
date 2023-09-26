import os

from dotenv import load_dotenv
import tempfile
from src.helper.path import get_absolute_path

load_dotenv(get_absolute_path([".env"]))


class Config:
    def __init__(self):
        self.DB_URL = os.getenv("DB_URL")
        self.FILE_TYPE = os.getenv("FILE_TYPE")
        self.FILE_PATH = get_absolute_path(os.getenv("FILE_PATH").split("/"))
        self.IMG_QUALITY = int(os.getenv("IMG_QUALITY"))
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
        self.ALLOWED_FILE_TYPE = os.getenv("ALLOWED_FILE_TYPE").split(",")
        self.TMP_FILE_PATH = get_absolute_path(os.getenv("TMP_FILE_PATH").split("/"))
        self.FILE_CONVERTED_TYPE = os.getenv("FILE_CONVERTED_TYPE")
        tempfile.tempdir = self.TMP_FILE_PATH


config = Config()
