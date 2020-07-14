import pandas as pd
import re
import datetime
import mysql.connector
import sys
from misc import obtain_city
from misc import obtain_time

# this is script will check if the file has already been uploaded, clean the data, and upload it
# arg1: name of the file to upload

def clean_upload_data(file_name):
    'Takes the file name of a text file with the original data, cleans it, and uploads it to the database'

    # connect to database
    db = mysql.connector.connect(
        host="db4free.net",
        user="nmbstest",
        password="nmbsRoutePlannerDataAnalysis"
    )

    curs = db.cursor()
    curs.execute("USE routeplannerdata")
    curs.execute('select file_name from files')
    previous_file_names = curs.fetchall()
    previous_file_names = [item[0] for item in previous_file_names]

    # check if file has already been uploaded
    if file_name in previous_file_names:
        print('File has already been uploaded.')
        return
    else:
        print('Processing file.')

    # load data
    with open(file_name) as file:
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

    # select only the necessary columns
    data = data[['originId',
                 'destId',
                 'searchForArrival',
                 'date',
                 'time',
                 'date_request',
                 'time_request'
                 # 'numF',
                 # 'numB'
                 ]]

    # rename columns
    data = data.rename({'originId': 'origin',
                        'destId': 'destination',
                        'searchForArrival': 'search_for_arrival',
                        'date': 'date_travel',
                        'time': 'time_travel'},
                       axis=1)

    # save csv
    data.to_csv(file_name + '_clean.csv', index=False)

    # update file table
    curs.execute("insert into files (file_name) values (%s)",
                 (file_name, ))


    # update searches table
    curs.execute("USE routeplannerdata")

    values = data.values.tolist()
    curs.executemany('insert into searches (origin, destination, search_for_arrival, date_travel, time_travel, date_request, time_request) values (%s, %s, %s, %s, %s, %s, %s)',
                     values)
    db.commit()
    db.close()


clean_upload_data(sys.argv[1])
