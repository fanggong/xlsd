from apscheduler.triggers.interval import IntervalTrigger

def get_trigger():
    return IntervalTrigger(seconds=10)
