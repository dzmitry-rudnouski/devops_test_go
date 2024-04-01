# pass go-app url as an argument

# This script is enough for minimal monitoring, which later can be improved to prometheus/grafana.
# It can be added to linux crontab or used as AWS Lambda.
#
# It checks 3 metrics:
# - status code, should be 200
# - diff between healthcheck timestamp and current time, can't be more than 5 seconds
# - diff between 2 healthcheck timestamps, if it less than 5 (and not 0), it means redis is not working

import sys
import requests
from datetime import datetime, timezone
import time

def send_alert():
    # send alert here: email, notification to chat, etc
    pass

def get_heartbeat(url):
    response_heartbeat = requests.request("GET", url)
    if response_heartbeat.status_code != 200:
        send_alert()
        raise Exception("Go-app is not available, http status: " + response_heartbeat.status_code)
    return response_heartbeat.text.split('=')[1].strip()

heartbeat_datetime = get_heartbeat(sys.argv[1])
heartbeat_datetime_sec = int(datetime.strptime(heartbeat_datetime, '%Y-%m-%d %I:%M:%S').replace(tzinfo=timezone.utc).timestamp())
current_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%d %I:%M:%S')
current_datetime_sec = int(datetime.strptime(current_datetime, '%Y-%m-%d %I:%M:%S').replace(tzinfo=timezone.utc).timestamp())

if current_datetime_sec - heartbeat_datetime_sec > 5:
    send_alert()
    raise Exception("Go-app timestamp is too old: " + heartbeat_datetime)

time.sleep(3)

heartbeat_datetime_2 = get_heartbeat(sys.argv[1])
heartbeat_datetime_2_sec = int(datetime.strptime(heartbeat_datetime_2, '%Y-%m-%d %I:%M:%S').replace(tzinfo=timezone.utc).timestamp())

if (heartbeat_datetime_2_sec - heartbeat_datetime_sec) in [1, 2, 3, 4]:
    send_alert()
    raise Exception("Redis doesn't work correctly")
