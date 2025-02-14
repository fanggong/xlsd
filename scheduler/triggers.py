from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta

def get_trigger():
    return IntervalTrigger(seconds=5)

def get_ten_minute_trigger():
    trigger = CronTrigger(minute='10,20,30,40,50,00')  # 每小时的 10, 20, 30, 40, 50, 00 分触发
    return trigger