import pandas as pd
from reports import missing_days
import sys

# this is script will return a json with the days for which there is no data in the database
# arg1: start date (request), inclusive (YYYY-MM-DD)
# arg2: end date (request), inclusive (YYYY-MM-DD)

# command example: python missing_days.py 2020-01-01 2021-01-01

# return requested table
result = missing_days(start=sys.argv[1],
                      end=sys.argv[2])

print(result)
sys.stdout.flush()
