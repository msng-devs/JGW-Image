from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import create_engine
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from src.core.config import Config
from jobs.data_job import clear_not_exist_img_task
from src.helper.path import get_absolute_path

config = Config()
engine = create_engine(f"sqlite:///{get_absolute_path(['data', 'jobs.db'])}")
job_store = {
    "default": SQLAlchemyJobStore(engine=engine)
}
scheduler = BlockingScheduler(job_store=job_store)

scheduler.add_job(clear_not_exist_img_task, "cron", hour=config.CLEAR_TRASH_TIME[0], minute=config.CLEAR_TRASH_TIME[1],
                  second=config.CLEAR_TRASH_TIME[2])
