# utils.py

import os
import datetime

def get_file_size_category(file_path):
    size = os.path.getsize(file_path)
    if size < 1_000_000:
        return 'Small'
    elif size < 10_000_000:
        return 'Medium'
    else:
        return 'Large'

def get_file_modified_date(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m')
