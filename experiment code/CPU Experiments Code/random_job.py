import task_submit
from task_submit import VGGTask,RESTask,RETask,DENTask,XCETask
import random
import kubernetes
import influxdb
import kubernetes
import requests
from multiprocessing import Process
import multiprocessing
import urllib
import urllib3
import time
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
from Global_client import Global_Influx
aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'

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
                'memory': match_memory(item['usage']['memory'])
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
    def __init__(self,url,args):
        multiprocessing.Process.__init__(self)
        self.url = url
        self.args = args
        self.derivation = args.derivation
        self.time_mess = {}
        # self.derivation = derivation
        self.arg = args
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
        for item in response['items']:
            self.time_mess[item['metadata']['name']] = [item['timestamp']]
        self.client.write_points(generate_item(response,self.measurement),'s',database=self.database)

        time.sleep(self.derivation)
        while True:
            response = catch_message(self.url)
            self.time_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            for item in response['items']:
                self.time_mess[item['metadata']['name']].append(item['timestamp'])
            self.client.write_points(generate_item(response, self.measurement), 's', database=self.database)
            if len(self.time_mess['creation'])%100==0 and len(self.time_mess['creation']) > 0:
                data_frame = pd.DataFrame(self.time_mess)
                data_frame.to_csv(self.save_path + '/' + 'struct.csv', mode='a+', index=False, sep=',')
                for key in self.time_mess:
                    self.time_mess[key] = []
            time.sleep(self.derivation)


def get_ns(v1):
        ns_list = []
        for i in v1.list_namespace().items:
            ns_list.append(i.metadata.name)
        return ns_list

def Monitor_job(tasks,lock,v1):
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
            print(tasks['ns'])
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
                        count_tmp = len(ns_tmp)
                        tasks['count'] = count_tmp
                        lock.release()
                else:
                    pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                    if 'Succeeded' in pod_status or 'Failed' in pod_status:
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
                        # job_tmp.pop(ns)
                        # tasks['job'] = job_tmp
                        tasks['count'] -= 1
                        lock.release()
                    time.sleep(5)

def Submit_job(tasks,lock,v1):
    while True:
        if tasks['start']==False:
            break
        lock.acquire()
        counts = tasks['count']
        lock.release()
        if counts >= tasks['size']:
            time.sleep(float(random.randint(10,15)))
            pass
        else:
            time.sleep(75)
            template_id = random.randint(1, 5)
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
            ps_r = random.randint(1,3)
            worker_r = random.randint(2,6)
            batch = random.randint(128,1024)
            print(tasks)
            if template_id == 1:
                channels = [24,32,40,48,64,72,80,96,120,128,160,192,240,256,320,384,400,480,512,576]
                x1 = random.randint(0,4)
                x2 = random.randint(4,7)
                x3 = random.randint(7,11)
                x4 = random.randint(11,15)
                x5 = random.randint(15,19)
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

                job = VGGTask(v1=v1, template_id=template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tasks['training_step'][template_id - 1],
                              batch_size=batch,
                              interval=tasks['interval'][template_id - 1], task_id=tasks['task_id'][template_id - 1],
                              rtimes=tasks['rtimes'][template_id - 1],
                              tag=tasks['tag'][template_id - 1], channel1=channel1, channel2=channel2,
                              channel3=channel3,
                              channel4=channel4, channel5=channel5,
                              num_layer1=num_layer1, num_layer2=num_layer2, num_layer3=num_layer3,
                              num_layer4=num_layer4,
                              num_layer5=num_layer5)

            elif template_id == 2:
                bottle = random.randint(0, 1)
                channels = [24,32,40,48,64,72,80,96,120,128,160,192,240,256,320,384,400,480,512,576]
                x1 = random.randint(0,3)
                x2 = random.randint(1,7)
                x3 = random.randint(8,14)
                x4 = random.randint(14,19)
                channel1 = channels[x1]
                channel2 = channels[x2]
                channel3 = channels[x3]
                channel4 = channels[x4]
                layer1 = random.randint(2, 6)
                layer2 = random.randint(2, 8)
                layer3 = random.randint(2, 40)
                layer4 = random.randint(2, 6)
                job = RESTask(v1=v1, template_id=template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tasks['training_step'][template_id - 1],
                              batch_size=batch,
                              interval=tasks['interval'][template_id - 1],
                              task_id=tasks['task_id'][template_id - 1], rtimes=tasks['rtimes'][template_id - 1],
                              tag=tasks['tag'][template_id - 1], bottle=bottle, layer1=layer1, layer2=layer2,
                              layer3=layer3,
                              layer4=layer4, channel1=channel1, channel2=channel2, channel3=channel3, channel4=channel4)
            elif template_id == 3:
                stack = random.randint(3, 16)
                channels = [12,16,24,32,40,48,64,72,80,96,120,128,160,192,240,256,320,384,400,480,512,576]
                x1 = random.randint(0,3)
                x2 = random.randint(2,5)
                x3 = random.randint(6,11)
                x4 = random.randint(6,11)
                channel1 = channels[x1]
                channel2 = channels[x2]
                channel3 = channels[x3]
                channel4 = channels[x4]
                job = RETask(v1=v1, template_id=template_id, ps_replicas=ps_r,
                             worker_replicas=worker_r,
                             training_step=tasks['training_step'][template_id - 1],
                             batch_size=batch,
                             interval=tasks['interval'][template_id - 1],
                             task_id=tasks['task_id'][template_id - 1], rtimes=tasks['rtimes'][template_id],
                             tag=tasks['tag'][template_id - 1], stack=stack, channel1=channel1, channel2=channel2,
                             channel3=channel3, channel4=channel4)
            elif template_id == 4:
                repeat = random.randint(4, 12)
                channels = [12,16,24,32,40,48,64,72,80,96,120,128,160,192,240,256,320,384,400,480,512,576,640,728,856,920,960,1024,1280,1408,1536,1600,1728,2048,2096]
                x1 = random.randint(0,5)
                x2 = random.randint(3,9)
                x3 = random.randint(9,12)
                x4 = random.randint(12,18)
                x5 = random.randint(19,24)
                x6 = random.randint(26,28)
                x7 = random.randint(29,31)
                x8 = random.randint(32,34)
                channel1 = channels[x1]
                channel2 = channels[x2]
                channel3 = channels[x3]
                channel4 = channels[x4]
                channel5 = channels[x5]
                channel6 = channels[x6]
                channel7 = channels[x7]
                channel8 = channels[x8]
                job = XCETask(v1=v1, template_id=template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tasks['training_step'][template_id - 1],
                              batch_size=batch,
                              interval=tasks['interval'][template_id - 1],
                              task_id=tasks['task_id'][template_id - 1],
                              rtimes=tasks['rtimes'][template_id - 1], tag=tasks['tag'][template_id - 1], repeat=repeat,
                              channel1=channel1, channel2=channel2, channel3=channel3,
                              channel4=channel4, channel5=channel5, channel6=channel6, channel7=channel7,
                              channel8=channel8)
            else:
                Ls = [16,32,40,48,50,60,64,80,100,120,128,160,180,200,240,250,256]
                ks = [8,10,12,16,24,32,40,48]
                x1 = random.randint(0,16)
                x2 = random.randint(0,7)
                L = Ls[x1]
                k = ks[x2]
                BC = random.randint(0, 1)
                job = DENTask(v1=v1, template_id=template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tasks['training_step'][template_id - 1],
                              batch_size=batch,
                              interval=tasks['interval'][template_id - 1],
                              task_id=tasks['task_id'][template_id - 1], rtimes=tasks['rtimes'][template_id - 1],
                              tag=tasks['tag'][template_id - 1], L=L, k=k, BC=BC)
            lock.acquire()
            if tasks['count'] < tasks['size']:
                job.create_tf()
                ns_tmp = tasks['ns']
                ns_tmp.append(job.name)
                tasks['ns'] = ns_tmp
                # job_tmp = tasks['job']
                # job_tmp[job.name] = job
                # tasks['job'] = job_tmp
                tasks['count'] += 1
            lock.release()



def jiance(tasks,lock):
    while True:
        if tasks['start']==True:
            time.sleep(120)
            lock.acquire()
            save_config(tasks)
            lock.release()
            print('saved configs')
            time.sleep(120)
        else:
            break

def save_config(config):
    config_content = {}
    for key,value in config.items():
        config_content[key] = value
       # if key != 'job' and key != 'ns':
       #     config_content[key] = value
        # task_content['task_id'] = tasks['task_id']
    fw = open('system_info.json', 'w', encoding='utf-8')
    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
    dic_json = json.dumps(config_content, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
    fw.write(dic_json)
    fw.close()

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
    mgr = multiprocessing.Manager()
    tasks = mgr.dict()
    lock = mgr.Lock()
    config_content = load_config('system_info.json')
    for key,value in config_content.items():
        tasks[key] = value
    print(tasks)
    # tasks['ns'] = []
    # tasks['count'] = 0
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
    node_p = Node_mess(url=url, args=args)
    submit_p = multiprocessing.Process(target=Submit_job,args=(tasks,lock,v1))
    monitor_p = multiprocessing.Process(target=Monitor_job,args=(tasks,lock,v1))
    jiance_p = multiprocessing.Process(target=jiance,args=(tasks,lock))
    # derivation
    node_p.daemon = True
    submit_p.daemon = True
    monitor_p.daemon = True
    jiance_p.daemon = True
    k1 = os.getpid()
    k2 = multiprocessing.current_process().pid
    # v1.delete_namespace()
    print(k1, k2)
    while True:
        boots = input("Please Input 'start' to start:\n")
        if boots == 'start':
            node_p.start()
            submit_p.start()
            monitor_p.start()
            jiance_p.start()
        if boots == 'end':
            tasks['start'] = False
            time.sleep(10)
            if tasks['count']>0:
                for ns in tasks['ns']:
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
                        # tasks['job'].pop(ns)
                        tasks['count'] = len(ns_tmp)
                        lock.release()
                    time.sleep(5)
            save_config(tasks)
            print('System end!')
            break


