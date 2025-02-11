from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

executors = {
    'default': ThreadPoolExecutor(max_workers=10),
    'processpool': ProcessPoolExecutor(max_workers=5)
}
