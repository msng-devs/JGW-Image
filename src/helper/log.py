import logging
from src.core.config import Config

confing = Config()

level = logging.INFO

if confing.LOGGING_LEVEL == "DEBUG":
    level = logging.DEBUG


def setup_logging():
    logging.basicConfig(level=level,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
