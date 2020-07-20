import pandas as pd
from reports import count_links
import sys

# this is script will return a json table with the top or bottom station pairings by number of searches
# arg1: start date, inclusive (YYYY-MM-DD)
# arg2: end date, inclusive (YYYY-MM-DD)
# arg3: date type {'travel', 'request'}
# arg4: most or least common stations {'top', 'bottom'}
# arg5: integer for number of rows to include

# command example: python count_links.py 2020-05-13 2020-05-14 travel top 10

result = count_links(start=sys.argv[1],
                     end=sys.argv[2],
                     date_type=sys.argv[3],
                     side=sys.argv[4],
                     quantity=int(sys.argv[5]),
                     return_json=True)

print(result)
sys.stdout.flush()
