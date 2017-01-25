from datetime import datetime
import time

RECIPIENTS = ['nico@nischwan.de']

def get_local_time():
    return datetime.fromtimestamp(time.mktime(time.localtime()))
