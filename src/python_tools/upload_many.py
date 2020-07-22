import sys
import pandas as pd
from funcs.clean_data import upload_many

# this script will check and upload all files in the directory
# arg1: name of the directory

stations = pd.read_csv('data/stations.csv')
upload_many(sys.argv[1], stations, small_test = True)
