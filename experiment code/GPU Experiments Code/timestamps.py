import os

from pytz import UTC
from dateutil.parser import parse

from datetime import datetime

EPOCH = UTC.localize(datetime.utcfromtimestamp(0))
print(datetime.utcfromtimestamp(0))
t = "2020-01-21T8:23:51Z"
print(t)
timestamp = parse(t)
print(EPOCH)
print(timestamp)
if not timestamp.tzinfo:
    print("XXX")
    timestamp = UTC.localize(timestamp)

s = (timestamp - EPOCH).total_seconds()
print(s)
print(int(1579594991*1e9))

os.system('date -d @' + str(int(1579594991)) + ' "+%Y-%m-%dT%H:%M:%SZ"')