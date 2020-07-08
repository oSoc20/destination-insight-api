import pandas as pd
import re
from urllib.parse import unquote

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

# grab request times
request_times = [re.match('^\[.*\]', el).group(0) for el in raw_content]

# divide string by variable
split_content = [re.sub('^.*\?', '', el).split('&') for el in raw_content]

# load data to data frame
data_list = []
for i, line in enumerate(split_content):
    vars_values = [el.split('=') for el in line]
    current_dict = {current_var_value[0]: current_var_value[1] for current_var_value in vars_values}
    if i == 1:
        print(current_dict)
    if 'originId' in current_dict:
        # decode url variables
        current_dict['originId'] = obtain_city(current_dict['originId'])
        current_dict['destId'] = obtain_city(current_dict['destId'])
        current_dict['time'] = obtain_time(current_dict['time'])
        # append values
        current_dict.update({'requestTime': request_times[i]})
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
             'time']]

# rename columns
data = data.rename({'originId': 'origin',
                    'destId': 'destination',
                    'searchForArrival': 'search_for_arrival',
                    'date': 'date_travel',
                    'time': 'time_travel'},
                   axis=1)

# save data frame to file
data.to_csv('data.csv', index=False)
