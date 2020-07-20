import pandas as pd
from reports import searches_by_time
import sys

# this is script will return a json table with the top or bottom station pairings by number of searches
# arg1: start date, inclusive (YYYY-MM-DD)
# arg2: end date, inclusive (YYYY-MM-DD)
# arg3: date type {'travel', 'request'}
# arg4: aggregate by day, month or year {'D', 'M', 'Y'}

# command example: python searches_by_time.py 2020-01-01 2021-01-01 travel M

# return requested table
result = searches_by_time(start=sys.argv[1],
                          end=sys.argv[2],
                          date_type=sys.argv[3],
                          aggregation=sys.argv[4])

print(result)
sys.stdout.flush()
