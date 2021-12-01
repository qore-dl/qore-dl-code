from Global_client import Global_Influx
import math
def database_create(databasename):
    database_list = Global_Influx.Client_all.get_list_database()
    creating = True
    for db in database_list:
        dbl = list(db.values())
        if databasename in dbl:
            creating = False
            break
    if creating:
        Global_Influx.Client_all.create_database(databasename)

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
