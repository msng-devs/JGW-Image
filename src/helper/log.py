import logging
from src.core.config import config


level = logging.INFO

if config.LOGGING_LEVEL == "DEBUG":
    level = logging.DEBUG


def setup_logging(who:str):
    logging.basicConfig(level=level,
                        format=f"[{who}] %(asctime)s - %(levelname)s - %(name)s - %(message)s")
