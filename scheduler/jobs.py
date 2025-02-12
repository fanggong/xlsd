from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.triggers import get_trigger
from tasks.sync_ods_cps_order import sync_ods_cps_order
from datetime import datetime, timedelta

import time


def register_jobs(scheduler: BackgroundScheduler):
    scheduler.add_job(
        sync_ods_cps_order, 
        id='sync_ods_cps_order',
        trigger=get_trigger(),
        executor='processpool',
        jobstore='default',
        max_instances=10, 
        replace_existing=True
    )