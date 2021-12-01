import multiprocessing
import os
import influxdb
import json
from pytz import UTC
from dateutil import parser
from datetime import datetime
import requests
import pandas as pd
import argparse
import kubernetes
import time
import math
from entity.nodeMessage import *
from util import influx_client


def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/home/NFSshare/nodedata', help='save path')
    parser.add_argument('--database',default="NODEMESSAGE",help="save database")
    parser.add_argument('--derivation',default=30,help='sampling rate')
    parser.add_argument('--measurement',default="NODEMESSAGE",help="save measurement")
    # parser.add_argument('--train_pg', action='store_true', help='whether train policy gradient')
    # parser.add_argument('--train_dqn', action='store_true', help='whether train DQN')
    # parser.add_argument('--test_pg', action='store_true', help='whether test policy gradient')
    # parser.add_argument('--test_dqn', action='store_true', help='whether test DQN')

    args = parser.parse_args()
    return args

def generate_item(response,measurement,tasks):
    node_cpu = tasks['cpu']
    node_memory = tasks['memory']
    points = []
    # content = {}
    timestamp = response['items'][0]['metadata']['creationTimestamp']
    for item in response['items']:
        content = {
            'measurement': measurement,
            'tags':{
                "node_name": node_name[item['metadata']['name']]
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
        # print("XXX")
        timestamp = UTC.localize(timestamp)

    s = (timestamp - EPOCH).total_seconds()
    return int(s)

def catch_message(url):
    global aToken

    aToken = update_token()
    headers = make_headers(aToken)
    try:
        response = requests.get(url,headers=headers,verify=False)
        res_json = response.json()
    except:
        res_json = {}
    return res_json


gap_time=30
database="project"
measurement="CPUANDMEM"
save_path="/home/NFSshare/nodedata"
def node_cpu_mem_monitor():
    url = 'https://172.16.20.190:6443/apis/metrics.k8s.io/v1beta1/nodes'
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    time_mess = {}
    cpu_mess = {}
    memory_mess = {}
    cpu_per = {}
    memory_per = {}
    tasks={}

    if 'cpu' not in tasks.keys():
        tasks['cpu'] = {}
    if 'memory' not in tasks.keys():
        tasks['memory'] = {}

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    response = catch_message(url)
    

    # print(response)
    items = v1.list_node().items

    tmp_node_cpu = {}
    tmp_node_mem = {}
    for node_item in items:
        tmp_node_cpu[node_item.metadata.name] = float(int(node_item.status.allocatable['cpu']) * 1e3)
        tmp_node_mem[node_item.metadata.name] = float(node_item.status.allocatable['memory'][:-2]) / 1024
    tasks['cpu'] = tmp_node_cpu
    tasks['memory'] = tmp_node_mem

    if not response:
        while (True):
            time.sleep(gap_time/2)
            response = catch_message(url)
            if response:
                break
    
    time_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
    cpu_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
    memory_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
    cpu_per['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
    memory_per['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
    for item in response['items']:
        time_mess[item['metadata']['name']] = [item['timestamp']]
        cpu_mess[item['metadata']['name']] = [match_cpu(item['usage']['cpu'])]
        memory_mess[item['metadata']['name']] = [match_memory(item['usage']['memory'])]
        cpu_per[item['metadata']['name']] = [
        float(match_cpu(item['usage']['cpu']) / tasks['cpu'][item['metadata']['name']])]
        memory_per[item['metadata']['name']] = [
        float(match_memory(item['usage']['memory']) / tasks['memory'][item['metadata']['name']])]
    influx_client.write_points(generate_item(response, measurement, tasks), 's', database=database)
    

    total_num = 0
    while True:
        time.sleep(gap_time)
        if total_num % 100 == 0:
            items = v1.list_node().items
            # self.node_cpu = {}
            # self.node_memory = {}
            tmp_node_cpu = {}
            tmp_node_mem = {}
            for node_item in items:
                tmp_node_cpu[node_item.metadata.name] = float(int(node_item.status.allocatable['cpu']) * 1e3)
                tmp_node_mem[node_item.metadata.name] = float(node_item.status.allocatable['memory'][:-2]) / 1024
            tasks['cpu'] = tmp_node_cpu
            tasks['memory'] = tmp_node_mem
        response = catch_message(url)
        if not response:
            continue
        time_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
        cpu_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
        memory_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
        cpu_per['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
        memory_per['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
        for item in response['items']:
            time_mess[item['metadata']['name']].append(item['timestamp'])
            cpu_mess[item['metadata']['name']].append(match_cpu(item['usage']['cpu']))
            memory_mess[item['metadata']['name']].append(match_memory(item['usage']['memory']))
            cpu_per[item['metadata']['name']].append(
                float(match_cpu(item['usage']['cpu']) / tasks['cpu'][item['metadata']['name']]))
            memory_per[item['metadata']['name']].append(
                float(match_memory(item['usage']['memory']) / tasks['memory'][item['metadata']['name']]))
        influx_client.write_points(generate_item(response, measurement, tasks=tasks), 's',
                                 database=database)
        if len(time_mess['creation']) % 100 == 0 and len(time_mess['creation']) > 0:
            data_frame = pd.DataFrame(time_mess)
            data_frame.to_csv(save_path + '/' + 'struct.csv', mode='a+', index=False, sep=',')
            # print(cpu_mess)
            # print(len(cpu_mess))
            data_frame2 = pd.DataFrame(cpu_mess)
            data_frame2.to_csv(save_path + '/' + 'node_cpu.csv', mode='a+', index=False, sep=',')
            data_frame3 = pd.DataFrame(memory_mess)
            data_frame3.to_csv(save_path + '/' + 'node_memory.csv', mode='a+', index=False, sep=',')
            data_frame4 = pd.DataFrame(cpu_per)
            data_frame4.to_csv(save_path + '/' + 'node_cpu_per.csv', mode='a+', index=False, sep=',')
            data_frame5 = pd.DataFrame(memory_per)
            data_frame5.to_csv(save_path + '/' + 'node_memory_per.csv', mode='a+', index=False, sep=',')
            for key in time_mess:
                time_mess[key] = []
                cpu_mess[key] = []
                memory_mess[key] = []
                memory_per[key] = []
                cpu_per[key] = []
        total_num += 1
