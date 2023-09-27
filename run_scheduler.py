from jobs.tasks import scheduler
from src.helper.log import setup_logging
if __name__ == '__main__':
    setup_logging()
    scheduler.start()
