import influxdb
import pandas as pd
client = influxdb.InfluxDBClient('192.168.128.10',port=8086,username='admin',password='admin',database="MONITOR")
result = client.query("select * from RER where time > 1580976233000000000 group by task order by asc")
result_keys = result.keys()
task_mg = [list(result[i]) for i in result_keys]
data_frame = {}
keyss = task_mg[0][0].keys()
key_list = list(keyss)
print(key_list)
for key in key_list:
    data_frame[key] = []

for i in task_mg:
    for j in i:
        for key in j.keys():
            tmp = data_frame[key]
            tmp.append(j[key])
            data_frame[key] = tmp

print(len(data_frame['batch_size']))
dataframe = pd.DataFrame(data_frame)
dataframe.to_csv('/tfdata/resource2/re_test.csv', mode='w+', index=False, sep=',')
client = influxdb.InfluxDBClient('192.168.128.10',port=8086,username='admin',password='admin',database="MONITOR")
result = client.query("select * from RESR where time > 1580976233000000000 group by task order by asc")
result_keys = result.keys()
task_mg = [list(result[i]) for i in result_keys]
data_frame = {}
keyss = task_mg[0][0].keys()
key_list = list(keyss)
print(key_list)
for key in key_list:
    data_frame[key] = []

for i in task_mg:
    for j in i:
        for key in j.keys():
            tmp = data_frame[key]
            tmp.append(j[key])
            data_frame[key] = tmp

print(len(data_frame['batch_size']))
dataframe = pd.DataFrame(data_frame)
dataframe.to_csv('/tfdata/resource2/res_test.csv', mode='w+', index=False, sep=',')
client = influxdb.InfluxDBClient('192.168.128.10',port=8086,username='admin',password='admin',database="MONITOR")
result = client.query("select * from VGGR where time > 1580976233000000000 group by task order by asc")
result_keys = result.keys()
task_mg = [list(result[i]) for i in result_keys]
data_frame = {}
keyss = task_mg[0][0].keys()
key_list = list(keyss)
print(key_list)
for key in key_list:
    data_frame[key] = []

for i in task_mg:
    for j in i:
        for key in j.keys():
            tmp = data_frame[key]
            tmp.append(j[key])
            data_frame[key] = tmp

print(len(data_frame['batch_size']))
dataframe = pd.DataFrame(data_frame)
dataframe.to_csv('/tfdata/resource2/vgg_test.csv', mode='w+', index=False, sep=',')

client = influxdb.InfluxDBClient('192.168.128.10',port=8086,username='admin',password='admin',database="MONITOR")
result = client.query("select * from XCER where time > 1580976233000000000 group by task order by asc")
result_keys = result.keys()
task_mg = [list(result[i]) for i in result_keys]
data_frame = {}
keyss = task_mg[0][0].keys()
key_list = list(keyss)
print(key_list)
for key in key_list:
    data_frame[key] = []

for i in task_mg:
    for j in i:
        for key in j.keys():
            tmp = data_frame[key]
            tmp.append(j[key])
            data_frame[key] = tmp

print(len(data_frame['batch_size']))
dataframe = pd.DataFrame(data_frame)
dataframe.to_csv('/tfdata/resource2/xce_test.csv', mode='w+', index=False, sep=',')





