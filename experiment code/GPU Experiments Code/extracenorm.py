import influxdb
from wenjianjihe import load_config,save_config
import kubernetes
import timestamps
import os

from pytz import UTC
from dateutil.parser import parse

from datetime import datetime

EPOCH = UTC.localize(datetime.utcfromtimestamp(0))


client = influxdb.InfluxDBClient(host='172.16.190.97',port=8086,username='admin',password='admin',database='PREDICT')

system = load_config('system_info.json')
aim_job = system['finish'][:]
aim_json = {}
for i in aim_job:
    pre_list = i.split('-')
    result_dict = {}
    measure = pre_list[0].upper()+'P'+pre_list[1]
    print(measure)
    result = client.query("select * from " + measure + " group by nodes order by asc")
    result_key = list(result.keys())
    for k in result_key:
        result_dict[k[-1]['nodes']] = []
        tmp_result = list(result[k])
        for j in tmp_result:
            j['time0'] = (parse(j['time']) - EPOCH).total_seconds()
        result_dict[k[-1]['nodes']] = list(tmp_result)
    save_config(result_dict, 'PROCESS/%s.json' % measure)





