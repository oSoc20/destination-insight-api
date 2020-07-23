import pandas as pd
import re
import datetime
import mysql.connector
from os import listdir, remove
from os.path import isfile, join, splitext, basename
import zipfile

from funcs.misc import obtain_city
from funcs.misc import obtain_time

def clean_upload_data(directory, file_name, stations, save_clean = False, small_test = False):
    """Takes the file name of a text file with the original data, cleans it, and uploads it to the database"""

    # print file name
    print('File to process: ' + file_name)

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
    ext = splitext(basename(file_name))[1]
    file_name = splitext(basename(file_name))[0]
    if file_name in previous_file_names:
        print('File has already been uploaded.')
        print('=' * 80)
        curs.close()
        db.close()
        return
    else:
        print('Processing file.')

    # unzip if necessary
    if ext == '.zip':
        full_name = join(directory, file_name + ext, )
        with zipfile.ZipFile(full_name, 'r') as zip_ref:
            zip_ref.extractall(directory)
        current_full_path = join(directory, 'tmp', file_name)
    else:
        current_full_path = join(directory, file_name)

    # load data
    with open(current_full_path) as file:
        raw_content = file.readlines()

    # only upload a few linens
    if small_test:
        raw_content = raw_content[1:200]

    # remove unzipped file
    if ext == '.zip':
        remove(current_full_path)

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
            current_dict['originId'] = obtain_city(current_dict['originId'], stations)
            current_dict['destId'] = obtain_city(current_dict['destId'], stations)
            current_dict['time'] = obtain_time(current_dict['time'])

            # add request times
            current_dict['date_request'] = request_times[i].date().strftime('%Y-%m-%d')
            current_dict['time_request'] = request_times[i].time().strftime('%H:%M')

            # append values
            data_list.append(current_dict)

    data = pd.DataFrame(data_list)

    # check that at least 1 valid row was found in the file
    if data.empty:
        print('No valid rows found in file.')
    else:
        # only keep the necessary columns
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

        # save csv and print snippet
        if save_clean:
            data.to_csv(current_full_path + '_clean.csv', index=False)
        print(data)

        # update file table
        curs.execute("insert into files (file_name) values (%s)",
                     (file_name, ))

        # update searches table
        curs.execute("USE routeplannerdata")

        values = data.values.tolist()
        curs.executemany('insert into searches (origin, destination, search_for_arrival, date_travel, time_travel, date_request, time_request) values (%s, %s, %s, %s, %s, %s, %s)',
                         values)
        db.commit()

        # close connection to database
        curs.close()
        db.close()

        print('File uploaded.')

    print('='*80)

def upload_many(directory, stations, small_test = False):
    """Upload all files (zip) in a directory to the database"""

    # detect all files directory
    file_names = [item for item in listdir(directory) if isfile(join(directory, item))]

    # for each file extract it, upload it, and remove temporary file
    for i,item in enumerate(file_names):
        clean_upload_data(directory, item, stations, small_test = small_test)
