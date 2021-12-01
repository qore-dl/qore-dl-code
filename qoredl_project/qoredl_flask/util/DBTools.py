import math

def match_cpu(raw_data):
    matched_data = raw_data*10
    return matched_data

def match_memory(raw_data):
    matched_data = (raw_data/1024.)/1024.
    return matched_data

def match_timestamp(raw_data,tag):
    if tag == 's':
        match_data = math.ceil(raw_data)
    elif tag == 'ms':
        match_data = math.ceil(raw_data*1e3)
    else:
        match_data = math.ceil(raw_data*1e9)
    return match_data
