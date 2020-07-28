from funcs.reports import searches_by_hour
import sys
import json
import numpy as np
# this is script will return a json with the amount of searches by hour and day of the week (total)
# arg1: start date, inclusive (YYYY-MM-DD)
# arg2: end date, inclusive (YYYY-MM-DD)
# arg3: date type {'travel', 'request'}

# command example: python searches_by_hour.py 2020-01-01 2021-01-01 travel

def convert(o):
    if isinstance(o, np.int64): return int(o)
    raise TypeError

# return requested table
result = searches_by_hour(start=sys.argv[1],
                          end=sys.argv[2],
                          time_type=sys.argv[3])

print(json.dumps(result, default=convert))
sys.stdout.flush()
