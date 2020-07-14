from reports import count_repetitions
import sys

# this is script will return a json table with the top or bottom stations by number of searches in origin or destination
# arg1: station type {'origin', 'destination'}
# arg2: start date, inclusive (YYYY-MM-DD)
# arg3: end date, inclusive (YYYY-MM-DD)
# arg4: date type {'travel', 'request'}
# arg5: most or least common stations {'top', 'bottom'}
# arg6: integer for number of rows to include

# command example: python count_repetitions.py origin 2020-05-13 2020-05-14 travel top 10


result = count_repetitions(column=sys.argv[1],
                           start=sys.argv[2],
                           end=sys.argv[3],
                           date_type=sys.argv[4],
                           side=sys.argv[5],
                           quantity=int(sys.argv[6]),
                           return_json=True)
print(result)
sys.stdout.flush()