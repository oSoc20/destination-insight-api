import pandas as pd
from reports import count_repetitions
import sys

# this is script will return a json table with the top or bottom stations by number of searches in origin or destination
# arg1: {'origin', 'destination'}
# arg2: {'top', 'bottom'}
# arg3: integer for number of rows to include

# read local data (for now)
data = pd.read_csv('data.csv')

# return requested table
result = count_repetitions(data, sys.argv[1], sys.argv[2], int(sys.argv[3]), return_json=True)
print(result)
sys.stdout.flush()