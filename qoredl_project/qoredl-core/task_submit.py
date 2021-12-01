#https://blog.csdn.net/orangefly0214/article/details/81387077
import MultiTemplate
from MultiTemplate import TaskTemplate
import numpy as np
# https://blog.csdn.net/u013812710/article/details/72886491
# https://blog.csdn.net/ismr_m/article/details/53100896
#https://blog.csdn.net/bcfdsagbfcisbg/article/details/78134172
import kubernetes
import os
import json
import influxdb
import time
import re
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor
# # from random_job3 import save_job_change_layout
# from random_job3 import save_job_change_resource

import yaml

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

def deletehelp(delete_job_name,v1):
    try:
        v1.delete_namespace(delete_job_name)
    except Exception as eeeeee:
        print(eeeeee)
        command0 = "kubectl get namespace " + delete_job_name + " -o json > /tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
        os.system(command0)
        tmp = load_config("/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        tmp["spec"]["finalizers"] = []
        save_config(tmp, "/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        try:
            command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/'+delete_job_name+'/finalize'
            os.system(command1)
        except Exception as helpe:
            print(helpe)
            commandopen = 'kubectl proxy --port=8081'
            os.system(commandopen)
            os.system(command1)

def deletehelp2(delete_job_name,v1):
    v1.delete_namespace(delete_job_name)
    command0 = "kubectl get namespace " + delete_job_name + " -o json > /tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
    os.system(command0)
    tmp = load_config("/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
    tmp["spec"]["finalizers"] = []
    save_config(tmp, "/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
    try:
        command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
        os.system(command1)
    except Exception as helpe:
        print(helpe)
        commandopen = 'kubectl proxy --port=8081'
        os.system(commandopen)
        os.system(command1)

def check_path(name):
    train_dir = os.path.join('/tfdata/k8snfs/', name)
    print(train_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    return train_dir

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
                 dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                 update_end=0.75, update_delay=2.0):
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
        self.retry = retry
        kubernetes.config.load_kube_config()
        self.v1 = kubernetes.client.CoreV1Api()
        self.v1.list_namespace()
        self.update_min_step = update_min_step
        self.step_update = step_update
        self.update_start = update_start
        self.update_end = update_end
        self.update_delay = update_delay
        self.influx_client = influxdb.InfluxDBClient(host='192.168.128.10',port=8086,username='admin',password='admin',database="NODEMESSAGE")
        self.node_list = ['k8s-master','k8s-worker0','k8s-worker2','k8sworker1','k8s-worker3','k8s-worker4','k8s-worker5']
        self.node_cpu = {}
        self.node_compute = {}
        self.node_compute['k8s-master'] = 1
        self.node_compute['k8s-worker0'] = 1
        self.node_compute['k8s-worker2'] = 1
        self.node_compute['k8sworker1'] = 1
        self.node_compute['k8s-worker3'] = 0
        self.node_compute['k8s-worker4'] = 0
        self.node_compute['k8s-worker5'] = 1
        self.node_compute['k8s-worker6'] = 0
        self.node_compute['k8s-worker7'] = 0
        self.node_compute['k8s-worker8'] = 0
        self.node_compute['k8s-worker9'] = 0
        self.node_compute['k8s-worker10'] = 0
        self.node_compute['k8s-worker11'] = 1
        self.node_compute['k8s-worker12'] = 0
        self.node_compute['k8s-worker13'] = 0
        self.node_compute['k8s-worker14'] = 0
        self.node_compute['k8s-worker15'] = 0
        self.node_compute['k8s-worker16'] = 0
        self.node_compute['k8s-worker17'] = 0
        self.node_compute['k8s-worker18'] = 0
        self.node_compute['k8s-worker19'] = 0
        self.node_compute['k8s-worker20'] = 0


        self.cpu_allocate = 2048
        self.memory_allocate = 2048

        self.node_cmtype = {}
        self.node_cmtype['k8s-master'] = 2
        self.node_cmtype['k8s-worker0'] = 1
        self.node_cmtype['k8s-worker2'] = 1
        self.node_cmtype['k8sworker1'] = 2
        self.node_cmtype['k8s-worker3'] = 1
        self.node_cmtype['k8s-worker4'] = 2
        self.node_cmtype['k8s-worker5'] = 1
        self.node_cmtype['k8s-worker6'] = 1
        self.node_cmtype['k8s-worker7'] = 1
        self.node_cmtype['k8s-worker8'] = 1
        self.node_cmtype['k8s-worker9'] = 1
        self.node_cmtype['k8s-worker10'] = 1
        self.node_cmtype['k8s-worker11'] = 1
        self.node_cmtype['k8s-worker12'] = 1
        self.node_cmtype['k8s-worker13'] = 1
        self.node_cmtype['k8s-worker14'] = 1
        self.node_cmtype['k8s-worker15'] = 1
        self.node_cmtype['k8s-worker16'] = 1
        self.node_cmtype['k8s-worker17'] = 1
        self.node_cmtype['k8s-worker18'] = 1
        self.node_cmtype['k8s-worker19'] = 1
        self.node_cmtype['k8s-worker20'] = 1


        self.node_disk = {}
        self.node_disk['k8s-master'] = 1
        self.node_disk['k8s-worker0'] = 1
        self.node_disk['k8s-worker2'] = 1
        self.node_disk['k8sworker1'] = 1
        self.node_disk['k8s-worker3'] = 0
        self.node_disk['k8s-worker4'] = 0
        self.node_disk['k8s-worker5'] = 0
        self.node_disk['k8s-worker6'] = 0
        self.node_disk['k8s-worker7'] = 0
        self.node_disk['k8s-worker8'] = 0
        self.node_disk['k8s-worker9'] = 0
        self.node_disk['k8s-worker10'] = 0
        self.node_disk['k8s-worker11'] = 1
        self.node_disk['k8s-worker12'] = 1
        self.node_disk['k8s-worker13'] = 1
        self.node_disk['k8s-worker14'] = 1
        self.node_disk['k8s-worker15'] = 1
        self.node_disk['k8s-worker16'] = 0
        self.node_disk['k8s-worker17'] = 1
        self.node_disk['k8s-worker18'] = 0
        self.node_disk['k8s-worker19'] = 0
        self.node_disk['k8s-worker20'] = 0



        self.deadline = 3600
        self.starttime = 0
        # self.lasttime =
        self.node_cpu['k8s-master'] = 64000 - 8000
        self.node_cpu['k8s-worker0'] = 24000 - 400
        self.node_cpu['k8s-worker2'] = 24000 - 400
        self.node_cpu['k8sworker1'] = 16000 - 520
        self.node_cpu['k8s-worker3'] = 24000 - 150
        self.node_cpu['k8s-worker4'] = 24000 - 150
        self.node_cpu['k8s-worker5'] = 24000 - 150
        self.node_cpu['k8s-worker6'] = 16000 - 150
        self.node_cpu['k8s-worker7'] = 16000 - 150
        self.node_cpu['k8s-worker8'] = 16000 - 150
        self.node_cpu['k8s-worker9'] = 16000 - 150
        self.node_cpu['k8s-worker10'] = 16000 - 150
        self.node_cpu['k8s-worker11'] = 24000 - 300
        self.node_cpu['k8s-worker12'] = 16000 - 150
        self.node_cpu['k8s-worker13'] = 16000 - 150
        self.node_cpu['k8s-worker14'] = 16000 - 150
        self.node_cpu['k8s-worker15'] = 16000 - 150
        self.node_cpu['k8s-worker16'] = 16000 - 150
        self.node_cpu['k8s-worker17'] = 24000 - 150
        self.node_cpu['k8s-worker18'] = 16000 - 150
        self.node_cpu['k8s-worker19'] = 32000 - 150
        self.node_cpu['k8s-worker20'] = 24000 - 150

        # self.node_cpu['k8s-master'] = 32000 - 8000
        # self.node_cpu['k8s-worker0'] = 24000 - 400
        # self.node_cpu['k8s-worker2'] = 24000 - 400
        # self.node_cpu['k8sworker1'] = 16000 - 520
        # self.node_cpu['k8s-worker3'] = 24000 - 150
        # self.node_cpu['k8s-worker4'] = 16000 - 150
        # self.node_cpu['k8s-worker5'] = 24000 - 150
        self.total_cpu = 0
        self.total_mem = 0.0
        self.node_memory = {}
        # self.node_memory['k8s-master'] = float(251*1024 - 32000)
        # self.node_memory['k8s-worker0'] = float(94*1024 - 4000)
        # self.node_memory['k8s-worker2'] = float(94*1024 - 3000)
        # self.node_memory['k8sworker1'] = float(125*1024 - 4500)
        # self.node_memory['k8s-worker3'] = float(94 * 1024 - 2200)
        # self.node_memory['k8s-worker4'] = float(125 * 1024 - 2200)
        # self.node_memory['k8s-worker5'] = float(94 * 1024 - 2200)
        self.node_memory['k8s-master'] = float(251 * 1024 - 32000)
        self.node_memory['k8s-worker0'] = float(94 * 1024 - 4000)
        self.node_memory['k8s-worker2'] = float(94 * 1024 - 3000)
        self.node_memory['k8sworker1'] = float(125 * 1024 - 4500)
        self.node_memory['k8s-worker3'] = float(94 * 1024 - 2200)
        self.node_memory['k8s-worker4'] = float(188 * 1024 - 2200)
        self.node_memory['k8s-worker5'] = float(94 * 1024 - 2200)
        self.node_memory['k8s-worker6'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker7'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker8'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker9'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker10'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker11'] = float(94 * 1024 - 2200)
        self.node_memory['k8s-worker12'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker13'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker14'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker15'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker16'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker17'] = float(94 * 1024 - 2000)
        self.node_memory['k8s-worker18'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker19'] = float(125 * 1024 - 2000)
        self.node_memory['k8s-worker20'] = float(94 * 1024 - 2000)
        
        node_keys = self.node_cpu.keys()
        for key in node_keys:
            self.total_cpu = self.total_cpu + self.node_cpu[key]
            self.total_mem = self.total_mem + self.node_memory[key]

        self.args = ['--training_step='+str(self.training_step),'--batch_size='+str(self.batch_size),'--interval='+str(self.interval),'--task_id='+str(self.task_id),'--rtimes='+str(self.rtimes),"--tag="+self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay)
                     ]

    def set_deadline(self,deadline,start_time):
        self.deadline = deadline
        self.starttime = start_time

    def set_resource(self,cpu_source,mem_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = mem_source



    #
    # def apply_tf(self,cpu_source,mem_source):
    #     self.cpu_allocate = cpu_source
    #     self.memory_allocate = mem_source

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
                    'training_step': self.training_step
                }
            }
        ]
        # print(step_to_train)
        step_update_influx.write_points(step_items, time_precision="ms", database="PREDICT")


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

        for key in nodes:
            command = 'kubectl label nodes ' + key + ' woksch-'
            os.system(command)
            command2 = 'kubectl label nodes ' + key + ' wokpro-'
            os.system(command2)
            nod_prori = point_base_list.index(point_base[key])
            # node_index[key] = nod_prori
            priori = ' wokpro=%d' % nod_prori
            command3 = 'kubectl label nodes ' + key + priori
            os.system(command3)
            if cpu_base[key] <= 0.42 and memory_base[key] <= 0.6:
                command = 'kubectl label nodes ' + key + ' woksch=true'
                os.system(command)
            else:
                command = 'kubectl label nodes ' + key + ' woksch=false'
                os.system(command)

        # return node_index,cpu_base,memory_base,total_cpu_use,total_mem_use






class VGGTask(SubTask):
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,channel1,channel2,channel3,channel4,channel5,num_layer1,num_layer2,num_layer3,num_layer4,num_layer5,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                 update_end=0.75, update_delay=2.0):
        SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,dbhost,retry,update_min_step,step_update,update_start,update_end,update_delay)
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag)
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
        # self.v1 = v1
        self.name = 'vgg-'+str(self.task_id)+'-'+str(self.rtimes)
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

    def get_remain(self, mode=0):
        filepath = '/tfdata/k8snfs/' + self.name + '/worker0/'
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
        job_path = '/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        job_config = load_config(job_path)
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
        batch = job_config['batch_res']
        flops = job_config['flops_res']
        params = job_config['params_res']
        cpu_high = job_config['cpu_high']
        mem_base = job_config['memory_base']
        cpu_alpha = self.cpu_allocate / cpu_high
        mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([batch, flops, params,cpu_alpha,mem_alpha])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self,cpu_source,memory_source,training_step,worker_replicas,ps_replicas):
        tmp = self.retry
        self.retry = tmp+1
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source

        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.batch_size),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay)
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
            time.sleep(20)
        if OK:
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()




    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/tfdata/tfcnn/expjob/%s.yaml' % self.name

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
        log_dir = '/tfdata/tfcnn/expjob/'

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
        name = 'vgg-'+str(self.task_id)+'-'+str(self.rtimes)
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source)+'m'
        mem_usage = str(mem_source)+'Mi'

        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
        train_dir = check_path(name)
        time.sleep(9)
        # result = self.influx_client.query("select * from "+"NODEMESSAGE"+" group by nodes order by desc limit 3")
        # node_list = self.get_node_list()
        # result_keys = result.keys()
        # nodes = [i[-1]['nodes'] for i in result_keys]
        # node_mg = [list(result[i]) for i in result_keys]
        # cpu_base = {}
        # memory_base = {}
        # point_base = {}
        # point_base_list = []
        # for i in range(len(node_mg)):
        #     cpu_base[nodes[i]] = 0
        #     memory_base[nodes[i]] = 0
        #     point_base[nodes[i]] = 0.0
        #     for j in range(len(node_mg[0])):
        #         cpu_base[nodes[i]] += node_mg[i][j]['cpu']
        #         memory_base[nodes[i]] += node_mg[i][j]['memory']
        #     cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0]))/self.node_cpu[nodes[i]]
        #     memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
        #     tmp = cpu_base[nodes[i]]*0.6+memory_base[nodes[i]]*0.4
        #     point_base[nodes[i]] = tmp
        #     point_base_list.append(tmp)
        #
        # list.sort(point_base_list)
        #
        # for key in nodes:
        #     command = 'kubectl label nodes '+key+' woksch-'
        #     os.system(command)
        #     command2 = 'kubectl label nodes '+key+' wokpro-'
        #     os.system(command2)
        #     nod_prori = point_base_list.index(point_base[key])
        #     priori = ' wokpro=%d' % nod_prori
        #     command3 = 'kubectl label nodes '+key+priori
        #     os.system(command3)
        #     if cpu_base[key] <= 0.56 and memory_base[key] <= 0.6:
        #         command = 'kubectl label nodes '+key+' woksch=true'
        #         os.system(command)
        #     else:
        #         command = 'kubectl label nodes ' + key + ' woksch=false'
        #         os.system(command)

        self.schedule_label()
        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage



        log_dir = '/tfdata/tfcnn/expjob/'
        # f = open(log_dir+str(name)+'.yaml', "w")
        f = open(log_dir + str(name) + '.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+log_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = 'vgg-'+str(self.task_id)+'-'+str(self.rtimes)
        log_dir = '/tfdata/tfcnn/expjob/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))

        if mode == 0:
            deletehelp2(name, self.v1)
            # self.v1.delete_namespace(name=name)

class RESTask(SubTask):
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,bottle,layer1,layer2,layer3,layer4,channel1,channel2,channel3,channel4,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                 update_end=0.75, update_delay=2.0):
        SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,dbhost,retry,update_min_step,step_update,update_start,update_end,update_delay)
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag)
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.channel4 = channel4
        self.bottle = bottle
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3
        self.layer4 = layer4
        self.name = 'res-'+str(self.task_id)+'-'+str(self.rtimes)
        if self.bottle == 1:
            self.num_layers = 3*(layer1+layer4+layer3+layer2)+2
        else:
            self.num_layers = 2 * (layer1 + layer4 + layer3 + layer2) + 2
        self.template = TaskTemplate.RES
        # self.v1 = v1
        self.measure = "RES %d" % self.task_id

    def get_node_list(self):
        node_list = [i.metadata.name for i in self.v1.list_node().items]
        return node_list

    def make_args(self):
        self.args.append('--bottle=' + str(self.bottle))
        self.args.append('--channel1='+str(self.channel1))
        self.args.append('--channel2='+str(self.channel2))
        self.args.append('--channel3='+str(self.channel3))
        self.args.append('--channel4='+str(self.channel4))
        self.args.append('--layer1='+str(self.layer1))
        self.args.append('--layer2='+str(self.layer2))
        self.args.append('--layer3='+str(self.layer3))
        self.args.append('--layer4='+str(self.layer4))

    def get_remain(self, mode=0):
        filepath = '/tfdata/k8snfs/' + self.name + '/worker0/'
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
        job_path = '/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        job_config = load_config(job_path)
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
        batch = job_config['batch_res']
        flops = job_config['flops_res']
        params = job_config['params_res']
        cpu_high = job_config['cpu_high']
        mem_base = job_config['memory_base']
        cpu_alpha = self.cpu_allocate / cpu_high
        mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([batch, flops, params,cpu_alpha,mem_alpha])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self, cpu_source, memory_source, training_step, worker_replicas, ps_replicas):
        tmp = self.retry
        self.retry = tmp + 1
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source

        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.batch_size),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay)
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
            time.sleep(20)
        if OK:
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()

    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/tfdata/tfcnn/expjob/%s.yaml' % self.name

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
        name = 'res-'+str(self.task_id)+'-'+str(self.rtimes)
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(mem_source) + 'Mi'
        # self.cpu_allocate = cpu_source
        # self.memory_allocate = mem_source
        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
        train_dir = check_path(name)

        time.sleep(12)
        # result = self.influx_client.query("select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 3")
        # node_list = self.get_node_list()
        # result_keys = result.keys()
        # nodes = [i[-1]['nodes'] for i in result_keys]
        # node_mg = [list(result[i]) for i in result_keys]
        # cpu_base = {}
        # memory_base = {}
        # point_base = {}
        # point_base_list = []
        # for i in range(len(node_mg)):
        #     cpu_base[nodes[i]] = 0
        #     memory_base[nodes[i]] = 0
        #     point_base[nodes[i]] = 0.0
        #     for j in range(len(node_mg[0])):
        #         cpu_base[nodes[i]] += node_mg[i][j]['cpu']
        #         memory_base[nodes[i]] += node_mg[i][j]['memory']
        #     cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
        #     memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
        #     tmp = cpu_base[nodes[i]] * 0.6 + memory_base[nodes[i]] * 0.4
        #     point_base[nodes[i]] = tmp
        #     point_base_list.append(tmp)
        #
        # list.sort(point_base_list)
        #
        # for key in nodes:
        #     command = 'kubectl label nodes ' + key + ' woksch-'
        #     os.system(command)
        #     command2 = 'kubectl label nodes ' + key + ' wokpro-'
        #     os.system(command2)
        #     nod_prori = point_base_list.index(point_base[key])
        #     priori = ' wokpro=%d' % nod_prori
        #     command3 = 'kubectl label nodes ' + key + priori
        #     os.system(command3)
        #     if cpu_base[key] <= 0.6 and memory_base[key] <= 0.6:
        #         command = 'kubectl label nodes ' + key + ' woksch=true'
        #         os.system(command)
        #     else:
        #         command = 'kubectl label nodes ' + key + ' woksch=false'
        #         os.system(command)
        self.schedule_label()
        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage

        log_dir = '/tfdata/tfcnn/expjob/'
        f = open(log_dir+str(name)+'.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+log_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = 'res-'+str(self.task_id)+'-'+str(self.rtimes)
        log_dir = '/tfdata/tfcnn/expjob/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))
        if mode == 0:
            deletehelp2(name, self.v1)
            # self.v1.delete_namespace(name=name)

class RETask(SubTask):
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,stack,channel1,channel2,channel3,channel4,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                 update_end=0.75, update_delay=2.0):
        SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,dbhost,retry,update_min_step,step_update,update_start,update_end,update_delay)
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag)
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.channel4 = channel4
        self.stack = stack
        self.num_layers = 6*self.stack+2
        self.template = TaskTemplate.RE
        self.name = 're-'+str(self.task_id)+'-'+str(self.rtimes)
        # self.v1 = v1
        self.measure = "RE %d" % self.task_id

    def get_node_list(self):
        node_list = [i.metadata.name for i in self.v1.list_node().items]
        return node_list

    def make_args(self):
        self.args.append('--stack='+str(self.stack))
        self.args.append('--channel1='+str(self.channel1))
        self.args.append('--channel2='+str(self.channel2))
        self.args.append('--channel3='+str(self.channel3))
        self.args.append('--channel4='+str(self.channel4))

    def get_remain(self, mode=0):
        filepath = '/tfdata/k8snfs/' + self.name + '/worker0/'
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
        job_path = '/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        job_config = load_config(job_path)
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
        batch = job_config['batch_res']
        flops = job_config['flops_res']
        params = job_config['params_res']
        cpu_high = job_config['cpu_high']
        mem_base = job_config['memory_base']
        cpu_alpha = self.cpu_allocate / cpu_high
        mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([batch, flops, params,cpu_alpha,mem_alpha])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self, cpu_source, memory_source, training_step, worker_replicas, ps_replicas):
        tmp = self.retry
        self.retry = tmp + 1
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source

        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.batch_size),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay)
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
            time.sleep(20)
        if OK:
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()

    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/tfdata/tfcnn/expjob/%s.yaml' % self.name

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
        name = 're-'+str(self.task_id)+'-'+str(self.rtimes)
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(mem_source) + 'Mi'
        # self.cpu_allocate = cpu_source
        # self.memory_allocate = mem_source
        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
        train_dir = check_path(name)

        time.sleep(12)
        self.schedule_label()
        # result = self.influx_client.query("select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 3")
        # node_list = self.get_node_list()
        # result_keys = result.keys()
        # nodes = [i[-1]['nodes'] for i in result_keys]
        # node_mg = [list(result[i]) for i in result_keys]
        # cpu_base = {}
        # memory_base = {}
        # point_base = {}
        # point_base_list = []
        # for i in range(len(node_mg)):
        #     cpu_base[nodes[i]] = 0
        #     memory_base[nodes[i]] = 0
        #     point_base[nodes[i]] = 0.0
        #     for j in range(len(node_mg[0])):
        #         cpu_base[nodes[i]] += node_mg[i][j]['cpu']
        #         memory_base[nodes[i]] += node_mg[i][j]['memory']
        #     cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
        #     memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
        #     tmp = cpu_base[nodes[i]] * 0.6 + memory_base[nodes[i]] * 0.4
        #     point_base[nodes[i]] = tmp
        #     point_base_list.append(tmp)
        #
        # list.sort(point_base_list)
        #
        # for key in nodes:
        #     command = 'kubectl label nodes ' + key + ' woksch-'
        #     os.system(command)
        #     command2 = 'kubectl label nodes ' + key + ' wokpro-'
        #     os.system(command2)
        #     nod_prori = point_base_list.index(point_base[key])
        #     priori = ' wokpro=%d' % nod_prori
        #     command3 = 'kubectl label nodes ' + key + priori
        #     os.system(command3)
        #     if cpu_base[key] <= 0.6 and memory_base[key] <= 0.6:
        #         command = 'kubectl label nodes ' + key + ' woksch=true'
        #         os.system(command)
        #     else:
        #         command = 'kubectl label nodes ' + key + ' woksch=false'
        #         os.system(command)

        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage

        log_dir = '/tfdata/tfcnn/expjob/'
        f = open(log_dir+str(name)+'.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+log_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = 're-'+str(self.task_id)+'-'+str(self.rtimes)
        log_dir = '/tfdata/tfcnn/expjob/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))
        if mode == 0:
            deletehelp2(name, self.v1)
            # self.v1.delete_namespace(name=name)


class XCETask(SubTask):
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,repeat,channel1,channel2,channel3,channel4,channel5,channel6,channel7,channel8,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                 update_end=0.75, update_delay=2.0):
        SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,dbhost,retry,update_min_step,step_update,update_start,update_end,update_delay)
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag)
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.channel4 = channel4
        self.channel5 = channel5
        self.channel6 = channel6
        self.channel7 = channel7
        self.channel8 = channel8
        self.repeat = repeat
        self.template = TaskTemplate.XCEPTION
        # self.v1 = v1
        self.name = 'xception-'+str(self.task_id)+'-'+str(self.rtimes)
        self.measure = "XCE %d" % self.task_id

    def get_node_list(self):
        node_list = [i.metadata.name for i in self.v1.list_node().items]
        return node_list

    def make_args(self):
        self.args.append('--repeat='+str(self.repeat))
        self.args.append('--channel1='+str(self.channel1))
        self.args.append('--channel2='+str(self.channel2))
        self.args.append('--channel3='+str(self.channel3))
        self.args.append('--channel4='+str(self.channel4))
        self.args.append('--channel5=' + str(self.channel5))
        self.args.append('--channel6=' + str(self.channel6))
        self.args.append('--channel7=' + str(self.channel7))
        self.args.append('--channel8=' + str(self.channel8))

    def get_remain(self, mode=0):
        filepath = '/tfdata/k8snfs/' + self.name + '/worker0/'
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

        # return atmp

    def predict_min(self,rfr):
        job_path = '/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        job_config = load_config(job_path)
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
        batch = job_config['batch_res']
        flops = job_config['flops_res']
        params = job_config['params_res']
        cpu_high = job_config['cpu_high']
        mem_base = job_config['memory_base']
        cpu_alpha = self.cpu_allocate / cpu_high
        mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([batch, flops, params,cpu_alpha,mem_alpha])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self, cpu_source, memory_source, training_step, worker_replicas, ps_replicas):
        tmp = self.retry
        self.retry = tmp + 1
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source

        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.batch_size),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay)
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
            time.sleep(20)
        if OK:
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()

    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/tfdata/tfcnn/expjob/%s.yaml' % self.name

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
        name = 'xception-'+str(self.task_id)+'-'+str(self.rtimes)
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(mem_source) + 'Mi'
        # self.cpu_allocate = cpu_source
        # self.memory_allocate = mem_source
        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
        train_dir = check_path(name)

        time.sleep(12)
        # result = self.influx_client.query("select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 3")
        # node_list = self.get_node_list()
        # result_keys = result.keys()
        # nodes = [i[-1]['nodes'] for i in result_keys]
        # node_mg = [list(result[i]) for i in result_keys]
        # cpu_base = {}
        # memory_base = {}
        # point_base = {}
        # point_base_list = []
        # for i in range(len(node_mg)):
        #     cpu_base[nodes[i]] = 0
        #     memory_base[nodes[i]] = 0
        #     point_base[nodes[i]] = 0.0
        #     for j in range(len(node_mg[0])):
        #         cpu_base[nodes[i]] += node_mg[i][j]['cpu']
        #         memory_base[nodes[i]] += node_mg[i][j]['memory']
        #     cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
        #     memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
        #     tmp = cpu_base[nodes[i]] * 0.6 + memory_base[nodes[i]] * 0.4
        #     point_base[nodes[i]] = tmp
        #     point_base_list.append(tmp)
        #
        # list.sort(point_base_list)
        #
        # for key in nodes:
        #     command = 'kubectl label nodes ' + key + ' woksch-'
        #     os.system(command)
        #     command2 = 'kubectl label nodes ' + key + ' wokpro-'
        #     os.system(command2)
        #     nod_prori = point_base_list.index(point_base[key])
        #     priori = ' wokpro=%d' % nod_prori
        #     command3 = 'kubectl label nodes ' + key + priori
        #     os.system(command3)
        #     if cpu_base[key] <= 0.6 and memory_base[key] <= 0.6:
        #         command = 'kubectl label nodes ' + key + ' woksch=true'
        #         os.system(command)
        #     else:
        #         command = 'kubectl label nodes ' + key + ' woksch=false'
        #         os.system(command)
        self.schedule_label()
        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage

        log_dir = '/tfdata/tfcnn/expjob/'
        f = open(log_dir+str(name)+'.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+log_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = 'xception-'+str(self.task_id)+'-'+str(self.rtimes)
        log_dir = '/tfdata/tfcnn/expjob/'

        response = os.system('kubectl delete -f ' + log_dir + str(name) + '.yaml')
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))
        if mode == 0:
            deletehelp2(name, self.v1)
            # self.v1.delete_namespace(name=name)


class DENTask(SubTask):
    def __init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,L,k,BC,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                 update_end=0.75, update_delay=2.0):
        SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,dbhost,retry,update_min_step,step_update,update_start,update_end,update_delay)
        # SubTask.__init__(self,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag)
        self.L = L
        self.k = k
        self.BC = BC
        self.template = TaskTemplate.DEN
        # self.v1 = v1
        self.name = 'den-'+str(self.task_id)+'-'+str(self.rtimes)
        self.measure = "DEN %d" % self.task_id

    def get_node_list(self):
        node_list = [i.metadata.name for i in self.v1.list_node().items]
        return node_list

    def make_args(self):
        self.args.append('--L='+str(self.L))
        self.args.append('--k='+str(self.k))
        self.args.append('--BC='+str(self.BC))

    def get_remain(self, mode=0):
        filepath = '/tfdata/k8snfs/' + self.name + '/worker0/'
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
        job_path = '/tfdata/k8snfs/%s/%s_res.json' % (self.name,self.name)
        job_config = load_config(job_path)
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
        batch = job_config['batch_res']
        flops = job_config['flops_res']
        params = job_config['params_res']
        cpu_high = job_config['cpu_high']
        mem_base = job_config['memory_base']
        cpu_alpha = self.cpu_allocate / cpu_high
        mem_alpha = self.memory_allocate / mem_base
        #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
        data = np.array([batch, flops, params,cpu_alpha,mem_alpha])
        data = np.mat(data)
        data = data.A
        iteration = rfr.predict(data)
        iteration = float(iteration)
        return iteration
        #  data = np.array([batch, flop, param])
        #                 data = np.mat(data)
        #                 data = data.A

    def retry_tf(self, cpu_source, memory_source, training_step, worker_replicas, ps_replicas):
        tmp = self.retry
        self.retry = tmp + 1
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source

        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        self.training_step = training_step
        self.worker_replicas = worker_replicas
        self.ps_replicas = ps_replicas

        self.args = ['--training_step=' + str(self.training_step), '--batch_size=' + str(self.batch_size),
                     '--interval=' + str(self.interval), '--task_id=' + str(self.task_id),
                     '--rtimes=' + str(self.rtimes), "--tag=" + self.tag,
                     '--retry=' + str(self.retry), '--dbhost=' + self.dbhost,
                     '--update_min_step=' + str(self.update_min_step), '--step_update=' + str(self.step_update),
                     '--update_start=' + str(self.update_start), '--update_end=' + str(self.update_end),
                     '--update_delay=' + str(self.update_delay)
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
            time.sleep(20)
        if OK:
            self.create_tf()
        else:
            if error1:
                check_ns(self.name)
                self.create_tf()
            else:
                deletehelp2(self.name, self.v1)
                # self.v1.delete_namespace(self.name)
                self.create_tf()
        # self.write_retry(mode=0)
        self.update_step()



    def assignment_resource(self, cpu_source, memory_source):
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(memory_source) + 'Mi'

        job_file = '/tfdata/tfcnn/expjob/%s.yaml' % self.name

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
        name = 'den-'+str(self.task_id)+'-'+str(self.rtimes)
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        cpu_usage = str(cpu_source) + 'm'
        mem_usage = str(mem_source) + 'Mi'
        # self.memory_allocate = mem_source
        # self.cpu_allocate = cpu_source
        ns_body = TaskTemplate.NS
        ns_body['metadata']['name'] = name
        if not check_ns(name):
            self.v1.create_namespace(ns_body)
        train_dir = check_path(name)

        time.sleep(12)
        # result = self.influx_client.query("select * from " + "NODEMESSAGE" + " group by nodes order by desc limit 3")
        # node_list = self.get_node_list()
        # result_keys = result.keys()
        # nodes = [i[-1]['nodes'] for i in result_keys]
        # node_mg = [list(result[i]) for i in result_keys]
        # cpu_base = {}
        # memory_base = {}
        # point_base = {}
        # point_base_list = []
        # for i in range(len(node_mg)):
        #     cpu_base[nodes[i]] = 0
        #     memory_base[nodes[i]] = 0
        #     point_base[nodes[i]] = 0.0
        #     for j in range(len(node_mg[0])):
        #         cpu_base[nodes[i]] += node_mg[i][j]['cpu']
        #         memory_base[nodes[i]] += node_mg[i][j]['memory']
        #     cpu_base[nodes[i]] = (cpu_base[nodes[i]] / len(node_mg[0])) / self.node_cpu[nodes[i]]
        #     memory_base[nodes[i]] = (memory_base[nodes[i]] / len(node_mg[0])) / self.node_memory[nodes[i]]
        #     tmp = cpu_base[nodes[i]] * 0.6 + memory_base[nodes[i]] * 0.4
        #     point_base[nodes[i]] = tmp
        #     point_base_list.append(tmp)
        #
        # list.sort(point_base_list)
        #
        # for key in nodes:
        #     command = 'kubectl label nodes ' + key + ' woksch-'
        #     os.system(command)
        #     command2 = 'kubectl label nodes ' + key + ' wokpro-'
        #     os.system(command2)
        #     nod_prori = point_base_list.index(point_base[key])
        #     priori = ' wokpro=%d' % nod_prori
        #     command3 = 'kubectl label nodes ' + key + priori
        #     os.system(command3)
        #     if cpu_base[key] <= 0.6 and memory_base[key] <= 0.6:
        #         command = 'kubectl label nodes ' + key + ' woksch=true'
        #         os.system(command)
        #     else:
        #         command = 'kubectl label nodes ' + key + ' woksch=false'
        #         os.system(command)
        self.schedule_label()
        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['replicas'] = self.ps_replicas
        self.template['spec']['tfReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.make_args()
        self.template['spec']['tfReplicaSpecs']['PS']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['args'] = self.args[:]
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = cpu_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        self.template['spec']['tfReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['requests']['memory'] = mem_usage

        log_dir = '/tfdata/tfcnn/expjob/'
        f = open(log_dir+str(name)+'.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl create -f '+log_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
        else:
            print("Error code:"+str(response))

    def delete_tf(self,mode=0):
        name = 'den-'+str(self.task_id)+'-'+str(self.rtimes)
        log_dir = '/tfdata/tfcnn/expjob/'

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
