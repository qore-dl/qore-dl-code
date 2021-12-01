#https://blog.csdn.net/orangefly0214/article/details/81387077
import MultiTemplate
from MultiTemplate import TaskTemplate,SATemplate
from pytz import UTC
from dateutil.parser import parse
import pandas as pd
import re

from datetime import datetime
import os
from subprocess import PIPE,Popen

EPOCH = UTC.localize(datetime.utcfromtimestamp(0))
import numpy as np
# https://blog.csdn.net/u013812710/article/details/72886491
# https://blog.csdn.net/ismr_m/article/details/53100896
#https://blog.csdn.net/bcfdsagbfcisbg/article/details/78134172
import kubernetes
import os
import json
import math
import influxdb
import time
import re
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor
# # from random_job3 import save_job_change_layout
# from random_job3 import save_job_change_resource

import yaml

node_index = {'Good1':1,'Good2':2,'Good3':3,'Norm1':4,'Norm2':5}
node_measure = {'izbp10smzw7rg0ih27wbl3z':'Good 1','izbp11dpzwhp6pia1tyr3kz':'Good 2','izbp11ycujbqzxrpj66jksz':'Good 3',
                'izbp156pkpio477f5f2tf6z':'Norm 1','izbp156pkpio477f5f2tf8z': 'Norm 2','izbp179ga4nl6y5b59bmphz': 'Master'}
node_name = {'izbp10smzw7rg0ih27wbl3z':'Good1','izbp11dpzwhp6pia1tyr3kz':'Good2','izbp11ycujbqzxrpj66jksz':'Good3',
                'izbp156pkpio477f5f2tf6z':'Norm1','izbp156pkpio477f5f2tf8z': 'Norm2','izbp179ga4nl6y5b59bmphz': 'Master'}
node_ip = {'izbp10smzw7rg0ih27wbl3z': '172.16.190.92','izbp11dpzwhp6pia1tyr3kz': '172.16.190.91','izbp11ycujbqzxrpj66jksz': '172.16.190.90',
           'izbp156pkpio477f5f2tf6z': '172.16.190.93','izbp156pkpio477f5f2tf8z': '172.16.190.96','izbp179ga4nl6y5b59bmphz': '172.16.190.97'}

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
    f.close()
    return config_content

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

def transtime(t):
    timestamp = parse(t)
    # print(EPOCH)
    # print(timestamp)
    if not timestamp.tzinfo:
        # print("XXX")
        timestamp = UTC.localize(timestamp)

    s = (timestamp - EPOCH).total_seconds()
    return s

def gpu_sch_base():
    influx_client = influxdb.InfluxDBClient(host='172.16.190.97', port=8086, username='admin', password='admin',
                                            database='NODEGPU')
    global node_measure,node_ip,node_index,node_name
    node_list = list(node_measure.keys())
    gpu_using = {}
    for node in node_list:
        gpu_using[node] = {}
        result = influx_client.query("select * from "+node_name[node]+" order by desc limit 20")
        res_key = list(result.keys())
        res_key0 = res_key[0]
        result_items = list(result[res_key0])
        item_keys = list(result_items[0].keys())
        item_number = len(result_items)
        for item_key in item_keys:
            gpu_using[node][item_key] = []
            if 'time' in item_key:
                for i in range(item_number):
                    gpu_using[node][item_key].append(transtime(result_items[i][item_key]))
            else:
                for i in range(item_number):
                    gpu_using[node][item_key].append(result_items[result_items[i][item_key]])
    legal = 'gpu\d+\w+'
    gpu_output = {}
    for node in node_list:
        for item_key in item_keys:
            matched = re.match(legal,item_key)
            if matched:
                gpu_output[node][item_key] = np.max(gpu_using[node][item_key][0])
            else:
                gpu_output[node][item_key] = gpu_using[node][item_key][0]
    return gpu_output







            #
            #     gpu_using[node][item_key] = []
            # else:
            #     gpu_using[node][item_key] = [result_items[0][]]

def deletehelp(delete_job_name,v1):
    try:
        v1.delete_namespace(delete_job_name)
    except Exception as eeeeee:
        print(eeeeee)
        command0 = "kubectl get namespace " + delete_job_name + " -o json > /data/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
        os.system(command0)
        tmp = load_config("/data/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        tmp["spec"]["finalizers"] = []
        save_config(tmp, "/data/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        try:
            command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/data/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/'+delete_job_name+'/finalize'
            os.system(command1)
        except Exception as helpe:
            print(helpe)
            commandopen = 'kubectl proxy --port=8081'
            os.system(commandopen)
            os.system(command1)

def deletehelp2(delete_job_name,v1):
    v1.delete_namespace(delete_job_name)
    try:
        command0 = "kubectl get namespace " + delete_job_name + " -o json > /data/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
        os.system(command0)
        tmp = load_config("/data/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        tmp["spec"]["finalizers"] = []
        save_config(tmp, "/data/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        try:
            command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/data/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
            os.system(command1)
        except Exception as helpe:
            print(helpe)
            commandopen = 'kubectl proxy --port=8081'
            os.system(commandopen)
            os.system(command1)
            raise
    except Exception as overe:
        print(overe)
        return

def check_path(name):
    '/ data / tfdata / k8snfs / vgg - 2 - 2'
    train_dir = os.path.join('/data/tfdata/k8snfs/', name)
    print(train_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    return train_dir



def save_job_change_layout(job_name,ps_n,worker_n):
    save_job_path = '/data/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    job_config = load_config(save_job_path)
    # 'ps_replicas': job.ps_replicas,'worker_replicas': job.worker_replicas
    job_config['ps_replicas'] = ps_n
    job_config['worker_replicas'] = worker_n
    save_config(job_config, save_job_path)

def save_job_change_resource(job_name,cpu_allocate,mem_allocate):
    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    # save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
    # save_config(job_config, save_job_path)
    job_res_config['cpu_source'] = cpu_allocate
    job_res_config['mem_source'] = mem_allocate
    save_config(job_res_config, save_res_path)

def check_ns(name):
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # v1.create_namespace()
    exist_ns = v1.list_namespace()
    exist_ns_name = []
    for i in exist_ns.items:
        exist_ns_name.append(i.metadata.name)
    if name in exist_ns_name:
        return True
    else:
        return False

class clusternode():
    def __init__(self,name,total_cpu,total_memory,compute_label,disk_label):
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.compute_label = compute_label
        self.disk_label = disk_label
        self.name = name


class SubTask():
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,
                 dbhost='172.16.190.97', retry=0, update_min_step=400, step_update=20, update_start=0.25,
                 update_end=0.9, update_delay=2.0,save_step = 5000,num_epochs=300,write_step=50,part=1,freq=5.0):
        self.template_id = template_id
        self.ps_replicas = ps_replicas
        self.worker_replicas = worker_replicas
        self.training_step = training_step
        self.interval = interval
        self.batch_size = batch_size
        self.task_id = task_id
        self.tag = tag
        self.rtimes = rtimes
        self.dbhost = dbhost
        self.freq = freq
        self.part = part
        self.real_batch = math.ceil(self.batch_size/self.part)
        self.retry = retry
        kubernetes.config.load_kube_config()
        self.v1 = kubernetes.client.CoreV1Api()
        # self.v1.list_namespace()
        self.update_min_step = update_min_step
        self.save_step = save_step
        self.write_step = write_step
        self.num_epochs = num_epochs

        self.step_update = step_update
        self.update_start = update_start
        self.update_end = update_end
        self.update_delay = update_delay
        self.influx_client = influxdb.InfluxDBClient(host='172.16.190.97',port=8086,username='admin',password='admin',database="NODEMESSAGE")
        self.batch_client = influxdb.InfluxDBClient(host='172.16.190.97',port=8086,username='admin',password='admin',database='BATCH')
        self.pre_client = influxdb.InfluxDBClient(host='172.16.190.97',port=8086,username='admin',password='admmin',database='PREDICT')
        self.node_list = ["izbp10smzw7rg0ih27wbl3z",
        "izbp11dpzwhp6pia1tyr3kz",
        "izbp11ycujbqzxrpj66jksz",
        "izbp156pkpio477f5f2tf6z",
        "izbp156pkpio477f5f2tf8z",
        "izbp179ga4nl6y5b59bmphz"]
        self.node_index = {'Good1': 1, 'Good2': 2, 'Good3': 3, 'Norm1': 4, 'Norm2': 5}
        self.node_measure = {'izbp10smzw7rg0ih27wbl3z': 'Good 1', 'izbp11dpzwhp6pia1tyr3kz': 'Good 2',
                        'izbp11ycujbqzxrpj66jksz': 'Good 3',
                        'izbp156pkpio477f5f2tf6z': 'Norm 1', 'izbp156pkpio477f5f2tf8z': 'Norm 2',
                        'izbp179ga4nl6y5b59bmphz': 'Master'}
        self.node_name = {'izbp10smzw7rg0ih27wbl3z': 'Good1', 'izbp11dpzwhp6pia1tyr3kz': 'Good2',
                     'izbp11ycujbqzxrpj66jksz': 'Good3',
                     'izbp156pkpio477f5f2tf6z': 'Norm1', 'izbp156pkpio477f5f2tf8z': 'Norm2',
                     'izbp179ga4nl6y5b59bmphz': 'Master'}
        self.node_ip = {'izbp10smzw7rg0ih27wbl3z': '172.16.190.92', 'izbp11dpzwhp6pia1tyr3kz': '172.16.190.91',
                   'izbp11ycujbqzxrpj66jksz': '172.16.190.90',
                   'izbp156pkpio477f5f2tf6z': '172.16.190.93', 'izbp156pkpio477f5f2tf8z': '172.16.190.96',
                   'izbp179ga4nl6y5b59bmphz': '172.16.190.97'}

        self.node_cpu = {}

        # self.node_compute = {}


        self.cpu_allocate = 1000
        self.memory_allocate = 2048

        self.node_cmtype = {}
        self.deadline = 3600
        self.starttime = 0
        self.node_list = ["izbp10smzw7rg0ih27wbl3z",
                          "izbp11dpzwhp6pia1tyr3kz",
                          "izbp11ycujbqzxrpj66jksz",
                          "izbp156pkpio477f5f2tf6z",
                          "izbp156pkpio477f5f2tf8z",
                          "izbp179ga4nl6y5b59bmphz"]
        self.gpu_node_list = ["izbp10smzw7rg0ih27wbl3z",
                          "izbp11dpzwhp6pia1tyr3kz",
                          "izbp11ycujbqzxrpj66jksz",
                          "izbp156pkpio477f5f2tf6z",
                          "izbp156pkpio477f5f2tf8z"]
        # self.lasttime =
        self.node_cpu["izbp10smzw7rg0ih27wbl3z"] = 32000 - 500   #132025460Ki
        self.node_cpu["izbp11dpzwhp6pia1tyr3kz"] = 32000 - 500  #132025460Ki
        self.node_cpu["izbp11ycujbqzxrpj66jksz"] = 32000 - 4800 #132025460Ki
        self.node_cpu["izbp156pkpio477f5f2tf6z"] = 8000 - 3000 # 32939400Ki
        self.node_cpu["izbp156pkpio477f5f2tf8z"] = 8000 - 500  #32939400Ki
        self.node_cpu["izbp179ga4nl6y5b59bmphz"] = 40000 - 4500 #194969644Ki

        self.total_cpu = 0
        self.total_mem = 0.0
        self.node_memory = {}

        self.node_memory["izbp10smzw7rg0ih27wbl3z"] = float(125 * 1024 - 320)
        self.node_memory["izbp11dpzwhp6pia1tyr3kz"] = float(125 * 1024 - 300)
        self.node_memory["izbp11ycujbqzxrpj66jksz"] = float(125 * 1024 - 4500)
        self.node_memory["izbp156pkpio477f5f2tf6z"] = float(31 * 1024 - 900)
        self.node_memory["izbp156pkpio477f5f2tf8z"] = float(31 * 1024 - 400)
        self.node_memory['izbp179ga4nl6y5b59bmphz'] = float(185 * 1024 - 4800)

        self.total_gpu = 14
        self.node_gpu = {}
        self.node_gpu["izbp10smzw7rg0ih27wbl3z"] = 4
        self.node_gpu["izbp11dpzwhp6pia1tyr3kz"] = 4
        self.node_gpu["izbp11ycujbqzxrpj66jksz"] = 4
        self.node_gpu["izbp156pkpio477f5f2tf6z"] = 1
        self.node_gpu["izbp156pkpio477f5f2tf8z"] = 1
        self.node_gpu['izbp179ga4nl6y5b59bmphz'] = 0
        
        node_keys = self.node_cpu.keys()
        for key in node_keys:
            self.total_cpu = self.total_cpu + self.node_cpu[key]
            self.total_mem = self.total_mem + self.node_memory[key]

        self.args = ['--training_step='+str(self.training_step),'--batch_size='+str(self.real_batch),'--interval='+str(self.interval),'--task_id='+str(self.task_id),'--rtimes='+str(self.rtimes),"--tag="+self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--num_epochs='+str(self.num_epochs),
                     '--save_step='+str(self.save_step),
                     '--write_step='+str(self.write_step),
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay),
                     '--freq='+str(self.freq),
                     '--num_gpus=1'
                     ]

    def set_deadline(self,deadline,start_time):
        self.deadline = deadline
        self.starttime = start_time

    def set_batch(self,batch,part2):
        self.batch_size = batch
        self.part = part2
        self.real_batch = math.ceil(self.batch_size / self.part)

    def set_resource(self,cpu_source,mem_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = mem_source



    #
    # def apply_tf(self,cpu_source,mem_source):
    #     self.cpu_allocate = cpu_source
    #     self.memory_allocate = mem_source
    def update_batch(self):
        batch_influx = influxdb.InfluxDBClient(host=self.dbhost,port=8086,username='admin',password='admin',database='BATCH')
        pre_list = self.measure.split(" ")
        # measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_b = pre_list[0] + 'B' + pre_list[-1]
        batch_items = [
            {
                'measurement': measure_b,
                'tags': {
                    'task': self.task_id,
                    'runtimes': self.rtimes,
                    'retry': self.retry
                },
                'fields': {
                    'batch': self.real_batch,
                    'part': self.part,
                    'base': self.batch_size
                }
            }
        ]
        batch_influx.write_points(batch_items, time_precision="ms", database="BATCH")

    def reload_count(self,reload):
        reload_influx = influxdb.InfluxDBClient(host=self.dbhost, port=8086, username='admin', password='admin',
                                               database='RELOAD')
        pre_list = self.measure.split(" ")
        # measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_b = pre_list[0] + 'D' + pre_list[-1]
        batch_items = [
            {
                'measurement': measure_b,
                'tags': {
                    'task': self.task_id,
                    'runtimes': self.rtimes,
                    'retry': self.retry
                },
                'fields': {
                   'reload': float(reload)
                }
            }
        ]
        reload_influx.write_points(batch_items, time_precision="ms", database='RELOAD')


    def update_step(self):
        step_update_influx = influxdb.InfluxDBClient(host=self.dbhost, port=8086, username='admin', password='admin',
                                                     database="PREDICT")

        pre_list = self.measure.split(" ")
        # measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_up = pre_list[0] + 'U' + pre_list[-1]

        step_items = [
            {
                'measurement': measure_up,
                'tags': {
                    'task': self.task_id,
                    'runtimes': self.rtimes,
                    'retry': self.retry
                },
                'fields': {
                    'ps': self.ps_replicas,
                    'worker':self.worker_replicas,
                    'num_gpu': self.part,
                    'training_step': self.training_step
                }
            }
        ]
        # print(step_to_train)
        step_update_influx.write_points(step_items, time_precision="ms", database="PREDICT")



    def select_k8s_gpu(self,mode=0):
        node_list = self.gpu_node_list[:]

        influx_client = influxdb.InfluxDBClient(host='172.16.190.97', port=8086, username='admin', password='admin',
                                                database="NODEGPU")
        k8s_des_gpu = {}
        for node in node_list:
            resutl = os.popen('kubectl describe nodes '+node+' | grep nvidia.com/gpu')
            kkk = (resutl.read().strip()).split('\n')
            kk0 = []
            for k in kkk:
                k1 = k.strip()
                k2 = re.sub(r'[\s][\s]*', ',', k1)
                k3 = k2.split(',')
                kk0.append(k3)
            if node not in list(k8s_des_gpu.keys()):
                k8s_des_gpu[node] = {}
            k8s_des_gpu[node]['total'] = int(kk0[0][-1])
            k8s_des_gpu[node]['allocated'] = int(kk0[-1][-1])
            k8s_des_gpu[node]['avail'] = k8s_des_gpu[node]['total'] - k8s_des_gpu[node]['allocated']

        if mode == 0:
            k8s_mon_gpu = {}
            for node in node_list:
                if node not in list(k8s_mon_gpu.keys()):
                    k8s_mon_gpu[node] = {}
                result = influx_client.query("select * from "+self.node_name[node]+" order by desc limit 20")
                if not result:
                    continue
                res_key0 = list(result.keys())
                result_item = list(result[res_key0[0]])
                # print("test items:")
                # print(result_item)
                k8s_mon_gpu[node]['total'] = result_item[0]['total']
                k8s_mon_gpu[node]['avail'] = result_item[0]['avail']
                length = len(result_item)
                item_keys = (result_item[0]).keys()
                gpu_using = {}
                gpu_mem = {}
                gpu_ids = {}
                if 'Good' in self.node_name[node]:
                    gpu_using_out = []
                    gpu_mem_out = []
                    for i in range(4):
                        gpu_mem[i] = []
                        gpu_using[i] = []
                        gpu_id = 'gpu%d' % i
                        gpu_id_u = 'gpu%du' % i
                        gpu_id_m = 'gpu%dm' % i

                        for j in range(length):
                            if result_item[j][gpu_id]:
                                if result_item[j][gpu_id]>0:
                                    gpu_using[i].append(result_item[j][gpu_id_u])
                                    gpu_mem[i].append(result_item[j][gpu_id_m])
                    good_k = list(gpu_using.keys())

                    for gk in good_k:
                        if gk is not None:
                            if result_item[0]['gpu%d' % int(gk)]:
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])] = {}
                    gpu_ids_key = list(gpu_ids.keys())
                    if -1 not in gpu_ids_key:
                        gpu_ids[-1] = {}
                    for gk in good_k:
                        if not gpu_using[gk]:
                            gpu_ids[-1]['uti'] = 0
                            gpu_ids[-1]['mem'] = 0
                            gpu_ids[-1]['base'] = 0
                        else:
                            gpu_using_out.append(max(gpu_using[gk]))
                            gpu_mem_out.append(max(gpu_mem[gk]))
                            if gk is not None:
                                if result_item[0]['gpu%d' % int(gk)]:
                                    gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['uti'] = max(gpu_using[gk])/100
                                    gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['mem'] = max(gpu_mem[gk])/16160
                                    gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['base'] = 0.7 * max(gpu_using[gk])/100 + 0.3 * max(gpu_mem[gk])/16160
                            else:
                                gpu_ids[-1]['uti'] = 0
                                gpu_ids[-1]['mem'] = 0
                                gpu_ids[-1]['base'] = 0
                    if not gpu_using_out:
                        k8s_mon_gpu[node]['uti'] = 0
                        k8s_mon_gpu[node]['mem'] = 0
                        k8s_mon_gpu[node]['base'] = 0
                    else:
                        k8s_mon_gpu[node]['uti'] = (np.mean(gpu_using_out) / 100)
                        k8s_mon_gpu[node]['mem'] = (np.mean(gpu_mem_out) / 16160)
                        k8s_mon_gpu[node]['base'] = 0.7 * k8s_mon_gpu[node]['uti'] + 0.3 * k8s_mon_gpu[node]['mem']
                    k8s_mon_gpu[node]['pid'] = gpu_ids
                else:
                    gpu_using[0] = []
                    gpu_mem[0] = []
                    gpu_id = 'gpu0'
                    gpu_id_u = 'gpu0u'
                    gpu_id_m = 'gpu0m'
                    # print(result_item)
                    for j in range(length):
                        if result_item[j][gpu_id]:
                            if result_item[j][gpu_id] > 0:
                                gpu_using[0].append(result_item[j][gpu_id_u])
                                gpu_mem[0].append(result_item[j][gpu_id_m])

                    if not gpu_using[0]:
                        k8s_mon_gpu[node]['uti'] = 0
                        k8s_mon_gpu[node]['mem'] = 0
                    else:
                        k8s_mon_gpu[node]['uti'] = (max(gpu_using[0]) / 100)
                        k8s_mon_gpu[node]['mem'] = (max(gpu_mem[0]) / 16160)
                    k8s_mon_gpu[node]['base'] = 0.7 * k8s_mon_gpu[node]['uti'] + 0.3 * k8s_mon_gpu[node]['mem']
                    if result_item[0][gpu_id]:
                        gpu_ids[int(result_item[0][gpu_id])] = {'uti':k8s_mon_gpu[node]['uti'],'mem':k8s_mon_gpu[node]['mem'],'base':k8s_mon_gpu[node]['base']}
                    else:
                        gpu_ids[-1] = {'uti':0,'mem':0,'base':0}
                    k8s_mon_gpu[node]['pid'] = gpu_ids
            des_key = list(k8s_des_gpu.keys())
            mon_key = list(k8s_mon_gpu.keys())
            true_node = list(set(des_key).intersection(set(mon_key)))
            k8s_out_put_gpu = {}
            differnece = list(set(node_list).difference(set(true_node)))
            print(differnece)
            if differnece:
                for noed in node_list:
                    if noed in differnece:
                        k8s_out_put_gpu[noed]['total'] = k8s_des_gpu[noed]['total']
                        k8s_out_put_gpu[noed]['avail'] = k8s_des_gpu[noed]['avail']
                        k8s_out_put_gpu[noed]['uti'] = 1
                        k8s_out_put_gpu[noed]['mem'] = 1
                        k8s_out_put_gpu[noed]['base'] = 1
                        k8s_out_put_gpu[noed]['pid'] = {}
                    else:
                        if k8s_des_gpu[noed]['total'] < k8s_mon_gpu[noed]['total']:
                            k8s_out_put_gpu[noed]['total'] = k8s_des_gpu[noed]['total']
                        else:
                            k8s_out_put_gpu[noed]['total'] = k8s_mon_gpu[noed]['total']

                        if k8s_des_gpu[noed]['avail'] < k8s_mon_gpu[noed]['avail']:
                            k8s_out_put_gpu[noed]['avail'] = k8s_des_gpu[noed]['avail']
                        else:
                            k8s_out_put_gpu[noed]['avail'] = k8s_mon_gpu[noed]['avail']

                        k8s_out_put_gpu[noed]['uti'] = k8s_mon_gpu[noed]['uti']
                        k8s_out_put_gpu[noed]['mem'] = k8s_mon_gpu[noed]['mem']
                        k8s_out_put_gpu[noed]['base'] = k8s_mon_gpu[noed]['base']
                        k8s_out_put_gpu[noed]['pid'] = k8s_mon_gpu[noed]['pid']
            else:
                for node in true_node:
                    if node not in list(k8s_out_put_gpu.keys()):
                        k8s_out_put_gpu[node] = {}
                    try:
                        if k8s_des_gpu[node]['total'] < k8s_mon_gpu[node]['total']:
                            k8s_out_put_gpu[node]['total'] = k8s_des_gpu[node]['total']
                        else:
                            k8s_out_put_gpu[node]['total'] = k8s_mon_gpu[node]['total']
                    except:
                        k8s_out_put_gpu[node]['total'] = k8s_des_gpu[node]['total']
                    try:
                        if k8s_des_gpu[node]['avail'] < k8s_mon_gpu[node]['avail']:
                            k8s_out_put_gpu[node]['avail'] = k8s_des_gpu[node]['avail']
                        else:
                            k8s_out_put_gpu[node]['avail'] = k8s_mon_gpu[node]['avail']
                    except:
                        k8s_out_put_gpu[node]['avail'] = k8s_des_gpu[node]['avail']
                    try:
                        k8s_out_put_gpu[node]['uti'] = k8s_mon_gpu[node]['uti']
                        k8s_out_put_gpu[node]['mem'] = k8s_mon_gpu[node]['mem']
                        k8s_out_put_gpu[node]['base'] = k8s_mon_gpu[node]['base']
                        k8s_out_put_gpu[node]['pid'] = k8s_mon_gpu[node]['pid']
                    except:
                        k8s_out_put_gpu[node]['uti'] = 1
                        k8s_out_put_gpu[node]['mem'] = 1
                        k8s_out_put_gpu[node]['base'] = 1
                        k8s_out_put_gpu[node]['pid'] = {}

            # return k8s_mon_gpu
            avail_dict = {}
            avail = []
            node_index = {}
            index_node = []
            for node in node_list:
                # avail_dict[int(k8s_out_put_gpu[node]['avail'])] = node
                avail.append(int(k8s_out_put_gpu[node]['avail']))
            # status = pd.value_counts(avail)
            # status = dict(status)
            # print(status)
            # status_key = list(status.keys())
            # avail_base = [int(s) for s in status_key]
            # print(avail)
            avail_base = list(set(avail))

            list.sort(avail_base, reverse=True)
            print(avail_base)
            for av in avail_base:
                avail_dict[av] = {}
                # avail_dict[av]['base'] = []

            for node in node_list:
                avail_dict[int(k8s_out_put_gpu[node]['avail'])][float(k8s_out_put_gpu[node]['base'])] = []
                # avail_dict[int(k8s_out_put_gpu[node]['avail'])]['base'].append(float(k8s_out_put_gpu[node]['base']))
            for node in node_list:
                avail_dict[int(k8s_out_put_gpu[node]['avail'])][float(k8s_out_put_gpu[node]['base'])].append(node)
            print(avail_dict)
            for av in avail_base:
                tmp_list = list(avail_dict[av].keys())
                list.sort(tmp_list)
                for p in tmp_list:
                    for node in avail_dict[av][p]:
                        index_node.append(node)
            index = 0
            print(index_node)
            for node in index_node:
                node_index[node] = index
                index+=1
            print(node_index)
            print(k8s_out_put_gpu)
            print(index_node)
            return node_index,k8s_out_put_gpu,index_node
        else:
            offset = int(mode)
            k8s_outputs = []
            node_index_total = []
            index_node_total = []
            for p in range(offset):
                pianyi = p*20
                k8s_mon_gpu = {}
                for node in node_list:
                    if node not in list(k8s_mon_gpu.keys()):
                        k8s_mon_gpu[node] = {}
                    result = influx_client.query("select * from " + self.node_name[node] + " order by desc limit 20 offset "+str(pianyi))
                    if not result:
                        continue
                    res_key0 = list(result.keys())
                    result_item = list(result[res_key0[0]])
                    k8s_mon_gpu[node]['total'] = result_item[0]['total']
                    k8s_mon_gpu[node]['avail'] = result_item[0]['avail']
                    length = len(result_item)
                    item_keys = (result_item[0]).keys()
                    gpu_using = {}
                    gpu_mem = {}
                    gpu_ids = {}
                    if 'Good' in self.node_name[node]:
                        gpu_using_out = []
                        gpu_mem_out = []
                        for i in range(4):
                            gpu_mem[i] = []
                            gpu_using[i] = []
                            gpu_id = 'gpu%d' % i
                            gpu_id_u = 'gpu%du' % i
                            gpu_id_m = 'gpu%dm' % i
                            for j in range(length):
                                if result_item[j][gpu_id] > 0:
                                    gpu_using[i].append(result_item[j][gpu_id_u])
                                    gpu_mem[i].append(result_item[j][gpu_id_m])
                        good_k = gpu_using.keys()
                        for gk in good_k:
                            gpu_ids[int(result_item[0]['gpu%d' % int(gk)])] = {}
                        for gk in good_k:
                            if not gpu_using[gk]:
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['uti'] = 0
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['mem'] = 0
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['base'] = 0
                            else:
                                gpu_using_out.append(max(gpu_using[gk]))
                                gpu_mem_out.append(max(gpu_mem[gk]))
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['uti'] = max(gpu_using[gk]) / 100
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['mem'] = max(gpu_mem[gk]) / 16160
                                gpu_ids[int(result_item[0]['gpu%d' % int(gk)])]['base'] = 0.7 * max(
                                    gpu_using[gk]) / 100 + 0.3 * max(gpu_mem[gk]) / 16160
                        if not gpu_using_out:
                            k8s_mon_gpu[node]['uti'] = 0
                            k8s_mon_gpu[node]['mem'] = 0
                            k8s_mon_gpu[node]['base'] = 0
                        else:
                            k8s_mon_gpu[node]['uti'] = (np.mean(gpu_using_out) / 100)
                            k8s_mon_gpu[node]['mem'] = (np.mean(gpu_mem_out) / 16160)
                            k8s_mon_gpu[node]['base'] = 0.7 * k8s_mon_gpu[node]['uti'] + 0.3 * k8s_mon_gpu[node]['mem']
                        k8s_mon_gpu[node]['pid'] = gpu_ids
                    else:
                        gpu_using[0] = []
                        gpu_mem[0] = []
                        gpu_id = 'gpu0'
                        gpu_id_u = 'gpu0u'
                        gpu_id_m = 'gpu0m'
                        for j in range(length):
                            if result_item[j][gpu_id] > 0:
                                gpu_using[0].append(result_item[j][gpu_id_u])
                                gpu_mem[0].append(result_item[j][gpu_id_m])

                        if not gpu_using[0]:
                            k8s_mon_gpu[node]['uti'] = 0
                            k8s_mon_gpu[node]['mem'] = 0
                        else:
                            k8s_mon_gpu[node]['uti'] = (max(gpu_using[0]) / 100)
                            k8s_mon_gpu[node]['mem'] = (max(gpu_mem[0]) / 16160)
                        k8s_mon_gpu[node]['base'] = 0.7 * k8s_mon_gpu[node]['uti'] + 0.3 * k8s_mon_gpu[node]['mem']
                        gpu_ids[int(result_item[0][gpu_id])] = {'uti': k8s_mon_gpu[node]['uti'],
                                                                'mem': k8s_mon_gpu[node]['mem'],
                                                                'base': k8s_mon_gpu[node]['base']}
                        k8s_mon_gpu[node]['pid'] = gpu_ids
                des_key = list(k8s_des_gpu.keys())
                mon_key = list(k8s_mon_gpu.keys())
                true_node = list(set(des_key).intersection(set(mon_key)))
                k8s_out_put_gpu = {}
                differnece = list(set(node_list).difference(set(true_node)))
                print(differnece)
                if differnece:
                    for noed in node_list:
                        if noed in differnece:
                            k8s_out_put_gpu[noed]['total'] = k8s_des_gpu[noed]['total']
                            k8s_out_put_gpu[noed]['avail'] = k8s_des_gpu[noed]['avail']
                            k8s_out_put_gpu[noed]['uti'] = 1
                            k8s_out_put_gpu[noed]['mem'] = 1
                            k8s_out_put_gpu[noed]['base'] = 1
                            k8s_out_put_gpu[noed]['pid'] = {}
                        else:
                            if k8s_des_gpu[noed]['total'] < k8s_mon_gpu[noed]['total']:
                                k8s_out_put_gpu[noed]['total'] = k8s_des_gpu[noed]['total']
                            else:
                                k8s_out_put_gpu[noed]['total'] = k8s_mon_gpu[noed]['total']

                            if k8s_des_gpu[noed]['avail'] < k8s_mon_gpu[noed]['avail']:
                                k8s_out_put_gpu[noed]['avail'] = k8s_des_gpu[noed]['avail']
                            else:
                                k8s_out_put_gpu[noed]['avail'] = k8s_mon_gpu[noed]['avail']

                            k8s_out_put_gpu[noed]['uti'] = k8s_mon_gpu[noed]['uti']
                            k8s_out_put_gpu[noed]['mem'] = k8s_mon_gpu[noed]['mem']
                            k8s_out_put_gpu[noed]['base'] = k8s_mon_gpu[noed]['base']
                            k8s_out_put_gpu[noed]['pid'] = k8s_mon_gpu[noed]['pid']
                else:
                    for node in true_node:
                        if node not in list(k8s_out_put_gpu.keys()):
                            k8s_out_put_gpu[node] = {}
                        if k8s_des_gpu[node]['total'] < k8s_mon_gpu[node]['total']:
                            k8s_out_put_gpu[node]['total'] = k8s_des_gpu[node]['total']
                        else:
                            k8s_out_put_gpu[node]['total'] = k8s_mon_gpu[node]['total']

                        if k8s_des_gpu[node]['avail'] < k8s_mon_gpu[node]['avail']:
                            k8s_out_put_gpu[node]['avail'] = k8s_des_gpu[node]['avail']
                        else:
                            k8s_out_put_gpu[node]['avail'] = k8s_mon_gpu[node]['avail']

                        k8s_out_put_gpu[node]['uti'] = k8s_mon_gpu[node]['uti']
                        k8s_out_put_gpu[node]['mem'] = k8s_mon_gpu[node]['mem']
                        k8s_out_put_gpu[node]['base'] = k8s_mon_gpu[node]['base']
                        k8s_out_put_gpu[node]['pid'] = k8s_mon_gpu[node]['pid']

                # return k8s_mon_gpu
                avail_dict = {}
                avail = []
                node_index = {}
                index_node = []
                for node in node_list:
                    # avail_dict[int(k8s_out_put_gpu[node]['avail'])] = node
                    avail.append(int(k8s_out_put_gpu[node]['avail']))
                # status = pd.value_counts(avail)
                # status = dict(status)
                # print(status)
                # status_key = list(status.keys())
                # avail_base = [int(s) for s in status_key]
                # print(avail)
                avail_base = list(set(avail))

                list.sort(avail_base, reverse=True)
                print(avail_base)
                for av in avail_base:
                    avail_dict[av] = {}
                    # avail_dict[av]['base'] = []

                for node in node_list:
                    avail_dict[int(k8s_out_put_gpu[node]['avail'])][float(k8s_out_put_gpu[node]['base'])] = []
                    # avail_dict[int(k8s_out_put_gpu[node]['avail'])]['base'].append(float(k8s_out_put_gpu[node]['base']))
                for node in node_list:
                    avail_dict[int(k8s_out_put_gpu[node]['avail'])][float(k8s_out_put_gpu[node]['base'])].append(node)
                print(avail_dict)
                for av in avail_base:
                    tmp_list = list(avail_dict[av].keys())
                    list.sort(tmp_list)
                    for p in tmp_list:
                        for node in avail_dict[av][p]:
                            index_node.append(node)
                index = 0
                print(index_node)
                for node in index_node:
                    node_index[node] = index
                    index += 1
                print(node_index)
                print(k8s_out_put_gpu)
                print(index_node)
                node_index_total.append(node_index)
                k8s_outputs.append(k8s_out_put_gpu)
                index_node_total.append(index_node)
            return node_index_total,k8s_outputs,index_node_total









    def schedule_base(self,mode=0):
        if mode == 0:
            result = self.influx_client.query(
                "select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 8")
            node_list = self.get_node_list()

            result_keys = result.keys()
            nodes = [i[-1]['nodes'] for i in result_keys]
            node_mg = [list(result[i]) for i in result_keys]
            cpu_base = {}
            memory_base = {}
            point_base = {}
            point_base_list = []
            # memory_base_list = []
            # cpu_base_list = []
            node_index = {}
            # total_cpu = 0
            # total_mem = 0
            total_cpu_use = 0.0
            total_mem_use = 0.0
            for i in range(len(node_mg)):
                cpu_base[nodes[i]] = 0
                memory_base[nodes[i]] = 0
                point_base[nodes[i]] = 0.0
                for j in range(len(node_mg[0])):
                    cpu_base[nodes[i]] += node_mg[i][j]['cpu']
                    memory_base[nodes[i]] += node_mg[i][j]['memory']
                cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
                memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
                total_cpu_use += (cpu_base[nodes[i]] * self.node_cpu[nodes[i]])
                total_mem_use += (memory_base[nodes[i]] * self.node_memory[nodes[i]])
                tmp = cpu_base[nodes[i]] * 0.675 + memory_base[nodes[i]] * 0.325
                point_base[nodes[i]] = tmp
                point_base_list.append(tmp)

            total_cpu_use = total_cpu_use / self.total_cpu
            total_mem_use = total_mem_use / self.total_mem

            list.sort(point_base_list)

            for key in nodes:
                #     command = 'kubectl label nodes ' + key + ' woksch-'
                #     os.system(command)
                #     command2 = 'kubectl label nodes ' + key + ' wokpro-'
                #     os.system(command2)
                nod_prori = point_base_list.index(point_base[key])
                node_index[key] = nod_prori
            #     priori = ' wokpro=%d' % nod_prori
            #     command3 = 'kubectl label nodes ' + key + priori
            #     os.system(command3)
            #     if cpu_base[key] <= 0.56 and memory_base[key] <= 0.6:
            #         command = 'kubectl label nodes ' + key + ' woksch=true'
            #         os.system(command)
            #     else:
            #         command = 'kubectl label nodes ' + key + ' woksch=false'
            #         os.system(command)



            return node_index, cpu_base, memory_base, total_cpu_use, total_mem_use
        else:
            offset = int(mode)
            cpu_base_total = []
            memory_base_total = []
            node_index_total = []
            total_cpu_use_total = []
            total_mem_use_total = []
            for k in range(offset):
                pianyi = k*8
                result = self.influx_client.query(
                    "select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 8 offset "+str(pianyi))
                result_keys = result.keys()
                nodes = [i[-1]['nodes'] for i in result_keys]
                node_mg = [list(result[i]) for i in result_keys]
                cpu_base = {}
                memory_base = {}
                point_base = {}
                point_base_list = []
                node_index = {}
                total_cpu_use = 0.0
                total_mem_use = 0.0
                for i in range(len(node_mg)):
                    cpu_base[nodes[i]] = 0
                    memory_base[nodes[i]] = 0
                    point_base[nodes[i]] = 0.0
                    for j in range(len(node_mg[0])):
                        cpu_base[nodes[i]] += node_mg[i][j]['cpu']
                        memory_base[nodes[i]] += node_mg[i][j]['memory']
                    cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
                    memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
                    total_cpu_use += (cpu_base[nodes[i]] * self.node_cpu[nodes[i]])
                    total_mem_use += (memory_base[nodes[i]] * self.node_memory[nodes[i]])
                    tmp = cpu_base[nodes[i]] * 0.78 + memory_base[nodes[i]] * 0.22
                    point_base[nodes[i]] = tmp
                    point_base_list.append(tmp)
                total_cpu_use = total_cpu_use / self.total_cpu
                total_mem_use = total_mem_use / self.total_mem

                list.sort(point_base_list)

                for key in nodes:
                    nod_prori = point_base_list.index(point_base[key])
                    node_index[key] = nod_prori

                # return node_index, cpu_base, memory_base, total_cpu_use, total_mem_use
                node_index_total.append(node_index)
                cpu_base_total.append(cpu_base)
                memory_base_total.append(memory_base)
                total_cpu_use_total.append(total_cpu_use)
                total_mem_use_total.append(total_mem_use)

            return node_index_total,cpu_base_total,memory_base_total,total_cpu_use_total,total_mem_use_total

    def write_retry(self,mode):
        write_retry_influx = influxdb.InfluxDBClient(host=self.dbhost, port=8086, username='admin', password='admin',
                                                     database="PREDICT")

        pre_list = self.measure.split(" ")
        # measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_write = pre_list[0] + 'W' + pre_list[-1]

        step_items = [
            {
                'measurement': measure_write,
                'tags': {
                    'task': self.task_id,
                    'runtimes': self.rtimes,
                    'retry': self.retry
                },
                'fields': {
                    'modulate': int(mode)
                }
            }
        ]
        # print(step_to_train)
        write_retry_influx.write_points(step_items, time_precision="ms", database="PREDICT")


    def schedule_label(self):
        result = self.influx_client.query("select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 8")
        node_list = self.get_node_list()
        result_keys = result.keys()
        nodes = [i[-1]['nodes'] for i in result_keys]
        node_mg = [list(result[i]) for i in result_keys]
        cpu_base = {}
        memory_base = {}
        point_base = {}
        point_base_list = []
        # memory_base_list = []
        # cpu_base_list = []
        # node_index = {}
        # total_cpu = 0
        # total_mem = 0
        # total_cpu_use = 0.0
        # total_mem_use = 0.0
        for i in range(len(node_mg)):
            cpu_base[nodes[i]] = 0
            memory_base[nodes[i]] = 0
            point_base[nodes[i]] = 0.0
            for j in range(len(node_mg[0])):
                cpu_base[nodes[i]] += node_mg[i][j]['cpu']
                memory_base[nodes[i]] += node_mg[i][j]['memory']
            cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
            memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
            # total_cpu_use += (cpu_base[nodes[i]]*self.node_cpu[nodes[i]])
            # total_mem_use += (memory_base[nodes[i]]*self.node_memory[nodes[i]])
            tmp = cpu_base[nodes[i]] * 0.78 + memory_base[nodes[i]] * 0.22
            point_base[nodes[i]] = tmp
            point_base_list.append(tmp)



        # total_cpu_use = total_cpu_use / self.total_cpu
        # total_mem_use = total_mem_use /self.total_mem


        list.sort(point_base_list)
        gpu_index, gpu_monitor,gpu_index_node = self.select_k8s_gpu(mode=0)
        gpu_nodes = list(gpu_index.keys())
        for gn in gpu_nodes:
            command = 'kubectl label nodes ' + gn + ' gpusch-'
            os.system(command)
            command2 = 'kubectl label nodes ' + gn + ' gpupro-'
            os.system(command2)
            gpriori = ' gpupro=%d' % int(gpu_index[gn])
            command3 = 'kubectl label nodes ' + gn + gpriori
            os.system(command3)
            if gpu_monitor[gn]['avail'] >= 1:
                command4 = 'kubectl label nodes ' +gn + ' gpusch=true'
                os.system(command4)
            else:
                command4 = 'kubectl label nodes ' + gn + ' gpusch=false'
                os.system(command4)

        for key in nodes:
            command = 'kubectl label nodes ' + key + ' cpusch-'
            os.system(command)
            command2 = 'kubectl label nodes ' + key + ' cpupro-'
            os.system(command2)
            nod_prori = point_base_list.index(point_base[key])
            # node_index[key] = nod_prori
            priori = ' cpupro=%d' % nod_prori
            command3 = 'kubectl label nodes ' + key + priori
            os.system(command3)
            if cpu_base[key] <= 0.42 and memory_base[key] <= 0.6:
                command = 'kubectl label nodes ' + key + ' cpusch=true'
                os.system(command)
            else:
                command = 'kubectl label nodes ' + key + ' cpusch=false'
                os.system(command)

        # return node_index,cpu_base,memory_base,total_cpu_use,total_mem_use






class VGGTask(SubTask):
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,channel1,channel2,channel3,channel4,channel5,num_layer1,num_layer2,num_layer3,num_layer4,num_layer5,kernel,unit1,unit2,dbhost='172.16.190.97', retry=0, update_min_step=1000, step_update=20, update_start=0.25,
                 update_end=0.9, update_delay=2.0,save_step=5000,num_epochs=300,write_step=50,part=1,freq=5.0):
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,dbhost,retry,update_min_step,step_update,update_start,update_end,update_delay)
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag)
        SubTask.__init__(self,template_id,ps_replicas=ps_replicas,worker_replicas=worker_replicas,training_step=training_step,
                         batch_size=batch_size,interval=interval,task_id=task_id,rtimes=rtimes,tag=tag,dbhost=dbhost,retry=retry,
                         update_min_step=update_min_step,step_update=step_update,update_start=update_start,update_end=update_end,update_delay=update_delay,save_step=save_step,num_epochs=num_epochs,write_step=write_step,part=part,freq=freq)


        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.channel4 = channel4
        self.channel5 = channel5
        self.num_layer1 = num_layer1
        self.num_layer2 = num_layer2
        self.num_layer3 = num_layer3
        self.num_layer4 = num_layer4
        self.num_layer5 = num_layer5
        self.num_layers = num_layer1+num_layer2+num_layer3+num_layer4+num_layer5+3
        self.template = TaskTemplate.VGG
        self.kernel = kernel
        self.unit1 = unit1
        self.unit2 = unit2
        # self.v1 = v1
        self.serviceaccount = SATemplate.SA
        self.role = SATemplate.BIND
        self.name = 'vgg-'+str(self.task_id)+'-'+str(self.rtimes)
        self.rolename = 'vgg-'+str(self.task_id)+'-'+str(self.rtimes)+'-reader'
        self.bindname = 'vgg-'+str(self.task_id)+'-'+str(self.rtimes)+'-bind'
        self.measure = "VGG %d" % self.task_id


    def get_node_list(self):
        node_list = [i.metadata.name for i in self.v1.list_node().items]
        return node_list

    def make_args(self):
        self.args.append('--channel1='+str(self.channel1))
        self.args.append('--channel2='+str(self.channel2))
        self.args.append('--channel3='+str(self.channel3))
        self.args.append('--channel4='+str(self.channel4))
        self.args.append('--channel5='+str(self.channel5))
        self.args.append('--num_layer1='+str(self.num_layer1))
        self.args.append('--num_layer2='+str(self.num_layer2))
        self.args.append('--num_layer3='+str(self.num_layer3))
        self.args.append('--num_layer4='+str(self.num_layer4))
        self.args.append('--num_layer5='+str(self.num_layer5))
        self.args.append('--num_layers='+str(self.num_layers))
        self.args.append('--kernel='+str(self.kernel))
        self.args.append('--unit1='+str(self.unit1))
        self.args.append('--unit2='+str(self.unit2))

    def get_remain(self, mode=0):
        filepath = '/data/tfdata/k8snfs/' + self.name + '/worker0/'
        file_list = os.listdir(filepath)
        step_influx = influxdb.InfluxDBClient(host=self.dbhost, port=8086, username='admin', password='admin',
                                              database="PREDICT")
        pre_list = self.measure.split(" ")
        measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_t = pre_list[0] + 'T' + pre_list[-1]
        result = step_influx.query("select training_step from " + measure_t + " order by desc limit 1")
        key = result.keys()
        result_inter = result[key[0]]
        result_items = list(result_inter)
        trains_step = result_items[0]['training_step']
        total_step = int(trains_step)
        atmp = 0
        if mode == 0:
            step = []
            for i in file_list:
                if 'model.ckpt' in i and 'meta' in i:
                    tmp = re.findall(r'\d+', i)
                    step.append(int(tmp[0]))
                    # tiqv.append(i)
            if not step:
                atmp = 0
            else:
                atmp = max(step)
        else:
            res = step_influx.query("select * from " + measure_s + " group by nodes,retry order by desc limit 1")
            res_key = list(res.keys())
            # keys = res.keys()
            if res_key:
                retry_time = [int(b['retry']) for a, b in res_key]
                retry_time = set(retry_time)
                retry = max(retry_time)
                # node_list = [b['nodes'] for a, b in keys]
                node_list = [b['nodes'] for a, b in res_key]
                dic_msg = {}
                for node in node_list:
                    for i in range(len(res_key)):
                        _, no = res_key[i]
                        if no['nodes'] == node and int(no['retry']) == retry:
                            dic_msg[node] = list(res[res_key[i]])
                step_list = []
                node_key = list(dic_msg.keys())
                # print(res_key)
                # print(retry)
                for node in node_key:
                    step_list.append(int(dic_msg[node][0]['step']))
                if not step_list:
                    atmp = 0
                else:
                    atmp = min(step_list)
            else:
                atmp = 0
            # for node in node_list:
            #     for i in range(len(keys)):
            #         _, no = keys[i]
            #         if no['nodes'] == node:
            #             dic_msg[node] = list(res[keys[i]])
        remain = total_step - atmp + 2
        if remain <= 0:
            remain = 0

        return remain,total_step,atmp

    def predict_min(self,rfr):
        # inputmem = open('rfr_batch.pkl', 'rb')
        # s2 = pickle.dump(rfr_batch, outputmem)
        # # est_gpu = pickle.load(inputgpu)
        # est_mem = pickle.load(inputmem)
        # mse_mem = mean_squared_error(y_gpu_test, est_mem.predict(X_gpu_test))
        job_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        # job_config = load_config(job_path)
        pre_list = self.measure.split(' ')
        measurement_b = '%sB%d' % (pre_list[0],self.task_id)
        measurement_t = "%sS%d" % (pre_list[0],self.task_id)
        result = self.batch_client.query("select * from " + measurement_b + " order by desc limit 1")
        res_key = list(result.keys())
        res_item = list(result[res_key[0]])
        now_batch = res_item[0]['batch']
        result = self.pre_client.query("select * from "+ measurement_t+ " order by desct limit 1")
        res_key = list(result.keys())
        res_item = list(result[res_key[0]])
        # 'flops': int(dictionary['flops']) // int(dictionary['batch_size']),
        # 'params': dictionary['params'],
        # 'gpus': FLAGS.num_gpus,
        flops = res_item[0]['flops']
        params = res_item[0]['params']
        gpus = res_item[0]['gpus']
        #    "deadline": 14843,
        #     "start_time": 1584816589.613,
        #     "cpu_source": 6046,
        #     "mem_source": 19225,
        #     "cpu_high": 8991,
        #     "memory_base": 8706,
        #     "batch_res": 785,
        #     "flops_res": 127834653,
        #     "params_res": 18273610,
        #     "step_base": 69,
        # batch = job_config['batch_res']
        # flops = job_config['flops_res']
        # params = job_config['params_res']
        # cpu_high = job_config['cpu_high']
        # mem_base = job_config['memory_base']
        # cpu_alpha = self.cpu_allocate / cpu_high
        # mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([now_batch, flops, params,gpus])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self,batch_size,training_step,worker_replicas,ps_replicas,part):
        tmp = self.retry
        self.retry = tmp+1
        # self.cpu_allocate = cpu_source
        # self.memory_allocate = memory_source
        self.batch_size = batch_size
        self.part = part
        self.real_batch = self.batch_size // self.part

        #cpu_usage = str(cpu_source) + 'm'
        #mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.real_batch),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--num_epochs=' + str(self.num_epochs),
                     '--save_step=' + str(self.save_step),
                     '--write_step=' + str(self.write_step),
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay),
                     '--freq=' + str(self.freq),
                     '--num_gpus=1'
                     ]
        self.write_retry(mode=1)
        self.delete_tf(mode=1)
        time.sleep(9)
        error1 = False
        OK = False
        for i in range(15):
            res = self.v1.list_namespace()
            res_item = list(res.items)
            aim = {}
            for i in res_item:
                aim[i.metadata.name] = i.status.phase
            aim_key = aim.keys()
            if self.name not in aim_key:
                error1 = True
                OK = False
                break
            panduan = aim[self.name].strip()
            if panduan == 'Active':
                OK = True
                break
            time.sleep(16)
        if OK:
            self.update_batch()
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.update_batch()
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.update_batch()
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()




    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/data/tfdata/tfcnn/expjob/job/%s.yaml' % self.name

        with open(job_file, 'r') as job_yaml:
            job_yaml_obj = yaml.load(job_yaml.read())
        job_yaml.close()

            # print(yaml_obj)
            # print(type(yaml_obj))

        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'][
            'cpu'] = cpu_usage
        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests'][
            'cpu'] = cpu_usage
        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'][
            'memory'] = mem_usage
        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests'][
            'memory'] = mem_usage



        f = open(job_file, "w")
        yaml.dump(job_yaml_obj, f)
        f.close()
        save_job_change_resource(self.name,cpu_source,memory_source)
        response = os.system('kubectl apply -f ' + job_file)
        if response == 0:
            print('assign task resource sucess')
        else:
            print("Error code:" + str(response))


    def assign_replicas(self,ps_n,worker_n):
        self.ps_replicas = ps_n
        self.worker_replicas = worker_n
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        name = 'vgg-' + str(self.task_id) + '-' + str(self.rtimes)
        log_dir = '/data/tfdata/tfcnn/expjob/job/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))
        if response == 0:
            self.create_tf()
        else:
            return

        # self.v1.delete_namespace(name=name)


    def create_tf(self):
        name = self.name
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source)+'m'
        mem_usage = str(mem_source)+'Mi'
        sa_dir = '/data/tfdata/tfcnn/expjob/sa/'
        bind_dir = '/data/tfdata/tfcnn/expjob/bind/'
        job_dir =  '/data/tfdata/tfcnn/expjob/job/'

        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
            self.serviceaccount['metadata']['name'] = self.rolename
            self.serviceaccount['metadata']['namespace'] = name

            # f = open(log_dir+str(name)+'.yaml', "w")
            f = open(sa_dir + str(name) + '-sa.yaml', "w")
            yaml.dump(self.serviceaccount, f)
            f.close()
            response = os.system('kubectl apply -f ' + sa_dir + str(name) + '-sa.yaml')
            if response == 0:
                print('create serviceaccount sucess')
            else:
                print("Error code:" + str(response))
            time.sleep(5)
            self.role['metadata']['name'] = self.bindname
            self.role['metadata']['namespace'] = self.name
            self.role['subjects'][0]['name'] = self.rolename
            self.role['subjects'][0]['namespace'] = self.name

            f = open(bind_dir + str(name) + '-bind.yaml', "w")
            yaml.dump(self.role, f)
            f.close()
            response = os.system('kubectl apply -f ' + bind_dir + str(name) + '-bind.yaml')
            if response == 0:
                print('create rolebind sucess')
            else:
                print("Error code:" + str(response))


        train_dir = check_path(name)
        time.sleep(8)

        self.schedule_label()
        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec'][ 'serviceAccount'] = self.rolename
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec'][ 'serviceAccount'] = self.rolename
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][1]['name'] = '%s-data' % name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][1]['name'] = '%s-data' % name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][1][
            'name'] = '%s-data' % name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][1][
            'name'] = '%s-data' % name

        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage



        # log_dir = '/data/tfdata/tfcnn/expjob/'
        # f = open(log_dir+str(name)+'.yaml', "w")
        f = open(job_dir + str(name) + '.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+job_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = self.name
        log_dir = '/data/tfdata/tfcnn/expjob/job/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))

        if mode == 0:
            deletehelp2(name, self.v1)
            # self.v1.delete_namespace(name=name)

class RESTask(SubTask):
    '''

    [ '--bot=1',
                                      '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=400', '--block1=3',
                                      '--block2=4', '--block3=7', '--block4=6', '--rate1=4', '--rate2=4', '--rate3=4', '--rate4=4',
                                      '--k0=7', '--k11=1', '--k12=3', '--k21=1', '--k22=3', '--k31=1', '--k32=3', '--k41=1', '--k42=3',
                                      '--num_gpus=1']
    '''
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,bot,block1,block2,block3,block4,channel1,channel2,channel3,channel4,rate1,rate2,rate3,rate4,k0,k11,k12,k21,k22,k31,k32,k41,k42,dbhost='172.16.190.97', retry=0, update_min_step=1000, step_update=20, update_start=0.25,
                 update_end=0.9, update_delay=2.0,save_step=5000,num_epochs=300,write_step=50,part=1,freq=5.0):
        SubTask.__init__(self, template_id, ps_replicas=ps_replicas, worker_replicas=worker_replicas,
                         training_step=training_step,
                         batch_size=batch_size, interval=interval, task_id=task_id, rtimes=rtimes, tag=tag,
                         dbhost=dbhost, retry=retry,
                         update_min_step=update_min_step, step_update=step_update, update_start=update_start,
                         update_end=update_end, update_delay=update_delay, save_step=save_step, num_epochs=num_epochs,
                         write_step=write_step, part=part, freq=freq)
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.channel4 = channel4
        self.bot = bot
        self.block1 = block1
        self.block2 = block2
        self.block3 = block3
        self.block4 = block4
        self.rate1 = rate1
        self.rate2 = rate2
        self.rate3 = rate3
        self.rate4 = rate4
        self.k0 = k0
        self.k11 = k11
        self.k12 = k12
        self.k21 = k21
        self.k22 = k22
        self.k31 = k31
        self.k32 = k32
        self.k41 = k41
        self.k42 = k42

        self.name = 'res-'+str(self.task_id)+'-'+str(self.rtimes)
        if self.bot == 1:
            self.num_layers = 3*(block1+block3+block3+block4)+2
        else:
            self.num_layers = 2 * (block1+block2+block3+block4) + 2
        self.template = TaskTemplate.RES
        self.serviceaccount = SATemplate.SA
        self.role = SATemplate.BIND
        self.rolename = 'res-' + str(self.task_id) + '-' + str(self.rtimes) + '-reader'
        self.bindname = 'res-' + str(self.task_id) + '-' + str(self.rtimes) + '-bind'
        # self.v1 = v1
        self.measure = "RES %d" % self.task_id

    def get_node_list(self):
        node_list = [i.metadata.name for i in self.v1.list_node().items]
        return node_list

    def make_args(self):
        '''

           [ '--bot=1',
                                             '--channel1=64', '--channel2=128', '--channel3=256', '--channel4=400', '--block1=3',
                                             '--block2=4', '--block3=7', '--block4=6', '--rate1=4', '--rate2=4', '--rate3=4', '--rate4=4',
                                             '--k0=7', '--k11=1', '--k12=3', '--k21=1', '--k22=3', '--k31=1', '--k32=3', '--k41=1', '--k42=3',
                                             '--num_gpus=1']
           '''
        self.args.append('--bot=' + str(self.bot))
        self.args.append('--channel1='+str(self.channel1))
        self.args.append('--channel2='+str(self.channel2))
        self.args.append('--channel3='+str(self.channel3))
        self.args.append('--channel4='+str(self.channel4))
        self.args.append('--block1='+str(self.block1))
        self.args.append('--block2='+str(self.block2))
        self.args.append('--block3='+str(self.block3))
        self.args.append('--block4='+str(self.block4))
        self.args.append('--rate1='+str(self.rate1))
        self.args.append('--rate2='+str(self.rate2))
        self.args.append('--rate3='+str(self.rate3))
        self.args.append('--rate4='+str(self.rate4))
        self.args.append('--k0='+str(self.k0))
        self.args.append('--k11='+str(self.k11))
        self.args.append('--k12='+str(self.k12))
        self.args.append('--k21='+str(self.k21))
        self.args.append('--k22='+str(self.k22))
        self.args.append('--k31='+str(self.k31))
        self.args.append('--k32='+str(self.k32))
        self.args.append('--k41='+str(self.k41))
        self.args.append('--k42='+str(self.k42))

    def get_remain(self, mode=0):
        filepath = '/data/tfdata/k8snfs/' + self.name + '/worker0/'
        file_list = os.listdir(filepath)
        step_influx = influxdb.InfluxDBClient(host=self.dbhost, port=8086, username='admin', password='admin',
                                              database="PREDICT")
        pre_list = self.measure.split(" ")
        measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_t = pre_list[0] + 'T' + pre_list[-1]
        result = step_influx.query("select training_step from " + measure_t + " order by desc limit 1")
        key = result.keys()
        result_inter = result[key[0]]
        result_items = list(result_inter)
        trains_step = result_items[0]['training_step']
        total_step = int(trains_step)
        atmp = 0
        if mode == 0:
            step = []
            for i in file_list:
                if 'model.ckpt' in i and 'meta' in i:
                    tmp = re.findall(r'\d+', i)
                    step.append(int(tmp[0]))
                    # tiqv.append(i)
            if not step:
                atmp = 0
            else:
                atmp = max(step)
        else:
            res = step_influx.query("select * from " + measure_s + " group by nodes,retry order by desc limit 1")
            res_key = list(res.keys())
            # keys = res.keys()
            if res_key:
                retry_time = [int(b['retry']) for a, b in res_key]
                retry_time = set(retry_time)
                retry = max(retry_time)
                # node_list = [b['nodes'] for a, b in keys]
                node_list = [b['nodes'] for a, b in res_key]
                dic_msg = {}
                for node in node_list:
                    for i in range(len(res_key)):
                        _, no = res_key[i]
                        if no['nodes'] == node and int(no['retry']) == retry:
                            dic_msg[node] = list(res[res_key[i]])
                step_list = []
                node_key = list(dic_msg.keys())
                for node in node_key:
                    step_list.append(int(dic_msg[node][0]['step']))
                if not step_list:
                    atmp = 0
                else:
                    atmp = min(step_list)
            else:
                atmp = 0
            # for node in node_list:
            #     for i in range(len(keys)):
            #         _, no = keys[i]
            #         if no['nodes'] == node:
            #             dic_msg[node] = list(res[keys[i]])
        remain = total_step - atmp + 2
        if remain <= 0:
            remain = 0
        return remain,total_step,atmp

    def predict_min(self,rfr):
        # inputmem = open('rfr_batch.pkl', 'rb')
        # s2 = pickle.dump(rfr_batch, outputmem)
        # # est_gpu = pickle.load(inputgpu)
        # est_mem = pickle.load(inputmem)
        # mse_mem = mean_squared_error(y_gpu_test, est_mem.predict(X_gpu_test))
        job_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        # job_config = load_config(job_path)
        pre_list = self.measure.split(' ')
        measurement_b = '%sB%d' % (pre_list[0],self.task_id)
        measurement_t = "%sS%d" % (pre_list[0],self.task_id)
        result = self.batch_client.query("select * from " + measurement_b + " order by desc limit 1")
        res_key = list(result.keys())
        res_item = list(result[res_key[0]])
        now_batch = res_item[0]['batch']
        result = self.pre_client.query("select * from "+ measurement_t+ " order by desct limit 1")
        res_key = list(result.keys())
        res_item = list(result[res_key[0]])
        # 'flops': int(dictionary['flops']) // int(dictionary['batch_size']),
        # 'params': dictionary['params'],
        # 'gpus': FLAGS.num_gpus,
        flops = res_item[0]['flops']
        params = res_item[0]['params']
        gpus = res_item[0]['gpus']
        #    "deadline": 14843,
        #     "start_time": 1584816589.613,
        #     "cpu_source": 6046,
        #     "mem_source": 19225,
        #     "cpu_high": 8991,
        #     "memory_base": 8706,
        #     "batch_res": 785,
        #     "flops_res": 127834653,
        #     "params_res": 18273610,
        #     "step_base": 69,
        # batch = job_config['batch_res']
        # flops = job_config['flops_res']
        # params = job_config['params_res']
        # cpu_high = job_config['cpu_high']
        # mem_base = job_config['memory_base']
        # cpu_alpha = self.cpu_allocate / cpu_high
        # mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([now_batch, flops, params,gpus])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self,batch_size,training_step,worker_replicas,ps_replicas,part):
        tmp = self.retry
        self.retry = tmp+1
        # self.cpu_allocate = cpu_source
        # self.memory_allocate = memory_source
        self.batch_size = batch_size
        self.part = part
        self.real_batch = self.batch_size // self.part

        #cpu_usage = str(cpu_source) + 'm'
        #mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.real_batch),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--num_epochs=' + str(self.num_epochs),
                     '--save_step=' + str(self.save_step),
                     '--write_step=' + str(self.write_step),
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay),
                     '--freq=' + str(self.freq),
                     '--num_gpus=1'
                     ]
        self.write_retry(mode=1)
        self.delete_tf(mode=1)
        time.sleep(9)
        error1 = False
        OK = False
        for i in range(15):
            res = self.v1.list_namespace()
            res_item = list(res.items)
            aim = {}
            for i in res_item:
                aim[i.metadata.name] = i.status.phase
            aim_key = aim.keys()
            if self.name not in aim_key:
                error1 = True
                OK = False
                break
            panduan = aim[self.name].strip()
            if panduan == 'Active':
                OK = True
                break
            time.sleep(16)
        if OK:
            self.update_batch()
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.update_batch()
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.update_batch()
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()

    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/data/tfdata/tfcnn/expjob/job/%s.yaml' % self.name

        with open(job_file, 'r') as job_yaml:
            job_yaml_obj = yaml.load(job_yaml.read())
        job_yaml.close()

        # print(yaml_obj)
        # print(type(yaml_obj))

        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'][
            'cpu'] = cpu_usage
        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests'][
            'cpu'] = cpu_usage
        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'][
            'memory'] = mem_usage
        job_yaml_obj['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests'][
            'memory'] = mem_usage

        f = open(job_file, "w")
        yaml.dump(job_yaml_obj, f)
        f.close()
        response = os.system('kubectl apply -f ' + job_file)
        if response == 0:
            print('assign task resource sucess')
        else:
            print("Error code:" + str(response))

    def create_tf(self):
        name = self.name
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source)+'m'
        mem_usage = str(mem_source)+'Mi'
        sa_dir = '/data/tfdata/tfcnn/expjob/sa/'
        bind_dir = '/data/tfdata/tfcnn/expjob/bind/'
        job_dir =  '/data/tfdata/tfcnn/expjob/job/'

        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
            self.serviceaccount['metadata']['name'] = self.rolename
            self.serviceaccount['metadata']['namespace'] = name

            # f = open(log_dir+str(name)+'.yaml', "w")
            f = open(sa_dir + str(name) + '-sa.yaml', "w")
            yaml.dump(self.serviceaccount, f)
            f.close()
            response = os.system('kubectl apply -f ' + sa_dir + str(name) + '-sa.yaml')
            if response == 0:
                print('create serviceaccount sucess')
            else:
                print("Error code:" + str(response))
            time.sleep(5)
            self.role['metadata']['name'] = self.bindname
            self.role['metadata']['namespace'] = self.name
            self.role['subjects'][0]['name'] = self.rolename
            self.role['subjects'][0]['namespace'] = self.name

            f = open(bind_dir + str(name) + '-bind.yaml', "w")
            yaml.dump(self.role, f)
            f.close()
            response = os.system('kubectl apply -f ' + bind_dir + str(name) + '-bind.yaml')
            if response == 0:
                print('create rolebind sucess')
            else:
                print("Error code:" + str(response))


        train_dir = check_path(name)
        time.sleep(8)

        self.schedule_label()

        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec'][ 'serviceAccount'] = self.rolename
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec'][ 'serviceAccount'] = self.rolename
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][1]['name'] = '%s-data' % name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][1]['name'] = '%s-data' % name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][1][
            'name'] = '%s-data' % name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][1][
            'name'] = '%s-data' % name

        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        # self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage



        # log_dir = '/data/tfdata/tfcnn/expjob/'
        # f = open(log_dir+str(name)+'.yaml', "w")
        f = open(job_dir + str(name) + '.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+job_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = 'res-'+str(self.task_id)+'-'+str(self.rtimes)
        log_dir = '/data/tfdata/tfcnn/expjob/job/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))
        if mode == 0:
            deletehelp2(name, self.v1)
            # self.v1.delete_namespace(name=name)

if __name__ == '__main__':
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # v1.create_namespace()
    v1.list_namespace()
    check_path('ceshi')
    # vgg = VGGTask(1,2,4,80,1.0,2,1,"ms",32,64,128,256,512,2,3,3,4,4)
    # vgg.create_tf()
