from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import register_jobs
from scheduler.jobstores import jobstores
from scheduler.executors import executors

import logging
import time

logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
    register_jobs(scheduler)
    scheduler.start()
    while True:
        time.sleep(1)
