import os

from dotenv import load_dotenv
import tempfile
from src.helper.path import get_relative_path
import logging

log = logging.getLogger(__name__)
load_dotenv(dotenv_path=get_relative_path(["env",f".env.{os.environ['API_SERVER_PROFILE']}"]))

class Config:
    def __init__(self):
        self.DB_URL = os.getenv("DB_URL")
        self.FILE_TYPE = os.getenv("FILE_TYPE")
        self.FILE_PATH = get_relative_path(os.getenv("FILE_PATH").split("/"))
        self.IMG_QUALITY = int(os.getenv("IMG_QUALITY"))
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
        self.ALLOWED_FILE_TYPE = os.getenv("ALLOWED_FILE_TYPE").split(",")
        self.TMP_FILE_PATH = get_relative_path(os.getenv("TMP_FILE_PATH").split("/"))
        self.FILE_CONVERTED_TYPE = os.getenv("FILE_CONVERTED_TYPE")
        self.CLEAR_TRASH_TIME = [int(x) for x in os.getenv("CLEAR_TRASH_TIME").split(":")]
        tempfile.tempdir = self.TMP_FILE_PATH

        self.MAIL_STORM_SERVER = os.getenv("MAIL_STORM_SERVER") if os.getenv("MAIL_STORM_SERVER") else None
        self.MAIL_STORM_PORT = os.getenv("MAIL_STORM_PORT") if os.getenv("MAIL_STORM_SERVER") else None
        self.MAIL_STORM_TO = os.getenv("MAIL_STORM_TO") if os.getenv("MAIL_STORM_SERVER") else None

        self.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")

    def print_setting(self):
        log.info(f"Set Up Env Name : {os.getenv('ENV_NAME')}")
        log.info(f"Set Up File Type : {self.FILE_TYPE}")
        log.info(f"Set Up File Path : {self.FILE_PATH}")
        log.info(f"Set Up Image Quality : {self.IMG_QUALITY}")
        log.info(f"Set Up Max File Size : {self.MAX_FILE_SIZE}")
        log.info(f"Set Up Allowed File Type : {self.ALLOWED_FILE_TYPE}")
        log.info(f"Set Up Temp File Path : {self.TMP_FILE_PATH}")
        log.info(f"Set Up File Converted Type : {self.FILE_CONVERTED_TYPE}")
        log.info(f"Set Up Clear Trash Time : {self.CLEAR_TRASH_TIME}")
        log.info(f"Set Up Logging Level : {self.LOGGING_LEVEL}")


config = Config()
