import argparse
import random
import multiprocessing
import time
import ast
import math
import kubernetes
import requests
import os
from subprocess import Popen, PIPE
import influxdb
from task_submit_torch import SubTask,ClusterAgent

from pytz import UTC
from dateutil import parser
from datetime import datetime
import psutil
import socket
# from max_heap import MaxHeap
# import worker_queue
# # from worker_queue import value_free_load,value_weight_load
# from Global_client import Global_Influx
import numpy as np
import json

def load_config(config_file):
    f = open(config_file,encoding='utf-8')
    res = f.read()
    config_content = json.loads(res)
    f.close()
    return config_content

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

def generate_item(response,pod_status_reason,ns,pod,timestamp,status_lock,measurement="EXPC1",rank=0,node='null',status="Running",mode=0):
    points = []
    reason_id = 0
    reason = ""
    print("got response")
    if response is None:
        content = {
            'measurement': measurement,
            'tags': {
                "node_name": node,
                "pod_id": rank
            },
            'fields': {
                'cpu': -1.0,
                'memory': -1.0
            },
            # 'time': match_timestamp(timestamp)
        }

        content['fields']['status'] = pod_status_reason['status'][status]
        if status == "Adjusting":
            reason = "Adjusting"
        else:
            reason = "Not exist"
    else:
        print("response is not None")
        if mode == 0:
            if status in pod_status_reason['status'].keys():
                status_id = pod_status_reason['reason'][status]['id']
                print("status id: %d" % status_id)
            else:
                status_lock.acquire()
                tmp_reason = pod_status_reason['reason']
                tmp_status = pod_status_reason['status']
                status_id = len(tmp_reason.keys())
                tmp_status[status] = status_id
                tmp_reason[status] = {'id': status_id, "item": []}
                try:
                    print("kubectl get pod %s -n %s" % (pod,ns))
                    p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
                    stdout, stderror = p.communicate()
                    output = stdout.decode('UTF-8').strip()
                    lines = output.split(os.linesep)
                    print("reason: %s" % lines[1].split()[2].strip())
                    tmp_reason[status]["item"].append(lines[1].split()[2].strip())
                except Exception as e:
                    tmp_reason[status] = {'id': status_id, "item": []}
                pod_status_reason['reason'] = tmp_reason
                pod_status_reason['status'] = tmp_status
                err_list_update(pod_status_reason)
                status_lock.release()
        else:
            if status in pod_status_reason['status'].keys():
                status_id = pod_status_reason['reason'][status]['id']
                try:
                    print("kubectl get pod %s -n %s" % (pod, ns))
                    p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
                    stdout, stderror = p.communicate()
                    output = stdout.decode('UTF-8').strip()
                    lines = output.split(os.linesep)
                    reason_now = lines[1].split()[2]
                    tmp_reason = pod_status_reason['reason']
                    reason = reason_now
                    print("reason: %s" % lines[1].split()[2].strip())
                    if reason_now in tmp_reason[status]["item"]:
                        reason_id = tmp_reason[status]["item"].index(reason_now)
                    else:
                        reason_id = len(tmp_reason[status]["item"])
                        tmp_reason_status = tmp_reason[status]
                        tmp_reasond_items = tmp_reason_status["item"][:]
                        tmp_reasond_items.append(reason_now)
                        tmp_reason_status['item'] = tmp_reasond_items
                        tmp_reason[status] = tmp_reason_status
                        status_lock.acquire()
                        pod_status_reason['reason'] = tmp_reason
                        err_list_update(pod_status_reason)
                        status_lock.release()
                except Exception as e:
                    print(e)
                    reason_id = 0
                    reason = "Unknown"
            else:
                tmp_reason = pod_status_reason['reason']
                tmp_status = pod_status_reason['status']
                status_id = len(tmp_reason.keys())
                tmp_status[status] = status_id
                tmp_reason[status] = {'id': status_id, "item": []}
                try:
                    print("kubectl get pod %s -n %s" % (pod, ns))
                    p = Popen(['kubectl', 'get', 'pod', pod, '-n', ns], stdout=PIPE)
                    stdout, stderror = p.communicate()
                    output = stdout.decode('UTF-8').strip()
                    lines = output.split(os.linesep)
                    reason_now = lines[1].split()[2].strip()
                    tmp_reason[status]["item"]=[reason_now]
                    print("reason: %s" % reason_now)
                    reason = reason_now
                except Exception as e:
                    reason = "Unknown"
                    reason_id = 0

                status_lock.acquire()
                pod_status_reason['reason'] = tmp_reason
                pod_status_reason['status'] = tmp_status
                status_lock.release()
                err_list_update(pod_status_reason)
                reason_id = 0

        content = {}
        # {'kind': 'Status', 'apiVersion': 'v1', 'metadata': {}, 'status': 'Failure', 'message': 'pod "ectd-voicecomm" not found',
        # 'reason': 'NotFound', 'details': {'name': 'ectd-voicecomm', 'kind': 'pod'}, 'code': 404}
        print(status)
        print("status id:"+str(status_id))
        print("reason id:"+str(reason_id))
        if 'code' in response.keys() or 'status' in response.keys():
            # if response['code'] == 404:
            content = {
                'measurement': measurement,
                'tags': {
                    "node_name": node,
                    "pod_id": rank
                },
                'fields': {
                    'cpu': 0.0,
                    'memory': 0.0
                }
                # 'time': match_timestamp(timestamp)
            }
        else:
            try:
                for i in range(len(response['containers'])):
                    if i == 0:
                        if timestamp is not None:
                            content = {
                            'measurement': measurement,
                            'tags': {
                                "node_name": node,
                                "pod_id": rank
                            },
                            'fields': {
                                'cpu': match_cpu(response['containers'][0]['usage']['cpu']),
                                'memory': match_memory(response['containers'][0]['usage']['memory'])
                            },
                            'time': match_timestamp(timestamp)
                            }
                        else:
                            content = {
                            'measurement': measurement,
                            'tags': {
                                "node_name": node,
                                "pod_id": rank
                            },
                            'fields': {
                                'cpu': match_cpu(response['containers'][0]['usage']['cpu']),
                                'memory': match_memory(response['containers'][0]['usage']['memory'])
                            }
                            }
                    else:
                        tmp_cpu = content['fields']['cpu']
                        tmp_cpu += match_cpu(response['containers'][i]['usage']['cpu'])
                        tmp_mem = content['fields']['memory']
                        tmp_mem += match_memory(response['containers'][i]['usage']['memory'])
                        content['fields']['cpu'] = tmp_cpu
                        content['fields']['memory'] = tmp_mem
            except Exception as e:
                content = {
                    'measurement': measurement,
                    'tags': {
                        "node_name": node,
                        "pod_id": rank
                    },
                    'fields': {
                        'cpu': 0.0,
                        'memory': 0.0
                    },
                    # 'time': match_timestamp(timestamp)
                }
        if mode == 0:
            content['fields']['status'] = status_id
        else:
            content['fields']['status'] = status_id
            content['fields']['reason'] = reason_id
    points.append(content)
    print(points)
    return points,status,reason

def parse():
    parser = argparse.ArgumentParser(description="Submit Moudle")
    parser.add_argument('--save_path', default='/home/NFSshare', help='save path')
    parser.add_argument('--database',default="project",help="save database")
    parser.add_argument("--poddatabase",default="podCpu",help="pod monitor database")
    # parser.add_argument('--derivation',default=10,help='sampling rate')
    parser.add_argument("--pool_size",type=int,default=10,help="pool size for the job monitor")
    # parser.add_argument('--measurement',default="NODEMESSAGE",help="save measurement")
    # parser.add_argument('--train_pg', action='store_true', help='whether train policy gradient')
    # parser.add_argument('--train_dqn', action='store_true', help='whether train DQN')
    # parser.add_argument('--test_pg', action='store_true', help='whether test policy gradient')
    # parser.add_argument('--test_dqn', action='store_true', help='whether test DQN')

    args = parser.parse_args()
    return args

def save_config(config,filename):
    config_content = {}
    for key,value in config.items():
        # if key != 'job' and key != 'ns':
        config_content[key] = value
        # task_content['task_id'] = tasks['task_id']
    fw = open(filename, 'w', encoding='utf-8')
    dic_json = json.dumps(config_content, ensure_ascii=False, indent=4)
    fw.write(dic_json)
    fw.close()

# 传入的参数，在第一阶段暂时包括：
# 1. 优先级: priority
# 2. 镜像名：image_name
# 3. 训练配置文件：training_config_file

# 4. 分布式训练节点总数: workers
# 5. cpu分配量：cpu_allocate
# 6.内存分配量：mem_allocate
# 7.数据加载进程数：num_workers
# 8. 是否启用pin_memory减少内存消耗
# 9.分布式模式：nccl /gloo
#关于监控的相关配置也可调节
# 1. 监控的采样间隔： interval
# 第二阶段再进行数据集传入后的支持工作
# 包括:
# 1. checkpoint: 模型
# 2. raw_data_path: 原始数据位置
# 3. train_data_file： 训练集索引位置
# 4. cv_data_file：可视化数据索引位置
# 5. cmvn配置文件

#第三阶段为指示调度增加期望deadline
# # 任务状态 status：发布时为iniital; 调度时为scheduling; 已完成调度为scheduled;调整时为adjusting;运行时根据情况获取；结束时为finished

# 一、工具函数部分：
def submit_save_job_config(job_raw_config,task_id,save_path="/home/NFSshare/expjob"):
    # def __init__(self,priority=0,retry=0,image_name='172.16.20.190:5000/wenet-k8s-torch:7.4',template_name="exp",training_config_file="train_conformer.yaml",model_dir="exp/model",task_id=1,master_replicas=1,
    #                  worker_replicas=1,cpu_allocate=-1,mem_allocate=-1,deadline=-1,train_data_file="raw_wav/train/format.data",cv_data_file="raw_wav/dev/format.data",
    #                  gpu=0,backend="nccl",num_workers=2,cmvn="global_cmvn",gpu_monitor_interval=30.0,gpu_monitor_failure=15,gpu_monitor_database="podGpu",gpu_monitor_database_server="172.16.20.190",pin_memory=True,node_message_path="/home/NFSshare/PROGECT/global_node.json",gpu_message_path="/home/NFSshare/PROGECT/global_uuid.json",
    #                  raw_data_path="asr-data",project_config_path="PROGECT",container_work_dir="/var/wenet/examples/aishell/s0"):
    job_config = {"priority":0,
                  "image_name":'172.16.20.190:5000/wenet-k8s-torch:8.2',
                  "training_config_file":"train_conformer.yaml",
                  "master_replicas":1,
                  "worker_replicas":1,
                  "cpu_allocate":-1,#core*1000
                  "mem_allocate":-1,#MB
                  "backend":"nccl",#nccl,gloo
                  "num_workers":2,#2
                  "gpu_monitor_interval":30.0,
                  "gpu_monitor_failure":15,
                  "pin_memory":True,
                  "template_name": "exp",
                  "task_id": -1,
                  "retry": 0,
                  "status": "initial",
                  "run_dir": "/var/wenet/examples/aishell/s0/exp/model"
                  }

    for key,value in job_raw_config.items():
        job_config[key] = value
    if job_config['task_id'] == -1:
        job_config['task_id'] = task_id
    else:
        job_config['retry'] = job_config['retry']+1
    job_config['status'] = "initial"
    job_config['starttime'] = time.time()
    filename = "%s/config/%s-%d.json" % (save_path, job_config["template_name"], task_id)
    history_filename = "%s/logs/%s-%d.json" % (save_path, job_config["template_name"], task_id)
    if os.path.exists(history_filename):
        job_log = load_config(history_filename)
    else:
        job_log = {}
    job_log[job_config['starttime']] = {}
    job_log[job_config['starttime']]['status'] = "initial"
    job_log[job_config['starttime']]['action'] = "start the job: %d times" % job_config['retry']
    save_config(job_config,filename)
    save_config(job_log,history_filename)
    return ("%s-%d" % (job_config["template_name"],task_id)),job_config['starttime'],job_config

def scheduling_save_job_config(job_name,save_path="/home/NFSshare/expjob/"):
    filename = "%s/config/%s.json" % (save_path,job_name)
    history_filename = "%s/logs/%s.json" % (save_path, job_name)
    job_config = load_config(filename)
    job_config['status'] = "scheduling"
    save_config(job_config,filename)
    job_log = load_config(history_filename)
    scheduling_time = time.time()
    job_log[scheduling_time] = {}
    job_log[scheduling_time]['status'] = "scheduling"
    job_log[scheduling_time]['action'] = "start to scheduling the job"
    save_config(job_log, history_filename)

def load_job_messages(job_name):
    save_job_path = '/home/NFSshare/expjob/config/%s.json' % (job_name)
    if os.path.exists(save_job_path):
        job_config = load_config(save_job_path)
        params_dic = {}
        keys = job_config.keys()
        for key in keys:
            params_dic[key] = job_config[key]
        # job_res_config = load_config(save_res_path)
        params_dic = {}
        keys = job_config.keys()
        for key in keys:
            params_dic[key] = job_config[key]
            if keys == "pin_memory":
                if job_config["pin_memory"]:
                    params_dic[key] = 1
                else:
                    params_dic[key] = 0
        params_dic['name'] = job_name
    else:
        params_dic = {}
    return params_dic

def reload_jobs(job_name,task_id):
    #full_flie_name = '/tfdata/tfcnn/expjob/%s.yaml' % job_name
    save_job_path = '/home/NFSshare/expjob/config/%s.json' % (job_name)
    # save_res_path = '/home/NFSshare/expjob/resconfig/%s_res.json' % (job_name)

    job_config = load_config(save_job_path)
    params_dic = {}
    keys = job_config.keys()
    for key in keys:
        params_dic[key] = job_config[key]
    # job_res_config = load_config(save_res_path)
    params_dic = {}
    keys = job_config.keys()
    for key in keys:
        params_dic[key] = job_config[key]
    # params_dic['v1'] = v1
    if task_id != -1:
        params_dic['task_id'] = task_id
        # params_dic['rtimes'] = task_id
    job_reload = SubTask(**params_dic)
    return job_reload

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

def get_cluster_message(cluster_agent,tasks,global_lock):
    cluster_agent.update_node()
    tmp_tasks = {}
    global_lock.acquire()
    for key,value in tasks.items():
        tmp_tasks[key] = value
    global_lock.release()
    return cluster_agent.node_resource,tmp_tasks

def get_cluster_tasks(tasks,global_lock):
    tmp_tasks = {}
    global_lock.acquire()
    for key, value in tasks.items():
        value_type =  str(type(value))
        if 'bool' in value_type:
            if value:
                tmp_tasks[key] = "true"
            else:
                tmp_tasks[key] = "false"
        else:
            tmp_tasks[key] = value
    global_lock.release()
    return tmp_tasks

def err_list_update(pod_status_reason):
    if not os.path.exists("/home/NFSshare/PROGECT"):
        os.makedirs("/home/NFSshare/PROGECT",exist_ok=True)
    # if not os.path.exists("/home/NFSshare/PROGECT/reason.json"):
    tmp_reason = pod_status_reason
    save_config(tmp_reason,"/home/NFSshare/PROGECT/reason.json")

#二、针对每个任务的跟踪进程，实现为进程池：
# Monitor_job是每个任务都具有的一个进程，用来采集监测各任务CPU，内存资源+判断任务状态，对调整做出反映
def Monitor_job(tasks,pod_status_reason,status_lock,job_name,global_lock,duration=30):
    time.sleep(5)
    aim_job = reload_jobs(job_name=job_name,task_id=-1)

    measurement = "%sC%d" % (aim_job.template_name.upper(),int(aim_job.task_id))
    client = influxdb.InfluxDBClient('172.16.20.190', port=8086, username='voicecomm', password='voicecomm',
                                     database="podCpu")
    # get_ns()
    count_for_exist = 0 # 若出现不在集群namespace中或不在运行时任务中的情况下，判断多长时间后关闭该任务
    count_for_error = 0 # 若出现各种错误无法恢复，则认为应停止任务
    count_for_attempt_assign = 0 # 若调整失败则稍后重试
    assignment_resource_done = False
    assingment_replicas_done = False
    while True:
        if tasks['start'] == False:
            break
        if aim_job.status not in ["Finished","Adjusting"]:
            print("start to monitor")
        ns_list = aim_job.cluster_agent.get_ns()
        global_lock.acquire()
        tmp_running_list = tasks['running']
        tmp_deleting_list = tasks['deleting']
        global_lock.release()
        running_jobs = list(tmp_running_list.keys())
        # pod_items = aim_job.cluster_agent.v1.list_namespaced_pod(job_name).items
        # print("%s have pod items: %s" % (aim_job.name, pod_items))
        print("%s status is :%s" % (job_name,aim_job.status))
        if job_name in tmp_deleting_list:
            aim_job.delete_tf(0)
            global_lock.acquire()
            tmp_deleting_list = tasks['deleting']
            tmp_deleting_list.remove(job_name)
            tasks['deleting'] = tmp_deleting_list
            global_lock.release()
            aim_job.set_status("Deleted")
            time.sleep(3)
            break
        if aim_job.status == "Deleted":
            print("exit because of deleted")
            break
        if (job_name not in ns_list or job_name not in running_jobs):
            if job_name not in tasks['adjust_aim']:
                count_for_exist += 1
                time.sleep(6)
                if count_for_exist <= 12:
                    continue
            else:
                count_for_exist = 0
        else:
            count_for_exist = 0
        if count_for_exist > 12:
            print("%s not exist" % job_name)
            aim_job.set_status("Deleted")
            continue
            # break
        # time1 = time.time()
        # print("%s have count_for_exist: %d" % (aim_job.name,count_for_exist))
        pod_items = aim_job.cluster_agent.v1.list_namespaced_pod(job_name).items
        # print("%s have pod items: %s" % (aim_job.name, pod_items))
        masters = {}
        workers = {}
        pod_list = {}

        if tasks['adjustment'] and job_name in tasks['adjust_aim']:
            count_for_attempt_assign = 0
            global_lock.acquire()
            tmp_adjusting_list = tasks['adjusting']
            global_lock.release()
            print(tmp_adjusting_list)
            if job_name not in tmp_adjusting_list.keys():
                global_lock.acquire()
                tasks['adjust_aim'] = []
                global_lock.release()
            else:
                # 开始进行调整
                aim_job.set_status("Adjusting")
                global_lock.acquire()
                adjust_config = tasks['adjusting'][job_name]
                global_lock.release()
                print("adjusting config:")
                print(adjust_config)
                ready_to_adjust_resource= False
                ready_to_adjust_replicas= False
                assignment_resource_done = False
                assingment_replicas_done = False
                count_for_attempt_assign = 0
                new_cpu = aim_job.cpu_allocate
                new_mem = aim_job.memory_allocate
                if "cpu_allocate" in adjust_config.keys() or "mem_allocate" in adjust_config.keys():
                    if "cpu_allocate" in adjust_config.keys():
                        if adjust_config['cpu_allocate'] != new_cpu:
                            ready_to_adjust_resource = True
                    if "mem_allocate" in adjust_config.keys():
                        if adjust_config['mem_allocate'] != new_mem:
                            ready_to_adjust_resource = True
                else:
                    assignment_resource_done = True
                if "master_replicas" in adjust_config.keys() or "worker_replicas" in adjust_config.keys():
                    if "master_replicas" in adjust_config.keys():
                        if adjust_config['master_replicas'] != aim_job.master_replicas:
                            ready_to_adjust_replicas = True
                    if "worker_replicas" in adjust_config.keys():
                        if adjust_config['worker_replicas'] != aim_job.worker_replicas:
                            ready_to_adjust_replicas = True
                else:
                    assignment_resource_done = True
                while True:
                    response = None
                    write_items, status, reason = generate_item(response, pod_status_reason, job_name, pod="",
                                                                timestamp=None,
                                                                status_lock=status_lock, measurement=measurement,
                                                                rank=-1,
                                                                node="null", status=aim_job.status)
                    print("start to write adjusting montior to database")
                    client.write_points(write_items, 's', database="podCpu")
                    print("write adjusting montior to database")
                    if ready_to_adjust_resource and not assignment_resource_done:
                        OK_resource, logs = aim_job.assignment_resource(cpu_source=new_cpu, memory_source=new_mem)
                        if OK_resource:
                            assignment_resource_done = True
                    if ready_to_adjust_replicas and not assingment_replicas_done:
                        OK_replicas, actual_master, actual_worker, logs = aim_job.assign_replicas(
                            adjust_config['master_replicas'], adjust_config['worker_replicas'])
                        if OK_replicas:
                            assingment_replicas_done = True
                        print("adjust replicas: %s" % OK_replicas)

                    if assingment_replicas_done and assingment_replicas_done:
                        break
                    else:
                        count_for_attempt_assign += 1
                        if count_for_attempt_assign >= 4:
                            break
                        time.sleep(12)
                print("OK to adjust: resource: %s replicas: %s" % (assignment_resource_done,assingment_replicas_done))
                global_lock.acquire()
                tasks['adjust_aim'] = []
                tmp_adjusting_list = tasks['adjusting']
                if job_name in tmp_adjusting_list.keys():
                    tmp_adjusting_list.pop(job_name)
                tasks['adjusting'] = tmp_adjusting_list
                aim_job.set_status("Running")
                global_lock.release()

        if not pod_items:
            print("%s is {}" % aim_job.name)
            if aim_job.status not in ["Adjusting","Failed","Finished",'Succeeded',"Deleted"]:
                aim_job.set_status("Failed")
                aim_job.save_job_logs("Do not have replicas!!")
                response = None
                write_items, status, reason = generate_item(response, pod_status_reason, job_name,pod="", timestamp=None,
                                                            status_lock=status_lock, measurement=measurement,
                                                            rank=-1,
                                                            node="null", status=aim_job.status)
                client.write_points(write_items, 's', database="podCpu")
                count_for_error += 1
            elif aim_job.status in ["Failed",'Succeeded']:
                response = None
                write_items, status, reason = generate_item(response, pod_status_reason, job_name, pod="",
                                                            timestamp=None,
                                                            status_lock=status_lock, measurement=measurement,
                                                            rank=-1,
                                                            node="null", status=aim_job.status)
                client.write_points(write_items, 's', database="podCpu")
                count_for_error += 1
            elif aim_job.status in ["Finished","Adjusting"]:
                print("%s(finish):%s" % (aim_job.name,aim_job.status))
                time.sleep(6)
                continue
            if aim_job.status in ['Deleted']:
                break
        else:
            aim_job.set_status("Running")
        for i in pod_items:
            pod_name = i.metadata.name
            pod_metas = pod_name.split("-")
            if "master" in pod_metas:
                masters[pod_name] = int(pod_metas[-1])
            else:
                workers[pod_name] = int(pod_metas[-1])
            pod_list[i.metadata.name]={'status':i.status.phase,'rank':0,'node':i.spec.node_name}

        for pod in masters.keys():
            pod_list[pod]['rank'] = masters[pod]
        num_of_master  = len(list(masters.keys()))
        for pod in workers.keys():
            pod_list[pod]['rank'] = num_of_master + workers[pod]
        num_of_workers = len(list(workers.keys()))
        # def generate_item(response,timestamp,measurement="system",rank=0,node='-1'):
        print(pod_list)
        timestamp = ""
        pod_status_list = {}
        for pod_name in pod_list.keys():
            # namespaces/knative-eventing/pods
            url = "https://172.16.20.190:6443/apis/metrics.k8s.io/v1beta1/namespaces/%s/pods/%s" % (
                job_name, pod_name)
            response = catch_message(url)
            print(response)

            if pod_list[pod_name]['rank'] == 0:
                try:
                    timestamp = response['metadata']['creationTimestamp']
                except Exception as e:
                    timestamp = None
            node_on = "null"
            try:
                node_on = aim_job.cluster_agent.node_to_id[pod_list[pod_name]['node']]
            except Exception as e0:
                node_on = "null"
            write_items,status,reason = generate_item(response, pod_status_reason, job_name, pod_name, timestamp,status_lock=status_lock,measurement=measurement, rank=pod_list[pod_name]['rank'],
                              node=node_on, status=pod_list[pod_name]['status'],mode=1)
            client.write_points(write_items, 's', database="podCpu")
            print("write into database")
            if status not in pod_status_list.keys():
                pod_status_list[status] = {}
            if reason not in pod_status_list[status].keys():
                pod_status_list[status][reason] = [pod_name]
            else:
                pod_status_list[status][reason].append(pod_name)
            print(pod_status_list)
        # print(time.time() - time1)
        # print(tasks['reason'])
        # 1.是否调整
        # 2.若调整，则进行调整
        # 3.若非调整：
        # 若均在run则返回即可
        # 若出现错误，判断错误是否删除任务
        print(pod_status_list)
        if (tasks['adjustment'] == False) or job_name not in tasks['adjust_aim']:
            pod_status_set = list(pod_status_list.keys())
            if len(pod_status_set) == 1 and "Running" in pod_status_set:
                count_for_error = 0
                reason_set = list(pod_status_list['Running'].keys())
                total_num = 0
                for j in reason_set:
                    total_num += len(pod_status_list["Running"][j])
                if total_num == aim_job.worker_replicas + aim_job.master_replicas:
                    aim_job.set_status("Running")
                    aim_job.save_job_logs("job is running")
                    # time.sleep(duration)
                else:
                    # 若数量不同步，则动态调整为相应配置
                    if len(reason_set) == 1 and 'Running' in reason_set:
                        aim_job.assign_replicas(master_n=num_of_master, worker_n=num_of_workers, mode=1)
                    # 若出现错误或者完成则稍后会变为其他状态不需要管理

            if ("Failed" in pod_status_set or 'Succeeded' in pod_status_list):
                count_for_error += 1
                if "Succeeded" in pod_status_set:
                    aim_job.set_status("Succeeded")
                else:
                    aim_job.set_status("Failed")

        if count_for_error > 10:
            aim_job.delete_tf(mode=1)
            aim_job.set_status("Finished")
            global_lock.acquire()
            tmp_adjusting_list = tasks['adjusting']
            if aim_job.name in tmp_adjusting_list.keys():
                tmp_adjusting_list.pop(job_name)
            if aim_job.name in tasks['adjust_aim']:
                tasks['adjust_aim'] = []
            global_lock.release()
        print("%s count for error is %d" % (job_name,count_for_error))
        time.sleep(duration)
            # Now we just realize the CPU and RAM monitor for the kube-system
            # After Submitting module finish, we will use this code to monitor all the Pytorch job namespace

# 三、响应式交互部分：
# 1.发布服务：
# job_config: 指出job的相关配置参数,
# 该函数为响应式：将job放入缓冲队列即可
def Submit_job(job_config,tasks,global_lock,schedule_lock,schedule_jobs,task_id=-1):
    new_id = task_id
    if new_id < 0:
        global_lock.acquire()
        tmp_id = tasks['global_id']
        new_id = tmp_id
        tmp_id = tmp_id + 1
        tasks['global_id'] = tmp_id
        global_lock.release()
        job_name,job_start_time,job_config2 = submit_save_job_config(job_raw_config=job_config, task_id=new_id)
        print(job_config2)
        schedule_lock.acquire()
        if job_name not in schedule_jobs.keys():
            schedule_jobs[job_name] = {"priority":job_config2['priority'],"start":job_start_time}
        schedule_lock.release()
    else:
        # lock.acquire()
        job_name, job_start_time,job_config2 = submit_save_job_config(job_raw_config=job_config, task_id=new_id)
        schedule_lock.acquire()
        if job_name not in schedule_jobs.keys():
            schedule_jobs[job_name] = {"priority": job_config2['priority'], "start": job_start_time}
            scheduling_save_job_config(job_name)
            print(schedule_jobs)
        schedule_lock.release()

    return job_name

# 2.发送调整请求服务：
# 响应式，一旦获得job开始考虑是否进行调整，即判断该任务是否在running中，若正在running那么就放入调整队列开始调整即可
# mode=0, 修改资源量
# mode=1 修改副本数量
# mode=0,cpu_allocate=-1,memory_allocate=-1,master_replicas=1,worker_replicas=1
#将任务放入调整池进行调整即可
# adjust_config: {"cpu_allocate":-1,"mem_allocate":-1,"master_relicas":1,"worker_replicas":1}
def Adjustment_jobs(tasks,global_lock,adjust_config):
    # job_name
    # adjust_confg:{"cpu_allocate":-1,"mem_allocate":-1,"master_replicas":1,"worker_replicas":1}
    # job_name,
    job_name = adjust_config['job_name']
    global_lock.acquire()
    tmp_running_jobs = tasks['running']
    # tmp_scheduling_jobs = tasks['scheduling']
    global_lock.release()
    if job_name not in tmp_running_jobs.keys():
        return False,"job not running" # 若未运行则不需要进行调整。
    else:
        task_id = int(job_name.split("-")[-1].strip())
        adjusting_job = reload_jobs(job_name,task_id)
        global_lock.acquire()
        adjusting_job_list =  tasks['adjusting']
        tmp_adjust_config = {"priority":adjusting_job.priority}
        if job_name in adjusting_job_list.keys():
            adjusting_job_item = adjusting_job_list[job_name]
            for key in adjusting_job_item.keys():
                tmp_adjust_config[key] = adjusting_job_item[key]
        for key in adjust_config.keys():
            tmp_adjust_config[key] = adjust_config[key]
        adjusting_job_list[job_name] = tmp_adjust_config
        tasks['adjusting'] = adjusting_job_list
        global_lock.release()
        return True,"Accepted" #进行调整

# 3. 发送删除请求服务：
#响应式函数，只要判断该任务仍在running列表中,或在scheduled_job中,然后将该任务从running列表中提取出来放入deleting列表中即可
def Delete_job(job_name,tasks,global_lock,schedule_lock,schedule_jobs):
    # job_name
    OK = False
    global_lock.acquire()
    tmp_running_list = tasks['running']
    tmp_scheduling_list = tasks['scheduling']
    tmp_deleting_list = tasks['deleting']
    reason = ""
    if job_name not in tmp_running_list.keys() and job_name not in tmp_scheduling_list.keys():
        OK = False
        reason = "Job not exists"
        # return False,job_name
    elif job_name in tmp_scheduling_list.keys():
        tmp_scheduling_list.pop(job_name)
        schedule_lock.acquire()
        if job_name in schedule_jobs.keys():
            schedule_jobs.pop(job_name)
        schedule_lock.release()
        tasks['scheduling'] = tmp_scheduling_list
        deleted_job = reload_jobs(job_name,-1)
        deleted_job.set_status("Deleted")
        reason = "Deleted Running job"
        OK = True
    elif job_name in tmp_running_list.keys():
        tmp_running_list.pop(job_name)
        tmp_deleting_list.append(job_name)
        tasks['deleting'] = tmp_deleting_list
        tasks['running'] = tmp_running_list
        reason = "Deleted Scheduling job"
        OK = True
    global_lock.release()
    return OK,job_name,reason

# 4.实时获取指定进程状态：
def GetJobStatus(job_name):
    # job_name
    aim_job = reload_jobs(job_name,-1)
    print(aim_job.status)
    return aim_job.status

# 四、后台运行服务进程部分
# 1.具体调度进程：
#可以考虑作为主进程，即获得待运行的工作进行调度即可
def Schedule_job(tasks,global_lock,schedule_lock,schedule_jobs,interval=10):
    cluster_agent = ClusterAgent(node_message_path="/home/NFSshare/PROGECT/global_node.json",gpu_message_path="/home/NFSshare/PROGECT/global_uuid.json")
    cluster_agent.update_node()
    status_id = {"Running": 0, "Failed": 1, "Succeeded": 2, "Pending": 3, "Unknown": 4,"Adjusting":5}
    specific_status = {"Running": {"id": 0, "item": ["Running", "CrashLoopBackOff", "Terminating", "RunContainerError",
                                                     "Unknown", "NodeLost"]},
                       "Failed": {"id": 1,
                                  "item": ["Error", "CrashLoopBackOff", "Terminating", "RunContainerError", "Unknown",
                                           "NodeLost", "Evicted", "OOMKilled", "ContainerCannotRun"]},
                       "Pending":{"id":3,"item":[]},
                       "Succeeded": {"id": 2, "item": ["Completed", "OOMKilled", "Evicted", "Terminating", "Unknown"]},
                       "Unknown": {"id": 4, "item": ["UnKnown"]},
                       "Adjusting":{"id":5,"item":[]}
                       }

    mgr = multiprocessing.Manager()
    pod_status_reason = mgr.dict()
    pod_status_reason['status'] = status_id
    pod_status_reason['reason'] = specific_status
    if os.path.exists("/home/NFSshare/PROGECT/reason.json"):
        old_data = load_config("/home/NFSshare/PROGECT/reason.json")
        if 'status' not in old_data.keys():
            save_config(pod_status_reason,"/home/NFSshare/PROGECT/reason.json")
    else:
        save_config(pod_status_reason, "/home/NFSshare/PROGECT/reason.json")
    pool = multiprocessing.Pool(processes=cluster_agent.total_gpu*2)
    status_lock = mgr.Lock()
    if tasks['init']:
        global_lock.acquire()
        tmp_running_list = tasks['running']
        # def Monitor_job(tasks,pod_status_reason,status_lock,job_name,global_lock,duration=30):
        if list(tmp_running_list.keys()):
            for job_name in tmp_running_list.keys():
                pool.apply_async(Monitor_job, args=(tasks, pod_status_reason, status_lock, job_name, global_lock, 15))
        global_lock.release()
    print("OK to start")
    while True:
        if tasks['start']:
            break
    print("Schedule process start")
    while True:
        if not tasks['start']:
            time.sleep(10)
            if not tasks['start']:
                break
        tmp_jobs = {}
        schedule_lock.acquire()
        for k in schedule_jobs.keys():
            tmp_jobs[k] = {'priority':schedule_jobs[k]['priority'],"start":schedule_jobs[k]["start"]}
        schedule_lock.release()
        print(tmp_jobs)
        global_lock.acquire()
        task_scheduling_list = {}
        for k in tmp_jobs:
            task_scheduling_list[k] = int(tmp_jobs[k]['priority'])
        tasks['scheduling'] = task_scheduling_list
        global_lock.release()
        print(tasks['scheduling'])
        if tasks['adjustment']:
            time.sleep(10)
        else:
            if not tmp_jobs:
                time.sleep(interval)
            else:
                to_schedule_jobs = []
                schedule_queue = {}
                for k in tmp_jobs.keys():
                    if int(tmp_jobs[k]['priority']) not in schedule_queue.keys():
                        schedule_queue[int(tmp_jobs[k]['priority'])] = {}
                    if tmp_jobs[k]['start'] not in schedule_queue[int(tmp_jobs[k]['priority'])].keys():
                        schedule_queue[int(tmp_jobs[k]['priority'])][tmp_jobs[k]['start']] = []
                    schedule_queue[int(tmp_jobs[k]['priority'])][tmp_jobs[k]['start']].append(k)
                levels = list(schedule_queue.keys())
                levels.sort()
                for j in range(len(levels) - 1, -1, -1):
                    start_times = list(schedule_queue[levels[j]].keys())
                    start_times.sort()
                    for t in start_times:
                        for item in schedule_queue[levels[j]][t]:
                            to_schedule_jobs.append(item)

                scheduling_task_id = int(to_schedule_jobs[0].split("-")[-1].strip())
                scheduling_job = reload_jobs(to_schedule_jobs[0], scheduling_task_id)
                try:
                    if scheduling_job.retry > 0:
                        OK, actual_master, actual_worker = scheduling_job.create_tf(checkpoint=True)
                    else:
                        OK, actual_master, actual_worker = scheduling_job.create_tf(checkpoint=False)
                    if OK:
                        scheduling_job.set_status("scheduled")
                        scheduling_job.save_job_logs(action="schedule the job successful")
                        global_lock.acquire()
                        tmp_running_list = tasks['running']
                        tmp_running_list[scheduling_job.name] = scheduling_job.priority
                        tmp_scheduling_list = tasks['scheduling']
                        if scheduling_job.name in tmp_scheduling_list.keys():
                            tmp_scheduling_list.pop(scheduling_job.name)
                        tasks['running'] = tmp_running_list
                        tasks['scheduling'] = tmp_scheduling_list
                        global_lock.release()
                        schedule_lock.acquire()
                        if scheduling_job.name in schedule_jobs.keys():
                            schedule_jobs.pop(scheduling_job.name)
                        schedule_lock.release()
                        # def Monitor_job(tasks,pod_status_reason,status_lock,job_name,global_lock,duration=30):
                        print("Generate a Monitor")
                        pool.apply_async(Monitor_job,args=(tasks,pod_status_reason,status_lock,scheduling_job.name,global_lock,15))
                    if not OK:
                        if actual_master <= 0 or actual_worker <= 0:
                            scheduling_job.save_job_logs(action="do not have enough resources")
                            # continue
                        else:
                            scheduling_job.save_job_logs(action="do not schedule success")
                            # continue
                except Exception as e:
                    print(e)
                    scheduling_job.save_job_logs(action="do not schedule success")
                    # continue
                time.sleep(interval)

# 2. 具体调整过程：
# 包括两个进程：
# 管理进程：1. 监控调整池，判断是否进入调整流程 2.指定当前要调整的任务
# 在每个Monitor_job中进行具体调整：
def AdjustPoolController(tasks,global_lock,interval=10):
    while True:
        if tasks['start']:
            break
    while True:
        if not tasks['start']:
            time.sleep(10)
            if not tasks['start']:
                break
        global_lock.acquire()
        tmp_ruunning_list = tasks['running']
        tmp_adjusting_list = tasks['adjusting']
        tmp_scheduling_list = tasks['scheduling']
        adjusting_jobs = list(tmp_adjusting_list.keys())
        scheduling_jobs = list(tmp_scheduling_list.keys())
        running_jobs = list(tmp_ruunning_list.keys())
        tmp_adjusting_levels = {}
        tmp_scheduling_levels = {}
        for job in adjusting_jobs:
            if job not in running_jobs:
                tmp_adjusting_list.pop(job)
            else:
                if tmp_adjusting_list[job]['priority'] not in tmp_adjusting_levels.keys():
                    tmp_adjusting_levels[tmp_adjusting_list[job]['priority']] = []
                tmp_adjusting_levels[tmp_adjusting_list[job]['priority']].append(job)
        # print()
        if not tmp_adjusting_list.keys() or not tmp_ruunning_list.keys():
            tasks['adjustment'] = False
            tasks['adjust_aim'] = []
        else:
            if not scheduling_jobs:
                tasks['adjustment'] = True
            else:
                for job in scheduling_jobs:
                    if tmp_scheduling_list[job] not in tmp_scheduling_levels.keys():
                        tmp_scheduling_levels[tmp_scheduling_list[job]] = []
                    tmp_scheduling_levels[tmp_scheduling_list[job]].append(job)
                if max(list(tmp_adjusting_levels.keys())) < max(list(tmp_scheduling_levels.keys())):
                    tasks['adjustment'] = False
                else:
                    tasks['adjustment'] = True
            # if tasks
            tmp_now_aim_adjustment = tasks['adjust_aim']
            print("not tmp_now_aim_adjustment: %s" % (not tmp_now_aim_adjustment))
            if not tmp_now_aim_adjustment:
                selecting_aims_levels = list(tmp_adjusting_levels.keys())
                print("selecting_aims_levels: %s" % selecting_aims_levels)
                if selecting_aims_levels:
                    if tmp_adjusting_levels[max(selecting_aims_levels)]:
                        tmp_now_aim_adjustment = [tmp_adjusting_levels[max(selecting_aims_levels)][0]]
                tasks['adjust_aim'] = tmp_now_aim_adjustment
        global_lock.release()
        print("adjust aim is :%s"% tasks['adjust_aim'])
        print(tmp_adjusting_levels)
        time.sleep(interval)

#3.实时备份当前任务日志信息：
def LogClsuterMessage(tasks,global_lock,scheduled_lock,schedule_jobs,interval=90):
    while True:
        if tasks['start']:
            break
    while True:
        if not tasks['start']:
            time.sleep(10)
            if not tasks['start']:
                break
        global_lock.acquire()
        save_config(tasks,"/home/NFSshare/PROGECT/system_info.json")
        global_lock.release()
        scheduled_lock.acquire()
        save_config(schedule_jobs,"/home/NFSshare/PROGECT/scheduling.json")
        scheduled_lock.release()
        print(schedule_jobs)
        time.sleep(interval)

def list_config_dir(base_path='/home/NFSshare/PROGECT/conf'):
    data_list = os.listdir(base_path)
    data_list = list(data_list)
    return data_list

# main 函数中为服务器端
def server_socket_function(conn):
    legal_aim = {"submit":['priority', 'image_name', 'training_config_file', 'master_replicas', 'worker_replicas', 'cpu_allocate', 'mem_allocate', 'backend', 'num_workers', 'gpu_monitor_interval', 'gpu_monitor_failure', 'pin_memory'],"end":[],"start":[],"adjust":['job_name', 'cpu_allocate', 'mem_allocate', 'master_replicas', 'worker_replicas'],"select":['level', 'job_name'],"delete":['job_name']}
    while True:
        msg_from_client = conn.recv(4096)
        msg_from_client_str = str(msg_from_client.decode('utf-8'))
        if msg_from_client_str in legal_aim:
            res_message = "200@Connected"
            conn.send(bytes(res_message, 'utf-8'))
            break
        else:
            res_message = "403@wrong funciton"
            conn.send(bytes(res_message, 'utf-8'))
            return "", {}
    msg_from_client = conn.recv(4096)
    response = {}
    try:
        msg_from_client_str = str(msg_from_client.decode('utf-8'))
    except Exception as e:
        msg_from_client_str = ""
    if not msg_from_client_str:
        response['code'] = 403
        response['reason'] = "not receive message"
        response_json = json.dumps(response)
        conn.send(bytes(response_json, 'utf-8'))
        return "",{}
    request_dict  = ast.literal_eval(msg_from_client_str)
    # for k,v in request_dict.items():
    aim = request_dict['aim']
    request_dict.pop("aim")
    request_key = list(request_dict.keys())
    if aim not in legal_aim.keys():
        response['code'] = 404
        response['reason'] = "do not find the aim page"
        response_json = json.dumps(response)
        conn.send(bytes(response_json, 'utf-8'))
        return "",{}
    else:
        for k in request_key:
            if k not in legal_aim[aim]:
                request_dict.pop(k)
        return aim,request_dict
        # msg_from_client = conn.recv(4096)
        # try_times = try_times + 1

        # msg_from_client_str = str(msg_from_client.decode('utf-8'))

if __name__ == '__main__':
    SERVER_HOST = '172.16.20.190'
    SERVER_PORT = 14527
    SERVER_ADDR = (SERVER_HOST,SERVER_PORT)
    cluster_agent = ClusterAgent(node_message_path="/home/NFSshare/PROGECT/global_node.json",gpu_message_path="/home/NFSshare/PROGECT/global_uuid.json")
    cluster_agent.update_node()
    # cluster_agent.node_resource
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    args = parse()
    # v1.list_node()
    mgr = multiprocessing.Manager()
    tasks = mgr.dict()
    tasks['init'] = True
    global_lock = mgr.Lock()
    schedule_lock = mgr.Lock()
    schedule_jobs = mgr.dict()
    if not os.path.exists('/home/NFSshare/PROGECT/system_info.json'):
        config_content = {}
    else:
        config_content = load_config('/home/NFSshare/PROGECT/system_info.json')
    if not os.path.exists("/home/NFSshare/PROGECT/scheduling.json"):
        schedule_jobs_content = {}
    else:
        schedule_jobs_content = load_config("/home/NFSshare/PROGECT/scheduling.json")
    for key,value in config_content.items():
        tasks[key] = value
    for key,value in schedule_jobs_content.items():
        schedule_jobs[key] = value
    print(tasks)
    print(schedule_jobs)
    if not config_content:
        tasks['running'] = {}
        tasks['scheduling'] = {}
        tasks['deleting'] = []
        tasks['adjustment'] = False
        tasks['adjust_aim'] = []
        tasks['adjusting'] = {}
        tasks['creation'] = []
        tasks['global_id'] = 6
        tasks['endtime']= []

    tasks['size'] = args.pool_size
    tasks['start'] = True
    if not os.path.exists('/home/NFSshare/PROGECT/system_info.json'):
        save_config(tasks,'/home/NFSshare/PROGECT/system_info.json')
    if not os.path.exists("/home/NFSshare/PROGECT/scheduling.json"):
        save_config(schedule_jobs,"/home/NFSshare/PROGECT/scheduling.json")

    # Monitor_job(tasks,lock,v1,jobs)
    # def Schedule_job(tasks,global_lock,schedule_lock,schedule_jobs,interval=10):
    scheuldle_process = multiprocessing.Process(target=Schedule_job,args=(tasks,global_lock,schedule_lock,schedule_jobs,10))
    # AdjustPoolController(tasks,global_lock,interval=10)
    adjust_controller_p = multiprocessing.Process(target=AdjustPoolController,args=(tasks,global_lock,15))
    # def LogClsuterMessage(tasks,global_lock,scheduled_lock,schedule_jobs,interval=90):
    log_cluster_p = multiprocessing.Process(target=LogClsuterMessage, args=(tasks,global_lock,schedule_lock,schedule_jobs,90))

    # scheuldle_process.daemon = True
    adjust_controller_p.daemon = True
    log_cluster_p.daemon = True

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDR)
    server.listen(5)
    if tasks['start']:
        time_open = math.ceil(time.time())
        tmp_list = tasks["creation"]
        tasks['start'] = True
        tmp_list.append(time_open)
        tasks["creation"] = tmp_list
        scheuldle_process.start()
        adjust_controller_p.start()
        log_cluster_p.start()
    while True:
        # 1. 前后端交互：
        conn, addr = server.accept()
        aim,request = server_socket_function(conn)
        print("get connection...")
        if not aim:
            conn.close()
            continue
        else:
            if aim == "start":
                if not tasks['start']:
                    time_open = math.ceil(time.time())
                    tmp_list = tasks["creation"]
                    tasks['start'] = True
                    tmp_list.append(time_open)
                    tasks["creation"] = tmp_list
                    scheuldle_process.start()
                    adjust_controller_p.start()
                    log_cluster_p.start()
                    response = {}
                    response['code'] = 202
                    response['reason'] = "Accepted and Started!"
                    response_json = json.dumps(response)
                    print(response)
                    conn.send(bytes(response_json, 'utf-8'))
                    conn.close()
                else:
                    response = {}
                    response['code'] = 405
                    response['reason'] = "has already started"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, 'utf-8'))
                    conn.close()
                    continue
            if aim == "end":
                if tasks['start']:
                    tasks['start'] = False
                    response = {}
                    response['code'] = 202
                    response['reason'] = "Accepted and Stopped!"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, 'utf-8'))
                    conn.close()
                    time.sleep(10)
                    scheuldle_process.join()
                    adjust_controller_p.join()
                    log_cluster_p.join()
                    time_last = math.ceil(time.time())
                    tmp_list = tasks['endtime']
                    tmp_list.append(time_last)
                    tasks["endtime"] = tmp_list
                    save_config(tasks, "/home/NFSshare/PROGECT/system_info.json")
                    save_config(schedule_jobs, "/home/NFSshare/PROGECT/scheduling.json")
                    print('System end!')
                    break
                else:
                    response = {}
                    response['code'] = 405
                    response['reason'] = "has already started"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, 'utf-8'))
                    conn.close()
            if aim == "submit":
                job_raw_config = {}
                if "image_name" not in request.keys() and "training_config_file" not in request.keys():
                    response = {}
                    response['code'] = 404
                    response['reason'] = "Do not find the image and the config"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
                elif "image_name" not in request.keys():
                    response = {}
                    response['code'] = 404
                    response['reason'] = "Do not find the image"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
                elif "training_config_file" not in request.keys():
                    response = {}
                    response['code'] = 404
                    response['reason'] = "Do not find the config"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
                else:
                    print(request)
                    for k, v in request.items():
                        job_raw_config[k] = v
                        if k == 'priority':
                            job_raw_config[k] = int(v)
                        if k == "master_replicas":
                            job_raw_config[k] = int(v)
                        if k == "worker_replicas":
                            job_raw_config[k] = int(v)
                        if k == "cpu_allocate":
                            job_raw_config[k] = int(v)
                        if k == "mem_allocate":
                            job_raw_config[k] = int(v)
                        if k == "num_workers":
                            job_raw_config[k] = int(v)
                        if k == "gpu_monitor_interval":
                            job_raw_config[k] = float(v)
                        if k == "gpu_monitor_failure":
                            job_raw_config[k] = int(v)
                        if k == "pin_memory":
                            if int(request['pin_memory']):
                                job_raw_config[k] = True
                            else:
                                job_raw_config[k] = False
                    response_job_name = Submit_job(job_raw_config, tasks, global_lock, schedule_lock, schedule_jobs)
                    submit_configs = load_job_messages(job_name=response_job_name)
                    if "pin_memory" in submit_configs:
                        if submit_configs["pin_memory"]:
                            submit_configs["pin_memory"] = 1
                        else:
                            submit_configs["pin_memory"] = 0
                    submit_configs['code'] = 202
                    submit_configs['reason'] = "Submit a job"
                    response_json = json.dumps(submit_configs)
                    conn.send(bytes(response_json, 'utf-8'))
                    conn.close()
            if aim == "adjust":
                adjust_config = {}
                if "job_name" not in request.keys():
                    response = {}
                    response['code'] = 404
                    response['reason'] = "Do not find the aim job"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
                else:
                    adjust_config['job_name'] = request['job_name']
                    for k, v in request.items():
                        if k == 'job_name':
                            adjust_config['job_name'] = request['job_name']
                        else:
                            adjust_config[k] = int(v)
                    print(adjust_config)
                    OK, reason = Adjustment_jobs(tasks, global_lock, adjust_config)
                    if OK:
                        response = {}
                        response['code'] = 202
                        response['reason'] = reason
                        for k, v in adjust_config.items():
                            response[k] = v
                        response_json = json.dumps(response)
                        conn.send(bytes(response_json, "utf-8"))
                        conn.close()
                    else:
                        response = {}
                        response['code'] = 403
                        response['reason'] = reason
                        response_json = json.dumps(response)
                        conn.send(bytes(response_json, "utf-8"))
                        conn.close()
            if aim == "delete":
                OK, job_name, reason = Delete_job(request['job_name'], tasks, global_lock, schedule_lock,
                                                  schedule_jobs)
                if OK:
                    response = {}
                    response['code'] = 202
                    response['reason'] = reason
                    response['job_name'] = job_name
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
                else:
                    response = {}
                    response['code'] = 404
                    response['reason'] = reason
                    response['job_name'] = job_name
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
            if aim == "select":
                level = int(request['level'])
                if level == 0:
                    job_message = load_job_messages(request['job_name'])
                    if not job_message:
                        response = {}
                        response['code'] = 404
                        response['reason'] = "Job Do not exists"
                        response_json = json.dumps(response)
                        conn.send(bytes(response_json, "utf-8"))
                        conn.close()
                    else:
                        response = {}
                        response['code'] = 202
                        response['reason'] = "Accepted"
                        for k, v in job_message.items():
                            response[k] = v
                            if k == "pin_memory":
                                if job_message['pin_memory']:
                                    response[k] = 1
                                else:
                                    response[k] = 0
                        response_json = json.dumps(response)
                        conn.send(bytes(response_json, "utf-8"))
                        conn.close()
                else:
                    tmp_cluster_tasks = get_cluster_tasks(tasks, global_lock)
                    response = {}
                    if not tmp_cluster_tasks:
                        response['code'] = 404
                        response['reason'] = "Do not find cluster"
                    else:
                        for k, v in tmp_cluster_tasks.items():
                            response[k] = v
                        response['code'] = 202
                        response['reason'] = "find the cluster"
                    response_json = json.dumps(response)
                    conn.send(bytes(response_json, "utf-8"))
                    conn.close()
            # try:
            # except Exception as e2:
            #     print(e2)
            #     continue

        # boots = input("Please Input 'start' to start:\n")
        # if boots == 'start':
        #     time_open = math.ceil(time.time())
        #     tmp_list = tasks["creation"]
        #     tasks['start'] = True
        #     tmp_list.append(time_open)
        #     tasks["creation"] = tmp_list
        #     scheuldle_process.start()
        #     adjust_controller_p.start()
        #     log_cluster_p.start()
        #
        # if boots == 'submit':
        #     print(tasks)
        #     job_config = {"priority":0,
        #           "image_name":'172.16.20.190:5000/wenet-k8s-torch:7.4',
        #           "training_config_file":"train_conformer.yaml",
        #           "master_replicas":1,
        #           "worker_replicas":1,
        #           "cpu_allocate":-1,
        #           "mem_allocate":-1,
        #           "backend":"nccl",
        #           "num_workers":2,
        #           "gpu_monitor_interval":30.0,
        #           "gpu_monitor_failure":15,
        #           "pin_memory":True,
        #           "template_name": "exp",
        #           "task_id": -1,
        #           "retry": 0,
        #           "status": "initial"
        #           }
        #     Submit_job(job_config,tasks,global_lock,schedule_lock,schedule_jobs)
        # if boots == 'delete':
        #     print(tasks)
        #     tmp_running_list = tasks['running']
        #     # tmp_running_list_keys = list()
        #     if not tmp_running_list.keys():
        #         continue
        #     else:
        #         aim_tasks = {}
        #         tmp_running_list_keys = list(tmp_running_list.keys())
        #         for k in tmp_running_list_keys:
        #             names = k.split("-")
        #             aim_tasks[int(names[-1])] = k
        #         ids = list(aim_tasks.keys())
        #         ids.sort()
        #         job_name = aim_tasks[ids[0]]
        #         Delete_job(job_name=job_name,tasks=tasks,global_lock=global_lock,schedule_lock=schedule_lock,schedule_jobs=schedule_jobs)
        # if boots == 'adjust':
        #     print(tasks)
        #     tmp_running_list = tasks['running']
        #     # tmp_running_list_keys = list()
        #     if not tmp_running_list.keys():
        #         continue
        #     else:
        #         aim_tasks = {}
        #         tmp_running_list_keys = list(tmp_running_list.keys())
        #         for k in tmp_running_list_keys:
        #             names = k.split("-")
        #             aim_tasks[int(names[-1])] = k
        #         ids = list(aim_tasks.keys())
        #         ids.sort()
        #         job_name = aim_tasks[ids[0]]
        #         aim_job = reload_jobs(job_name,-1)
        #         if aim_job.worker_replicas < 3:
        #             adjust_config = {"worker_replicas":aim_job.worker_replicas+1}
        #         else:
        #             adjust_config = {"worker_replicas": aim_job.worker_replicas - 1}
        #         Adjustment_jobs(tasks=tasks,global_lock=global_lock,job_name=job_name,adjust_config=adjust_config)
        # if boots == 'end':
        #     tasks['start'] = False
        #     time.sleep(10)
        #     scheuldle_process.join()
        #     adjust_controller_p.join()
        #     log_cluster_p.join()
        #     time_last = math.ceil(time.time())
        #     tmp_list = tasks['endtime']
        #     tmp_list.append(time_last)
        #     tasks["endtime"] = tmp_list
        #     save_config(tasks, "/home/NFSshare/PROGECT/system_info.json")
        #     save_config(schedule_jobs,"/home/NFSshare/PROGECT/scheduling.json")
        #     print('System end!')
        #     break