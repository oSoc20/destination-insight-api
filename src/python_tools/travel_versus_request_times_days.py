from reports import travel_versus_request_times_days
import sys

# this is script will return a json with the difference in days between the request and the travel times
# the last bin includes all the searches with differences equal or greater than 30
# searches for travels BEFORE the request time are ignored
# arg1: start date, inclusive (YYYY-MM-DD)
# arg2: end date, inclusive (YYYY-MM-DD)
# arg3: date type {'travel', 'request'}

# command example: python travel_versus_request_times.py 2020-05-13 2020-05-14 travel

result = travel_versus_request_times_days(start=sys.argv[1],
                                          end=sys.argv[2],
                                          date_type=sys.argv[3],
                                          draw_plot=False,
                                          return_json=True)
print(result)
sys.stdout.flush()
