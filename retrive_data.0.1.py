#!/usr/bin/python3
"""
get data from remote monitoring raspberry; crontab activated
"""

import os
from urllib.request import urlretrieve

SERVER_PATH = '192.168.3.180/aurora/aurora-log.csv'
DATA_FILE = 'aurora-log.csv'
LOGIN_DATA = 'pi:xk2006b'

# Import data from raspberry monitor device
def retrive_data():
    dest_filepath = os.path.join('./', DATA_FILE)
    urlretrieve('ftp://' + LOGIN_DATA + '@' + SERVER_PATH, dest_filepath)

if __name__ == '__main__':
    retrive_data()

