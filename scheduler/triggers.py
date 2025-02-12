from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta

def get_trigger():
    return IntervalTrigger(seconds=5)
