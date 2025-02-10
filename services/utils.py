from datetime import datetime

def timestamp2datetime(timestamp):
    try:
        timestamp = int(timestamp)
        if timestamp == 0:
            return None
        else:
            return datetime.fromtimestamp(timestamp / 1000)
    except BaseException as e:
        return None