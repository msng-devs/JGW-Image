import logging

level = logging.DEBUG


def setup_logging():
    logging.basicConfig(level=level,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")