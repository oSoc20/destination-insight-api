import sys
from clean_data import clean_upload_data

# this script will check if the file has already been uploaded, clean the data, and upload it
# arg1: name of the directory that contains the file
# arg2: name of the file to upload

clean_upload_data(sys.argv[1], sys.argv[2], small_test = True)
