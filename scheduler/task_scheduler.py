from scheduler.tasks.sync_ods_cps_order import sync_ods_cps_order
from scheduler.job_runner import run_job

import schedule
import time
import logging

logger = logging.getLogger(__name__)


def start_scheduler():
    schedule.every(2).hours.do(run_job, sync_ods_cps_order)

    logger.info('Scheduler started...')
    while True:
        schedule.run_pending()
        time.sleep(1)
