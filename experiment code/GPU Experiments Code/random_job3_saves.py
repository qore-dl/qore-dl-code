import task_submit
from task_submit import VGGTask,RESTask,RETask,DENTask,XCETask
import random
import kubernetes
import influxdb
import kubernetes
import yaml
import requests
from multiprocessing import Process
import multiprocessing
import urllib
import urllib3
import time
import numpy as np
np.set_printoptions(suppress=True)        #设置print选项的参数
import os
import json
import math
import pandas as pd
import argparse
import random
import multiprocessing
import time
from pytz import UTC
from dateutil import parser
from datetime import datetime
import psutil
import socket
from max_heap import MaxHeap
import worker_queue
# from worker_queue import value_free_load,value_weight_load
from Global_client import Global_Influx
aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
aTokenw = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
LOSSHOST = '192.168.128.21'
LOSSPORT = 12527
def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/tfdata/nodedata', help='save path')
    parser.add_argument('--database',default="NODEMESSAGE",help="save database")
    parser.add_argument('--derivation',default=10,help='sampling rate')
    parser.add_argument('--measurement',default="NODEMESSAGE",help="save measurement")
    # parser.add_argument('--train_pg', action='store_true', help='whether train policy gradient')
    # parser.add_argument('--train_dqn', action='store_true', help='whether train DQN')
    # parser.add_argument('--test_pg', action='store_true', help='whether test policy gradient')
    # parser.add_argument('--test_dqn', action='store_true', help='whether test DQN')

    args = parser.parse_args()
    return args

def update_token():
    cacheData = os.popen(
        "echo $(kubectl describe secret $(kubectl get secret -n kube-system | grep ^admin-user | awk '{print $1}') -n kube-system | grep -E '^token'| awk '{print $2}')").read()
    cacheToken = cacheData[:-1]
    newToken = str(cacheToken)

    return newToken

def make_headers(Token):
    text = 'Bearer ' + Token
    headers = {'Authorization': text}
    return headers

def catch_message(url):
    global aToken

    aToken = update_token()
    headers = make_headers(aToken)

    response = requests.get(url,headers=headers,verify=False)
    res_json = response.json()
    return res_json

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

    # Global_Influx.Client_all.create_database(databasename)


def match_cpu(raw_data):
    cache = raw_data[:-1]
    matched_data = math.ceil(int(cache)/1e6)
    return matched_data

def match_memory(raw_data):
    cache = raw_data[:-2]
    matched_data = math.ceil(int(cache)/1024)
    return matched_data

def match_timestamp(raw_data):
    EPOCH = UTC.localize(datetime.utcfromtimestamp(0))
    timestamp = parser.parse(raw_data)
    if not timestamp.tzinfo:
        print("XXX")
        timestamp = UTC.localize(timestamp)

    s = (timestamp - EPOCH).total_seconds()
    return int(s)



def generate_item(response,measurement):
    node_cpu = {}
    node_cpu['k8s-master'] = 32000
    node_cpu['k8s-worker0'] = 24000
    node_cpu['k8s-worker2'] = 24000
    node_cpu['k8sworker1'] = 16000
    node_cpu['k8s-worker3'] = 24000
    node_cpu['k8s-worker4'] = 16000
    node_cpu['k8s-worker5'] = 24000
    node_memory = {}
    node_memory['k8s-master'] = float(251 * 1024)
    node_memory['k8s-worker0'] = float(94 * 1024)
    node_memory['k8s-worker2'] = float(94 * 1024)
    node_memory['k8sworker1'] = float(125 * 1024)
    node_memory['k8s-worker3'] = float(94 * 1024)
    node_memory['k8s-worker4'] = float(125 * 1024)
    node_memory['k8s-worker5'] = float(94 * 1024)
    points = []
    # content = {}
    timestamp = response['items'][0]['metadata']['creationTimestamp']
    for item in response['items']:
        content = {
            'measurement': measurement,
            'tags':{
                "nodes": item['metadata']['name']
            },
            'fields': {
                'cpu': match_cpu(item['usage']['cpu']),
                'memory': match_memory(item['usage']['memory']),
                'cpu_percent': float(match_cpu(item['usage']['cpu'])/node_cpu[item['metadata']['name']]),
                'memory_percent': float(match_memory(item['usage']['memory']) / node_memory[item['metadata']['name']])
            },
            'time': match_timestamp(timestamp)
        }
        points.append(content)
    return points


def DeletefromDB(Client,DatabaseName):
    databases = Client.get_list_database()
    for Cn in databases:
        if DatabaseName in Cn.values():
            Client.drop_database(DatabaseName)
            break


class Node_mess(multiprocessing.Process):
    def __init__(self,url,args,tasks,v1):
        multiprocessing.Process.__init__(self)
        self.url = url
        self.args = args
        self.derivation = args.derivation
        self.time_mess = {}
        self.cpu_mess = {}
        self.memory_mess = {}
        self.cpu_per = {}
        self.memory_per = {}
        self.node_cpu = {}
        self.node_cpu['k8s-master'] = 32000
        self.node_cpu['k8s-worker0'] = 24000
        self.node_cpu['k8s-worker2'] = 24000
        self.node_cpu['k8sworker1'] = 16000
        self.node_cpu['k8s-worker3'] = 24000
        self.node_cpu['k8s-worker4'] = 16000
        self.node_cpu['k8s-worker5'] = 24000
        self.node_memory = {}
        self.node_memory['k8s-master'] = float(251 * 1024)
        self.node_memory['k8s-worker0'] = float(94 * 1024)
        self.node_memory['k8s-worker2'] = float(94 * 1024)
        self.node_memory['k8sworker1'] = float(125 * 1024)
        self.node_memory['k8s-worker3'] = float(94 * 1024)
        self.node_memory['k8s-worker4'] = float(125 * 1024)
        self.node_memory['k8s-worker5'] = float(94 * 1024)
        # self.derivation = derivation
        self.arg = args
        self.tasks = tasks
        self.v1 = v1
        self.database = args.database
        self.measurement = args.measurement
        self.save_path = args.save_path
        if not os.path.exists(self.arg.save_path):
            os.makedirs(self.arg.save_path)
        database_create(self.database)
        self.client = influxdb.InfluxDBClient('192.168.128.10',port=8086,username='admin',password='admin',database=self.database)
        #derivation
    # def node_measurement(self,node_list):
    #     # Global_Influx.Client_all.get_list_measurements()


    def run(self):
        print(multiprocessing.current_process().pid)
        print(os.getpid())
        response = catch_message(self.url)
        self.time_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
        self.cpu_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
        self.memory_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
        self.cpu_per['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
        self.memory_per['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
        for item in response['items']:
            self.time_mess[item['metadata']['name']] = [item['timestamp']]
            self.cpu_mess[item['metadata']['name']] = [match_cpu(item['usage']['cpu'])]
            self.memory_mess[item['metadata']['name']] = [match_memory(item['usage']['memory'])]
            self.cpu_per[item['metadata']['name']] = [float(match_cpu(item['usage']['cpu'])/self.node_cpu[item['metadata']['name']])]
            self.memory_per[item['metadata']['name']] = [float(match_memory(item['usage']['memory']) / self.node_memory[item['metadata']['name']])]
        self.client.write_points(generate_item(response,self.measurement),'s',database=self.database)

        time.sleep(self.derivation)
        while True:
            response = catch_message(self.url)
            self.time_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            self.cpu_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            self.memory_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            self.cpu_per['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            self.memory_per['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            for item in response['items']:
                self.time_mess[item['metadata']['name']].append(item['timestamp'])
                self.cpu_mess[item['metadata']['name']].append(match_cpu(item['usage']['cpu']))
                self.memory_mess[item['metadata']['name']].append(match_memory(item['usage']['memory']))
                self.cpu_per[item['metadata']['name']].append(float(match_cpu(item['usage']['cpu'])/self.node_cpu[item['metadata']['name']]))
                self.memory_per[item['metadata']['name']].append(float(match_memory(item['usage']['memory']) / self.node_memory[item['metadata']['name']]))
            self.client.write_points(generate_item(response, self.measurement), 's', database=self.database)
            if len(self.time_mess['creation'])%30==0 and len(self.time_mess['creation']) > 0:
                data_frame = pd.DataFrame(self.time_mess)
                data_frame.to_csv(self.save_path + '/' + 'struct.csv', mode='a+', index=False, sep=',')
                print(self.cpu_mess)
                print(len(self.cpu_mess))
                for keyss in self.cpu_mess:
                    print(keyss+": "+str(len(self.cpu_mess[keyss])))
                data_frame2 = pd.DataFrame(self.cpu_mess)
                data_frame2.to_csv(self.save_path + '/' + 'node_cpu.csv', mode='a+', index=False, sep=',')
                data_frame3 = pd.DataFrame(self.memory_mess)
                data_frame3.to_csv(self.save_path + '/' + 'node_memory.csv', mode='a+', index=False, sep=',')
                data_frame4 = pd.DataFrame(self.cpu_per)
                data_frame4.to_csv(self.save_path + '/' + 'node_cpu_per.csv', mode='a+', index=False, sep=',')
                data_frame5 = pd.DataFrame(self.memory_per)
                data_frame5.to_csv(self.save_path + '/' + 'node_memory_per.csv', mode='a+', index=False, sep=',')
                f1 = open('/tfdata/nodedata/node.json', 'r', encoding='utf-8')
                res = f1.read()
                a = json.loads(res)
                f1.close()
                node_layout = {}
                node_list = [i.metadata.name for i in self.v1.list_node().items]
                for node in node_list:
                    node_layout[node] = []
                for ns in tasks['ns']:
                    tmp_layout = tasks['nslayout']
                    if tmp_layout[ns]:
                        pod_list = [i for i in self.v1.list_namespaced_pod(ns).items]
                        for pod in pod_list:
                            try:
                                node_layout[pod.spec.node_name].append(pod.metadata.name)
                            except Exception as e0:
                                print(e0)
                a.append(node_layout)
                f2 = open('/tfdata/nodedata/node.json', 'w', encoding='utf-8')
                node_json = json.dumps(a, ensure_ascii=False, indent=4)  # list转成json，字典转成字符串
                f2.write(node_json)
                f2.close()
                for key in self.time_mess:
                    self.time_mess[key] = []
                    self.cpu_mess[key] = []
                    self.memory_mess[key] = []
                    self.memory_per[key] = []
                    self.cpu_per[key] = []
            time.sleep(self.derivation)


def get_ns(v1):
        ns_list = []
        for i in v1.list_namespace().items:
            ns_list.append(i.metadata.name)
        return ns_list

# def get_layout():

def Monitor_job(tasks,lock,v1,jobs):
    time.sleep(10)
    while True:
        if tasks['start'] == False:
            break
        ns_list = get_ns(v1)
        print(ns_list)
        if tasks['start'] == True and tasks['count'] == 0:
            time.sleep(30)
            pass
        else:
            for ns in tasks['ns']:
                print(ns+'If in list:'+str(ns in ns_list))
                if ns not in ns_list:
                    try_times = 10
                    while try_times > 0:
                        time.sleep(float(random.randint(5, 10)))
                        if ns in ns_list:
                            break
                        try_times=try_times-1
                    if try_times <=0 :
                        lock.acquire()
                        ns_tmp = tasks['ns']
                        ns_tmp.remove(ns)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        is_layout.pop(ns)
                        tasks['nslayout'] = is_layout
                        count_tmp = len(ns_tmp)
                        tasks['count'] = count_tmp
                        lock.release()
                else:
                    # print(b[0].status.container_statuses[0].state.terminated.reason)
                    pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                    # if 'Running' in pod_status:
                    #
                    #     time.sleep(5)
                    #     lock.acquire()
                    #     print("Select the loayout!")
                    #     tmp_layout = tasks['nslayout']
                    #     tmp_keys = list(tmp_layout.keys())
                    #     if ns in tmp_keys and tmp_layout[ns]==False:
                    #         tmp_layout_config = {}
                    #         for i in v1.list_namespaced_pod(ns).items:
                    #             tmp_layout_config[i.metadata.name] = i.spec.node_name
                    #         fp = open('/tfdata/k8snfs/'+ns+'/layout.json', 'w', encoding='utf-8')
                    #         # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    #         dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    #         fp.write(dicc_json)
                    #         fp.close()
                    #         tmp_layout[ns] = True
                    #         tasks['nslayout'] = tmp_layout
                    #     lock.release()
                    if 'Succeeded' in pod_status or 'Failed' in pod_status:
                        # # print(b[0].status.container_statuses[0].state.terminated.reason)
                        # pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                        # ['OOMKilled']
                        time.sleep(15)
                        try:
                            exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                                           v1.list_namespaced_pod(ns).items]
                            print(exit_reason)
                            exit_ict = {'reasons': exit_reason}
                            exit_path = '/tfdata/k8snfs/%s/exit_reason.json' % ns
                            exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                            fw_exit = open(exit_path, 'w', encoding='utf-8')
                            fw_exit.write(exit_json)
                            fw_exit.close()
                        except Exception as e:
                            print(e)
                        time.sleep(10)
                        lock.acquire()
                        # job_tmp = tasks['job']
                        # job = job_tmp[ns]
                        # job.delete_tf()
                        # command = 'kubectl delete -f /tfdata/tfcnn/expjob/'+ns+'.yaml'
                        command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + ns + '.yaml'
                        os.system(command)
                        v1.delete_namespace(ns)
                        ns_tmp = tasks['ns']
                        ns_tmp.remove(ns)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        is_layout.pop(ns)
                        for i in range(len(jobs)):
                            if jobs[i] == ns:
                                jobs.pop(i)
                                break
                        tasks['nslayout'] = is_layout
                        # job_tmp.pop(ns)
                        # tasks['job'] = job_tmp
                        tasks['count'] -= 1
                        lock.release()
                    time.sleep(5)

def make_time_query(time_base,mode=0):
    if mode == 0:
        time_query = (math.floor(time_base-1))
        time_query_str = str(time_query)+'000000000'
    else:
        time_query = (math.ceil(time_base+1))
        time_query_str = str(time_query)+'000000000'
    return time_query_str





def catch_node_step_msg(jobs,job_name,tasks,lock,batch,flops,params,mode):
    node_influx_client = influxdb.InfluxDBClient(host='192.168.128.10',username='admin',password='admin',database='NODEMESSAGE')
    step_influx_client = influxdb.InfluxDBClient(host='192.168.128.10',username='admin',password='admin',database='PREDICT')
    jieshu = False
    lock.acquire()
    for jo in jobs:
        if jo == job_name:
            job = reload_jobs(job_name,-1)
            print('reload job success!')
            break
    lock.release()
    count = 0
    while True:
        pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
        run_result = pd.value_counts(pod_status)
        run_result_dict = dict(run_result)
        print(run_result_dict)
        if 'Running' in pod_status and run_result_dict['Running'] == (job.ps_replicas + job.worker_replicas):
            time.sleep(10)
            lock.acquire()
            print("Select the loayout!")
            tmp_layout = tasks['nslayout']
            tmp_keys = list(tmp_layout.keys())
            if job_name in tmp_keys and tmp_layout[job_name] == False:
                tmp_layout_config = {}
                for i in job.v1.list_namespaced_pod(job_name).items:
                    tmp_layout_config[i.metadata.name] = i.spec.node_name
                fp = open('/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                fp.write(dicc_json)
                fp.close()
                tmp_layout[job_name] = True
                tasks['nslayout'] = tmp_layout
            lock.release()
            break
        elif 'Succeeded' in pod_status or 'Failed' in pod_status:
            jieshu = True
            print("Exception exit! Pending Problem!")
            return
        elif not run_result_dict:
            if count > 10:
                jieshu = True
                print("Exception exit! Creating Problem!")
                return
            count+=1
            time.sleep(30)
        else:
            time.sleep(30)

    job_measure = job.measure
    print("job measure: %s" % job.measure)
    pre_list = job_measure.split(' ')
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_load = pre_list[0]+'L'+pre_list[-1]
    ns_name = job.name
    tmp_creation = tasks['creation'][:]
    if mode < 0:
        time_base = tasks['creation'][-1]
    else:
        time_base = tasks['creation'][-1]
    # time_avg = []
    ns_layout = {}
    # worker_num = 0

    while True:
        lock.acquire()
        tmp_layout = tasks["nslayout"]
        lock.release()
        print("Get the layout config!")
        if jieshu:
            break
        if tmp_layout[ns_name]:
            layout_file = '/tfdata/k8snfs/%s/layout.json' % ns_name
            layout_dict = load_config(layout_file)
            layout_key = list(layout_dict.keys())
            for layout_msg in layout_key:
                if 'worker' in layout_msg:
                    idx = layout_msg[-1]
                    ns_key = 'worker'+idx
                    ns_layout[ns_key] = layout_dict[layout_msg]
                    # worker_num = worker_num+1
            print(ns_layout)
            break
        else:
            time.sleep(10)

    # time_query = ((time_base - 1)* 1e9)
    time_query_str = make_time_query(time_base,mode=0)
    print('first time query: %s' % time_query_str)
    res = step_influx_client.query(
        "select * from " + measure_s + " where time >= " + time_query_str + " group by nodes order by asc limit 10")
    keys = res.keys()
    print('first query success!')
    print(keys)
    mana = 0
    step_base = read_step_base(job.name)
    step_high = step_base+1
    while True:
        # step_base = 0
        print("%s try_time=%d" % (job_name,mana))
        print(keys)
        if jieshu:
            break
        if mana > 100:
            jieshu = True
            break
        pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
        if 'Succeeded' in pod_status or 'Failed' in pod_status:
            break
        if keys and len(keys) == job.worker_replicas:
            print("Start to get load-run data")
            node_list = [b['nodes'] for a, b in keys]
            dic_msg = {}
            for node in node_list:
                for i in range(len(keys)):
                    _, no = keys[i]
                    if no['nodes'] == node:
                        dic_msg[node] = list(res[keys[i]])
            print(dic_msg)
            time_base_list = []
            time_low_list = []
            time_node_avg = {}
            time_avg = []
            step_base_list = []
            for node in node_list:
                time_low_list.append(int(match_timestamp(dic_msg[node][0]['time'])))
                time_base_list.append(int(match_timestamp(dic_msg[node][-1]['time'])))
                time_avg_list = [float(i['time_d']) for i in dic_msg[node]]
                step_base_list.append(int(dic_msg[node][-1]['step']))
                time_avg_node = np.mean(time_avg_list)
                time_node_avg[node] = time_avg_node
                time_avg.append(time_avg_node)
            print(time_avg)
            step_base = max(step_base_list)
            write_step_base(job.name,step_base)
            print("step base is %d" % step_base)
            print(type(step_base))
            time_low = math.floor(min(time_low_list)-5)
            time_high = math.ceil(max(time_base_list)+10)
            time_low_str = make_time_query(time_low,mode=0)
            time_high_str = make_time_query(time_high,mode=1)
            # result = self.influx_client.query("select * from "+"NODEMESSAGE"+" group by nodes order by desc limit 3")
            load_result = node_influx_client.query("select * from NODEMESSAGE where time >= "+time_low_str+" and time <= "+time_high_str+" group by nodes order by asc")
            total_worker_node_list = job.get_node_list()
            result_keys = load_result.keys()
            print(load_result)
            worker_nodes = [i[-1]['nodes'] for i in result_keys]
            print(worker_nodes)
            worker_node_mg = [list(load_result[i]) for i in result_keys]
            print(worker_node_mg)
            if not worker_node_mg:
                load_result = node_influx_client.query("select * from NODEMESSAGE where time >= "+time_low_str+" group by nodes order by asc")
                total_worker_node_list = job.get_node_list()
                result_keys = load_result.keys()
                print(load_result)
                worker_nodes = [i[-1]['nodes'] for i in result_keys]
                print(worker_nodes)
                worker_node_mg = [list(load_result[i]) for i in result_keys]
                print(worker_node_mg)
            cpu_use = {}
            total_cpu_use = 0.0
            total_memory_use = 0.0
            total_cpu = 0
            total_memory = 0
            memory_use = {}
            print(len(worker_node_mg))
            print('start to write first points!')
            try:
                for i in range(len(worker_node_mg)):
                    cpu_use[worker_nodes[i]] = 0
                    memory_use[worker_nodes[i]] = 0
                    for j in range(len(worker_node_mg[i])):
                        print(len(worker_node_mg[i]))
                        try:
                            cpu_use[worker_nodes[i]] += worker_node_mg[i][j]['cpu']
                            print(cpu_use)
                            memory_use[worker_nodes[i]] += worker_node_mg[i][j]['memory']
                        except Exception as e0:
                            print(e0)
                    cpu_use[worker_nodes[i]] = (cpu_use[worker_nodes[i]] / len(worker_node_mg[i])) / job.node_cpu[
                        worker_nodes[i]]
                    memory_use[worker_nodes[i]] = (memory_use[worker_nodes[i]] / len(worker_node_mg[i])) / \
                                                  job.node_memory[worker_nodes[i]]
                    total_cpu_use += (cpu_use[worker_nodes[i]] * job.node_cpu[worker_nodes[i]])
                    total_cpu += job.node_cpu[worker_nodes[i]]
                    total_memory_use += (memory_use[worker_nodes[i]] * job.node_memory[worker_nodes[i]])
                    total_memory += job.node_memory[worker_nodes[i]]
                print(cpu_use)
                print(memory_use)
            except Exception as e:
                print(e)
            total_cpu_use = total_cpu_use / total_cpu
            total_memory_use = total_memory_use / total_memory
            points = []
            #     # content = {}
            #     timestamp = response['items'][0]['metadata']['creationTimestamp']
            for node in node_list:
                content = {
                    'measurement': measure_load,
                    'tags':{
                        "nodes": node,
                        "workerpoint":ns_layout[node],
                        "task_id": job.task_id,
                        "runtimes":job.rtimes,
                        "retry":job.retry
                    },
                    'fields': {
                        'node_cpu': cpu_use[ns_layout[node]],
                        'node_memory': memory_use[ns_layout[node]],
                        'time_avg': time_node_avg[node],
                        'total_cpu': total_cpu_use,
                        'total_memory': total_memory_use,
                        'cpu_allocate': job.cpu_allocate,
                        'memory_allocate':job.memory_allocate,
                        'node_compute': job.node_compute[ns_layout[node]],
                        'node_cmtype': job.node_cmtype[ns_layout[node]],
                        'node_disk': job.node_disk[ns_layout[node]],
                        'batch': batch,
                        'flops':flops,
                        'params':params,
                        'ps':job.ps_replicas,
                        'worker':job.worker_replicas
                        }
                    }
                points.append(content)
            print(points[0])
            try:
                step_influx_client.write_points(points, 's', database="PREDICT")
                print("Success to write a point!")
            except Exception as e:
                print(e)

            time_base = math.floor(min(time_base_list))
            print(time_base)
            time_sleep = max(time_avg)*8
            time.sleep(time_sleep)
            break
        else:
            time.sleep(10)
        # res = client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
            try:
                res = step_influx_client.query(
                "select * from " + measure_s + " where time >= " + time_query_str + " group by nodes order by asc limit 10")
                keys = res.keys()
            except Exception as e1:
                print(e1)
            mana = mana + 1
    if jieshu:
        print("Please check the error!!!")
        return
    while True:
        if tasks['start']==False:
            break
#        lock.acquire()
        tmp_ns = tasks["ns"]
 #       lock.release()
        if job.name not in tmp_ns :
            break
        pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
        if 'Succeeded' in pod_status or 'Failed' in pod_status:
            break

        time_query_str = make_time_query(time_base, mode=0)

        res = step_influx_client.query(
            "select * from " + measure_s + " where time >= " + time_query_str + " group by nodes order by asc limit 10")
        keys = res.keys()

        node_list = [b['nodes'] for a, b in keys]
        dic_msg = {}
        for node in node_list:
            for i in range(len(keys)):
                _, no = keys[i]
                if no['nodes'] == node:
                    dic_msg[node] = list(res[keys[i]])

        time_base_list = []
        time_low_list = []
        time_node_avg = {}
        time_avg = []
        step_hight_list = []

        for node in node_list:
            time_low_list.append(match_timestamp(dic_msg[node][0]['time']))
            time_base_list.append(match_timestamp(dic_msg[node][-1]['time']))
            time_avg_list = [float(i['time_d']) for i in dic_msg[node]]
            # step_base_list.append(int(dic_msg[node][-1]['step']))
            step_hight_list.append(int(dic_msg[node][-1]['step']))
            time_avg_node = np.mean(time_avg_list)
            time_node_avg[node] = time_avg_node
            time_avg.append(time_avg_node)

        time_low = math.floor(min(time_low_list) - 7)
        time_high = math.ceil(max(time_base_list) + 8)
        step_high = max(step_hight_list)
        print("step high is %d" % step_high)
        print(step_hight_list)
        time_low_str = make_time_query(time_low, mode=0)
        time_high_str = make_time_query(time_high, mode=1)
        # result = self.influx_client.query("select * from "+"NODEMESSAGE"+" group by nodes order by desc limit 3")
        load_result = node_influx_client.query(
            "select * from NODEMESSAGE where time >= " + time_low_str + " and time <= " + time_high_str + " group by nodes order by asc")
        total_worker_node_list = job.get_node_list()
        result_keys = load_result.keys()
        worker_nodes = [i[-1]['nodes'] for i in result_keys]
        worker_node_mg = [list(load_result[i]) for i in result_keys]
        cpu_use = {}
        total_cpu_use = 0.0
        total_memory_use = 0.0
        total_cpu = 0
        total_memory = 0
        memory_use = {}
        for i in range(len(worker_node_mg)):
            cpu_use[worker_nodes[i]] = 0
            memory_use[worker_nodes[i]] = 0
            for j in range(len(worker_node_mg[i])):
                cpu_use[worker_nodes[i]] += worker_node_mg[i][j]['cpu']
                memory_use[worker_nodes[i]] += worker_node_mg[i][j]['memory']
            cpu_use[worker_nodes[i]] = (cpu_use[worker_nodes[i]] / len(worker_node_mg[i])) / job.node_cpu[
                worker_nodes[i]]
            memory_use[worker_nodes[i]] = (memory_use[worker_nodes[i]] / len(worker_node_mg[i])) / job.node_memory[
                worker_nodes[i]]
            total_cpu_use += (cpu_use[worker_nodes[i]]*job.node_cpu[worker_nodes[i]])
            total_cpu += job.node_cpu[worker_nodes[i]]
            total_memory_use += (memory_use[worker_nodes[i]]*job.node_memory[worker_nodes[i]])
            total_memory += job.node_memory[worker_nodes[i]]
        total_cpu_use = total_cpu_use / total_cpu
        total_memory_use = total_memory_use / total_memory

        points = []
        #     # content = {}
        #     timestamp = response['items'][0]['metadata']['creationTimestamp']
        for node in node_list:
            content = {
                'measurement': measure_load,
                'tags': {
                    "nodes": node,
                    "workerpoint":ns_layout[node],
                    "task_id": job.task_id,
                    "runtimes":job.rtimes,
                    "retry":job.retry
                },
                'fields': {
                    'node_cpu': cpu_use[ns_layout[node]],
                    'node_memory': memory_use[ns_layout[node]],
                    'time_avg': time_node_avg[node],
                    'total_cpu': total_cpu_use,
                    'total_memory': total_memory_use,
                    'cpu_allocate': job.cpu_allocate,
                    'memory_allocate': job.memory_allocate,
                    'node_compute': job.node_compute[ns_layout[node]],
                    'node_cmtype': job.node_cmtype[ns_layout[node]],
                    'node_disk': job.node_disk[ns_layout[node]],
                    'batch': batch,
                    'flops': flops,
                    'params': params,
                    'ps': job.ps_replicas,
                    'worker': job.worker_replicas
                }
            }
            points.append(content)
        step_influx_client.write_points(points, 's', database="PREDICT")
        print("write a point success!!!")
        time_base = math.floor(min(time_base_list))
        try:
            print("now running: %d " % (step_high - step_base))
        except Exception as e:
            print(e)
        if step_high - step_base >= 20:
            alpha = random.randint(0, 5) * 0.1 + 0.5
            beta = random.randint(0,5)*0.1+0.87
            print("before apply:%d" % job.cpu_allocate)
            job.set_resource(cpu_source=(math.ceil(job.cpu_allocate * alpha)), mem_source=(math.ceil(job.memory_allocate * beta)))
            try:
                job.assignment_resource(cpu_source=(math.ceil(job.cpu_allocate * alpha)),memory_source=(math.ceil(job.memory_allocate * beta)))
            except Exception as e0:
                print(e0)
            print("apply job success!")
            print("after apply: %d" % job.cpu_allocate)
            step_base = step_high
            write_step_base(job.name,step_base)
        print("now step base is %d" % step_base)
        print("next select based on time %d" % time_base)
        time_sleep = max(time_avg) * 8
        time.sleep(time_sleep)








    # result = step_influx_client.query("select * from " + measure_s + " group by nodes order by desc limit 3")
#     1580976233000000000

def get_load_value(node_index,cpu_base,memory_base,total_cpu_base,total_memory_base):
    keys = node_index.keys()
    alpha = 0.62
    cpu_score = 0
    memory_score = 0
    node_use = []
    node_cpu = []
    node_mem = []
    for key in keys:
        if node_index[key] < 3:
            node_use.append(key)
    for key in node_use:
        cpu_score+= cpu_base[key]
        node_cpu.append(cpu_base[key])
        memory_score+= memory_base[key]
        node_mem.append(memory_base[key])
    cpu_score = cpu_score/len(node_use)
    memory_score = memory_score/len(node_use)

    cpu_score = alpha*cpu_score+(1-alpha)*total_cpu_base
    memory_score = alpha*memory_score+(1-alpha)*total_memory_base

    return cpu_score,memory_score,node_cpu,node_mem


def Submit_job(tasks,lock,v1,jobs):
    global LOSSHOST,LOSSPORT
    ADDR = (LOSSHOST,LOSSPORT)
    max_buffer_size = 4
    job_basic = reload_jobs(tasks['last'],-1)
    max_free_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_free_load)
    max_wight_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_weight_load)
    worker_buffer = tasks['buffer']
    first_reload = False
    time.sleep(20)
    if worker_buffer:
        first_reload = True
    pool = multiprocessing.Pool(processes=5)
    for job0 in jobs:
        save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job0, job0)
        #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
        # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
        # 'cpu_high':cpu_base,'batch_res':batch_res,
        # 'flops_res':flops_res,'params_res':params_res}
        res_config = load_config(save_res_path)
        batch_res = res_config['batch_res']
        flops_res = res_config['flops_res']
        params_res = res_config['params_res']
        # catch_node_step_msg(jobs=,job_name=,tasks=,lock=,batch=,flops=,params=,mode=)

        pool.apply_async(catch_node_step_msg,args=(jobs,job0,tasks,lock,batch_res,flops_res,params_res,-1))

    while True:
        if tasks['start']==False:
            break
        lock.acquire()
        counts = tasks['count']
        bufer_count = tasks['buffercount']
        lock.release()
        if (counts >= tasks['size']) and (bufer_count >= max_buffer_size):
            time.sleep(float(random.randint(10,15)))
            pass
        elif tasks['next'] and counts < tasks['size']:
            job_name = tasks['next']
            job = reload_jobs(job_name,-1)
            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
            # mem_need = job.total_mem * total_mem_use + job.worker_replicas * job.memory_allocate + 2048 * job.ps_replicas
            # cpu_need = job.total_cpu * total_cpu_use + job.worker_replicas * job.cpu_allocate + 1000 * job.ps_replicas
            catch_worker = 0
            catch_ps = 0

            node_keys = cpu_nodes.keys()
            for key in node_keys:
                catch_ps_c = 0
                catch_ps_m = 0
                catch_worker_c = 0
                catch_worker_m = 0
                can_use_cpu = job.node_cpu[key] * (1 - cpu_nodes[key])
                can_use_mem = job.node_memory[key] * (1 - memory_nodes[key])
                first_try = True
                endcpu = False
                endmem = False
                while (not endcpu) or (not endmem):
                    if first_try:
                        if can_use_cpu - 1000 > 0:
                            catch_ps_c += 1
                            can_use_cpu = can_use_cpu - 1000
                        else:
                            if can_use_cpu - job.cpu_allocate > 0:
                                catch_worker_c += 1
                                can_use_cpu = can_use_cpu - job.cpu_allocate
                        if can_use_mem - 2048 > 0:
                            catch_ps_m += 1
                            can_use_mem = can_use_mem - 2048
                        else:
                            if can_use_mem - job.memory_allocate > 0:
                                catch_worker_m += 1
                                can_use_mem = can_use_mem - job.memory_allocate
                        first_try = False
                    else:
                        if can_use_cpu - job.cpu_allocate > 0:
                            catch_worker_c += 1
                            can_use_cpu = can_use_cpu - job.cpu_allocate
                        else:
                            if can_use_cpu - 1000 > 0:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 1000
                            else:
                                endcpu = True

                        if can_use_mem - job.memory_allocate > 0:
                            catch_worker_m += 1
                            can_use_mem = can_use_mem - job.memory_allocate
                        else:
                            if can_use_mem - 2048 > 0:
                                catch_ps_m += 1
                                can_use_mem = can_use_mem - 2048
                            else:
                                endmem = True

                if catch_worker_c < catch_worker_m:
                    catch_worker += catch_worker_c
                else:
                    catch_worker += catch_worker_m

                if catch_ps_c < catch_ps_m:
                    catch_ps += catch_ps_c
                else:
                    catch_ps += catch_ps_m

                if catch_ps >= 1 and catch_worker>=1:
                    break

            if catch_ps > 0 and catch_worker > 0:
                lock.acquire()
                job.create_tf()
                ns_tmp = tasks['ns']
                ns_tmp.append(job.name)
                tasks['ns'] = ns_tmp
                # job_tmp = tasks['job']
                # job_tmp[job.name] = job
                # tasks['job'] = job_tmp
                is_layout = tasks['nslayout']
                is_layout[job.name] = False
                tasks['nslayout'] = is_layout
                jobs.append(job.name)
                tasks['count'] += 1
                pool.apply_async(catch_node_step_msg,args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                tasks['next'] = ''
                lock.release()
            else:
                time.sleep(30)



        else:
            time.sleep(150)
            deadline = random.randint(3600, 18000)
            if tasks['reload'] == 0:
                template_id = random.randint(1, 4)
                print(template_id)
                lock.acquire()
                tmp1 = tasks['task_id']
                tmp1[template_id - 1] += 1
                tasks['task_id'] = tmp1
                tmp2 = tasks['rtimes']
                tmp2[template_id - 1] += 1
                tasks['rtimes'] = tmp2
                # tasks['ps_replicas'][template_id - 1] = random.randint(1, 3)
                # tasks['worker_replicas'][template_id - 1] = random.randint(2, 6)
                # tasks['batch_size'][template_id - 1] = random.randint(128, 1024)
                lock.release()
                ps_r = random.randint(1, 3)
                worker_r = random.randint(1, 4)
                batch = random.randint(128, 1024)
                measure = "VGG 1"
                print(tasks)
                if template_id == 1:
                    channels = [24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400, 480,
                                512,
                                576]
                    x1 = random.randint(0, 4)
                    x2 = random.randint(4, 7)
                    x3 = random.randint(7, 11)
                    x4 = random.randint(11, 15)
                    x5 = random.randint(15, 19)
                    channel1 = channels[x1]
                    channel2 = channels[x2]
                    channel3 = channels[x3]
                    channel4 = channels[x4]
                    channel5 = channels[x5]

                    num_layer1 = random.randint(2, 4)
                    num_layer2 = random.randint(2, 4)
                    num_layer3 = random.randint(3, 6)
                    num_layer4 = random.randint(3, 8)
                    num_layer5 = random.randint(3, 8)
                    # def __init__(self,v1,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,repeat,channel1,channel2,channel3,channel4,channel5,channel6,channel7,channel8,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                    #                  update_end=0.75, update_delay=2.0):
                    job = VGGTask(template_id=template_id, ps_replicas=ps_r,
                                  worker_replicas=worker_r,
                                  training_step=tasks['training_step'][template_id - 1],
                                  batch_size=batch,
                                  interval=tasks['interval'][template_id - 1],
                                  task_id=tasks['task_id'][template_id - 1],
                                  rtimes=tasks['rtimes'][template_id - 1],
                                  tag=tasks['tag'][template_id - 1], channel1=channel1, channel2=channel2,
                                  channel3=channel3,
                                  channel4=channel4, channel5=channel5,
                                  num_layer1=num_layer1, num_layer2=num_layer2, num_layer3=num_layer3,
                                  num_layer4=num_layer4,
                                  num_layer5=num_layer5
                                  )
                    job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                  'worker_replicas': job.worker_replicas,
                                  'training_step': job.training_step,
                                  'batch_size': job.batch_size,
                                  'interval': job.interval, 'task_id': job.task_id,
                                  'rtimes': job.rtimes,
                                  'tag': job.tag, 'channel1': job.channel1, 'channel2': job.channel2,
                                  'channel3': job.channel3,
                                  'channel4': job.channel4, 'channel5': job.channel5,
                                  'num_layer1': job.num_layer1, 'num_layer2': job.num_layer2,
                                  'num_layer3': job.num_layer3,
                                  'num_layer4': job.num_layer4,
                                  'num_layer5': job.num_layer5}

                    dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                            'channel4': channel4,
                            'channel5': channel5, 'num_layer1': num_layer1, 'num_layer2': num_layer2,
                            'num_layer3': num_layer3, 'num_layer4': num_layer4, 'num_layer5': num_layer5}


                elif template_id == 2:
                    bottle = random.randint(0, 1)
                    channels = [24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400, 480,
                                512,
                                576]
                    x1 = random.randint(0, 3)
                    x2 = random.randint(1, 7)
                    x3 = random.randint(8, 14)
                    x4 = random.randint(14, 19)
                    channel1 = channels[x1]
                    channel2 = channels[x2]
                    channel3 = channels[x3]
                    channel4 = channels[x4]
                    layer1 = random.randint(2, 6)
                    layer2 = random.randint(2, 8)
                    layer3 = random.randint(2, 40)
                    layer4 = random.randint(2, 6)

                    job = RESTask(template_id=template_id, ps_replicas=ps_r,
                                  worker_replicas=worker_r,
                                  training_step=tasks['training_step'][template_id - 1],
                                  batch_size=batch,
                                  interval=tasks['interval'][template_id - 1],
                                  task_id=tasks['task_id'][template_id - 1],
                                  rtimes=tasks['rtimes'][template_id - 1],
                                  tag=tasks['tag'][template_id - 1], bottle=bottle, layer1=layer1, layer2=layer2,
                                  layer3=layer3,
                                  layer4=layer4, channel1=channel1, channel2=channel2, channel3=channel3,
                                  channel4=channel4)

                    job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                  'worker_replicas': job.worker_replicas,
                                  'training_step': job.training_step,
                                  'batch_size': job.batch_size,
                                  'interval': job.interval,
                                  'task_id': job.task_id, 'rtimes': job.rtimes,
                                  'tag': job.tag, 'bottle': job.bottle, 'layer1': job.layer1, 'layer2': job.layer2,
                                  'layer3': job.layer3,
                                  'layer4': job.layer4, 'channel1': job.channel1, 'channel2': job.channel2,
                                  'channel3': job.channel3, 'channel4': job.channel4}

                    dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                            'channel4': channel4,
                            'layer1': layer1, 'layer2': layer2,
                            'layer3': layer3, 'layer4': layer4, 'bottle': bottle}

                elif template_id == 3:
                    stack = random.randint(3, 16)
                    channels = [12, 16, 24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400,
                                480,
                                512, 576]
                    x1 = random.randint(0, 3)
                    x2 = random.randint(2, 5)
                    x3 = random.randint(6, 11)
                    x4 = random.randint(6, 11)
                    channel1 = channels[x1]
                    channel2 = channels[x2]
                    channel3 = channels[x3]
                    channel4 = channels[x4]
                    job = RETask(template_id=template_id, ps_replicas=ps_r,
                                 worker_replicas=worker_r,
                                 training_step=tasks['training_step'][template_id - 1],
                                 batch_size=batch,
                                 interval=tasks['interval'][template_id - 1],
                                 task_id=tasks['task_id'][template_id - 1], rtimes=tasks['rtimes'][template_id - 1],
                                 tag=tasks['tag'][template_id - 1], stack=stack, channel1=channel1,
                                 channel2=channel2,
                                 channel3=channel3, channel4=channel4
                                 )
                    dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                            'channel4': channel4, 'stack_num': stack}

                    job_config = {
                        'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                        'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                        'batch_size': job.batch_size, 'interval': job.interval,
                        'task_id': job.task_id, 'rtimes': job.rtimes,
                        'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1, 'channel2': job.channel2,
                        'channel3': job.channel3, 'channel4': job.channel4
                    }

                elif template_id == 4:
                    repeat = random.randint(4, 12)
                    channels = [12, 16, 24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400,
                                480,
                                512, 576, 640, 728, 856, 920, 960, 1024, 1280, 1408, 1536, 1600, 1728, 2048, 2096]
                    x1 = random.randint(0, 5)
                    x2 = random.randint(3, 9)
                    x3 = random.randint(9, 12)
                    x4 = random.randint(12, 18)
                    x5 = random.randint(19, 24)
                    x6 = random.randint(26, 28)
                    x7 = random.randint(29, 31)
                    x8 = random.randint(32, 34)
                    channel1 = channels[x1]
                    channel2 = channels[x2]
                    channel3 = channels[x3]
                    channel4 = channels[x4]
                    channel5 = channels[x5]
                    channel6 = channels[x6]
                    channel7 = channels[x7]
                    channel8 = channels[x8]
                    job = XCETask(template_id=template_id, ps_replicas=ps_r,
                                  worker_replicas=worker_r,
                                  training_step=tasks['training_step'][template_id - 1],
                                  batch_size=batch,
                                  interval=tasks['interval'][template_id - 1],
                                  task_id=tasks['task_id'][template_id - 1],
                                  rtimes=tasks['rtimes'][template_id - 1], tag=tasks['tag'][template_id - 1],
                                  repeat=repeat,
                                  channel1=channel1, channel2=channel2, channel3=channel3,
                                  channel4=channel4, channel5=channel5, channel6=channel6, channel7=channel7,
                                  channel8=channel8)

                    job_config = {
                        'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                        'worker_replicas': job.worker_replicas,
                        'training_step': job.training_step,
                        'batch_size': job.batch_size,
                        'interval': job.interval,
                        'task_id': job.task_id,
                        'rtimes': job.rtimes, 'tag': job.tag, 'repeat': job.repeat, 'channel1': job.channel1,
                        'channel2': job.channel2, 'channel3': job.channel3, 'channel4': job.channel4,
                        'channel5': job.channel5,
                        'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8
                    }

                    dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                            'channel4': channel4, 'channel5': channel5, 'channel6': channel6, 'channel7': channel7,
                            'channel8': channel8, 'repeat': repeat}

                else:
                    Ls = [16, 32, 40, 48, 50, 60, 64, 80, 100, 120, 128, 160, 180, 200, 240, 250, 256]
                    ks = [8, 10, 12, 16, 24, 32, 40, 48]
                    x1 = random.randint(0, 16)
                    x2 = random.randint(0, 7)
                    L = Ls[x1]
                    k = ks[x2]
                    BC = random.randint(0, 1)
                    job = DENTask(template_id=template_id, ps_replicas=ps_r,
                                  worker_replicas=worker_r,
                                  training_step=tasks['training_step'][template_id - 1],
                                  batch_size=batch,
                                  interval=tasks['interval'][template_id - 1],
                                  task_id=tasks['task_id'][template_id - 1],
                                  rtimes=tasks['rtimes'][template_id - 1],
                                  tag=tasks['tag'][template_id - 1], L=L, k=k, BC=BC)

                    job_config = {
                        'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                        'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                        'batch_size': job.batch_size, 'interval': job.interval, 'task_id': job.task_id,
                        'rtimes': job.rtimes,
                        'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC
                    }

                    # batch, flops, params = denfpmodel.denfp(batch=256, BC=0, k=24, L=100, num_classes=10)
                    dict = {'batch': batch, 'BC': BC, 'k': k, 'L': L, 'num_classes': 10}
                measure = job.measure
                lock.acquire()
                # tmp_reload = tasks['reload']
                # tmp_reload = tmp_reload+1
                # tasks['reload'] = tmp_reload
                tasks['base'] = job.name
                lock.release()
            else:
                job_base_name = tasks['base']
                job_base_name_list = job_base_name.split('-')
                if job_base_name_list[0] == 'vgg':
                    template_id = 1
                elif job_base_name_list[0] == 'res':
                    template_id = 2
                elif job_base_name_list[0] == 're':
                    template_id = 3
                elif job_base_name_list[0] == 'xception':
                    template_id = 4
                else:
                    template_id = 5
                lock.acquire()
                tmp1 = tasks['task_id']
                tmp1[template_id - 1] += 1
                tasks['task_id'] = tmp1
                tmp2 = tasks['rtimes']
                tmp2[template_id - 1] += 1
                tasks['rtimes'] = tmp2
                # tasks['ps_replicas'][template_id - 1] = random.randint(1, 3)
                # tasks['worker_replicas'][template_id - 1] = random.randint(2, 6)
                # tasks['batch_size'][template_id - 1] = random.randint(128, 1024)
                lock.release()
                tmp_task_id = tmp1[template_id - 1]
                job = reload_jobs(job_base_name, task_id=tmp_task_id)

                if template_id == 1:
                    job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                  'worker_replicas': job.worker_replicas,
                                  'training_step': job.training_step,
                                  'batch_size': job.batch_size,
                                  'interval': job.interval, 'task_id': job.task_id,
                                  'rtimes': job.rtimes,
                                  'tag': job.tag, 'channel1': job.channel1, 'channel2': job.channel2,
                                  'channel3': job.channel3,
                                  'channel4': job.channel4, 'channel5': job.channel5,
                                  'num_layer1': job.num_layer1, 'num_layer2': job.num_layer2,
                                  'num_layer3': job.num_layer3,
                                  'num_layer4': job.num_layer4,
                                  'num_layer5': job.num_layer5}

                    dict = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                            'channel3': job.channel3,
                            'channel4': job.channel4,
                            'channel5': job.channel5, 'num_layer1': job.num_layer1, 'num_layer2': job.num_layer2,
                            'num_layer3': job.num_layer3, 'num_layer4': job.num_layer4,
                            'num_layer5': job.num_layer5}
                elif template_id == 2:
                    job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                  'worker_replicas': job.worker_replicas,
                                  'training_step': job.training_step,
                                  'batch_size': job.batch_size,
                                  'interval': job.interval,
                                  'task_id': job.task_id, 'rtimes': job.rtimes,
                                  'tag': job.tag, 'bottle': job.bottle, 'layer1': job.layer1, 'layer2': job.layer2,
                                  'layer3': job.layer3,
                                  'layer4': job.layer4, 'channel1': job.channel1, 'channel2': job.channel2,
                                  'channel3': job.channel3, 'channel4': job.channel4}

                    dict = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                            'channel3': job.channel3,
                            'channel4': job.channel4,
                            'layer1': job.layer1, 'layer2': job.layer2,
                            'layer3': job.layer3, 'layer4': job.layer4, 'bottle': job.bottle}
                elif template_id == 3:
                    dict = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                            'channel3': job.channel3,
                            'channel4': job.channel4, 'stack_num': job.stack}

                    job_config = {
                        'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                        'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                        'batch_size': job.batch_size, 'interval': job.interval,
                        'task_id': job.task_id, 'rtimes': job.rtimes,
                        'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1, 'channel2': job.channel2,
                        'channel3': job.channel3, 'channel4': job.channel4
                    }
                elif template_id == 4:
                    job_config = {
                        'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                        'worker_replicas': job.worker_replicas,
                        'training_step': job.training_step,
                        'batch_size': job.batch_size,
                        'interval': job.interval,
                        'task_id': job.task_id,
                        'rtimes': job.rtimes, 'tag': job.tag, 'repeat': job.repeat, 'channel1': job.channel1,
                        'channel2': job.channel2, 'channel3': job.channel3, 'channel4': job.channel4,
                        'channel5': job.channel5,
                        'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8
                    }

                    dict = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                            'channel3': job.channel3,
                            'channel4': job.channel4, 'channel5': job.channel5, 'channel6': job.channel6,
                            'channel7': job.channel7,
                            'channel8': job.channel8, 'repeat': job.repeat}
                else:
                    job_config = {
                        'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                        'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                        'batch_size': job.batch_size, 'interval': job.interval, 'task_id': job.task_id,
                        'rtimes': job.rtimes,
                        'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC
                    }

                    # batch, flops, params = denfpmodel.denfp(batch=256, BC=0, k=24, L=100, num_classes=10)
                    dict = {'batch': job.batch_size, 'BC': job.BC, 'k': job.k, 'L': job.L, 'num_classes': 10}
                measure = job.measure

            lock.acquire()
            if tasks['count'] < tasks['size'] or tasks['buffercount'] < max_buffer_size:

                #loss_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                #loss_client.connect(ADDR)
                client_pre = influxdb.InfluxDBClient(host=job.dbhost, port=8086, username='admin', password='admin',
                                            database="PREDICT")
                pre_list = measure.split(" ")
                measure_s = pre_list[0] + 'S' + pre_list[-1]
                measure_t = pre_list[0] + 'T' + pre_list[-1]

                step_items = [
                    {
                        'measurement': measure_t,
                        'tags': {
                            'task': job.task_id,
                            'runtimes': job.rtimes,
                            'retry': job.retry
                        },
                        'fields': {
                            'training_step': job.training_step
                        }
                    }
                ]
                # print(step_to_train)
                client_pre.write_points(step_items, time_precision="ms", database="PREDICT")
                # if job.training_step > 200:
                loss_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                loss_client.connect(ADDR)
                loss_client.send(bytes(measure, 'utf-8'))
                connect_try = 5
                try_times = 1
                connected = False
                while True:
                    if try_times > connect_try:
                        break
                    msg_from_server = loss_client.recv(4096)
                    if not msg_from_server:
                        break
                    msg_from_server_str = str(msg_from_server.decode('utf-8'))
                    msg_from_server_list = msg_from_server_str.split(" ")
                    if msg_from_server_list[0] == '400':
                        connected = True
                        break
                    loss_client.send(bytes(measure, 'utf-8'))
                    try_times = try_times + 1

                if not connected:
                    print("Connected or send message error!")
                    loss_client.close()
                    continue
                print(msg_from_server_str)
                print("connected success!")
                dict_json = json.dumps(dict)
                loss_client.send(bytes(dict_json, 'utf-8'))
                ress = loss_client.recv(4096)
                ress_str = str(ress.decode('utf-8'))
                ress_lists = ress_str.split(' ')
                if ress_lists[0] == '400':
                    batch_res = int(ress_lists[1])
                    flops_res = int(ress_lists[2])
                    params_res = int(ress_lists[3])
                    cpu_predict = float(ress_lists[-2])
                    cpu_base = math.ceil(1.12*cpu_predict)
                    mem_predict = float(ress_lists[-1])
                    mem_base = math.ceil(1.35*mem_predict)
                    res_to_server = '1'
                    loss_client.send(bytes(res_to_server, 'utf-8'))

                else:
                    res_to_server = '0'
                    loss_client.send(bytes(res_to_server, 'utf-8'))
                    loss_client.close()
                    continue
                loss_client.close()
                # lock.acquire()
                tmp_reload = tasks['reload']
                # lock.release()
                if tmp_reload == 0:
                    alpha = 1
                    beta = 1
                else:
                    alpha = random.randint(2,12)*0.1+0.5
                    beta = random.randint(0,10)*0.1+1
                # alpha = 1
                # beta = 1
                job.set_resource(cpu_source=(math.ceil(cpu_base * alpha)), mem_source=(math.ceil(mem_base * beta)))
                start_time = '%.3f' % time.time()
                start_time = float(start_time)
                job.set_deadline(deadline=deadline, start_time=start_time)
                job_res_config = {'deadline': job.deadline, 'start_time': job.starttime, 'cpu_source': job.cpu_allocate,
                                  'mem_source': job.memory_allocate, 'cpu_high': cpu_base, 'memory_base': mem_base,'batch_res': batch_res,
                                  'flops_res': flops_res, 'params_res': params_res,'step_base':0}
                save_config_dir = task_submit.check_path(job.name)
                save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job.name, job.name)
                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                save_config(job_config, save_job_path)
                save_config(job_res_config, save_res_path)
                if tasks['count'] < tasks['size'] and tasks['buffercount'] == 0:
                    node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                    cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,
                                                                                         cpu_base=cpu_nodes,
                                                                                          memory_base=memory_nodes,
                                                                                          total_cpu_base=total_cpu_use,
                                                                                          total_memory_base=total_mem_use)

                    if cpu_value < 0.4:
                        job.worker_replicas = random.randint(4,6)


                    elif cpu_value < 0.7:
                        job.worker_replicas = random.randint(3, 4)

                    else:
                        job.worker_replicas = random.randint(1,2)

                    job.ps_replicas = random.randint(math.ceil(job.worker_replicas / 4),
                                                     math.ceil(job.worker_replicas / 2))

                    save_job_change_layout(job.name,job.ps_replicas,job.worker_replicas)

                    mem_need = job.total_mem*total_mem_use + job.worker_replicas*job.memory_allocate+2048*job.ps_replicas
                    cpu_need = job.total_cpu*total_cpu_use+job.worker_replicas*job.cpu_allocate+1000*job.ps_replicas
                    catch_worker = 0
                    catch_ps = 0

                    node_keys = cpu_nodes.keys()
                    reach_ps = False
                    reach_worker = False
                    for key in node_keys:
                        catch_ps_c = 0
                        catch_ps_m = 0
                        catch_worker_c = 0
                        catch_worker_m = 0
                        can_use_cpu = job.node_cpu[key]*(1-cpu_nodes[key])
                        can_use_mem = job.node_memory[key] * (1 - memory_nodes[key])
                        first_try = True
                        endcpu = False
                        endmem = False
                        while (not endcpu) or (not endmem):
                            if first_try:
                                if can_use_cpu - 1000 > 0 and not reach_ps:
                                    catch_ps_c+=1
                                    can_use_cpu = can_use_cpu - 1000
                                else:
                                    if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                        catch_worker_c+=1
                                        can_use_cpu = can_use_cpu - job.cpu_allocate
                                if can_use_mem - 2048 > 0 and not reach_ps:
                                    catch_ps_m+=1
                                    can_use_mem = can_use_mem - 2048
                                else:
                                    if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                        catch_worker_m+=1
                                        can_use_mem = can_use_mem - job.memory_allocate
                                first_try = False
                            else:
                                if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                    catch_worker_c += 1
                                    can_use_cpu = can_use_cpu - job.cpu_allocate
                                else:
                                    if can_use_cpu - 1000 > 0 and not reach_ps:
                                        catch_ps_c += 1
                                        can_use_cpu = can_use_cpu - 1000
                                    else:
                                        endcpu = True

                                if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                    catch_worker_m += 1
                                    can_use_mem = can_use_mem - job.memory_allocate
                                else:
                                    if can_use_mem - 2048 > 0 and not reach_ps:
                                        catch_ps_m += 1
                                        can_use_mem = can_use_mem - 2048
                                    else:
                                        endmem = True

                        if catch_worker_c < catch_worker_m:
                            catch_worker += catch_worker_c
                        else:
                            catch_worker += catch_worker_m

                        if catch_ps_c < catch_ps_m:
                            catch_ps += catch_ps_c
                        else:
                            catch_ps += catch_ps_m
                        if catch_ps >= job.ps_replicas:
                            reach_ps = True
                        if catch_worker >= job.worker_replicas:
                            reach_worker = True
                        if catch_ps >= job.ps_replicas and catch_worker >= job.worker_replicas:
                            break
                    print("catch_ps: %d catch_worker: %d" % (catch_ps,catch_worker))
                    if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                        if catch_ps >0 and catch_worker > 0:
                            if catch_worker > job.worker_replicas:
                                catch_worker = job.worker_replicas
                            if catch_ps > job.ps_replicas:
                                catch_ps = job.ps_replicas
                            job.ps_replicas = catch_ps
                            job.worker_replicas = catch_worker
                            save_job_change_layout(job.name,catch_ps,catch_worker)
                            job.create_tf()
                            ns_tmp = tasks['ns']
                            ns_tmp.append(job.name)
                            tasks['ns'] = ns_tmp
                            # job_tmp = tasks['job']
                            # job_tmp[job.name] = job
                            # tasks['job'] = job_tmp
                            is_layout = tasks['nslayout']
                            is_layout[job.name] = False
                            tasks['nslayout'] = is_layout
                            jobs.append(job.name)
                            tasks['count'] += 1
                            pool.apply_async(catch_node_step_msg,
                                             args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                        else:
                            job.ps_replicas = 1
                            job.worker_replicas = 1
                            save_job_change_layout(job.name, 1, 1)
                            tasks['next'] = job.name
                            # tasks['next'] = job.name
                    else:

                        job.create_tf()
                        ns_tmp = tasks['ns']
                        ns_tmp.append(job.name)
                        tasks['ns'] = ns_tmp
                        # job_tmp = tasks['job']
                        # job_tmp[job.name] = job
                        # tasks['job'] = job_tmp
                        is_layout = tasks['nslayout']
                        is_layout[job.name] = False
                        tasks['nslayout'] = is_layout
                        jobs.append(job.name)
                        tasks['count'] += 1
                        pool.apply_async(catch_node_step_msg,
                                         args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))

                elif tasks['count'] >= tasks['size']:
                    worker_buffer = tasks['buffer']
                    worker_buffer.append(job.name)
                    tasks['buffer'] = worker_buffer
                    tmp_buffer_count = tasks['buffercount']
                    tmp_buffer_count = tmp_buffer_count+1
                    tasks['buffercount'] = tmp_buffer_count

                else:
                    worker_buffer = tasks['buffer']
                    worker_buffer.append(job.name)
                    tmp_buffer_count = tasks['buffercount']
                    tmp_buffer_count = tmp_buffer_count + 1
                    tasks['buffercount'] = tmp_buffer_count
                    node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                    cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,cpu_base=cpu_nodes,memory_base=memory_nodes,total_cpu_base=total_cpu_use,total_memory_base=total_mem_use)
                    if cpu_value < 0.4:
                        selected = False
                        for job_name in worker_buffer:
                            rea = max_free_heap.add(job_name)
                            if rea is not None:
                                selected_job_name = rea
                                selected = True
                                break
                        if not selected:
                            selected_job_name = max_free_heap.items[0]
                        print(selected_job_name)
                        worker_buffer = max_free_heap.items
                        print(worker_buffer)
                        if not selected:
                            ceshi_name = worker_buffer.pop(0)
                        # tmp_buffer = tasks['buffer']
                        # tmp_buffer.remove(selected_job_name)
                            print(ceshi_name)
                        tasks['buffer'] = worker_buffer[:]
                        # tmp_buffer_size =
                        max_free_heap.clear()
                        if selected:
                            tasks['buffercount'] = max_buffer_size
                        else:
                            tmp_buffer_count = tmp_buffer_count - 1
                            tasks['buffercount'] = tmp_buffer_count
                    else:
                        selected = False
                        for job_name in worker_buffer:
                            # max_wight_heap
                            rea = max_wight_heap.add(job_name)
                            if rea is not None:
                                selected_job_name = rea
                                selected = True
                                break
                        if not selected:
                            selected_job_name = max_wight_heap.items[0]
                        worker_buffer = max_wight_heap.items
                        print(worker_buffer)
                        print(selected_job_name)
                        if not selected:
                            ceshi_name = worker_buffer.pop(0)
                        # tmp_buffer = tasks['buffer']
                        # tmp_buffer.remove(selected_job_name)
                            print(ceshi_name)
                        tasks['buffer'] = worker_buffer[:]
                        # tmp_buffer_size =
                        max_wight_heap.clear()
                    if selected:
                        tasks['buffercount'] = max_buffer_size
                    else:
                        tmp_buffer_count = tmp_buffer_count - 1
                        tasks['buffercount'] = tmp_buffer_count
                    job = reload_jobs(selected_job_name, -1)
                    if cpu_value < 0.4:
                        job.worker_replicas = random.randint(4, 6)


                    elif cpu_value < 0.7:
                        job.worker_replicas = random.randint(3, 4)

                    else:
                        job.worker_replicas = random.randint(1, 2)

                    job.ps_replicas = random.randint(math.ceil(job.worker_replicas / 4),
                                                     math.ceil(job.worker_replicas / 2))

                    save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas)

                    mem_need = job.total_mem * total_mem_use + job.worker_replicas * job.memory_allocate + 2048 * job.ps_replicas
                    cpu_need = job.total_cpu * total_cpu_use + job.worker_replicas * job.cpu_allocate + 1000 * job.ps_replicas
                    catch_worker = 0
                    catch_ps = 0

                    node_keys = cpu_nodes.keys()
                    reach_ps = False
                    reach_worker = False
                    for key in node_keys:
                        catch_ps_c = 0
                        catch_ps_m = 0
                        catch_worker_c = 0
                        catch_worker_m = 0
                        can_use_cpu = job.node_cpu[key] * (1 - cpu_nodes[key])
                        can_use_mem = job.node_memory[key] * (1 - memory_nodes[key])
                        first_try = True
                        endcpu = False
                        endmem = False
                        while (not endcpu) or (not endmem):
                            if first_try:
                                if can_use_cpu - 1000 > 0 and not reach_ps:
                                    catch_ps_c += 1
                                    can_use_cpu = can_use_cpu - 1000
                                else:
                                    if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                        catch_worker_c += 1
                                        can_use_cpu = can_use_cpu - job.cpu_allocate
                                if can_use_mem - 2048 > 0 and not reach_ps:
                                    catch_ps_m += 1
                                    can_use_mem = can_use_mem - 2048
                                else:
                                    if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                        catch_worker_m += 1
                                        can_use_mem = can_use_mem - job.memory_allocate
                                first_try = False
                            else:
                                if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                    catch_worker_c += 1
                                    can_use_cpu = can_use_cpu - job.cpu_allocate
                                else:
                                    if can_use_cpu - 1000 > 0 and not reach_ps:
                                        catch_ps_c += 1
                                        can_use_cpu = can_use_cpu - 1000
                                    else:
                                        endcpu = True

                                if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                    catch_worker_m += 1
                                    can_use_mem = can_use_mem - job.memory_allocate
                                else:
                                    if can_use_mem - 2048 > 0 and not reach_ps:
                                        catch_ps_m += 1
                                        can_use_mem = can_use_mem - 2048
                                    else:
                                        endmem = True

                        if catch_worker_c < catch_worker_m:
                            catch_worker += catch_worker_c
                        else:
                            catch_worker += catch_worker_m

                        if catch_ps_c < catch_ps_m:
                            catch_ps += catch_ps_c
                        else:
                            catch_ps += catch_ps_m

                        if catch_ps >= job.ps_replicas:
                            reach_ps = True

                        if catch_worker >= job.worker_replicas:
                            reach_worker = True

                        if catch_ps >= job.ps_replicas and catch_worker >= job.worker_replicas:
                            break
                    print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                    if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                        if catch_ps > 0 and catch_worker > 0:
                            if catch_worker > job.worker_replicas:
                                catch_worker = job.worker_replicas
                            if catch_ps > job.ps_replicas:
                                catch_ps = job.ps_replicas
                            job.ps_replicas = catch_ps
                            job.worker_replicas = catch_worker

                            save_job_change_layout(job.name, catch_ps, catch_worker)
                            job.create_tf()
                            ns_tmp = tasks['ns']
                            ns_tmp.append(job.name)
                            tasks['ns'] = ns_tmp
                            # job_tmp = tasks['job']
                            # job_tmp[job.name] = job
                            # tasks['job'] = job_tmp
                            is_layout = tasks['nslayout']
                            is_layout[job.name] = False
                            tasks['nslayout'] = is_layout
                            jobs.append(job.name)
                            tasks['count'] += 1
                            pool.apply_async(catch_node_step_msg,
                                             args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                        else:
                            job.ps_replicas = 1
                            job.worker_replicas = 1
                            save_job_change_layout(job.name,1,1)
                            tasks['next'] = job.name
                    else:
                        job.create_tf()
                        ns_tmp = tasks['ns']
                        ns_tmp.append(job.name)
                        tasks['ns'] = ns_tmp
                        # job_tmp = tasks['job']
                        # job_tmp[job.name] = job
                        # tasks['job'] = job_tmp
                        is_layout = tasks['nslayout']
                        is_layout[job.name] = False
                        tasks['nslayout'] = is_layout
                        jobs.append(job.name)
                        tasks['count'] += 1
                        pool.apply_async(catch_node_step_msg,
                                         args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))

                tmp_reload = tasks['reload']
                tmp_reload = tmp_reload + 1
                if tmp_reload == 6:
                    tmp_reload = 0
                tasks['reload'] = tmp_reload
                # ns_tmp = tasks['ns']
                # ns_tmp.append(job.name)
                # tasks['ns'] = ns_tmp
                # # job_tmp = tasks['job']
                # # job_tmp[job.name] = job
                # # tasks['job'] = job_tmp
                # is_layout = tasks['nslayout']
                # is_layout[job.name] = False
                # tasks['nslayout'] = is_layout
                # jobs.append(job.name)
                # tasks['count'] += 1

                # pool.apply_async(catch_node_step_msg,args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res,1))
            lock.release()





def save_config(config,filename):
    config_content = {}
    for key,value in config.items():
        # if key != 'job' and key != 'ns':
        config_content[key] = value
        # task_content['task_id'] = tasks['task_id']
    fw = open(filename, 'w', encoding='utf-8')
    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
    dic_json = json.dumps(config_content, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
    fw.write(dic_json)
    fw.close()

def jiance(tasks,lock):
    while True:
        if tasks['start']==True:
            time.sleep(120)
            lock.acquire()
            save_config(tasks,'system_info.json')
            lock.release()
            print('saved configs')
            time.sleep(120)
        else:
            break

def save_job_change_layout(job_name,ps_n,worker_n):
    save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    job_config = load_config(save_job_path)
    # 'ps_replicas': job.ps_replicas,'worker_replicas': job.worker_replicas
    job_config['ps_replicas'] = ps_n
    job_config['worker_replicas'] = worker_n
    save_config(job_config, save_job_path)

def save_job_change_resource(job_name,cpu_allocate,mem_allocate):
    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    # save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
    # save_config(job_config, save_job_path)
    job_res_config['cpu_source'] = cpu_allocate
    job_res_config['mem_source'] = mem_allocate
    save_config(job_res_config, save_res_path)


def read_step_base(job_name):
    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    key = job_res_config.keys()
    key_list = list(key)
    if 'step_base' not in key_list:
        job_res_config['step_base'] = 0
    step_base = job_res_config['step_base']
    return int(step_base)

def write_step_base(job_name,step_base):
    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    job_res_config['step_base'] = step_base
    save_config(job_res_config,save_res_path)
    print("save step base successfully!!!")



def reload_jobs(job_name,task_id):
    #full_flie_name = '/tfdata/tfcnn/expjob/%s.yaml' % job_name
    save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
   # with open(full_flie_name,'r') as yaml_job:
        #job_obj = yaml.load(yaml_job.read())

    job_config = load_config(save_job_path)
    job_res_config = load_config(save_res_path)
    params_dic = {}
    keys = job_config.keys()
    for key in keys:
        params_dic[key] = job_config[key]
    # params_dic['v1'] = v1
    if task_id != -1:
        params_dic['task_id'] = task_id
        params_dic['rtimes'] = task_id
    if job_config['template_id'] == 1:
        job_reload = VGGTask(**params_dic)
    elif job_config['template_id'] == 2:
        job_reload = RESTask(**params_dic)
    elif job_config['template_id'] == 3:
        job_reload = RETask(**params_dic)
    elif job_config['template_id'] == 4:
        job_reload = XCETask(**params_dic)
    else:
        job_reload = DENTask(**params_dic)
   # job_reload.template = job_obj
    #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,'cpu_source':job.cpu_allocate,
    # 'mem_source':job.memory_allocate,'cpu_high':cpu_base}
    job_reload.cpu_allocate = job_res_config['cpu_source']
    job_reload.memory_allocate = job_res_config['mem_source']
    job_reload.deadline = job_res_config['deadline']
    job_reload.starttime = job_res_config['start_time']

    return job_reload
    # job_name_list = job_name.split('-')
    # job = VGGTask()

def load_config(config_file):
    # # json串是一个字符串
    # f = open('product.json', encoding='utf-8')
    # res = f.read()
    # product_dic = json.loads(res)  # 把json串，变成python的数据类型，只能转换json串内容
    # print(product_dic)
    # print(product_dic['iphone'])
    # # t = json.load(f)
    # # print(t) #传一个文件对象，它会帮你直接读json文件，并转换成python数据
    # # print(t['iphone'])
    # f.close()
    f = open(config_file,encoding='utf-8')
    res = f.read()
    config_content = json.loads(res)
    return config_content



if __name__ == '__main__':
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # v1.list_node()
    mgr = multiprocessing.Manager()
    tasks = mgr.dict()
    lock = mgr.Lock()
    jobs = mgr.list()
    config_content = load_config('system_info.json')
    for key,value in config_content.items():
        tasks[key] = value
    print(tasks)
    for ns in tasks["ns"]:
        # job_reload = reload_jobs(ns,-1)
        jobs.append(ns)
   # tasks['ns'] = []
    # tasks['job'] = {}
    q = multiprocessing.Manager().Queue(maxsize=tasks['size'])
    tasks['start'] = True
    # print(tasks)
    # print(type(tasks))
    # task_content = {}
    # task_content['task_id'] = [0,0,0,0,0]
    # task_content['rtimes'] = [0,0,0,0,0]
    # task_content['size'] = 3
    # task_content['training_step'] = [80,80,80,80,80]
    # task_content['ps_replicas'] = [2, 2, 2, 2, 2]
    # task_content['count'] = 0
    # task_content['worker_replicas'] = [4, 4, 4, 4, 4]
    # task_content['training_step'] = [80, 80, 80, 80, 80]
    # task_content['interval'] = [1.0, 1.0, 1.0, 0.5, 1.0]
    # task_content['batch_size'] = [128, 128, 128, 128, 128]
    # task_content['tag'] = ["ms", "ms", "ms", "ms", "ms"]
    # save_config(task_content)
    # print(tasks.items())
    # print(type(tasks['task_id']))
    # task_content['task_id'] = tasks['task_id']
   #  fw = open('system_info.json', 'w', encoding='utf-8')
   # # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
   #  dic_json = json.dumps(task_content, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
   #  fw.write(dic_json)
   #  fw.close()

    url = 'https://192.168.128.10:6443/apis/metrics.k8s.io/v1beta1/nodes'
    args = parse()
    client = influxdb.InfluxDBClient('192.168.128.10', port=8086, username='admin', password='admin',
                                     database=args.database)
    # node_p = Node_mess(url=url,derivation=10,args=args)
    node_p = Node_mess(url=url, args=args,tasks=tasks,v1=v1)
    # Submit_job(tasks=,lock=,v1=,jobs=)
    # Monitor_job(tasks,lock,v1,jobs)
    submit_p = multiprocessing.Process(target=Submit_job,args=(tasks,lock,v1,jobs))
    monitor_p = multiprocessing.Process(target=Monitor_job,args=(tasks,lock,v1,jobs))
    jiance_p = multiprocessing.Process(target=jiance, args=(tasks, lock))
    # derivation
    node_p.daemon = True
    # submit_p.daemon = True
    # monitor_p.daemon = True
    jiance_p.daemon = True
    k1 = os.getpid()
    # v1.list_namespace(timeout=)
    k2 = multiprocessing.current_process().pid
    # v1.delete_namespace()
    print(k1, k2)
    while True:
        boots = input("Please Input 'start' to start:\n")
        if boots == 'start':
            time_open = math.ceil(time.time())
            tmp_list = tasks["creation"]
            tmp_list.append(time_open)
            tasks["creation"] = tmp_list
            node_p.start()
            submit_p.start()
            monitor_p.start()
            jiance_p.start()
        if boots == 'end':
            tasks['start'] = False
            time.sleep(10)
            submit_p.join()
            monitor_p.join()
            if tasks['count']>0:
                for ns in tasks['ns']:
                    print(tasks['ns'])
                    print("deal ns:"+ns)
                    pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                    if 'Succeeded' in pod_status or 'Failed' in pod_status:
                        time.sleep(float(random.randint(3, 10)))
                        lock.acquire()
                        ns_tmp = tasks['ns']
                        command = 'kubectl delete -f /tfdata/tfcnn/expjob/'+ns+'.yaml'
                        os.system(command)
                        v1.delete_namespace(ns)
                        # tasks['job'][ns].delete_tf()
                        ns_tmp.remove(ns)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        print("is layout: \n")
                        print(is_layout)
                        is_layout.pop(ns)
                        tasks['nslayout'] = is_layout
                        print("after deal: \n")
                        print(tasks['nslayout'])
                        # tasks['job'].pop(ns)
                        tasks['count'] = len(ns_tmp)
                        print(tasks['count'])
                        lock.release()
                    time.sleep(5)
            time_last = math.ceil(time.time())
            tmp_list = tasks['endtime']
            tmp_list.append(time_last)
            tasks["endtime"] = tmp_list
            save_config(tasks,filename='system_info.json')
            print('System end!')
            break




