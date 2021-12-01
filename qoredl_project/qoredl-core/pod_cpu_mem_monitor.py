import multiprocessing
import os
import influxdb
import json
from pytz import UTC
from dateutil import parser
from datetime import datetime
# import time
import requests
import pandas as pd
from Global_client import Global_Influx
import argparse
import time
import json
import kubernetes
import math
import random
import os
from subprocess import Popen, PIPE

#目前识别的Pod状态：
# pod_status = [j.status.phase for j in reload_tmp.v1.list_namespaced_pod(i).items]
status_id = {"Running":0,"Failed":1,"Succeeded":2,"Pending":3,"Unknown":4}
specific_status = {"Running":{"id":0,"item":["Running","CrashLoopBackOff","Terminating","RunContainerError","Unknown","NodeLost"]},
                   "Failed":{"id":1,"item":["Error","CrashLoopBackOff","Terminating","RunContainerError","Unknown","NodeLost","Evicted","OOMKilled","ContainerCannotRun"]},
                   "Succeeded":{"id":2,"item":["Completed","OOMKilled","Evicted","Terminating","Unknown"]},
                   "Unknown":{"id":3,"item":["UnKnown"]}
                   }
node_ip = {'ubuntu': '172.16.20.151','voicecomm': '172.16.20.190'}
node_index = {'GPU1':1,'GPU2':2,'GPU3':3,'GPU4':4,'GPU5':5}
ip_node = {'172.16.20.151':'ubuntu','172.16.20.190':'voicecomm'}
node_id = {'ubuntu': 'GPU2','voicecomm': 'GPU1'}
# p = Popen([nvidia_smi, "--query-gpu=uuid,index,utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
#                   stdout=PIPE)
# p = Popen(["kubectl", "get", "pods","-n kube-system"],
#                 stdout=PIPE)

def get_ns(v1):
    ns_list = []
    for i in v1.list_namespace().items:
        ns_list.append(i.metadata.name)
    return ns_list

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

def load_config(config_file):
    f = open(config_file,encoding='utf-8')
    res = f.read()
    config_content = json.loads(res)
    return config_content

def err_list_update(tasks):
    if not os.path.exists("/home/NFSshare/PROGECT"):
        os.makedirs("/home/NFSshare/PROGECT",exist_ok=True)
    # if not os.path.exists("/home/NFSshare/PROGECT/reason.json"):
    tmp_reason = tasks['reason']
    save_config(tmp_reason,"/home/NFSshare/PROGECT/reason.json")



def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/home/NFSshare/nodedata', help='save path')
    parser.add_argument('--database',default="PODMESSAGE",help="save database")
    parser.add_argument('--derivation',default=10,help='sampling rate')
    parser.add_argument('--measurement',default="PODMESSAGE",help="save measurement")
    # parser.add_argument('--train_pg', action='store_true', help='whether train policy gradient')
    # parser.add_argument('--train_dqn', action='store_true', help='whether train DQN')
    # parser.add_argument('--test_pg', action='store_true', help='whether test policy gradient')
    # parser.add_argument('--test_dqn', action='store_true', help='whether test DQN')

    args = parser.parse_args()
    return args

def update_token():
    cacheData = os.popen(
        "echo $(kubectl describe secret $(kubectl get secret -n kube-system | grep ^metric-reader | awk '{print $1}') -n kube-system | grep -E '^token'| awk '{print $2}')").read()
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

def match_cpu(raw_data):
    cache = raw_data[:-1]
    tmp_match = "%.2f" % float(int(cache)/1e6)
    matched_data = float(tmp_match)
    return matched_data

def match_memory(raw_data):
    cache = raw_data[:-2]
    tmp_match = "%.2f" % float(int(cache)/1024)
    matched_data = float(tmp_match)
    return matched_data

def match_timestamp(raw_data):
    EPOCH = UTC.localize(datetime.utcfromtimestamp(0))
    timestamp = parser.parse(raw_data)
    if not timestamp.tzinfo:
        print("XXX")
        timestamp = UTC.localize(timestamp)

    s = (timestamp - EPOCH).total_seconds()
    return int(s)

def generate_item(response,tasks,ns,pod,timestamp,measurement="EXPC1",rank=0,node='null',status="Running",mode=0):
    # node_cpu = tasks['cpu']
    # node_memory = tasks['memory']
    points = []
    # content = {}
    # timestamp = response['metadata']['creationTimestamp']
    reason_id = 0
    if mode == 0:
        if status in tasks['reason'].keys():
            status_id = tasks['reason'][status]['id']
        else:
            tmp_reason = tasks['reason']
            status_id = len(tmp_reason.keys())
            tmp_reason[status] = {'id':status_id,"item":[]}
            p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
            stdout, stderror = p.communicate()
            output = stdout.decode('UTF-8').strip()
            lines = output.split(os.linesep)
            tmp_reason[status]["item"].append(lines[1].split()[2].strip())
            tasks['reason'] = tmp_reason
            err_list_update(tasks=tasks)
    else:
        if status in tasks['reason'].keys():
            status_id = tasks['reason'][status]['id']
            p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
            stdout, stderror = p.communicate()
            output = stdout.decode('UTF-8').strip()
            lines = output.split(os.linesep)
            reason_now = lines[1].split()[2]
            tmp_reason = tasks['reason']

            if reason_now in tmp_reason[status]["item"]:
                reason_id = tmp_reason[status]["item"].index(reason_now)
            else:
                reason_id =len(tmp_reason[status]["item"])
                tmp_reasond_items = tmp_reason[status]["item"][:]
                tmp_reasond_items.append(reason_now)
                tmp_reason_status = tmp_reason[status]
                tmp_reason_status['item'] = tmp_reasond_items
                tmp_reason[status] = tmp_reason_status
                tasks['reason'] = tmp_reason
                err_list_update(tasks)
        else:
            tmp_reason = tasks['reason']
            status_id = len(tmp_reason.keys())
            tmp_reason[status] = {'id': status_id, "item": []}
            p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
            stdout, stderror = p.communicate()
            output = stdout.decode('UTF-8').strip()
            lines = output.split(os.linesep)
            tmp_reason[status]["item"].append(lines[1].split()[2].strip())
            tasks['reason'] = tmp_reason
            err_list_update(tasks=tasks)
            reason_id = 0

    content = {}

    for i in range(len(response['containers'])):
        if i == 0:
            content = {
            'measurement': measurement,
            'tags':{
                "nodes": node,
                "pod":rank
            },
            'fields': {
                'cpu': match_cpu(response['containers'][0]['usage']['cpu']),
                'memory': match_memory(response['containers'][0]['usage']['memory'])
            },
            'time': match_timestamp(timestamp)
            }
        else:
            tmp_cpu = content['fields']['cpu']
            tmp_cpu += match_cpu(response['containers'][i]['usage']['cpu'])
            tmp_mem = content['fields']['memory']
            tmp_mem += match_memory(response['containers'][i]['usage']['memory'])
            content['fields']['cpu'] = tmp_cpu
            content['fields']['memory'] = tmp_mem
    if mode == 0:
        content['fields']['status'] = status_id
    else:
        content['fields']['status'] = status_id
        content['fields']['reason'] = reason_id
    points.append(content)
    return points

def Monitor_job(tasks,v1,lock,duration):
    time.sleep(5)
    while True:
        if tasks['start'] == False:
            break
        ns_list = get_ns(v1)
        # print(ns_list)
        if tasks['start'] == True and tasks['count'] == 0:
            time.sleep(duration)
            pass
        else:
            # Now we just realize the CPU and RAM monitor for the kube-system
            # After Submitting module finish, we will use this code to monitor all the Pytorch job namespace
            time1 = time.time()
            for ns in tasks['ns']:
            #     # print(ns+'If in list:'+str(ns in ns_list))
                if ns not in ns_list and ns not in tasks['retry'] and not tasks['modulate']:
                    try_times = 5
                    while try_times > 0:
                        time.sleep(float(random.randint(3, 5)))
                        ns_list = get_ns(v1)
                        if ns in ns_list:
                            break
                        try_times=try_times-1
                    if try_times <=0:
                        lock.acquire()
                        ns_tmp = tasks['ns']
                        if ns in ns_tmp:
                            ns_tmp.remove(ns)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        is_layout_keys = list(is_layout.keys())
                        if ns in is_layout_keys:
                            is_layout.pop(ns)
                        tasks['nslayout'] = is_layout
                        count_tmp = len(ns_tmp)
                        tasks['count'] = count_tmp
                        lock.release()
                else:
                    pod_items = v1.list_namespaced_pod(ns).items
                    pod_list = [{i.metadata.name: i.status.phase} for i in pod_items]
                    # def generate_item(response,timestamp,measurement="system",rank=0,node='-1'):
                    timestamp = ""

                    for pod_i in range(len(pod_list)):
                        # namespaces/knative-eventing/pods
                        pod_name = list(pod_list[pod_i].keys())[0]
                        url = "https://172.16.20.190:6443/apis/metrics.k8s.io/v1beta1/namespaces/%s/pods/%s" % (ns, pod_name)
                        response = catch_message(url)
                        if pod_i == 0:
                            timestamp = response['metadata']['creationTimestamp']
                        node_on = "null"
                        try:
                            node_on = ip_node[pod_items[pod_i].status.host_ip]
                        except Exception as e0:
                            node_on = "null"
                        # print(response)
                        # def generate_item(response,tasks,ns,pod,timestamp,measurement="system",rank=0,node='null',status="Running",mode=0):
                        client.write_points(generate_item(response,tasks,ns,pod_name,timestamp,measurement="EXPC1",rank=pod_i,node=node_on,status=pod_list[pod_i][pod_name]),'s',database=args.database)
                        # print(generate_item(response, tasks, ns, pod_name, timestamp, measurement="system", rank=pod_i,
                        #             node=node_on, status=pod_list[pod_i][pod_name]))
            print(time.time() - time1)
            # print(tasks['reason'])
            time.sleep(duration)

def get_container_status(ns,pod):
    p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
    stdout, stderror = p.communicate()
    output = stdout.decode('UTF-8').strip()
    lines = output.split(os.linesep)
    reason_now = lines[1].split()[2]
    return reason_now
    # tmp_reason = tasks['reason']

def get_pod_logs(ns,pod):
    p = Popen(['kubectl','logs','-n',ns,pod], stdout=PIPE)
    stdout, stderror = p.communicate()
    output = stdout.decode('UTF-8').strip()
    return str(output).strip()

def get_pod_list(ns):
    pod_items = v1.list_namespaced_pod(ns).items
    pod_list = [{i.metadata.name: i.status.phase} for i in pod_items]
    return pod_list

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
if __name__ == '__main__':
    args = parse()
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    mgr = multiprocessing.Manager()
    tasks = mgr.dict()
    lock = mgr.Lock() #同步锁
    duration = 30
    tasks['start'] = True
    if not os.path.exists("/home/NFSshare/PROGECT/reason.json"):
        tasks['reason'] = specific_status
        save_config(specific_status,"/home/NFSshare/PROGECT/reason.json")
    else:
        tasks['reason'] = load_config("/home/NFSshare/PROGECT/reason.json")

    database_create(args.database)
    client = influxdb.InfluxDBClient('172.16.20.190', port=8086, username='voicecomm', password='voicecomm',
                                     database=args.database)
    # monitor_p = multiprocessing.Process(target=Monitor_job, args=(tasks,v1,lock,duration))
    # monitor_p.daemon = True
    time_open = math.ceil(time.time())
    tasks['start'] = True
    tasks['count'] = 1
    tasks['ns'] = ["confirmer-1-1"]
    tasks['nslayout'] = {"confirmer-1-1": True}
    Monitor_job(tasks,v1,lock,duration)
    # tmp_list = tasks["creation"]
    # tmp_list.append(time_open)
    # tasks["creation"] = tmp_list
    # monitor_p.start()

    # while True:
    #     boots = input("Please Input 'start' to start:\n")
    #     if boots == 'start':
    #         time_open = math.ceil(time.time())
    #         tasks['start'] = True
    #         tasks['count'] = 1
    #         tasks['ns'] = ["confirmer-1-1"]
    #         tasks['nslayout'] = {"confirmer-1-1":True}
    #         # tmp_list = tasks["creation"]
    #         # tmp_list.append(time_open)
    #         # tasks["creation"] = tmp_list
    #         monitor_p.start()
    #         # submit_p.start()
    #         # monitor_p.start()
    #         # jiance_p.start()
    #     if boots == 'end':
    #         # tasks.keys()
    #         tasks['start'] = False
    #         monitor_p.join()
    #         time.sleep(10)