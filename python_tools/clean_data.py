import pandas as pd
import re
from urllib.parse import unquote
import datetime

def obtain_city(url):
    'Decode city field'
    url = unquote(url)
    url_split = url.split('@')
    for item in url_split:
        if 'O=' in item:
            return item[2:]

def obtain_time(time):
    'If necessary decode time field'
    if '%' in time:
        return unquote(time)
    else:
        return time

# load data
with open('data') as file:
    raw_content = file.readlines()

# grab and clean request times
request_times = [re.match('^\[.*\]', el).group(0) for el in raw_content]
request_times = [datetime.datetime.strptime(el,'[%d/%b/%Y:%H:%M:%S]') for el in request_times]

# divide string by variable
split_content = [re.sub('^.*\?', '', el).split('&') for el in raw_content]

# load data to data frame
data_list = []
for i, line in enumerate(split_content):
    vars_values = [el.split('=') for el in line]
    current_dict = {current_var_value[0]: current_var_value[1] for current_var_value in vars_values}
    if 'originId' in current_dict:
        # decode url variables
        current_dict['originId'] = obtain_city(current_dict['originId'])
        current_dict['destId'] = obtain_city(current_dict['destId'])
        current_dict['time'] = obtain_time(current_dict['time'])
        # add request times
        current_dict['date_request'] = request_times[i].date().strftime('%Y-%m-%d')
        current_dict['time_request'] = request_times[i].time().strftime('%H:%M')
        # append values
        data_list.append(current_dict)

data = pd.DataFrame(data_list)

# extract and save variable names
with open('column_names.txt', 'w') as file_handler:
    file_handler.write('\n'.join(str(item) for item in data.columns))

# select only the necessary columns
data = data[['originId',
             'destId',
             'searchForArrival',
             'date',
             'time',
             'date_request',
             'time_request']]

# rename columns
data = data.rename({'originId': 'origin',
                    'destId': 'destination',
                    'searchForArrival': 'search_for_arrival',
                    'date': 'date_travel',
                    'time': 'time_travel'},
                   axis=1)

# save data frame to file
data[1:1000].to_csv('data.csv', index=False)
