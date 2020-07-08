import pandas as pd
from misc import count_links
import sys

# this is script will return a json table with the top or bottom station pairings by number of searches
# arg1: {'top', 'bottom'}
# arg2: integer for number of rows to include

# read local data (for now)
data = pd.read_csv('data.csv')

# return requested table
result = count_links(data, sys.argv[1], int(sys.argv[2]), return_json=True)
print(result)
sys.stdout.flush()