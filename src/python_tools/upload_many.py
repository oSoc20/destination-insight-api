import sys
from clean_data import upload_many

# this script will check and upload all files in the directory
# arg1: name of the directory

upload_many(sys.argv[1], small_test = True)

