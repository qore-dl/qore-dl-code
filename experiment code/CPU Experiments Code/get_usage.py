import influxdb
import time
import pandas as pd
influx_client = influxdb.InfluxDBClient(host='192.168.128.10',port=8086,username='admin',password='admin',database="NODEMESSAGE")
try:
    result = influx_client.query(
        "select * from " + "NODEMESSAGE" + " group by nodes order by asc")
except Exception as ee:
    time.sleep(5)
    result = influx_client.query(
        "select * from " + "NODEMESSAGE" + " group by nodes order by asc")
# node_list = self.get_node_list()
# print(node_list)
result_keys = result.keys()
nodes = [i[-1]['nodes'] for i in result_keys]
if 'k8s-worker9' in nodes:
    nodes.remove('k8s-worker9')
# print(nodes)
# node_mg = [list(result[i]) for i in result_keys]
node_mg = []
for i in result_keys:
    if 'worker9' not in i[-1]['nodes']:
        node_mg.append(list(result[i]))
# print("load node mess sucess!")
print("node len is %d" % len(node_mg))
cpu_base = {}
memory_base = {}
cpu_pre_base = {}
mem_pre_base = {}

for i in range(len(node_mg)):
    cpu_base[nodes[i]] = {'time':[],'cpu':[]}
    memory_base[nodes[i]] = {'time':[],'mem':[]}
    cpu_pre_base[nodes[i]] = {'time':[],'cpupre':[]}
    mem_pre_base[nodes[i]] = {'time':[],'mempre':[]}
    print(len(node_mg))
    for j in range(len(node_mg[i])):
        cpu_base[nodes[i]]['time'].append(node_mg[i][j]['time'])
        cpu_base[nodes[i]]['cpu'].append(node_mg[i][j]['cpu'])
        memory_base[nodes[i]]['time'].append(node_mg[i][j]['time'])
        memory_base[nodes[i]]['mem'].append(node_mg[i][j]['memory'])

        cpu_pre_base[nodes[i]]['time'].append(node_mg[i][j]['time'])
        cpu_pre_base[nodes[i]]['cpupre'].append(node_mg[i][j]['cpu_percent'])
        mem_pre_base[nodes[i]]['time'].append(node_mg[i][j]['time'])
        mem_pre_base[nodes[i]]['mempre'].append(node_mg[i][j]['memory_percent'])

    cpuf = pd.DataFrame(cpu_base[nodes[i]])
    cpuf.to_csv('cpu' + '/' + '%s.csv' % nodes[i], mode='a+', index=False, sep=',')
    memf = pd.DataFrame(memory_base[nodes[i]])
    memf.to_csv('memory' + '/' + '%s.csv' % nodes[i], mode='a+', index=False, sep=',')
    mem_pref = pd.DataFrame(mem_pre_base[nodes[i]])
    mem_pref.to_csv('mem_pre' + '/' + '%s.csv' % nodes[i], mode='a+', index=False, sep=',')
    cpu_pref = pd.DataFrame(cpu_pre_base[nodes[i]])
    cpu_pref.to_csv('cpu_pre' + '/' + '%s.csv' % nodes[i], mode='a+', index=False, sep=',')



