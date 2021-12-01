# 1584927559
import task_submit
from task_submit import VGGTask,RESTask
import random
import kubernetes
import influxdb
import kubernetes
import signal
from TimeoutException import TimeoutError,Myhandler
import yaml
import requests
from multiprocessing import Process
import multiprocessing
import urllib
import urllib3
import time
import operator
import numpy as np
# from utils import Timer
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor
import time
# from sklearn.preprocessing import MinMaxScaler
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
# aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
# aTokenw = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
# aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJteWFkbWluLXRva2VuLTdqcDl3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im15YWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI3MjhhMzdiOC1jNDA4LTExZWEtODc4My0wMDE2M2UwOWUzODMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06bXlhZG1pbiJ9.ftVVRAsCk7Od45U_C6yfTutRDPsese-JvSGWNgIYcMlxaPfSxKnr7MO1QIug1RG55ZjLhiMcwQPMV74Bw2at2AqKn_mbk_enkwIPm7bZzkL6KG5p_9EnkZRLrsOx0I3jEsGu9cqPRgsR3XIf7njFyGvUSnX6gp7PaGfkT52qnFQD6TRy3ugxvvBqlG0RIMqMuNy2E9GsT8PwuiPPL_oVe4TaQqX6GoyNgdjby8XiSwdpiBUotJlOa_xH_css5Rd3sANzi3-Vei1_qWBeWetrtEzjMkwQzjWEg9MVxh66gQiZySKtfx0hPnRDq9fwQ08MWP2A8vx_UQnJji6wnnSC6Q'
# aTokenw = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJteWFkbWluLXRva2VuLTdqcDl3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im15YWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI3MjhhMzdiOC1jNDA4LTExZWEtODc4My0wMDE2M2UwOWUzODMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06bXlhZG1pbiJ9.ftVVRAsCk7Od45U_C6yfTutRDPsese-JvSGWNgIYcMlxaPfSxKnr7MO1QIug1RG55ZjLhiMcwQPMV74Bw2at2AqKn_mbk_enkwIPm7bZzkL6KG5p_9EnkZRLrsOx0I3jEsGu9cqPRgsR3XIf7njFyGvUSnX6gp7PaGfkT52qnFQD6TRy3ugxvvBqlG0RIMqMuNy2E9GsT8PwuiPPL_oVe4TaQqX6GoyNgdjby8XiSwdpiBUotJlOa_xH_css5Rd3sANzi3-Vei1_qWBeWetrtEzjMkwQzjWEg9MVxh66gQiZySKtfx0hPnRDq9fwQ08MWP2A8vx_UQnJji6wnnSC6Q'
aToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyZWFkZXItdG9rZW4tenFtd3YiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoicmVhZGVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNWU2ZmJjMDItYzljMS0xMWVhLTg3ODMtMDAxNjNlMDllMzgzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnJlYWRlciJ9.tQ4SMtyJxdvQes21W6glYz510u0wtLU8IloYZJSvHkKS4EykgmyzRndmCqJNnUe2KpAgQfeMp1ivHCbvaJ2w3XOKqePwLO6ngla6zG7SJvWwd3SdtjcT8i6dC01MzyI0T3HxQzttLvHM4RrGthM7-0NNzTlth-AqTTdh6HOnuznedortez7nz8t5-C4vRDoRBZXa6qq9vcxiaoJPd7aEfJD3QjDl0E7nJg0DlvxH1sIlCCRWEe_d3FhmF8llmRO132ZNsDvI5qAgLBQBeKPzIkxfd8gTvarxcQqD97sDU_0ppSkyHmVSEgGh5VKGI9M5BqSjW2RUybA_jz2kJXvTew"
aTokenw = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyZWFkZXItdG9rZW4tenFtd3YiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoicmVhZGVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNWU2ZmJjMDItYzljMS0xMWVhLTg3ODMtMDAxNjNlMDllMzgzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnJlYWRlciJ9.tQ4SMtyJxdvQes21W6glYz510u0wtLU8IloYZJSvHkKS4EykgmyzRndmCqJNnUe2KpAgQfeMp1ivHCbvaJ2w3XOKqePwLO6ngla6zG7SJvWwd3SdtjcT8i6dC01MzyI0T3HxQzttLvHM4RrGthM7-0NNzTlth-AqTTdh6HOnuznedortez7nz8t5-C4vRDoRBZXa6qq9vcxiaoJPd7aEfJD3QjDl0E7nJg0DlvxH1sIlCCRWEe_d3FhmF8llmRO132ZNsDvI5qAgLBQBeKPzIkxfd8gTvarxcQqD97sDU_0ppSkyHmVSEgGh5VKGI9M5BqSjW2RUybA_jz2kJXvTew"
# eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJteWFkbWluLXRva2VuLTdqcDl3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im15YWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI3MjhhMzdiOC1jNDA4LTExZWEtODc4My0wMDE2M2UwOWUzODMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06bXlhZG1pbiJ9.ftVVRAsCk7Od45U_C6yfTutRDPsese-JvSGWNgIYcMlxaPfSxKnr7MO1QIug1RG55ZjLhiMcwQPMV74Bw2at2AqKn_mbk_enkwIPm7bZzkL6KG5p_9EnkZRLrsOx0I3jEsGu9cqPRgsR3XIf7njFyGvUSnX6gp7PaGfkT52qnFQD6TRy3ugxvvBqlG0RIMqMuNy2E9GsT8PwuiPPL_oVe4TaQqX6GoyNgdjby8XiSwdpiBUotJlOa_xH_css5Rd3sANzi3-Vei1_qWBeWetrtEzjMkwQzjWEg9MVxh66gQiZySKtfx0hPnRDq9fwQ08MWP2A8vx_UQnJji6wnnSC6Q
LOSSHOST = '172.16.190.97'
LOSSPORT = 12527
DNA_SIZE = 4
XBOUND = [1,2]
XBOUND2 = [0.5,0.95]
YBOUND2 = [0.65,0.95]
YBOUND = [1,3]
CROSSOVER_RATE = 0.8
CROSS_RATE=0.8
POP_SIZE = 6
N_GENERATIONS = 4
sleep_last_length = (68/3)*3
pop_total = []
GPU_EST = joblib.load("est_gpu.pkl")
'''
修改：动态调整策略，发布频率，监控代码迁移,资源配置
'''

rfr2 = joblib.load('rfr_batch.pkl')
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
def reload_jobs(job_name,task_id):
    save_job_path = '/data/tfdata/' \
                    'nfs/%s/%s.json' % (job_name, job_name)
    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    save_batch_path = '/data/tfdata/k8snfs/%s/%s_change.json' % (job_name,job_name)
   # with open(full_flie_name,'r') as yaml_job:
        #job_obj = yaml.load(yaml_job.read())

    job_config = load_config(save_job_path)
    job_res_config = load_config(save_res_path)
    job_batch_config = load_config(save_batch_path)
    params_dic = {}
    keys = job_config.keys()
    for key in keys:
        params_dic[key] = job_config[key]
    params_dic['batch_size'] = job_batch_config['batch']
    params_dic['part'] = job_batch_config['part']

    # params_dic['v1'] = v1
    if task_id != -1:
        params_dic['task_id'] = task_id
        params_dic['rtimes'] = task_id
    if job_config['template_id'] == 1:
        job_reload = VGGTask(**params_dic)
        job_reload.measure = "VGG %d" % job_reload.task_id
    elif job_config['template_id'] == 2:
        job_reload = RESTask(**params_dic)
        job_reload.measure = "RES %d" % job_reload.task_id
   # job_reload.template = job_obj
    #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,'cpu_source':job.cpu_allocate,
    # 'mem_source':job.memory_allocate,'cpu_high':cpu_base}
    job_reload.cpu_allocate = job_res_config['cpu_source']
    job_reload.memory_allocate = job_res_config['mem_source']
    job_reload.deadline = job_res_config['deadline']
    job_reload.starttime = job_res_config['start_time']
    return job_reload

job_basic0 = reload_jobs("res-1-1",-1)
basic_job_cpu = job_basic0.total_cpu
basic_job_mem = job_basic0.total_mem

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

def translateDNA(pop):
    global DNA_SIZE,XBOUND,YBOUND
    print(pop.shape)
    #pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目：
    # x_pop = pop[:,1::2]#从第1列开始，步进为2
    x_pop = pop[:,::1]#从第0列开始，步进为2
    # #pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)完成解码:二进制码求相应十进制值然后压缩到相应范围内即可完成解码
    x = x_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(XBOUND[-1] - XBOUND[0])+XBOUND[0]
    # y = y_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(YBOUND[-1] - YBOUND[0])+YBOUND[0]
    return x

def existss(pop_total,gene,init=1):
    if init == 0:
        gene10 = gene.dot(2 ** np.arange(DNA_SIZE)[::-1])
        pop_total = list(gene10)
        return pop_total
    else:
        gene10 = int(gene.dot(2 ** np.arange(DNA_SIZE)[::-1]))
        if gene10 in pop_total:
            return True
        else:
            pop_total.append(gene10)
            return False



def translateDNA2(pop):
    global DNA_SIZE,XBOUND2,YBOUND2
    print(pop.shape)
    x_pop = pop[:, 1::2]  # 从第1列开始，步进为2
    y_pop = pop[:, ::2]  # 从第0列开始，步进为2
    # #pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)完成解码:二进制码求相应十进制值然后压缩到相应范围内即可完成解码
    x = x_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (XBOUND2[-1] - XBOUND2[0]) + XBOUND2[0]
    y = y_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (YBOUND2[-1] - YBOUND2[0]) + YBOUND2[0]
    return x, y

def predict_min_map1(job_exp):
    job_name = job_exp['name']
    batch = job_exp['batch']
    need = job_exp['need']
    part = job_exp['part']
    rest = job_exp['rest']
    global rfr2
    global basic_job_cpu
    global basic_job_mem
    job_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
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

    real_batch0 = job_config['real_batch']
    flops = job_config['flops_res']
    params = job_config['params_res']
    real_batch = batch // part
    if real_batch >= 78:
        real_batch = 78
    elif real_batch < 1:
        real_batch = 1

    # cpu_high = job_config['cpu_high']
    # mem_base = job_config['memory_base']
    # cpu_alpha = cpu/ cpu_high
    # mem_alpha = mem/ mem_base
    #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
    # data = np.array([real_batch,flops,params,1])
    data = np.array([real_batch, params, 1])
    data = np.mat(data)
    data = data.A
    iteration = rfr2.predict(data)
    iteration = float(iteration)
    delta = (real_batch0*rest)/real_batch
    now_time = delta*iteration
    pred = ((need - now_time)/need)+(5e-5)
    # pred = (0 - iteration) * (
    #             (ps * 700 + worker * cpu) / basic_job_cpu + (ps * 2048 + worker * mem) / basic_job_mem)
    return pred

def predict_min_map3(job_exp):
    job_name = job_exp['name']
    cpu = job_exp['cpu']
    mem = job_exp['mem']
    global rfr2
    global basic_job_cpu
    global basic_job_mem
    job_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
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
    cpu_alpha = cpu/ cpu_high
    mem_alpha = mem/ mem_base
    #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
    data = np.array([batch, flops, params, cpu_alpha, mem_alpha])
    data = np.mat(data)
    data = data.A
    iteration = rfr2.predict(data)
    iteration = float(iteration)
    pred = 0 - iteration
    # pred = (0 - iteration) * (
    #             (ps * 700 + worker * cpu) / basic_job_cpu + (ps * 2048 + worker * mem) / basic_job_mem)
    return pred

def predict_min_map4(job_exp):
    job_name = job_exp['name']
    cpu = job_exp['cpu']
    mem = job_exp['mem']
    global rfr2
    global basic_job_cpu
    global basic_job_mem
    job_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
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
    cpu_alpha = cpu/ cpu_high
    mem_alpha = mem/ mem_base
    #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
    data = np.array([batch, flops, params, cpu_alpha, mem_alpha])
    data = np.mat(data)
    data = data.A
    iteration = rfr2.predict(data)
    iteration = float(iteration)
    worker = job_exp['worker']
    mini0 = job_exp['mini0']
    cpu_allocate = job_exp['callo']
    mem_allocate = job_exp['mallo']
    # mini_batch = predict_min(aim, cpu_pre[i], mem_pre[i], rfr)
    score = worker * (0.75 * (cpu_allocate - cpu) / basic_job_cpu + 0.25 * (mem_allocate - mem) / basic_job_mem)
    minik = iteration / mini0
    score = score / minik
    # pred.append(score)
    # pred = (0 - iteration) * (
    #             (ps * 700 + worker * cpu) / basic_job_cpu + (ps * 2048 + worker * mem) / basic_job_mem)
    return score

def  get_fitness1(aim,pop,batch,part,need,rest):

    batch_alpha = translateDNA(pop)
    batch_pre = (batch)*batch_alpha
    # mem_pre = mem_base*mem_alpha
    job_exp_list = []
    # job_name = job_exp['name']
    # cpu = job_exp['cpu']
    # mem = job_exp['mem']


    for i in range(len(batch_pre)):
        batch_pre[i] = math.ceil(batch_pre[i])
        if batch_pre[i] >= 78:
            batch_pre[i] = 78
        if batch_pre[i] <= 1:
            batch_pre[i] = 1

        job_exp_list.append({'name':aim,'batch':(batch_pre[i]),'part':part,'need':need,'rest':rest})
    # pred = []
    pool_fit = multiprocessing.Pool(4)
    # job_name = job_exp['name']
    # batch = job_exp['batch']
    # need = job_exp['need']
    # part = job_exp['part']
    # rest = job_exp['rest']
    pred = pool_fit.map(predict_min_map1,job_exp_list)
    pool_fit.close()
    pool_fit.join()
    # for i in range(len(cpu_pre)):
    #     mini_batch = predict_min(aim,cpu_pre[i],mem_pre[i],rfr)
    #     mini_batch = float(mini_batch)
    #     pred.append((0-mini_batch)*((ps*700+worker*cpu_pre[i])/total_cpu+(ps*2048+worker*mem_pre[i])/total_memory))
    pred = np.array(pred)
    # pred = mini_batch
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

def get_fitness3(aim,pop,cpu_base,mem_base):
    #任务完成不了了，所以直接看minbatch可以减少多少而不是资源利用
    cpu_alpha,mem_alpha = translateDNA(pop)
    cpu_pre = cpu_base*cpu_alpha
    mem_pre = mem_base*mem_alpha
    job_exp_list = []
    for i in range(len(cpu_pre)):
        job_exp_list.append({'name':aim,'cpu':cpu_pre[i],'mem':mem_pre[i]})
    pool_fit = multiprocessing.Pool(6)
    pred = pool_fit.map(predict_min_map3, job_exp_list)
    pool_fit.close()
    pool_fit.join()
    # pred = []
    # for i in range(len(cpu_pre)):
    #     mini_batch = predict_min(aim,cpu_pre[i],mem_pre[i],rfr)
    #     mini_batch = float(mini_batch)
    #     pred.append((0-mini_batch))
    pred = np.array(pred)
    # pred = mini_batch
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

def get_fitness4(aim,pop,cpu_base,mem_base,cpu_allocate,mem_allocate,worker,mini0):
    #任务可以完成，现在要减少资源，当然就是看减少资源的总量和减少资源造成的minibatch之间的权衡
    cpu_alpha,mem_alpha = translateDNA2(pop)
    cpu_pre = cpu_allocate*cpu_alpha
    mem_pre = mem_allocate*mem_alpha
    job_exp_list = []
    for i in range(len(cpu_pre)):
        if cpu_pre[i] < 0.45 * cpu_base:
            cpu_pre[i] = math.ceil(0.45 * cpu_base)
        if mem_pre[i] < 0.9 * mem_base:
            mem_pre[i] = math.ceil(0.9 * mem_base)
        job_exp_list.append({'name': aim, 'cpu': cpu_pre[i], 'mem': mem_pre[i],'worker':worker,'mini0':mini0,'callo':cpu_allocate,'mallo':mem_allocate})
    pool_fit = multiprocessing.Pool(6)
    pred = pool_fit.map(predict_min_map4, job_exp_list)
    pool_fit.close()
    pool_fit.join()
    pred = np.array(pred)
    return (pred - min(pred)) + 1e-4

def select(pop,fitness):
    global POP_SIZE
    idx = np.random.choice(np.arange(pop.shape[0]),size=POP_SIZE,replace=True,p=fitness/fitness.sum())
#     不熟悉numpy的朋友可以查阅一下这个函数，主要是使用了choice里的最后一个参数p，参数p描述了从np.arange(POP_SIZE)里选择每一个元素的概率，
#     概率越高约有可能被选中，最后返回被选中的个体即可。
#     print(idx)
#     k = set(idx)
#     pl = dict()
#     for id in k:
#         pl[id] = 0
#     for id in idx:
#         pl[id] = pl[id]+1
#     print(len(list(k)))
#     print(pl)
    return pop[idx]

def predict_min_first(rfr,batch,flops,params,template):
    # data = np.array([batch, flops, params, 1])
    data = np.array([batch, params, 1])
    data = np.mat(data)
    data = data.A
    iteration = rfr.predict(data)
    if template == 2:
        iteration = float(float(iteration)*random.randint(20,32)/16)
    else:
        iteration = float(float(iteration)*random.randint(32,128)/16)
    return iteration

def predict_min(job_name,rfr,batch0=-1,part0=-1):
    job_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_config_path = '/data/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    job_change_path = '/data/tfdata/k8snfs/%s/%s_change.json' % (job_name, job_name)
    job_config = load_config(job_path)
    job_config2 = load_config(job_config_path)
    batch_config = load_config(job_change_path)

    batch = job_config['batch_res']
    flops = job_config['flops_res']
    params = job_config['params_res']

    if batch0 >0 and part0 > 0:
        real_batch = batch0 // part0
    else:
        real_batch = job_config['real_batch']
    #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
    # data = np.array([real_batch, flops, params, 1])
    data = np.array([real_batch, params, 1])
    data = np.mat(data)
    data = data.A
    iteration = rfr.predict(data)
    template = int(job_config2['template_id'])
    if template == 2:
        iteration = float(float(iteration)*random.randint(20,32)/16)
    else:
        iteration = float(float(iteration)*random.randint(32,128)/16)
    return iteration



def crossover_and_mutation(pair):
    global pop_total
    global POP_SIZE,N_GENERATIONS,CROSS_RATE
    new_pop = []
    i = 0
    # pop_sizes = len(pop)
    father = pair[0]
    mother = pair[1]

    # print(father)
    # 遍历种群中的每一个个体，将该个体作为父亲
    # 孩子先得到父亲的全部基因（这里我把一串二进制串的那些0，1称为基因）
    child = np.array(list(father)[:])
    i = i + 1
    child2 = []
    # print(child.shape)
    cross = False
    if np.random.rand() < CROSS_RATE:
        cross = True
        # # 产生子代时不是必然发生交叉，而是以一定的概率发生交叉
        # mother = pop[np.random.randint(POP_SIZE)]  # 再种群中选择另一个个体，并将该个体作为母亲
        # # if i == len(pop):
        # #     i = 0
        # # mother = pop[i]
        child2 = np.array(list(mother)[:])
        cross_points = np.random.randint(low=0, high=DNA_SIZE)  # 随机产生交叉的点
        child[cross_points:] = mother[cross_points:]  # 孩子得到位于交叉点后的母亲的基因
        child2[cross_points:] = father[cross_points:]
    mutation(child)  # 每个后代有一定的机率发生变异
    exist_res = existss(pop_total, child)
    if exist_res:
        new_pop.append(father)
    else:
        if cross:
            # print(child2)
            # print(child2.shape)
            mutation(child2)
            exist_res = existss(pop_total, child2)
            if not exist_res:
                new_pop.append(child2)
        new_pop.append(child)
        # new_pop.append(child2)
        # print(child)
        # print(father)
        if not operator.eq(list(child), list(father)) and not operator.eq(list(child2), list(father)):
            new_pop.append(father)

    return new_pop

# def make_new_pop(inpop):

def mutation(child, MUTATION_RATE=0.003):
    if np.random.rand() < MUTATION_RATE: 				#以MUTATION_RATE的概率进行变异
        mutate_point = np.random.randint(0, DNA_SIZE-1)	#随机产生一个实数，代表要变异基因的位置
        child[mutate_point] = child[mutate_point]^1 	#将变异点的二进制为反转

def kongxian(batch_size,part,flops,params,pop):
    global GPU_EST
    batch_alpha = translateDNA(pop)
    delete_pop = []
    for i in range(len(batch_alpha)):
        new_batch = batch_alpha[i]*batch_size
        real_new = new_batch//part
        if real_new <= 1:
            real_new = 1
        if real_new >= 78:
            real_new = 78
        # res = GPU_EST.predict(np.array([real_new,flops,params]).reshape(1,3))
        res = GPU_EST.predict(np.array([real_new, params]).reshape(1, 2))
        if res == 1:
            continue
        else:
            delete_pop.append(i)
    return delete_pop



def kongxian2(node_list,res_cpu,res_mem,ps,cpu_allocate,mem_allocate,node_index,k8s_monitor,index_node,worker_now):
    k8s_tmp = k8s_monitor
    res_load = [res_cpu[i] for i in node_list]
    # job_aim = reload_jobs(aim_name,-1)
    catch = False
    list.sort(res_load)
    using = ''
    if res_load[-1] >= cpu_allocate:
        res_load[-1] = res_load[-1] - cpu_allocate
        list.sort(res_load)
        if res_load[-1] > 1000*ps:
            nodes = list(k8s_monitor.keys())
            for node in nodes:
                if k8s_tmp[node]['avail'] > 0:
                    tmp_k8s_ava = k8s_tmp[node]['avail']
                    tmp_k8s_ava = tmp_k8s_ava - 1
                    k8s_tmp[node]['avail'] = tmp_k8s_ava
                    catch = True
                    using = node
                    break
            if catch:
                if worker_now >= 6:
                    tmp_k8s_ava = k8s_tmp[using]['avail']
                    tmp_k8s_ava = tmp_k8s_ava+1
                    k8s_tmp[using]['avail'] = tmp_k8s_ava
                    return False,k8s_tmp
                else:
                    return True,k8s_tmp
            else:
                return  False,k8s_tmp
        else:
            return False,k8s_tmp
    else:
        return False,k8s_tmp

def catch_task_gpu(job_name,k8s_monitor_x):
    using_job = reload_jobs(job_name,-1)
    result = {}
    result_list = {'uti':[],'mem':[],'base':[]}
    node_index,k8s_monitor,index_node = using_job.select_k8s_gpu()
    node_list = list(k8s_monitor.keys())
    process_client = influxdb.InfluxDBClient(host='172.16.190.97',port=8086,username='admin',password='admin',database='PREDICT')
    pre_list = job_name.split('-')
    pres = pre_list[0].upper()
    pres = pres.strip()
    measurement = pres+'P'+pre_list[-1]


    print(measurement)
    process = process_client.query("select * from "+measurement+' group by nodes order by desc limit 1')
    proce_key = list(process.keys())
    name_list = {}
    for proc in proce_key:
        name_list[proc[-1]['nodes']] = list(process[proc])[0]['proc']
    name = list(name_list.keys())
    for n in name:
        aim_process = int(name_list[n])
        for node in node_list:
            gpu_dict = k8s_monitor[node]['pid']
            gpu_key = list(gpu_dict.keys())
            # print(type(gpu_key[0]))
            gpu_keys = [int(i) for i in gpu_key]
            if aim_process in gpu_keys:
                result_list['uti'].append(gpu_dict[aim_process]['uti'])
                result_list['mem'].append(gpu_dict[aim_process]['mem'])
                result_list['base'].append(gpu_dict[aim_process]['base'])
                break
    if not result_list['uti'] or not result_list['mem'] or not result_list['base']:
        result['uti'] = -1
        result['mem'] = -1
        result['base'] = -1
    else:
        result['uti'] = np.mean(result_list['uti'][:])
        result['mem'] = np.mean(result_list['mem'][:])
        result['base'] = np.mean(result_list['base'][:])

    return result



def finish(res_iter,pop,res_time,cpu_allocate,mem_allocate,cpu_base,mem_base,rfr,aim):
    cpu_alpha,mem_alpha = translateDNA2(pop)
    delete_pop = []
    cpu_pre = cpu_allocate*cpu_alpha
    mem_pre = mem_allocate*mem_alpha
    for i in range(len(cpu_pre)):
        if cpu_pre[i] < 0.45 * cpu_base:
            cpu_pre[i] = math.ceil(0.45 * cpu_base)
        if mem_pre[i] < 0.9 * mem_base:
            mem_pre[i] = math.ceil(0.9 * mem_base)
        mini_batch = predict_min(aim,rfr)
        if mini_batch*res_iter > res_time:
            delete_pop.append(i)

    return delete_pop

def finish2(total_step,res_time,reload_point,worker,ps,change_ps,mini_batch):
    if worker == 1:
        return False
    if ps - change_ps <= 0:
        return False
    need_time = mini_batch*((total_step*worker/(worker-1)) - reload_point)
    if res_time >= need_time:
        return True
    else:
        return False


def assign_jobs(tasks,rfr,lock):
    global DNA_SIZE,POP_SIZE,N_GENERATIONS
    global pop_total
    #选择标准有两个：
    '''
    1.对于每次选择，选择无法按时完成的任务，使用deadline
    为保证规模并不过分高，则每次选择的是最紧急的任务要进行调整
    2.对于系统负载而言，如果系统资源负载不高的话，则可以考虑调整资源，使其负载率较高--->增大batch size
    3.对于系统而言，如果资源利用率持续低于某个阈值的话可以考虑增加某个任务的负载--> 资源敏感度
    4.每次在调增任务时尝试选择调减任务，然后减少其资源的分配--->减少卡的数量

    :return:
    '''
    step_influx_client = influxdb.InfluxDBClient(host='172.16.190.97', username='admin', password='admin',
                                                 database='PREDICT')

    piotential = []
    job_basic = reload_jobs(tasks['last'], -1)
    print("reload a  job success!!")
    node_list_global = job_basic.node_list
    res_cpu = job_basic.node_cpu

    res_mem = job_basic.node_memory
    res_config0 = {}
    layout_config0 = {}
    lock.acquire()
    tmp_ns = tasks['ns']
    tmp_layout = tasks['nslayout']
    tmp_layout_key = tmp_layout.keys()
    for i in tmp_ns:
        layout_file = '/data/tfdata/k8snfs/%s/layout.json' % i
        res_file = '/data/tfdata/k8snfs/%s/%s_res.json' % (i,i)
        job_file = '/data/tfdata/k8snfs/%s/%s.json' % (i,i)
        batch_file =  '/data/tfdata/k8snfs/%s/%s_change.json' % (i,i)
        res_config = load_config(res_file)
        job_config = load_config(job_file)
        batch_config = load_config(batch_file)
        # "ps_replicas": 2,
        # "worker_replicas": 5,

        res_config0[i] = res_config
        res_config0[i]['ps'] = job_config["ps_replicas"]
        res_config0[i]['worker'] = job_config["worker_replicas"]
        layout_config0[i] = {}
        if os.path.exists(layout_file):
            tmp_cpu = {}
            tmp_mem = {}
            tmp_config = load_config(layout_file)
            tmp_layout_config = {}
            tmp_key = list(tmp_config.keys())
            for tk in tmp_key:
                tmp_cpu[tmp_config[tk]] = 0
                tmp_mem[tmp_config[tk]] = 0
                tmp_layout_config[tmp_config[tk]] = {'ps':0,'worker':0}
            for tk in tmp_key:
                if 'ps' in tk:
                    tmp_cpu[tmp_config[tk]]+= 2000
                    tmp_mem[tmp_config[tk]]+= 2048
                    tmp_layout_config[tmp_config[tk]]['ps']+=1
                else:
                    # "cpu_source": 6046,
                    # "mem_source": 19225,
                    tmp_cpu[tmp_config[tk]]+=res_config['cpu_source']
                    tmp_mem[tmp_config[tk]]+=res_config['mem_source']
                    tmp_layout_config[tmp_config[tk]]['worker'] += 1
            tmp_cpu_key = list(tmp_cpu.keys())
            for tck in tmp_cpu_key:
                res_cpu[tck] = res_cpu[tck] - tmp_cpu[tck]
                res_mem[tck] = res_mem[tck] - tmp_mem[tck]
            layout_config0[i] = tmp_layout_config
        if (i in tmp_layout_key) and tmp_layout[i]:
            piotential.append(i)
    lock.release()
    print("The aim can choose to modulate:")
    print(piotential)
    print("The modulation base config:")
    print(res_config0)
    print("The system machine resource condition:")
    print("CPU condition:")
    print(res_cpu)
    print("Memory condition:")
    print(res_mem)
    print("Layout condition:")
    print(layout_config0)
    if not piotential:
        return {},-1
    assign_config = {}
    # for i in piotential:
    #     assign_config[i] = {}
    aim1 = ''
    aim2 = ''
    mode = 0
    aim = {}
    if not piotential:
        print("Do not have jobs!!")
        return {},-1
    node_index, k8s_monitor, index_node = job_basic.select_k8s_gpu()

    print("The aim can choose to modulate:")
    print(piotential)
    print("The modulation base config:")
    print(res_config0)
    print("The system machine resource condition:")
    print("The GPU condition")
    print(k8s_monitor)
    print("CPU condition:")
    print(res_cpu)
    print("Memory condition:")
    print(res_mem)
    print("Layout condition:")
    print(layout_config0)
    for i in piotential:
        reload_tmp = reload_jobs(i, -1)
        lock.acquire()
        tmp_ns2 = tasks['ns']
        lock.release()
        if i not in tmp_ns2:
            piotential.remove(i)
            res_cpu[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['cpu_source']
            res_mem[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['mem_source']
            res_cpu[ke00] += layout_config0[i][ke00]['ps'] * 2000
            res_mem[ke00] += layout_config0[i][ke00]['ps'] * 2048
            continue
        pod_status = [j.status.phase for j in reload_tmp.v1.list_namespaced_pod(i).items]
        run_result = pd.value_counts(pod_status)
        run_result_dict = dict(run_result)
        if not run_result_dict:
            piotential.remove(i)
        if 'Succeeded' in pod_status or 'Failed' in pod_status:
            piotential.remove(i)
            # if assign_config[i]:
            key00 = layout_config0[i].keys()
            for ke00 in key00:
                res_cpu[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['cpu_source']
                res_mem[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['mem_source']
                res_cpu[ke00] += layout_config0[i][ke00]['ps'] * 2000
                res_mem[ke00] += layout_config0[i][ke00]['ps'] * 2048
            continue
        tmp_re = reload_tmp.deadline - (time.time() - reload_tmp.starttime)
        tmp_iter, total_step, _ = reload_tmp.get_remain(mode=1)
        reload_iter, _, reload_point = reload_tmp.get_remain(mode=0)
        pre_list = reload_tmp.measure.split(" ")
        measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_t = pre_list[0] + 'T' + pre_list[-1]
        res = step_influx_client.query(
            "select * from " + measure_s + " group by nodes order by desc limit 2")
        keys = list(res.keys())
        dic_msg = {}
        time_avg = []
        now_mini = 0.0
        if keys:
            node_list = [b['nodes'] for a, b in keys]
            print("A job node list is:")
            print(node_list)
            for node in node_list:
                for j in range(len(keys)):
                    _, no = keys[j]
                    if no['nodes'] == node:
                        dic_msg[node] = list(res[keys[j]])
            for node in node_list:
                time_avg_list = [float(k['time_d']) for k in dic_msg[node]]
                time_avg_node = np.mean(time_avg_list)
                time_avg.append(time_avg_node)
            print('current time condition:')
            print(time_avg)
            if time_avg:
                now_mini = np.mean(time_avg)
            else:
                now_mini = predict_min(i,rfr)
        else:
            now_mini = predict_min(i, rfr)
        need_time = tmp_iter * now_mini
        res_config0[i]['need'] = need_time
        res_config0[i]['remain_time'] = tmp_re
        res_config0[i]['mini'] = now_mini
        res_config0[i]['remain_iter'] = tmp_iter
        res_config0[i]['reload_iter'] = reload_iter
        res_config0[i]['total_step'] = total_step
        res_config0[i]['reload_point'] = reload_point
        tmp_gpu_task = catch_task_gpu(i,k8s_monitor)
        res_config0[i]['gpuuti'] = tmp_gpu_task['uti']
        res_config0[i]['gpumem'] = tmp_gpu_task['mem']
        res_config0[i]['gpubase'] = tmp_gpu_task['base']

        # save_config(res_config, res_path)
        rescha = need_time - tmp_re
        aim_keys = list(aim.keys())
        if rescha not in aim_keys:
            aim[rescha] = []
        aim[rescha].append(i)
    aim_time = list(aim.keys())
    print("The aim can go to modulate:")
    print(aim)
    print("The time space to be modulate:")
    print(aim_time)
    aim1 = ''
    aim2 = ''
    mode = 0
    print("Something add to the base config:")
    print(res_config0)
    if aim_time:
        list.sort(aim_time)
        if aim_time[-1] <= 0:
            #所有任务都可以完成
            relise_cpu = 0
            relise_mem = 0
            for node in node_list_global:
                relise_cpu+=res_cpu[node]
                relise_mem +=res_mem[node]
            relise_cpu = relise_cpu/job_basic.total_cpu
            relise_mem = relise_mem/job_basic.total_mem
            relise = 0.75*relise_cpu+0.25*relise_mem
            avail = 0
            node_ss = list(k8s_monitor.keys())
            for node in node_ss:
                avail+= k8s_monitor[node]['avail']
            avail = float(avail / 14)
            if avail > 0.4:
                #若GPU资源空闲，此时可以增加节点或者增加任务的base，至少有五张卡空闲
                #选择两个任务增加卡，增加该任务的batch
                #加完了卡以后判断利用率最低的任务，增加batch,
                if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                    aim1 = aim[aim_time[-1]][0]
                    print(aim1)
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[-1]][0]
                    print(aim1)
                    aim_time_po = []
                    up_limit = min(3, len(aim_time))
                    up_limit = 0 - up_limit
                    for i in range(up_limit, 0):
                        for j in aim[aim_time[i]]:
                            aim_time_po.append(j)
                    aim_mingan = {}
                    for j in aim_time_po:
                        aim_mingan[float(res_config0[j]['gpubase'])] = j
                    mingan = list(aim_mingan.keys())
                    list.sort(mingan,reverse=True)
                    if mingan[0] < 0 and len(aim_time_po)>1:
                        aim2 = aim_time_po[-2]
                        if aim2 == aim1:
                            aim2 = ''
                    else:
                        aim2 = aim_mingan[mingan[0]]
                        if aim1 == aim2:
                            if len(mingan)>1:
                                aim2 = aim_mingan[mingan[1]]
                            else:
                                aim2 = aim_time_po[-2]
                                if aim2 == aim1:
                                    aim2 = ''
                mode = 1
            else:
                # 资源比较紧张，考虑减少距离deadline最远，资源利用率最低的任务的卡
                # 释放完卡后选择利用率最低的任务，增加batch，同时增加要加资源的任务的batch
                if len(aim_time) == 1 and len(aim[aim_time[0]]) == 1:
                    aim1 = aim[aim_time[0]][0]
                    print(aim1)
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[0]][0]
                    print(aim1)
                    aim_time_po = []
                    up_limit = min(3, len(aim_time))
                    # up_limit = 0 - up_limit
                    for i in range(0, up_limit):
                        if aim_time[i] >= 0:
                            break
                        for j in aim[aim_time[i]]:
                            aim_time_po.append(j)
                    aim_mingan = {}
                    for j in aim_time_po:
                        if float(res_config0[j]['gpubase']) > 0:
                            aim_mingan[float(res_config0[j]['gpubase'])] = j
                    mingan = list(aim_mingan.keys())
                    if not mingan and len(aim_time_po)>1:
                        aim2 = aim_time_po[1]
                        if aim2 == aim1:
                            aim2 = ''
                    else:
                        list.sort(mingan)
                        aim2 = aim_mingan[mingan[0]]
                        if aim2 == aim1:
                            if len(mingan) > 1:
                                aim2 = aim_mingan[mingan[1]]
                            else:
                                aim2 = aim_time_po[1]
                            if aim2 == aim1:
                                aim2 = ''
                mode = 4

        elif aim_time[0] < 0:
            # 有任务完不成，有任务可以完成，考虑减少资源和增大资源，减少离deadline最远且对资源最不敏感的任务，增大超时最严重的任务
            # 返回任务
            # 增加资源的任务为超时最严重的任务，没有疑问，减少资源的任务则为离deadline较远且对资源最不敏感的任务，即剥夺资源带来的影响最小：
            if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                aim1 = aim[aim_time[-1]][0]
                print(aim1)
                aim2 = ''
            else:
                aim1 = aim[aim_time[-1]][0]
                print(aim1)
                aim_time_po = []
                up_limit = min(3, len(aim_time))
                # up_limit = 0 - up_limit
                for i in range(0, up_limit):
                    if aim_time[i] >= 0:
                        break
                    for j in aim[aim_time[i]]:
                        aim_time_po.append(j)
                aim_mingan = {}
                up_limit2 = min(2, len(aim_time_po))

                for j in range (0,up_limit2):
                    if float(res_config0[aim_time_po[j]]['gpubase']) > 0:
                        aim_mingan[float(res_config0[aim_time_po[j]]['gpubase'])] = aim_time_po[j]
                mingan = list(aim_mingan.keys())
                if not mingan:
                    aim2 = aim_time_po[0]
                    if aim2 == aim1:
                        aim2 = ''
                else:
                    list.sort(mingan, reverse=True)
                    aim2 = aim_mingan[mingan[-1]]
                    if aim2 == aim1:
                        if len(mingan) > 1:
                            aim2 = aim_mingan[mingan[-2]]
                        else:
                            aim2 = aim_time_po[0]
                        if aim2 == aim1:
                            aim2 = ''
            mode = 2
        elif aim_time[0] >= 0:
            if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                aim1 = aim[aim_time[-1]][0]
                aim2 = ''
                print(aim1)
            else:
                # 都完不成，则返回超时最严重的两个任务，开始启发式评估方案，增加batch，增加节点
                aim1 = aim[aim_time[-1]][0]
                print(aim1)
                if len(aim[aim_time[-1]]) > 1:
                    # print("wenti")
                    aim2 = aim[aim_time[-1]][1]
                else:
                    # print("chuxianwenti")
                    aim2 = aim[aim_time[-2]][0]
                print(aim2)
            mode = 3
    print('The mode will be used: %d' % mode)
    print('The first aim and second aim:')
    print(aim1)
    print(aim2)
    if mode == 0:
        print("Mode %d Do not find fit job to get modluation for number of GPUS!!" % mode)
        assign_config = {}
    elif mode == 1:
        if not aim1:
            print("Mode %d Do not find fit job to get modluation for number of GPUS!!" % mode)
            assign_config = {}
        # 具体实施方案：增减一个节点就可以了
        # 具体实施方案，则为两种选择，修改节点数和增加每个节点的资源，在这里评估指标变为节约的时间/资源
        # 可选方案：增加1个节点/添加相应的资源，判断方法：节约的时间/添加的资源，如果资源超过范围则丢弃该方案，直到找到合适的方案，备选方案为
        # job_aim1 = reload_jobs(aim1, -1)
        else:
            method1 = {}
            method2 = {}
            aim1_path = '/data/tfdata/k8snfs/%s/%s.json' % (aim1,aim1)
            aim1_config = load_config(aim1_path)
            aim1_workernow = int(aim1_config["worker_replicas"])
            node_index_k, k8s_monitor_k, index_node_k = job_basic.select_k8s_gpu()
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 1,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                         index_node_k,aim1_workernow)
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                         index_node_k,aim1_workernow)
            print("after allocate to aim1:")
            print(k8s_monitor_k)
            if not change_number:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                         index_node_k,aim1_workernow)

            if change_number:
                assign_config[aim1] = [method1]
            else:
                assign_config[aim1] = []

            pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(len(pop_total))
            for _ in range(N_GENERATIONS):
                input_pop = []
                for father in pop:
                    mother = pop[np.random.randint(POP_SIZE)]
                    input_pop.append([father, mother])
                pool_cross = multiprocessing.Pool(4)
                pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
                pool_cross.close()
                pool_cross.join()
                # pop = crossover_and_mutation(input_pop)
                pop = []
                for item in pop_tmp:
                    for item2 in item:
                        pop.append(item2)
                pop = np.array(pop)
                fitness = get_fitness1(aim1, pop, res_config0[aim1]['batch_res'], res_config0[aim1]['part'],
                                       need=res_config0[aim1]['need'], rest=res_config0[aim1]['remain_iter'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
                    break

            delete_pop = kongxian(batch_size=res_config0[aim1]['batch_res'], part=res_config0[aim1]['part'],
                                  flops=res_config0[aim1]['flops_res'], params=res_config0[aim1]['params_res'], pop=pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size != 0:
                fitness = get_fitness1(aim=aim1, pop=pop_new, batch=res_config0[aim1]['batch_res'],
                                       part=res_config0[aim1]['part'], need=res_config0[aim1]['need'],
                                       rest=res_config0[aim1]['remain_iter'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                batch_mode = translateDNA(pop_new)
                aim1_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim1]['batch_res'])
                if aim1_batch >= 78:
                    aim1_batch = 78
                if aim1_batch <= res_config0[aim1]['part']:
                    aim1_batch = res_config0[aim1]['part']
                method2 = {'type': 2, 'batch': aim1_batch}
                assign_config[aim1].append(method2)
            # "cpu_high": 8991,
            # "memory_base": 8706,
            if assign_config[aim1]:
                if assign_config[aim1][0]['type'] == 1:
                    res_condition = {}
                    res_load = [res_cpu[i] for i in node_list_global]
                    for no_k0 in node_list_global:
                        res_condition[res_cpu[no_k0]] = no_k0
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    res_cpu[deal_node] -= res_config0[aim1]['cpu_source']
                    res_mem[deal_node] -= res_config0[aim1]['mem_source']
                    # layout_config0[aim1][deal_node]['worker']+=1
                    aim1_tmp_layout = layout_config0[aim1]
                    aim1_tlk = list(aim1_tmp_layout.keys())
                    if deal_node in aim1_tlk:
                        layout_config0[aim1][deal_node]['worker'] += 1
                    else:
                        layout_config0[aim1][deal_node] = {'ps': 0, 'worker': 1}
                    res_condition.pop(res_load[-1])
                    update_reload = res_load[-1] - res_config0[aim1]['cpu_source']
                    res_condition[update_reload] = deal_node
                    res_load[-1] = update_reload
                    if assign_config[aim1][0]['ps'] != 0:
                        list.sort(res_load)
                        deal_node = res_condition[res_load[-1]]
                        res_cpu[deal_node] -= 1000
                        res_mem[deal_node] -= 2048
                        aim1_tmp_layout = layout_config0[aim1]
                        aim1_tlk = list(aim1_tmp_layout.keys())
                        if deal_node in aim1_tlk:
                            layout_config0[aim1][deal_node]['ps'] += 1
                        else:
                            layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}
            if not aim2:
                assign_config[aim2] = []
            else:
                aim1 = aim2
                # job_aim2 = reload_jobs(aim1, -1)
                method1 = {}
                method2 = {}
                print("before modulate aim2")
                print(k8s_monitor_k)
                aim1_path = '/data/tfdata/k8snfs/%s/%s.json' % (aim1, aim1)
                aim1_config = load_config(aim1_path)
                aim1_workernow = int(aim1_config["worker_replicas"])
                if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                    method1 = {'type': 1, 'ps': 1, 'worker': 1}
                    change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 1,
                                                             res_config0[aim1]['cpu_source'],
                                                             res_config0[aim1]['mem_source'], node_index_k,
                                                             k8s_monitor_k,
                                                             index_node_k,aim1_workernow)
                else:
                    method1 = {'type': 1, 'ps': 0, 'worker': 1}
                    change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                             res_config0[aim1]['cpu_source'],
                                                             res_config0[aim1]['mem_source'], node_index_k,
                                                             k8s_monitor_k,
                                                             index_node_k,aim1_workernow)

                if not change_number:
                    method1 = {'type': 1, 'ps': 0, 'worker': 1}
                    change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                             res_config0[aim1]['cpu_source'],
                                                             res_config0[aim1]['mem_source'], node_index_k,
                                                             k8s_monitor_k,
                                                             index_node_k,aim1_workernow)
                if change_number:
                    assign_config[aim1] = [method1]
                else:
                    assign_config[aim1] = []

                pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
                pop_total = []
                pop_total = existss(pop_total, pop, init=0)
                print(len(pop_total))
                for _ in range(N_GENERATIONS):
                    input_pop = []
                    for father in pop:
                        mother = pop[np.random.randint(POP_SIZE)]
                        input_pop.append([father, mother])
                    pool_cross = multiprocessing.Pool(4)
                    pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
                    pool_cross.close()
                    pool_cross.join()
                    # pop = crossover_and_mutation(input_pop)
                    pop = []
                    for item in pop_tmp:
                        for item2 in item:
                            pop.append(item2)
                    pop = np.array(pop)
                    fitness = get_fitness1(aim1, pop, res_config0[aim1]['batch_res'], res_config0[aim1]['part'],
                                           need=res_config0[aim1]['need'], rest=res_config0[aim1]['remain_iter'])
                    pop = select(pop, fitness)  # 选择生成新的种群
                    if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
                        break

                delete_pop = kongxian(batch_size=res_config0[aim1]['batch_res'], part=res_config0[aim1]['part'],
                                      flops=res_config0[aim1]['flops_res'], params=res_config0[aim1]['params_res'],
                                      pop=pop)
                delete_pop = list(delete_pop)
                # ac = np.delete(ac,[1,3,5],axis=0)
                pop_new = np.delete(pop, delete_pop, axis=0)
                if pop_new.size != 0:
                    fitness = get_fitness1(aim=aim1, pop=pop_new, batch=res_config0[aim1]['batch_res'],
                                           part=res_config0[aim1]['part'], need=res_config0[aim1]['need'],
                                           rest=res_config0[aim1]['remain_iter'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    batch_mode = translateDNA(pop_new)
                    aim1_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim1]['batch_res'])
                    if aim1_batch >= 78:
                        aim1_batch = 78
                    if aim1_batch <= res_config0[aim1]['part']:
                        aim1_batch = res_config0[aim1]['part']
                    method2 = {'type': 2, 'batch': aim1_batch}
                    assign_config[aim1].append(method2)



                    # print("最优的基因型：", pop[max_fitness_index])
                    # print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))
    elif mode == 2:
        #一增一减，结合4和3即可轻松给出了
        #首先对于aim1,增加资源：
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {}, mode
        method1 = {}
        method2 = {}
        change_number = False
        node_index_k, k8s_monitor_k, index_node_k = job_basic.select_k8s_gpu()
        aim1_path = '/data/tfdata/k8snfs/%s/%s.json' % (aim1, aim1)
        aim1_config = load_config(aim1_path)
        aim1_workernow = int(aim1_config["worker_replicas"])
        if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
            method1 = {'type': 1, 'ps': 1, 'worker': 1}
            change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 1,
                                                     res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                                     node_index_k, k8s_monitor_k, index_node_k,aim1_workernow)
        else:
            method1 = {'type': 1, 'ps': 0, 'worker': 1}
            change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                     res_config0[aim1]['cpu_source'],
                                                     res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                     index_node_k,aim1_workernow)

        if not change_number:
            method1 = {'type': 1, 'ps': 0, 'worker': 1}
            change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                     res_config0[aim1]['cpu_source'],
                                                     res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                     index_node_k,aim1_workernow)


        # "cpu_high": 8991,
        # "memory_base": 8706,
        if change_number:
            assign_config[aim1] = [method1]
        else:
            assign_config[aim1] = []

        pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
        pop_total = []
        pop_total = existss(pop_total, pop, init=0)
        print(len(pop_total))
        for _ in range(N_GENERATIONS):
            input_pop = []
            for father in pop:
                mother = pop[np.random.randint(POP_SIZE)]
                input_pop.append([father, mother])
            pool_cross = multiprocessing.Pool(4)
            pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
            pool_cross.close()
            pool_cross.join()
            # pop = crossover_and_mutation(input_pop)
            pop = []
            for item in pop_tmp:
                for item2 in item:
                    pop.append(item2)
            pop = np.array(pop)
            fitness = get_fitness1(aim1, pop, res_config0[aim1]['batch_res'], res_config0[aim1]['part'],
                                   need=res_config0[aim1]['need'], rest=res_config0[aim1]['remain_iter'])
            pop = select(pop, fitness)  # 选择生成新的种群
            if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
                break

        delete_pop = kongxian(batch_size=res_config0[aim1]['batch_res'], part=res_config0[aim1]['part'],
                              flops=res_config0[aim1]['flops_res'], params=res_config0[aim1]['params_res'], pop=pop)
        delete_pop = list(delete_pop)
        # ac = np.delete(ac,[1,3,5],axis=0)
        pop_new = np.delete(pop, delete_pop, axis=0)
        if pop_new.size != 0:
            fitness = get_fitness1(aim=aim1, pop=pop_new, batch=res_config0[aim1]['batch_res'],
                                   part=res_config0[aim1]['part'], need=res_config0[aim1]['need'],
                                   rest=res_config0[aim1]['remain_iter'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            batch_mode = translateDNA(pop_new)
            aim1_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim1]['batch_res'])
            if aim1_batch >= 78:
                aim1_batch = 78
            if aim1_batch <= res_config0[aim1]['part']:
                aim1_batch = res_config0[aim1]['part']
            method2 = {'type': 2, 'batch': aim1_batch}
            assign_config[aim1].append(method2)
        # "cpu_high": 8991,
        # "memory_base": 8706,
        if assign_config[aim1]:
            if assign_config[aim1][0]['type'] == 1:
                res_condition = {}
                res_load = [res_cpu[i] for i in node_list_global]
                for no_k0 in node_list_global:
                    res_condition[res_cpu[no_k0]] = no_k0
                list.sort(res_load)
                deal_node = res_condition[res_load[-1]]
                res_cpu[deal_node] -= res_config0[aim1]['cpu_source']
                res_mem[deal_node] -= res_config0[aim1]['mem_source']
                # layout_config0[aim1][deal_node]['worker']+=1
                aim1_tmp_layout = layout_config0[aim1]
                aim1_tlk = list(aim1_tmp_layout.keys())
                if deal_node in aim1_tlk:
                    layout_config0[aim1][deal_node]['worker'] += 1
                else:
                    layout_config0[aim1][deal_node] = {'ps': 0, 'worker': 1}
                res_condition.pop(res_load[-1])
                update_reload = res_load[-1] - res_config0[aim1]['cpu_source']
                res_condition[update_reload] = deal_node
                res_load[-1] = update_reload
                if assign_config[aim1][0]['ps'] != 0:
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    res_cpu[deal_node] -= 1000
                    res_mem[deal_node] -= 2048
                    aim1_tmp_layout = layout_config0[aim1]
                    aim1_tlk = list(aim1_tmp_layout.keys())
                    if deal_node in aim1_tlk:
                        layout_config0[aim1][deal_node]['ps'] += 1
                    else:
                        layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}
        if not aim2:
            assign_config[aim2] = []
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)
            method1 = {}
            method2 = {}
            print("before modulate aim2")
            print(k8s_monitor_k)
            aim1_path = '/data/tfdata/k8snfs/%s/%s.json' % (aim1, aim1)
            aim1_config = load_config(aim1_path)
            aim1_workernow = int(aim1_config["worker_replicas"])
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 1,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k,
                                                         k8s_monitor_k,
                                                         index_node_k,aim1_workernow)
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k,
                                                         k8s_monitor_k,
                                                         index_node_k,aim1_workernow)

            if not change_number:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k,
                                                         k8s_monitor_k,
                                                         index_node_k,aim1_workernow)
            if change_number:
                assign_config[aim1] = [method1]
            else:
                assign_config[aim1] = []

            pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(len(pop_total))
            for _ in range(N_GENERATIONS):
                input_pop = []
                for father in pop:
                    mother = pop[np.random.randint(POP_SIZE)]
                    input_pop.append([father, mother])
                pool_cross = multiprocessing.Pool(4)
                pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
                pool_cross.close()
                pool_cross.join()
                # pop = crossover_and_mutation(input_pop)
                pop = []
                for item in pop_tmp:
                    for item2 in item:
                        pop.append(item2)
                pop = np.array(pop)
                fitness = get_fitness1(aim1, pop, res_config0[aim1]['batch_res'], res_config0[aim1]['part'],
                                       need=res_config0[aim1]['need'], rest=res_config0[aim1]['remain_iter'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
                    break

            delete_pop = kongxian(batch_size=res_config0[aim1]['batch_res'], part=res_config0[aim1]['part'],
                                  flops=res_config0[aim1]['flops_res'], params=res_config0[aim1]['params_res'],
                                  pop=pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size != 0:
                fitness = get_fitness1(aim=aim1, pop=pop_new, batch=res_config0[aim1]['batch_res'],
                                       part=res_config0[aim1]['part'], need=res_config0[aim1]['need'],
                                       rest=res_config0[aim1]['remain_iter'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                batch_mode = translateDNA(pop_new)
                aim1_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim1]['batch_res'])
                if aim1_batch >= 78:
                    aim1_batch = 78
                if aim1_batch <= res_config0[aim1]['part']:
                    aim1_batch = res_config0[aim1]['part']
                method2 = {'type': 2, 'batch': aim1_batch}
                assign_config[aim1].append(method2)

                # print("最优的基因型：", pop[max_fitness_index])
                # print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))

        # "cpu_high": 8991,
        # "memory_base": 8706,
        if assign_config[aim1]:
            if assign_config[aim1][0]['type'] == 1:
                res_condition = {}
                res_load = [res_cpu[i] for i in node_list_global]
                for no_k0 in node_list_global:
                    res_condition[res_cpu[no_k0]] = no_k0
                list.sort(res_load)
                deal_node = res_condition[res_load[-1]]
                res_cpu[deal_node] -= res_config0[aim1]['cpu_source']
                res_mem[deal_node] -= res_config0[aim1]['mem_source']
                # layout_config0[aim1][deal_node]['worker']+=1
                aim1_tmp_layout = layout_config0[aim1]
                aim1_tlk = list(aim1_tmp_layout.keys())
                if deal_node in aim1_tlk:
                    layout_config0[aim1][deal_node]['worker'] += 1
                else:
                    layout_config0[aim1][deal_node] = {'ps': 0, 'worker': 1}
                res_condition.pop(res_load[-1])
                update_reload = res_load[-1] - res_config0[aim1]['cpu_source']
                res_condition[update_reload] = deal_node
                res_load[-1] = update_reload
                if assign_config[aim1][0]['ps'] != 0:
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    res_cpu[deal_node] -= 1000
                    res_mem[deal_node] -= 2048
                    aim1_tmp_layout = layout_config0[aim1]
                    aim1_tlk = list(aim1_tmp_layout.keys())
                    if deal_node in aim1_tlk:
                        layout_config0[aim1][deal_node]['ps'] += 1
                    else:
                        layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}
        if not aim2:
            assign_config[aim2] = []
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)

            if res_config0[aim1]['ps'] > math.ceil(res_config0[aim1]['worker'] / 2):
                method1 = {'type': 1, 'ps': -1, 'worker': -1}
                change_number = finish2(res_config0[aim1]['total_step'], res_config0[aim1]['remain_time'],
                                        res_config0[aim1]['reload_point'], res_config0[aim1]['worker'],
                                        res_config0[aim1]['ps'], 1, res_config0[aim1]['mini'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': -1}
                change_number = finish2(res_config0[aim1]['total_step'], res_config0[aim1]['remain_time'],
                                        res_config0[aim1]['reload_point'], res_config0[aim1]['worker'],
                                        res_config0[aim1]['ps'], 0, res_config0[aim1]['mini'])


            if not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = []
            else:
                assign_config[aim1] = [method1]
    elif mode == 3:
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {}, mode
        # 具体实施方案，则为两种选择，修改节点数和增加每个节点的资源，在这里评估指标变为节约的时间/资源
        # 可选方案：增加1个节点/添加相应的资源，判断方法：节约的时间/添加的资源，如果资源超过范围则丢弃该方案，直到找到合适的方案，备选方案为
        # job_aim1 = reload_jobs(aim1, -1)
        method1 = {}
        method2 = {}
        change_number = False
        node_index_k, k8s_monitor_k, index_node_k = job_basic.select_k8s_gpu()
        aim1_path = '/data/tfdata/k8snfs/%s/%s.json' % (aim1, aim1)
        aim1_config = load_config(aim1_path)
        aim1_workernow = int(aim1_config["worker_replicas"])
        if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
            method1 = {'type': 1, 'ps': 1, 'worker': 1}
            change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 1,
                                                     res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                                     node_index_k, k8s_monitor_k, index_node_k,aim1_workernow)
        else:
            method1 = {'type': 1, 'ps': 0, 'worker': 1}
            change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                     res_config0[aim1]['cpu_source'],
                                                     res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                     index_node_k,aim1_workernow)

        if not change_number:
            method1 = {'type': 1, 'ps': 0, 'worker': 1}
            change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                     res_config0[aim1]['cpu_source'],
                                                     res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                     index_node_k,aim1_workernow)

        # "cpu_high": 8991,
        # "memory_base": 8706,
        if change_number:
            assign_config[aim1] = [method1]
        else:
            assign_config[aim1] = []

        pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
        pop_total = []
        pop_total = existss(pop_total, pop, init=0)
        print(len(pop_total))
        for _ in range(N_GENERATIONS):
            input_pop = []
            for father in pop:
                mother = pop[np.random.randint(POP_SIZE)]
                input_pop.append([father, mother])
            pool_cross = multiprocessing.Pool(4)
            pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
            pool_cross.close()
            pool_cross.join()
            # pop = crossover_and_mutation(input_pop)
            pop = []
            for item in pop_tmp:
                for item2 in item:
                    pop.append(item2)
            pop = np.array(pop)
            fitness = get_fitness1(aim1, pop, res_config0[aim1]['batch_res'], res_config0[aim1]['part'],
                                   need=res_config0[aim1]['need'], rest=res_config0[aim1]['remain_iter'])
            pop = select(pop, fitness)  # 选择生成新的种群
            if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
                break

        delete_pop = kongxian(batch_size=res_config0[aim1]['batch_res'], part=res_config0[aim1]['part'],
                              flops=res_config0[aim1]['flops_res'], params=res_config0[aim1]['params_res'], pop=pop)
        delete_pop = list(delete_pop)
        # ac = np.delete(ac,[1,3,5],axis=0)
        pop_new = np.delete(pop, delete_pop, axis=0)
        if pop_new.size != 0:
            fitness = get_fitness1(aim=aim1, pop=pop_new, batch=res_config0[aim1]['batch_res'],
                                   part=res_config0[aim1]['part'], need=res_config0[aim1]['need'],
                                   rest=res_config0[aim1]['remain_iter'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            batch_mode = translateDNA(pop_new)
            aim1_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim1]['batch_res'])
            if aim1_batch >= 78:
                aim1_batch = 78
            if aim1_batch <= res_config0[aim1]['part']:
                aim1_batch = res_config0[aim1]['part']
            method2 = {'type': 2, 'batch': aim1_batch}
            assign_config[aim1].append(method2)

        # "cpu_high": 8991,
        # "memory_base": 8706,
        if assign_config[aim1]:
            if assign_config[aim1][0]['type']==1:
                res_condition = {}
                res_load = [res_cpu[i] for i in node_list_global]
                for no_k0 in node_list_global:
                    res_condition[res_cpu[no_k0]] = no_k0
                list.sort(res_load)
                deal_node = res_condition[res_load[-1]]
                res_cpu[deal_node]-=res_config0[aim1]['cpu_source']
                res_mem[deal_node]-=res_config0[aim1]['mem_source']
                # layout_config0[aim1][deal_node]['worker']+=1
                aim1_tmp_layout = layout_config0[aim1]
                aim1_tlk = list(aim1_tmp_layout.keys())
                if deal_node in aim1_tlk:
                    layout_config0[aim1][deal_node]['worker'] += 1
                else:
                    layout_config0[aim1][deal_node] = {'ps': 0, 'worker': 1}
                res_condition.pop(res_load[-1])
                update_reload = res_load[-1]-res_config0[aim1]['cpu_source']
                res_condition[update_reload] = deal_node
                res_load[-1] = update_reload
                if assign_config[aim1][0]['ps']!=0:
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    res_cpu[deal_node] -= 1000
                    res_mem[deal_node] -= 2048
                    aim1_tmp_layout = layout_config0[aim1]
                    aim1_tlk = list(aim1_tmp_layout.keys())
                    if deal_node in aim1_tlk:
                        layout_config0[aim1][deal_node]['ps'] += 1
                    else:
                        layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}
        if not aim2:
            assign_config[aim2] = []
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)
            method1 = {}
            method2 = {}
            aim1_path = '/data/tfdata/k8snfs/%s/%s.json' % (aim1, aim1)
            aim1_config = load_config(aim1_path)
            aim1_workernow = int(aim1_config["worker_replicas"])
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 1,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                         index_node_k,aim1_workernow)
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                         index_node_k,aim1_workernow)

            if not change_number:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number, k8s_monitor_k = kongxian2(node_list_global, res_cpu, res_mem, 0,
                                                         res_config0[aim1]['cpu_source'],
                                                         res_config0[aim1]['mem_source'], node_index_k, k8s_monitor_k,
                                                         index_node_k,aim1_workernow)

            if change_number:
                assign_config[aim1] = [method1]
            else:
                assign_config[aim1] = []
            pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(len(pop_total))
            for _ in range(N_GENERATIONS):
                input_pop = []
                for father in pop:
                    mother = pop[np.random.randint(POP_SIZE)]
                    input_pop.append([father, mother])
                pool_cross = multiprocessing.Pool(4)
                pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
                pool_cross.close()
                pool_cross.join()
                # pop = crossover_and_mutation(input_pop)
                pop = []
                for item in pop_tmp:
                    for item2 in item:
                        pop.append(item2)
                pop = np.array(pop)
                fitness = get_fitness1(aim1, pop, res_config0[aim1]['batch_res'], res_config0[aim1]['part'],
                                       need=res_config0[aim1]['need'], rest=res_config0[aim1]['remain_iter'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
                    break

            delete_pop = kongxian(batch_size=res_config0[aim1]['batch_res'], part=res_config0[aim1]['part'],
                                  flops=res_config0[aim1]['flops_res'], params=res_config0[aim1]['params_res'], pop=pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size != 0:
                fitness = get_fitness1(aim=aim1, pop=pop_new, batch=res_config0[aim1]['batch_res'],
                                       part=res_config0[aim1]['part'], need=res_config0[aim1]['need'],
                                       rest=res_config0[aim1]['remain_iter'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                batch_mode = translateDNA(pop_new)
                aim1_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim1]['batch_res'])
                if aim1_batch >= 78:
                    aim1_batch = 78
                if aim1_batch <= res_config0[aim1]['part']:
                    aim1_batch = res_config0[aim1]['part']
                method2 = {'type': 2, 'batch': aim1_batch}
                assign_config[aim1].append(method2)

    elif mode == 4:
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {},mode
        # job_aim1 = reload_jobs(aim1, -1)

        if res_config0[aim1]['ps'] > math.ceil(res_config0[aim1]['worker'] / 2):
            method1 = {'type': 1, 'ps': -1, 'worker': -1}
            change_number =finish2(res_config0[aim1]['total_step'],res_config0[aim1]['remain_time'],res_config0[aim1]['reload_point'],res_config0[aim1]['worker'],res_config0[aim1]['ps'],1,res_config0[aim1]['mini'])
        else:
            method1 = {'type': 1, 'ps': 0, 'worker': -1}
            change_number = finish2(res_config0[aim1]['total_step'], res_config0[aim1]['remain_time'],
                                    res_config0[aim1]['reload_point'], res_config0[aim1]['worker'],
                                    res_config0[aim1]['ps'], 0, res_config0[aim1]['mini'])

        if not change_number:
            print("Mode %d Can not find a way to aim1!!" % mode)
            assign_config[aim1] = []
        else:
            assign_config[aim1] = [method1]

        if not aim2:
            assign_config[aim2] = []
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)

            if res_config0[aim1]['ps'] > math.ceil(res_config0[aim1]['worker'] / 2):
                method1 = {'type': 1, 'ps': -1, 'worker': -1}
                change_number = finish2(res_config0[aim1]['total_step'], res_config0[aim1]['remain_time'],
                                        res_config0[aim1]['reload_point'], res_config0[aim1]['worker'],
                                        res_config0[aim1]['ps'], 1, res_config0[aim1]['mini'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': -1}
                change_number = finish2(res_config0[aim1]['total_step'], res_config0[aim1]['remain_time'],
                                        res_config0[aim1]['reload_point'], res_config0[aim1]['worker'],
                                        res_config0[aim1]['ps'], 0, res_config0[aim1]['mini'])

            if not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = []
            else:
                assign_config[aim1] = [method1]

    else:
        print("Mode %d Do not find fit job to get modluation for number of GPUS!!" % mode)
        assign_config = {}
        # return {}, mode
    #寻找资源利用率最低的任务，增加batch，采用启发式式算法

    resource_ver = {}
    can_modi_batch = list(res_config0.keys())

    print("can using to modify the batch:")
    print(piotential)
    assigned = list(assign_config.keys())
    if assigned:
        for assign in assigned:
            if assign in piotential:
                piotential.remove(assign)
    print("The batch based meassage:")
    print(res_config0)
    if not piotential:
        return assign_config,mode
    for i in piotential:
        if 'gpubase' in list(res_config0[i].keys()):
            resource_ver[float(res_config0[i]['gpubase'])] = i
    resource_ver_key = list(resource_ver.keys())
    if not resource_ver_key:
        return assign_config,mode
    list.sort(resource_ver_key)
    aim3 = ''
    for k in resource_ver_key:
        if k > 0:
            aim3 = resource_ver[resource_ver_key[0]]
            break
    if not aim3:
        return assign_config,mode
    assign_key = list(assign_config.keys())
    if aim3 not in assign_key:
        assign_config[aim3] = []
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
    pop_total = []
    pop_total = existss(pop_total, pop, init=0)
    print(len(pop_total))
    for _ in range(N_GENERATIONS):
        input_pop = []
        for father in pop:
            mother = pop[np.random.randint(POP_SIZE)]
            input_pop.append([father, mother])
        pool_cross = multiprocessing.Pool(6)
        pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
        pool_cross.close()
        pool_cross.join()
        # pop = crossover_and_mutation(input_pop)
        pop = []
        for item in pop_tmp:
            for item2 in item:
                pop.append(item2)
        pop = np.array(pop)
        fitness = get_fitness1(aim3, pop,res_config0[aim3]['batch_res'],res_config0[aim3]['part'],need=res_config0[aim3]['need'],rest=res_config0[aim3]['remain_iter'])
        pop = select(pop, fitness)  # 选择生成新的种群
        if len(pop_total) >= 2 ** (DNA_SIZE) - 1:
            break

    delete_pop = kongxian(batch_size=res_config0[aim3]['batch_res'],part=res_config0[aim3]['part'],flops=res_config0[aim3]['flops_res'],params=res_config0[aim3]['params_res'],pop=pop)
    delete_pop = list(delete_pop)
    # ac = np.delete(ac,[1,3,5],axis=0)
    pop_new = np.delete(pop, delete_pop, axis=0)
    if pop_new.size == 0:
        return assign_config,mode

    fitness = get_fitness1(aim=aim3,pop=pop_new,batch=res_config0[aim3]['batch_res'],part=res_config0[aim3]['part'],need=res_config0[aim3]['need'],rest=res_config0[aim3]['remain_iter'])
    max_fitness_index = np.argmax(fitness)
    print("max_fitness:", fitness[max_fitness_index])
    batch_mode = translateDNA(pop_new)
    aim3_batch = math.ceil(batch_mode[max_fitness_index] * res_config0[aim3]['batch_res'])
    if aim3_batch >= 78:
        aim3_batch = 78
    if aim3_batch <= res_config0[aim3]['part']:
        aim3_batch = res_config0[aim3]['part']
    method2 = {'type': 2, 'batch': aim3_batch}
    assign_config[aim3].append(method2)
    return assign_config,mode

def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/data/tfdata/nodedata', help='save path')
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
    # cacheData = os.popen(
    #     "echo $(kubectl describe secret $(kubectl get secret -n kube-system | grep ^admin-user | awk '{print $1}') -n kube-system | grep -E '^token'| awk '{print $2}')").read()
    cacheData = os.popen("echo $(kubectl describe secrets reader-token-zqmwv -n kube-system)")
    cacheToken = cacheData[:-1]
    newToken = str(cacheToken)

    return newToken

def make_headers(Token):
    text = 'Bearer ' + Token
    headers = {'Authorization': text}
    return headers

def catch_message(url):
    global aToken

    # aToken = update_token()
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
    node_list = ["izbp10smzw7rg0ih27wbl3z",
                      "izbp11dpzwhp6pia1tyr3kz",
                      "izbp11ycujbqzxrpj66jksz",
                      "izbp156pkpio477f5f2tf6z",
                      "izbp156pkpio477f5f2tf8z",
                      "izbp179ga4nl6y5b59bmphz"]
    gpu_node_list = ["izbp10smzw7rg0ih27wbl3z",
                          "izbp11dpzwhp6pia1tyr3kz",
                          "izbp11ycujbqzxrpj66jksz",
                          "izbp156pkpio477f5f2tf6z",
                          "izbp156pkpio477f5f2tf8z"]
    # self.lasttime =
    node_cpu["izbp10smzw7rg0ih27wbl3z"] = 32000 - 500  # 132025460Ki
    node_cpu["izbp11dpzwhp6pia1tyr3kz"] = 32000 - 500  # 132025460Ki
    node_cpu["izbp11ycujbqzxrpj66jksz"] = 32000 - 4800  # 132025460Ki
    node_cpu["izbp156pkpio477f5f2tf6z"] = 8000 - 3000  # 32939400Ki
    node_cpu["izbp156pkpio477f5f2tf8z"] = 8000 - 500  # 32939400Ki
    node_cpu["izbp179ga4nl6y5b59bmphz"] = 40000 - 4500  # 194969644Ki
    node_memory = {}
    node_memory["izbp10smzw7rg0ih27wbl3z"] = float(125 * 1024 - 320)
    node_memory["izbp11dpzwhp6pia1tyr3kz"] = float(125 * 1024 - 300)
    node_memory["izbp11ycujbqzxrpj66jksz"] = float(125 * 1024 - 4500)
    node_memory["izbp156pkpio477f5f2tf6z"] = float(31 * 1024 - 900)
    node_memory["izbp156pkpio477f5f2tf8z"] = float(31 * 1024 - 400)
    node_memory['izbp179ga4nl6y5b59bmphz'] = float(185 * 1024 - 4800)
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
        self.node_cpu["izbp10smzw7rg0ih27wbl3z"] = 32000 - 500  # 132025460Ki
        self.node_cpu["izbp11dpzwhp6pia1tyr3kz"] = 32000 - 500  # 132025460Ki
        self.node_cpu["izbp11ycujbqzxrpj66jksz"] = 32000 - 4800  # 132025460Ki
        self.node_cpu["izbp156pkpio477f5f2tf6z"] = 8000 - 3000  # 32939400Ki
        self.node_cpu["izbp156pkpio477f5f2tf8z"] = 8000 - 500  # 32939400Ki
        self.node_cpu["izbp179ga4nl6y5b59bmphz"] = 40000 - 4500  # 194969644Ki
        self.node_memory = {}
        self.node_memory["izbp10smzw7rg0ih27wbl3z"] = float(125 * 1024 - 320)
        self.node_memory["izbp11dpzwhp6pia1tyr3kz"] = float(125 * 1024 - 300)
        self.node_memory["izbp11ycujbqzxrpj66jksz"] = float(125 * 1024 - 4500)
        self.node_memory["izbp156pkpio477f5f2tf6z"] = float(31 * 1024 - 900)
        self.node_memory["izbp156pkpio477f5f2tf8z"] = float(31 * 1024 - 400)
        self.node_memory['izbp179ga4nl6y5b59bmphz'] = float(185 * 1024 - 4800)
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
        self.client = influxdb.InfluxDBClient('172.16.190.97',port=8086,username='admin',password='admin',database=self.database)
        #derivation
    # def node_measurement(self,node_list):
    #     # Global_Influx.Client_all.get_list_measurements()


    def run(self):
        print(multiprocessing.current_process().pid)
        print(os.getpid())
        response = catch_message(self.url)
        print(self.url)
        print(response)
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
                f1 = open('/data/tfdata/nodedata/node.json', 'r', encoding='utf-8')
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
                f2 = open('/data/tfdata/nodedata/node.json', 'w', encoding='utf-8')
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

# def get_remain():


def Monitor_job(tasks,lock,v1,jobs):
    time.sleep(10)
    while True:
        if tasks['start'] == False:
            break
        ns_list = get_ns(v1)
        # print(ns_list)
        if tasks['start'] == True and tasks['count'] == 0:
            time.sleep(30)
            pass
        else:
            for ns in tasks['ns']:
                # print(ns+'If in list:'+str(ns in ns_list))
                if ns not in ns_list and ns not in tasks['retry'] and not tasks['modulate']:
                    try_times = 5
                    while try_times > 0:
                        time.sleep(float(random.randint(3, 5)))
                        ns_list = get_ns(v1)
                        if ns in ns_list:
                            break
                        try_times=try_times-1
                    if try_times <=0 :
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

def make_time_query(time_base,mode=0):
    if mode == 0:
        time_query = (math.floor(time_base-1))
        time_query_str = str(time_query)+'000000000'
    else:
        time_query = (math.ceil(time_base+1))
        time_query_str = str(time_query)+'000000000'
    return time_query_str





def catch_node_step_msg(jobs,job_name,tasks,lock,batch,flops,params,real_batch,mode):
    node_influx_client = influxdb.InfluxDBClient(host='172.16.190.97',username='admin',password='admin',database='NODEMESSAGE')
    step_influx_client = influxdb.InfluxDBClient(host='172.16.190.97',username='admin',password='admin',database='PREDICT')
    jieshu = False

    lock.acquire()
    for jo in jobs:
        if jo == job_name:
            job = reload_jobs(job_name,-1)
            print('reload job success!')
            break
    lock.release()
    print("kaishi: %s" % job_name)

    job_measure = job.measure
    print("job measure: %s" % job.measure)
    pre_list = job_measure.split(' ')
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_load = pre_list[0] + 'L' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    count = 0
    count2 = 0
    count000 = 0
    countt00 = 0
    count111 = 0
    time.sleep(15)
    while True:
        pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job.name).items]
        run_result = pd.value_counts(pod_status)
        run_result_dict = dict(run_result)
        print(run_result_dict)
        print("%s aim is: %d" % (job_name,(job.ps_replicas + job.worker_replicas)))
        if 'Running' in pod_status and run_result_dict['Running'] == (job.ps_replicas + job.worker_replicas):
            time.sleep(10)

            print("Select the loayout!")
            tmp_layout = tasks['nslayout']
            tmp_keys = list(tmp_layout.keys())
            if job_name in tmp_keys and tmp_layout[job_name] == False:
                tmp_layout_config = {}
                for i in job.v1.list_namespaced_pod(job_name).items:
                    tmp_layout_config[i.metadata.name] = i.spec.node_name
                fp = open('/data/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                fp.write(dicc_json)
                fp.close()
                lock.acquire()
                tmp_layout[job_name] = True
                tasks['nslayout'] = tmp_layout
                lock.release()
            break
        # elif 'Running' in pod_status:
        elif 'Succeeded' in pod_status or 'Failed' in pod_status:
            if count000 <= 2:
                count000+=1
                time.sleep(13.5)
            else:
                jieshu = True
                print("Exception exit! Pending Problem!")
                lock.acquire()
                tmp_reload_ns = tasks['retry']
                lock.release()
                print("Retrying jobs is:")
                print(tmp_reload_ns)
                print(not tasks['modulate'])
                print(job.name not in tmp_reload_ns and not tasks['modulate'])
                try:
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config_keys = list(res_job_config.keys())
                    if 'endtime' not in res_job_config_keys:
                        res_job_config['endtime'] = time.time() - 30
                    save_config(res_job_config, save_res_path)
                    print("save end time success!!")
                except Exception as eee:
                    print("Delete Problem:")
                    print(eee)
                time.sleep(3)
                if job.name not in tmp_reload_ns and not tasks['modulate']:
                    time.sleep(5)
                    try:
                        exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                                       v1.list_namespaced_pod(job.name).items]
                        print(exit_reason)
                        exit_ict = {'reasons': exit_reason}
                        exit_path = '/data/tfdata/k8snfs/%s/exit_reason.json' % ns
                        exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                        fw_exit = open(exit_path, 'w', encoding='utf-8')
                        fw_exit.write(exit_json)
                        fw_exit.close()
                    except Exception as e:
                        print(e)
                    time.sleep(3)
                    lock.acquire()
                    command = 'kubectl delete -f /data/tfdata/tfcnn/expjob/job/' + job.name + '.yaml'
                    os.system(command)
                    deletehelp2(job.name,v1)
                    # v1.delete_namespace(job.name)
                    ns_tmp = tasks['ns']
                    ns_tmp.remove(job.name)
                    tasks['ns'] = ns_tmp
                    is_layout = tasks['nslayout']
                    is_layout.pop(job.name)
                    for i in range(len(jobs)):
                        if jobs[i] == job.name:
                            jobs.pop(i)
                            break
                    tasks['nslayout'] = is_layout
                    tasks['count'] -= 1
                    # jobs_tmp = jobs
                    # jobs_tmp.remove(job.name)
                    # jobs = jobs_tmp
                    finishes = tasks['finish']
                    finishes.append(job.name)
                    tasks['finish'] = finishes
                    print("finish remove %s from jobs!" % job.name)
                    lock.release()
                    return
                else:
                    time.sleep(10)
        elif 'Pending' in pod_status:
            # pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
            tmp_layout = tasks['nslayout']
            tmp_keys = list(tmp_layout.keys())
            if job_name in tmp_keys:
                tmp_layout_config = {}
                for i in job.v1.list_namespaced_pod(job_name).items:
                    if i.status.phase == 'Running':
                        tmp_layout_config[i.metadata.name] = i.spec.node_name
                if tmp_layout_config:
                    fp = open('/data/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    fp.write(dicc_json)
                    fp.close()
            save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
            save_batch_path =  '/data/tfdata/k8snfs/%s/%s_change.json' % (job.name, job.name)
            res_config = load_config(save_res_path)
            batch_config = load_config(save_batch_path)
            keys_res = res_config.keys()
            if 'reloadtime' not in keys_res:
                res_config['reloadtime'] = []
            # 'cpu_high': cpu_base, 'memory_base': mem_base
            if count2 < 3:
                count2+=1
                time.sleep(20)
            elif job.ps_replicas > job.worker_replicas and job.ps_replicas>1:
                print("reduce ps server!!")
                # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                aim_steps = step_influx_client.query(
                    "select training_step from " + measure_t + " order by desc limit 1")
                aim_key = aim_steps.keys()
                result_inter = aim_steps[aim_key[0]]
                result_items = list(result_inter)
                aim_step = int(result_items[0]['training_step'])
                print(aim_step)
                save_job_change_layout(job.name, job.ps_replicas - 1, job.worker_replicas,aim_step,mode=1)
                # aim_step = aim_step
                time_1 = 0
                lock.acquire()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.append(job.name)
                tasks['retry'] = tmp_retry_job
                tmp_layout = tasks['nslayout']
                tmp_layout[job.name] = False
                tasks['nslayout'] = tmp_layout
                time1 = time.time()
                job.retry_tf(job.batch_size,aim_step,job.worker_replicas,(job.ps_replicas - 1),job.part)
                time2 = time.time()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.remove(job.name)
                tasks['retry'] = tmp_retry_job
                lock.release()
                time.sleep(7)
                job.write_retry(mode=0)
                tmp_reload = res_config['reloadtime']
                tmp_reload.append((time2 - time1))
                res_config['reloadtime'] = tmp_reload
                save_config(res_config,save_res_path)
                count2+=1
                time.sleep(19.5)
                print("reduce ps server successfully!")
            elif job.worker_replicas > 1:
                tmp_replicas = job.worker_replicas
                print("reduce worker number!!")
                # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                aim_steps = step_influx_client.query(
                    "select training_step from " + measure_t + " order by desc limit 1")
                aim_key = aim_steps.keys()
                result_inter = aim_steps[aim_key[0]]
                result_items = list(result_inter)
                aim_step = int(result_items[0]['training_step'])
                print(aim_step)
                aim_step = math.ceil((aim_step*tmp_replicas)/(job.worker_replicas-1))
                save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas - 1,aim_step,mode=1)
                lock.acquire()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.append(job.name)
                tasks['retry'] = tmp_retry_job
                tmp_layout = tasks['nslayout']
                tmp_layout[job.name] = False
                tasks['nslayout'] = tmp_layout
                time1 = time.time()
                job.retry_tf(job.batch_size,aim_step,job.worker_replicas-1,job.ps_replicas,job.part)
                time2 = time.time()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.remove(job.name)
                tasks['retry'] = tmp_retry_job
                lock.release()
                time.sleep(7)
                job.write_retry(mode=0)
                tmp_reload = res_config['reloadtime']
                tmp_reload.append((time2 - time1))
                res_config['reloadtime'] = tmp_reload
                save_config(res_config,save_res_path)
                count2+=1
                print("reduce worker number successfully!!")
                time.sleep(19.5)
            elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                if count2 > 8:
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    save_job_change_layout(job.name, 1, 1, aim_step, mode=1)
                    lock.acquire()
                    command = 'kubectl delete -f /data/tfdata/tfcnn/expjob/job/' + job.name + '.yaml'
                    os.system(command)
                    deletehelp2(job.name, v1)
                    # v1.delete_namespace(job.name)
                    ns_tmp = tasks['ns']
                    ns_tmp.remove(job.name)
                    tasks['ns'] = ns_tmp
                    is_layout = tasks['nslayout']
                    is_layout.pop(job.name)
                    for i in range(len(jobs)):
                        if jobs[i] == job.name:
                            jobs.pop(i)
                            break
                    tasks['nslayout'] = is_layout
                    # job_tmp.pop(ns)
                    # tasks['job'] = job_tmp
                    tasks['count'] -= 1
                    tmp_next = tasks['next']
                    tmp_next.append(job.name)
                    tmp_next_time_config = tasks['nexttimes']
                    tmp_next_time_config[job.name] = 0
                    tasks['nexttimes'] = tmp_next_time_config
                    tasks['next'] = tmp_next
                    lock.release()
                    time.sleep(15)
                    jieshu = True
                    print("Exception exit! Pending Problem!")
                    return
                else:
                    count2 +=1
                    time.sleep(22.5)
        elif run_result_dict['Running'] == 1:
            save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
            res_config = load_config(save_res_path)
            # keys_res = res_config.keys()
            if countt00 < 3:
                countt00 += 1
                time.sleep(15)
            else:
                tmp_replicas = job.worker_replicas
                print("create worker and ps number!!")
                # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                aim_steps = step_influx_client.query(
                    "select training_step from " + measure_t + " order by desc limit 1")
                aim_key = aim_steps.keys()
                result_inter = aim_steps[aim_key[0]]
                result_items = list(result_inter)
                aim_step = int(result_items[0]['training_step'])
                print(aim_step)
                # aim_step = math.ceil((aim_step * tmp_replicas) / (job.worker_replicas - 1))
                save_job_change_layout(job.name, job.ps_replicas + 1, job.worker_replicas + 1, aim_step, mode=1)
                lock.acquire()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.append(job.name)
                tasks['retry'] = tmp_retry_job
                time1 = time.time()
                job.retry_tf(job.batch_size, aim_step, job.worker_replicas + 1,
                             job.ps_replicas + 1,job.part)
                time2 = time.time()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.remove(job.name)
                tasks['retry'] = tmp_retry_job
                lock.release()
                time.sleep(9)
                job.write_retry(mode=0)
                tmp_reload = res_config['reloadtime']
                tmp_reload.append((time2 - time1))
                res_config['reloadtime'] = tmp_reload
                save_config(res_config, save_res_path)
                count2 += 1
                print("create worker number successfully!!")
                time.sleep(19.5)
        elif not run_result_dict:
            ceshi_tmp_ns = tasks['ns']
            if job.name not in ceshi_tmp_ns:
                if count111 <= 4:
                    count111+=1
                    time.sleep(22)
                else:
                    return
            if count >= 8:
                jieshu = True
                print("Exception exit! Creating Problem!")
                save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                res_job_config = load_config(save_res_path)
                res_job_config['errtime'] = time.time() - 5
                save_config(res_job_config, save_res_path)
                lock.acquire()
                deletehelp2(job.name, v1)
                # v1.delete_namespace(job.name)
                ns_tmp = tasks['ns']
                ns_tmp.remove(job.name)
                tasks['ns'] = ns_tmp
                is_layout = tasks['nslayout']
                is_layout.pop(job.name)
                for i in range(len(jobs)):
                    if jobs[i] == job.name:
                        jobs.pop(i)
                        break
                tasks['nslayout'] = is_layout
                # job_tmp.pop(ns)
                # tasks['job'] = job_tmp
                tasks['count'] -= 1
                lock.release()
                return
            count+=1
            time.sleep(22)
        else:
            time.sleep(22)
    count11 = 0
    countt00 = 0
    count22 = 0
    count000 = 0
    count111 = 0
    while True:
        # print(b[0].status.container_statuses[0].state.terminated.reason)
        # lock.acquire()
        tmp_retrys = tasks['retry']
        # tmp_reload_ns = tasks['retry']
        tmp_retry_solution = tasks['solution']
        # lock.release()
        solution_keys = list(tmp_retry_solution.keys())
        if job.name in tmp_retrys and job.name in solution_keys:
            lock.acquire()
            tmp_layout = tasks['nslayout']
            tmp_layout[job.name] = False
            tasks['nslayout'] = tmp_layout
            lock.release()
            solution = tmp_retry_solution[job.name]
            pod_status = [i.status.phase for i in v1.list_namespaced_pod(job.name).items]
            save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
            res_job_config = load_config(save_res_path)
            res_job_config_keys = list(res_job_config.keys())
            if (not pod_status) or 'Succeeded' in pod_status or 'Failed' in pod_status:
                lock.acquire()
                tmp_retry_job = tasks['retry']
                tmp_retry_job.remove(job.name)
                tasks['retry'] = tmp_retry_job
                tmp_retry_solution3 = tasks['solution']
                tmp_retry_solution3.pop(job.name)
                tasks['solution'] = tmp_retry_solution3
                lock.release()
            else:
                solution_type  = [int(k['type']) for k in solution]
                solution_resource = {}
                for k in solution_type:
                    for p in solution:
                        if int(p['type']) == k:
                            solution_resource[k] = p
                print(solution_resource)
                print(solution_type)
                if 2 in solution_type:
                    tmp_batch = job.batch_size
                    save_job_change_resource(job.name,job.batch_size,solution_resource[2]['batch'],job.part)
                    print("save success")
                    job.set_batch(solution_resource[2]['batch'],job.part)
                    print("set batch ok!!")
                    # method2 = {'type':2,'cpu':aim1_cpu,'mem':aim1_mem}
                    job.update_batch()
                    remain, total_step, atmp = job.get_remain(mode=1)
                    aim_step2 = math.ceil(atmp+(remain*tmp_batch/solution_resource[2]['batch']))
                    job.training_step = int(aim_step2)
                    print(aim_step2)
                    tmp_retry = job.retry
                    tmp_retry = tmp_retry+1
                    job.retry = tmp_retry
                    save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas,aim_step2,mode=1)
                    print("save layout success!!")
                    try:
                        job.write_retry(mode=1)
                        job.update_step()
                        job.write_retry(mode=0)
                    except Exception as e0:
                        print(e0)
                    print('update successful!!')
                    solution_type.remove(2)
                    solution_resource.pop(2)
                    print("successful!!")
                    print(solution_type)
                    print(solution_resource)
                    lock.acquire()
                    try:
                        if not solution_resource or not solution_type:
                            tmp_retry_job = tasks['retry']
                            tmp_retry_job.remove(job.name)
                            tasks['retry'] = tmp_retry_job
                            tmp_retry_solution3 = tasks['solution']
                            tmp_retry_solution3.pop(job.name)
                            tasks['solution'] = tmp_retry_solution3
                    except Exception as ee2:
                        print(ee2)
                    lock.release()
                    print("modulate finish")
                if 1 in solution_type:
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    tmp_replicas = job.worker_replicas
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    aim_worker_replicas = job.worker_replicas + int(solution_resource[1]['worker'])
                    if aim_worker_replicas <= 0:
                        aim_worker_replicas = 1
                    aim_step = math.ceil((aim_step * tmp_replicas) / (aim_worker_replicas))
                    aim_ps_replicas = job.ps_replicas + int(solution_resource[1]['ps'])
                    if aim_ps_replicas <= 0:
                        aim_ps_replicas = 1
                    if aim_worker_replicas <= 0:
                        aim_worker_replicas = 1
                    save_job_change_layout(job.name, aim_ps_replicas, aim_worker_replicas, aim_step, mode=1)
                    lock.acquire()
                    # method1 = {'type': 1, 'ps': 0, 'worker': 1}
                    time1 = time.time()
                    job.retry_tf(job.batch_size, aim_step, aim_worker_replicas, aim_ps_replicas,job.part)
                    time2 = time.time()
                    solution_type.remove(1)
                    solution_resource.pop(1)
                    # job.assignment_resource(math.ceil(solution['cpu']), math.ceil(solution['mem']))
                    if not solution_resource or not solution_type:
                        tmp_retry_job = tasks['retry']
                        tmp_retry_job.remove(job.name)
                        tasks['retry'] = tmp_retry_job
                        tmp_retry_solution3 = tasks['solution']
                        tmp_retry_solution3.pop(job.name)
                        tasks['solution'] = tmp_retry_solution3
                    print('success!!')
                    lock.release()
                    print("modulate success!!")
                    time.sleep(4)
                    reload = time2 - time1
                    job.reload_count(reload)
                    time.sleep(4.2)
                    count33 = 0
                    while count33 < 15:
                        pod_status3 = [i.status.phase for i in v1.list_namespaced_pod(job.name).items]
                        run_result3 = pd.value_counts(pod_status3)
                        run_result_dict3 = dict(run_result3)
                        print("Retry assignmenting for pods:")
                        print(run_result_dict3)
                        if 'Running' in pod_status3 and run_result_dict3['Running'] == (
                                job.ps_replicas + job.worker_replicas):
                            break
                        else:
                            count33+=1
                            time.sleep(5.6)
                    job.write_retry(mode=0)
        else:
            pod_status2 = [i.status.phase for i in v1.list_namespaced_pod(job.name).items]
            run_result2 = pd.value_counts(pod_status2)
            run_result_dict2 = dict(run_result2)
            print(run_result_dict2)
            if 'Running' in pod_status2 and run_result_dict2['Running'] == (job.ps_replicas + job.worker_replicas) and run_result_dict2['Running']>1:
                time.sleep(6)
                lock.acquire()
                print("Select the loayout!")
                tmp_layout = tasks['nslayout']
                lock.release()
                tmp_keys = list(tmp_layout.keys())
                if job_name in tmp_keys and tmp_layout[job_name] == False:
                    tmp_layout_config = {}
                    for i in job.v1.list_namespaced_pod(job_name).items:
                        tmp_layout_config[i.metadata.name] = i.spec.node_name
                    fp = open('/data/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    fp.write(dicc_json)
                    fp.close()
                    tmp_layout[job_name] = True
                    lock.acquire()
                    tasks['nslayout'] = tmp_layout
                    lock.release()
                else:
                    time.sleep(10)
            elif ('Succeeded' in pod_status2 or 'Failed' in pod_status2):
                if count000 <= 2:
                    time.sleep(13.5)
                    count000+=1
                else:
                    # # print(b[0].status.container_statuses[0].state.terminated.reason)
                    # pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                    # ['OOMKilled']
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config_keys = list(res_job_config.keys())
                    if 'endtime' not in res_job_config_keys:
                        res_job_config['endtime'] = time.time() - 10
                    save_config(res_job_config, save_res_path)
                    time.sleep(3)
                    if (job.name not in tmp_retrys) and not tasks['modulate']:
                        try:
                            exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                                           v1.list_namespaced_pod(job.name).items]
                            print(exit_reason)
                            exit_ict = {'reasons': exit_reason}
                            exit_path = '/data/tfdata/k8snfs/%s/exit_reason.json' % ns
                            exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                            fw_exit = open(exit_path, 'w', encoding='utf-8')
                            fw_exit.write(exit_json)
                            fw_exit.close()
                        except Exception as e:
                            print(e)
                        time.sleep(5)

                        lock.acquire()
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjob/job/' + job.name + '.yaml'
                        os.system(command)
                        print("delete this job %s!!!" % job.name)
                        deletehelp2(job.name, v1)
                        # v1.delete_namespace(job.name)
                        ns_tmp = tasks['ns']
                        ns_tmp.remove(job.name)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        is_layout.pop(job.name)
                        for i in range(len(jobs)):
                            if jobs[i] == job.name:
                                jobs.pop(i)
                                break
                        tasks['nslayout'] = is_layout
                        tasks['count'] -= 1
                        # jobs_tmp = jobs
                        # jobs_tmp.remove(job.name)
                        # jobs = jobs_tmp
                        finishes = tasks['finish']
                        finishes.append(job.name)
                        tasks['finish'] = finishes
                        lock.release()
                        break
            elif 'Pending' in pod_status2:
                # pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
                tmp_layout = tasks['nslayout']
                tmp_keys = list(tmp_layout.keys())
                if job_name in tmp_keys:
                    tmp_layout_config = {}
                    for i in job.v1.list_namespaced_pod(job_name).items:
                        if i.status.phase == 'Running':
                            tmp_layout_config[i.metadata.name] = i.spec.node_name
                    if tmp_layout_config:
                        fp = open('/data/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                        # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                        dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                        fp.write(dicc_json)
                        fp.close()
                save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                res_config = load_config(save_res_path)
                keys_res = res_config.keys()
                if 'reloadtime' not in keys_res:
                    res_config['reloadtime'] = []
                # 'cpu_high': cpu_base, 'memory_base': mem_base
                if count22 < 4:
                    count22 += 1
                    time.sleep(20)
                elif job.ps_replicas > job.worker_replicas and job.ps_replicas > 1:
                    print("reduce ps server!!")
                    # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    save_job_change_layout(job.name, job.ps_replicas - 1, job.worker_replicas, aim_step, mode=1)
                    # aim_step = aim_step
                    time_1 = 0
                    lock.acquire()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.append(job.name)
                    tasks['retry'] = tmp_retry_job
                    time1 = time.time()
                    job.retry_tf(job.batch_size, aim_step, job.worker_replicas,
                                 (job.ps_replicas - 1),job.part)
                    time2 = time.time()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.remove(job.name)
                    tasks['retry'] = tmp_retry_job
                    lock.release()
                    time.sleep(9)
                    job.write_retry(mode=0)

                    job.reload_count(float(time2-time1))
                    count22 += 1
                    time.sleep(20)
                    print("reduce ps server successfully!")
                elif job.worker_replicas > 1:
                    tmp_replicas = job.worker_replicas
                    print("reduce worker number!!")
                    # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    aim_step = math.ceil((aim_step * tmp_replicas) / (job.worker_replicas - 1))
                    save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas - 1, aim_step, mode=1)
                    lock.acquire()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.append(job.name)
                    tasks['retry'] = tmp_retry_job
                    time1 = time.time()
                    job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, job.worker_replicas - 1,
                                 job.ps_replicas)
                    time2 = time.time()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.remove(job.name)
                    tasks['retry'] = tmp_retry_job
                    lock.release()
                    time.sleep(9)
                    job.write_retry(mode=0)
                    # tmp_reload = res_config['reloadtime']
                    # tmp_reload.append((time2 - time1))
                    # res_config['reloadtime'] = tmp_reload
                    # save_config(res_config, save_res_path)
                    job.reload_count(float(time2-time1))
                    count22 += 1
                    print("reduce worker number successfully!!")
                    time.sleep(18.5)
                elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                    if count22 > 8:
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])
                        print(aim_step)
                        save_job_change_layout(job.name, 1, 1, aim_step, mode=1)

                        lock.acquire()
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjob/job/' + job.name + '.yaml'
                        os.system(command)
                        deletehelp2(job.name, v1)
                        # v1.delete_namespace(job.name)
                        ns_tmp = tasks['ns']
                        ns_tmp.remove(job.name)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        is_layout.pop(job.name)
                        for i in range(len(jobs)):
                            if jobs[i] == job.name:
                                jobs.pop(i)
                                break
                        tasks['nslayout'] = is_layout
                        tasks['count'] -= 1
                        tmp_next = tasks['next']
                        tmp_next.append(job.name)
                        tmp_next_time_config = tasks['nexttimes']
                        tmp_next_time_config[job.name] = 0
                        tasks['nexttimes'] = tmp_next_time_config
                        tasks['next'] = tmp_next
                        lock.release()
                        time.sleep(12)
                        jieshu = True
                        print("Exception exit! Pending Problem!")
                        return
                    else:
                        count22 += 1
                        time.sleep(21.5)
            elif run_result_dict2['Running'] == 1:
                if countt00 < 3:
                    countt00 += 1
                    time.sleep(15)
                else:
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    # keys_res = res_config.keys()
                    tmp_replicas = job.worker_replicas
                    print("create worker and ps number!!")
                    # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    # aim_step = math.ceil((aim_step * tmp_replicas) / (job.worker_replicas - 1))
                    save_job_change_layout(job.name, job.ps_replicas + 1, job.worker_replicas + 1, aim_step, mode=1)
                    lock.acquire()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.append(job.name)
                    tasks['retry'] = tmp_retry_job
                    time1 = time.time()
                    job.retry_tf(job.batch_size,aim_step,job.worker_replicas + 1,
                                 job.ps_replicas + 1,job.part)
                    time2 = time.time()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.remove(job.name)
                    tasks['retry'] = tmp_retry_job
                    lock.release()
                    time.sleep(9)
                    job.write_retry(mode=0)
                    tmp_reload = res_config['reloadtime']
                    tmp_reload.append((time2 - time1))
                    res_config['reloadtime'] = tmp_reload
                    save_config(res_config, save_res_path)
                    count22 += 1
                    print("create worker number successfully!!")
                    time.sleep(21.5)

            elif not run_result_dict2:
                # ceshi_tmp_ns = tasks['ns']
                ceshi_tmp_ns = tasks['ns']
                if job.name not in ceshi_tmp_ns:
                    if count111 <= 5:
                        count111 += 1
                        time.sleep(15)
                    else:
                        return
                if count11 > 8:
                    jieshu = True
                    print("Exception exit! Creating Problem!")
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config['errtime'] = time.time() - 5
                    save_config(res_job_config, save_res_path)
                    lock.acquire()
                    command = 'kubectl delete -f /data/tfdata/tfcnn/expjob/job/' + job.name + '.yaml'
                    os.system(command)
                    deletehelp2(job.name, v1)
                    # v1.delete_namespace(job.name)
                    ns_tmp = tasks['ns']
                    ns_tmp.remove(job.name)
                    tasks['ns'] = ns_tmp
                    is_layout = tasks['nslayout']
                    is_layout.pop(job.name)
                    for i in range(len(jobs)):
                        if jobs[i] == job.name:
                            jobs.pop(i)
                            break
                    tasks['nslayout'] = is_layout
                    # job_tmp.pop(ns)
                    # tasks['job'] = job_tmp
                    tasks['count'] -= 1
                    lock.release()
                    return
                count11 += 1
                time.sleep(21)
            else:
                time.sleep(12)

#     1580976233000000000

def get_load_value(node_index,cpu_base,memory_base,total_cpu_base,total_memory_base):
    keys = node_index.keys()
    alpha = 0.675
    cpu_score = 0
    memory_score = 0
    node_use = []
    node_cpu = []
    node_mem = []
    for key in keys:
        if node_index[key] <=12:
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

def check_parts(est_gpu,bath_size,flops,params):
    # bfp = np.array([bath_size,flops,params]).reshape(1,3)
    bfp = np.array([bath_size,params]).reshape(1, 2)
    predict_res = est_gpu.predict(bfp)
    pre_res = int(predict_res[0])
    part = 1
    real_batch = bath_size // part
    if pre_res == 1:
        part = 1
    else:
        while True:
            part = part+1
            real_batch = bath_size // part
            if real_batch < 1:
                real_batch = 1
                # bfp = np.array([real_batch, flops, params]).reshape(1, 3)
                bfp = np.array([real_batch, params]).reshape(1,2)
                predict_res = est_gpu.predict(bfp)
                pre_res = int(predict_res[0])
                if pre_res == 1:
                    part = bath_size
                    break
                else:
                    part = -1
                    break

            else:
                # bfp = np.array([real_batch, flops, params]).reshape(1, 3)
                bfp = np.array([real_batch, params]).reshape(1,2)
                predict_res = est_gpu.predict(bfp)
                pre_res = int(predict_res[0])
                if pre_res == 1:
                    part = part
                    break

    return part




def check_path(name):
    train_dir = os.path.join('/data/tfdata/k8snfs/', name)
    print(train_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    return train_dir

def write_step_meg(job_name):
    job = reload_jobs(job_name,-1)
    measure = job.measure
    client_pre = influxdb.InfluxDBClient(host=job.dbhost, port=8086, username='admin', password='admin',
                                         database="PREDICT")
    pre_list = measure.split(" ")
    # measure_s = pre_list[0] + 'S' + pre_list[-1]
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
                'training_step': job.training_step,
                'worker': job.worker_replicas,
                'ps': job.ps_replicas,
                'part': job.part
            }
        }
    ]
    client_pre.write_points(step_items, time_precision="ms", database="PREDICT")
    print('write initial measure_t success!!')
    job.write_retry(mode=0)
    # step_items = [
    #             {
    #                 'measurement': measure_up,
    #                 'tags': {
    #                     'task': self.task_id,
    #                     'runtimes': self.rtimes,
    #                     'retry': self.retry
    #                 },
    #                 'fields': {
    #                     'ps': self.ps_replicas,
    #                     'worker':self.worker_replicas,
    #                     'training_step': self.training_step
    #                 }
    #             }
    #         ]
    # print(step_to_train)


def loss_server_conn(ADDR,measure):
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

    return connected

def tongji_adjust_number(aim_list):
    try:
        tongji_wenjian = load_config('modnum.json')
    except Exception as ee0:
        tongji_wenjian = {}
        save_config(tongji_wenjian,'modnum.json')
        tongji_wenjian = load_config('modnum.json')
    aim_key_lists = list(tongji_wenjian.keys())
    for i in aim_list:
        if i in aim_key_lists:
            tongji_wenjian[i]+=1
        else:
            tongji_wenjian[i]=1
    save_config(tongji_wenjian,'modnum.json')
def tongji_waiting_queue(submit_job_name,time_submit_now):
    try:
        waiting_time = load_config('waiting_time.json')
    except Exception as ee0:
        waiting_time = {}
        save_config(waiting_time,'waiting_time.json')
        waiting_time = load_config('waiting_time.json')
    waited = list(waiting_time.keys())
    if submit_job_name not in waited:
        waiting_time[submit_job_name] = time_submit_now
    save_config(waiting_time,'waiting_time.json')


def Submit_job(tasks,lock,v1,jobs):
    try:
        rfr = joblib.load('rfr_batch.pkl')
    except Exception as e0:
        print(e0)
    try:
        est_gpu = joblib.load('est_gpu.pkl')
    except Exception as e00:
        print(e00)
    # est_mem = joblib.load('est_mem.pkl')
    # est_cpu = joblib.load('est_cpu.pkl')
    print('start to reload')
    print(jobs)
    global LOSSHOST,LOSSPORT,sleep_last_length
    ADDR = (LOSSHOST,LOSSPORT)
    PREHOST = '172.16.190.97'
    PREPORT = 12529
    ADDR2 = (PREHOST,PREPORT)
    max_buffer_size = 20
    job_basic = reload_jobs(tasks['last'],-1)
    max_free_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_free_load_gpu)
    max_wight_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_weight_load_gpu)
    worker_buffer = tasks['buffer']
    first_reload = False
    time.sleep(16)
    if worker_buffer:
        first_reload = True
    pool = multiprocessing.Pool(processes=10)
    for job0 in jobs:
        save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job0, job0)
        #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
        # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
        # 'cpu_high':cpu_base,'batch_res':batch_res,
        # 'flops_res':flops_res,'params_res':params_res}
        res_config = load_config(save_res_path)
        batch_res = res_config['batch_res']
        flops_res = res_config['flops_res']
        params_res = res_config['params_res']
        real_batch = res_config['real_batch']
        job01 = reload_jobs(job0,-1)
        # catch_node_step_msg(jobs=,job_name=,tasks=,lock=,batch=,flops=,params=,mode=)
        loss_server_conn(ADDR,job01.measure)
        pool.apply_async(catch_node_step_msg,args=(jobs,job0,tasks,lock,batch_res,flops_res,params_res,real_batch,-1))
    global_count = 1
    try:
        now_create = np.load('nowcreate.npy')
    except Exception as ee00:
        now_create = 0
        # np.save('nowcreate.npy')
        np.save('nowcreate.npy',now_create)

    while True:
        print("Global Count is :%d" % global_count)
        if tasks['start']==False:
            break
        if global_count > 2 and global_count % 7 != 0 and global_count%10 != 0:
            lock.acquire()
            counts = tasks['count']
            bufer_count = tasks['buffercount']
            lock.release()
            print(bufer_count)
            if tasks['next'] and counts < tasks['size']:
                print("panduan tasks in next")
                lock.acquire()
                tmp_next = tasks['next']
                job_name = tmp_next.pop(0)
                job_next_time = tasks['nexttimes']
                job_next_time_job_name = job_next_time[job_name]
                job_next_time_job_name = job_next_time_job_name+1
                job_next_time[job_name] = job_next_time_job_name
                tasks['nexttimes'] = job_next_time
                # tasks['nexttimes'][job_name] = job_next_time
                tasks['next'] = tmp_next
                lock.release()
                job = reload_jobs(job_name, -1)
                print("%s in next reload!" % job_name)
                node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                gpu_node_index,k8s_monitor,index_node_gpu = job_basic.select_k8s_gpu()
                catch_worker = 0
                catch_ps = 0
                catch_worker2 = 0
                node_keys = cpu_nodes.keys()
                gpu_nodes = list(gpu_node_index.keys())
                for gpu in gpu_nodes:
                    catch_worker_g = 0
                    can_use_gpu = k8s_monitor[gpu]['avail']
                    first_try = True
                    end_gpu = False
                    while not end_gpu:
                        if first_try:
                            if can_use_gpu - 1 >= 0:
                                catch_worker_g+=1
                                can_use_gpu = can_use_gpu - 1
                            first_try = False
                        else:
                            if can_use_gpu-1 >= 0 and catch_worker_g < job.worker_replicas:
                                catch_worker_g+=1
                                can_use_gpu = can_use_gpu - 1
                            else:
                                end_gpu = True
                    catch_worker2 += catch_worker_g
                    if catch_worker2 >= 1:
                        break
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
                    count_trys = 0
                    while (not endcpu) or (not endmem):
                        if first_try:
                            if can_use_cpu - 2000 >= 0:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 2000
                            else:
                                if can_use_cpu - job.cpu_allocate > 0:
                                    catch_worker_c += 1
                                    can_use_cpu = can_use_cpu - job.cpu_allocate

                            if can_use_mem - 2048 >= 0:
                                catch_ps_m += 1
                                can_use_mem = can_use_mem - 2048
                            else:
                                if can_use_mem - job.memory_allocate > 0:
                                    catch_worker_m += 1
                                    can_use_mem = can_use_mem - job.memory_allocate
                            first_try = False
                        else:
                            if can_use_cpu - 1600 >= 0 and catch_ps < job.ps_replicas:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 1600

                            else:
                                if can_use_cpu - job.cpu_allocate >= 0 and catch_worker < job.worker_replicas:
                                    catch_worker_c += 1
                                    can_use_cpu = can_use_cpu - job.cpu_allocate
                                else:
                                    endcpu = True

                            if can_use_mem - job.memory_allocate >= 0 and catch_ps < job.ps_replicas:
                                catch_worker_m += 1
                                can_use_mem = can_use_mem - job.memory_allocate
                            else:
                                if can_use_mem - 2048 >= 0 and catch_worker < job.worker_replicas:
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

                    # if catch_worker2 < catch_worker:
                    #     catch_worker = catch_worker2
                    if catch_ps >= 1 and catch_worker >= 1:
                        break
                if catch_worker2 <= catch_worker:
                    catch_worker = catch_worker2
                print("In next catch ps: %d,worker:%d" % (catch_ps, catch_worker))
                if catch_ps > 0 and catch_worker > 0:
                    # lock.acquire()
                    job.update_step()
                    print("in next update step success!!")
                    write_step_meg(job.name)
                    job.update_batch()
                    connected = False
                    try_times = 1
                    while True:
                        if try_times > 5:
                            break
                        print(job.measure)
                        print(ADDR)
                        connected = loss_server_conn(ADDR, job.measure)
                        print("connect result:")
                        print(connected)
                        if connected:
                            break
                        else:
                            try_times += 1
                    if not connected:
                        print("Conncet error!!Try again Later!!")
                        # lock.release()
                        continue
                    submit_time_now = time.time()
                    tongji_waiting_queue(job.name,submit_time_now)
                    lock.acquire()
                    job.create_tf()
                    ns_tmp = tasks['ns']
                    ns_tmp.append(job.name)
                    tasks['ns'] = ns_tmp
                    is_layout = tasks['nslayout']
                    is_layout[job.name] = False
                    tasks['nslayout'] = is_layout
                    jobs.append(job.name)
                    tasks['count'] += 1
                    tmp_next_time_config = tasks['nexttimes']
                    tmp_next_time_config.pop(job_name)
                    tasks['nexttimes'] = tmp_next_time_config
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    batch_res = res_config['batch_res']
                    flops_res = res_config['flops_res']
                    params_res = res_config['params_res']
                    real_batch = res_config['real_batch']
                    pool.apply_async(catch_node_step_msg,
                                     args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res,real_batch,1))
                    # tasks['next'] = ''
                    lock.release()
                else:
                    lock.acquire()
                    tmp_buffer_count0 = tasks['buffercount']
                    catch_tmp_nexttimes = tasks['nexttimes']
                    catch_tmp_ps_re_job_name = catch_tmp_nexttimes[job_name]

                    if catch_tmp_ps_re_job_name >=3 and tmp_buffer_count0 < max_buffer_size:
                        tmp_buffer_pool = tasks['buffer']
                        tmp_buffer_pool.append(job.name)
                        tasks['buffer'] = tmp_buffer_pool
                        tmp_buffer_count0+=1
                        tasks['buffercount'] = tmp_buffer_count0
                        tmp_next_time_config = tasks['nexttimes']
                        tmp_next_time_config.pop(job_name)
                        tasks['nexttimes'] =  tmp_next_time_config
                    else:
                        tmp_next = tasks['next']
                        tmp_next.append(job_name)
                        # tmp_next_time_config = tasks['nexttimes']
                        # tmp_next_time_config[job.name] = 0
                        # tasks['nexttimes'] = tmp_next_time_config
                        tasks['next'] = tmp_next
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    lock.release()
                    time.sleep(22)
            elif counts < tasks['size'] and bufer_count>0:
                lock.acquire()
                tmp_buffer_count = tasks['buffercount']
                worker_buffer = tasks['buffer']
                lock.release()
                node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,
                                                                                      cpu_base=cpu_nodes,
                                                                                      memory_base=memory_nodes,
                                                                                      total_cpu_base=total_cpu_use,
                                                                                      total_memory_base=total_mem_use)
                node_index_gpu, k8s_monitor, index_node_gpu = job_basic.select_k8s_gpu()
                catch_worker2 = 0
                node_using = list(node_index_gpu.keys())
                total_ava = 0
                top_ava = 0
                total_total = 0
                top_total = 0
                for i in range(len(index_node_gpu)):
                    total_ava += k8s_monitor[index_node_gpu[i]]['avail']
                    total_total += k8s_monitor[index_node_gpu[i]]['total']
                    if i <= 2:
                        top_ava += k8s_monitor[index_node_gpu[i]]['avail']
                        top_total += k8s_monitor[index_node_gpu[i]]['total']

                base = 0.6 * ((top_total - top_ava) / top_total) + 0.4*((total_total - total_ava) / total_total)
                if base < 0.5:
                    selected = False
                    selected_job_name = ''
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
                    selected_job_name = ''
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
                selected_res_config_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (selected_job_name,selected_job_name)
                selected_res_config2 = load_config(selected_res_config_path)
                #"flops_res": 1000000000000,
                #"params_res"
                using_flops = selected_res_config2['flops_res']
                using_param = selected_res_config2["params_res"]
                tmp_ps_replicas = job.ps_replicas
                tmp_worker_replicas = job.worker_replicas
                mini_batch = predict_min_first(rfr=rfr, batch=job.real_batch, flops=using_flops, params=using_param,template=job.template_id)
                mini_batch = float(mini_batch)
                tmp_rest = job.deadline+job.starttime-time.time()
                if tmp_rest > 0:
                    worker_need = math.ceil(
                        job.training_step * job.worker_replicas * mini_batch / ((tmp_rest) * job.part))
                    worker_need_total = worker_need * job.part
                else:
                    if base < 0.5:
                        worker_need_total = random.randint(2, 4)
                    elif base < 0.7:
                        worker_need_total = random.randint(1, 3)
                    else:
                        worker_need_total = random.randint(1, 2)
                print(worker_need_total)
                print(job.part)
                panduanyici = random.randint(4,5)
                if worker_need_total > panduanyici:
                    worker_need_total = int(panduanyici)
                node_index_gpu, k8s_monitor, index_node_gpu = job_basic.select_k8s_gpu()
                catch_worker2 = 0
                node_using = list(node_index_gpu.keys())
                total_ava = 0
                top_ava = 0
                for i in range(len(index_node_gpu)):
                    total_ava += k8s_monitor[index_node_gpu[i]]['avail']
                    if i <= 2:
                        top_ava += k8s_monitor[index_node_gpu[i]]['avail']

                if worker_need_total <= top_ava:
                    catch_worker2 = worker_need_total
                elif worker_need_total <= total_ava:
                    if top_ava:
                        catch_worker2 = top_ava
                    else:
                        catch_worker2 = 0
                else:
                    if not total_ava:
                        catch_worker2 = 0
                    else:
                        if total_ava > 1:
                            catch_worker2 = total_ava - 1
                        else:
                            catch_worker2 = 1

                tmp_ps_replicas = job.ps_replicas
                tmp_worker_replicas = job.worker_replicas

                if catch_worker2 > 0:
                    job.worker_replicas = catch_worker2

                if cpu_value < 0.4:
                    catch_tmp_ps_re = math.ceil(worker_need_total/2)
                elif cpu_value < 0.7:
                    catch_tmp_ps_re = math.ceil(worker_need_total/3)
                else:
                    catch_tmp_ps_re = math.ceil(worker_need_total/4)
                if catch_tmp_ps_re < 1:
                    catch_tmp_ps_re = 1
                job.ps_replicas = catch_tmp_ps_re
                mem_need = job.total_mem * total_mem_use + job.worker_replicas * job.memory_allocate + 2048 * job.ps_replicas
                cpu_need = job.total_cpu * total_cpu_use + job.worker_replicas * job.cpu_allocate + 2000 * job.ps_replicas
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
                            if can_use_cpu - 2048 > 0 and not reach_ps:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 2048
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
                                if can_use_cpu - 2048 > 0 and not reach_ps:
                                    catch_ps_c += 1
                                    can_use_cpu = can_use_cpu - 2048
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
                    if catch_ps >= catch_tmp_ps_re:
                        reach_ps = True
                    if catch_worker >= catch_worker2:
                        reach_worker = True
                    if catch_ps >= catch_tmp_ps_re and catch_worker >= catch_worker2:
                        break
                print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                catch_ps = min([catch_ps, catch_tmp_ps_re])
                catch_worker = min([catch_worker, catch_worker2])
                if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                    tmp_ps = job.ps_replicas
                    tmp_worker = job.worker_replicas
                    if catch_ps > 0 and catch_worker > 0:
                        if catch_worker > worker_need_total:
                            catch_worker = worker_need_total
                        if catch_worker > job.worker_replicas:
                            catch_worker = job.worker_replicas
                        if catch_ps > job.ps_replicas:
                            catch_ps = job.ps_replicas
                        job.ps_replicas = catch_ps
                        job.worker_replicas = catch_worker
                        job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                        save_job_change_layout(job.name, catch_ps, catch_worker, job.training_step)
                        job.update_step()
                        job.update_batch()
                        write_step_meg(job.name)
                        connected = False
                        try_times = 1
                        while True:
                            if try_times > 5:
                                break
                            connected = loss_server_conn(ADDR, job.measure)
                            if connected:
                                break
                            else:
                                try_times += 1
                        if not connected:
                            print("Conncet error!!Try again Later!!")
                            # lock.release()
                            continue
                        submit_time_now = time.time()
                        tongji_waiting_queue(job.name, submit_time_now)
                        job.create_tf()
                        ns_tmp = tasks['ns']
                        ns_tmp.append(job.name)
                        tasks['ns'] = ns_tmp

                        is_layout = tasks['nslayout']
                        is_layout[job.name] = False
                        tasks['nslayout'] = is_layout
                        jobs.append(job.name)
                        tasks['count'] += 1

                        save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                        res_config = load_config(save_res_path)
                        batch_res = res_config['batch_res']
                        flops_res = res_config['flops_res']
                        params_res = res_config['params_res']
                        real_batch = res_config['real_batch']

                        pool.apply_async(catch_node_step_msg,
                                         args=(
                                             jobs, job.name, tasks, lock, batch_res, flops_res, params_res, real_batch,
                                             1))
                    else:
                        job.ps_replicas = 1
                        job.worker_replicas = 1
                        job.training_step = math.ceil(job.training_step * tmp_worker_replicas)
                        save_job_change_layout(job.name, 1, 1, training_step=job.training_step)
                        # tasks['next'] = job.name
                        lock.acquire()
                        tmp_next = tasks['next']
                        tmp_next.append(job.name)
                        tmp_next_time_config = tasks['nexttimes']
                        tmp_next_time_config[job.name] = 0
                        tasks['nexttimes'] = tmp_next_time_config
                        tasks['next'] = tmp_next
                        lock.release()
                else:
                    job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                    save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, job.training_step)
                    job.update_step()
                    job.update_batch()
                    write_step_meg(job.name)
                    connected = False
                    try_times = 1
                    while True:
                        if try_times > 5:
                            break
                        connected = loss_server_conn(ADDR, job.measure)
                        if connected:
                            break
                        else:
                            try_times += 1
                    if not connected:
                        print("Conncet error!!Try again Later!!")
                        # lock.release()
                        continue
                    submit_time_now = time.time()
                    tongji_waiting_queue(job.name, submit_time_now)
                    lock.acquire()
                    job.create_tf()
                    # lock.acquire()
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
                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    batch_res = res_config['batch_res']
                    flops_res = res_config['flops_res']
                    params_res = res_config['params_res']
                    real_batch = res_config['real_batch']
                    pool.apply_async(catch_node_step_msg,
                                     args=(
                                         jobs, job.name, tasks, lock, batch_res, flops_res, params_res,real_batch, 1))
                    lock.release()
            global_count+=1
            time.sleep(sleep_last_length)
        if global_count % 10 == 0 or global_count<=2:
            print('start to submit a job!!')
            for _ in range(10):
                lock.acquire()
                counts = tasks['count']
                bufer_count = tasks['buffercount']
                lock.release()
                if ((counts >= tasks['size']) and (bufer_count >= max_buffer_size)) or now_create>25:
                    time.sleep(float(random.randint(7,9)))
                    pass
                else:
                    print('select a job!!')
                    time.sleep(40)
                    template_id = random.randint(1,2)
                    if tasks['reload'] == 0:
                        template_id = random.randint(1, 2)
                        # if template_id == 3:
                        #     template_id = random.randint(1,2)
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
                        lock.release()
                        ps_r = random.randint(1, 2)
                        worker_r = random.randint(1, 3)
                        batch = random.randint(4,72)
                        measure = "VGG 1"
                        print(tasks)
                        if template_id == 1:
                            layer1 = random.randint(1, 3)
                            layer2 = random.randint(1, 4)
                            layer3 = random.randint(1, 6)
                            layer4 = random.randint(1, 7)
                            layer5 = random.randint(1, 8)
                            kernel = random.randint(1, 7)
                            unit1 = random.randint(512, 4096+2048)
                            unit2 = random.randint(512, 4096+2048)
                            channel1 = random.randint(24, 96)
                            channel2 = random.randint(48, 160)
                            channel3 = random.randint(128, 320)
                            channel4 = random.randint(128, 640)
                            channel5 = random.randint(240, 1024)
                            first_step = math.ceil(tasks['training_step'][template_id - 1]*random.randint(2,10)/8)

                            job = VGGTask(template_id=template_id, ps_replicas=ps_r,
                                          worker_replicas=worker_r,
                                          training_step=first_step,
                                          batch_size=batch,
                                          interval=tasks['interval'][template_id - 1],
                                          task_id=tasks['task_id'][template_id - 1],
                                          rtimes=tasks['rtimes'][template_id - 1],
                                          tag=tasks['tag'][template_id - 1], channel1=channel1, channel2=channel2,
                                          channel3=channel3,
                                          channel4=channel4, channel5=channel5,
                                          num_layer1=layer1, num_layer2=layer2, num_layer3=layer3,
                                          num_layer4=layer4,
                                          num_layer5=layer5,kernel=kernel,unit1=unit1,unit2=unit2,part=1
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
                                          'num_layer5': job.num_layer5,
                                          'unit1': job.unit1,
                                          'unit2': job.unit2,
                                          'kernel': job.kernel,
                                          'retry': job.retry,
                                          'part':job.part}

                            dict = {'batch_size': job.real_batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                                    'channel4': channel4,
                                    'channel5': channel5, 'num_layer1': layer1, 'num_layer2': layer2,
                                    'num_layer3': layer3, 'num_layer4': layer4, 'num_layer5': layer5,'kernel':kernel,'unit1':unit1,'unit2':unit2}


                        elif template_id == 2:
                            layer1 = random.randint(1, 5)
                            layer2 = random.randint(2, 6)
                            layer3 = random.randint(2, 38)
                            layer4 = random.randint(2, 10)

                            kernel = random.randint(2, 9)
                            k0 = kernel
                            k11 = random.randint(1, 5)
                            k12 = random.randint(2, 9)
                            k21 = random.randint(1, 5)
                            k22 = random.randint(2, 9)
                            k31 = random.randint(1, 5)
                            k32 = random.randint(2, 9)
                            k41 = random.randint(1, 5)
                            k42 = random.randint(2, 9)

                            rate1 = random.randint(2, 6)
                            rate2 = random.randint(2, 6)
                            rate3 = random.randint(2, 6)
                            rate4 = random.randint(2, 6)

                            bot = random.randint(0, 3)

                            channel1 = random.randint(32, 80)
                            channel2 = random.randint(48, 160)
                            channel3 = random.randint(96, 320)
                            channel4 = random.randint(128, 768)

                            first_step = math.ceil(tasks['training_step'][template_id - 1] * random.randint(2, 10) / 8)

                            job = RESTask(template_id=template_id, ps_replicas=ps_r,
                                          worker_replicas=worker_r,
                                          training_step=first_step,
                                          batch_size=batch,
                                          interval=tasks['interval'][template_id - 1],
                                          task_id=tasks['task_id'][template_id - 1],
                                          rtimes=tasks['rtimes'][template_id - 1],
                                          tag=tasks['tag'][template_id - 1], bot=bot, block1=layer1,
                                          block2=layer2,
                                          block3=layer3,
                                          block4=layer4, channel1=channel1, channel2=channel2, channel3=channel3,
                                          channel4=channel4,rate1=rate1,rate2=rate2,rate3=rate3,rate4=rate4,k0=k0,k11=k11,k12=k12,k21=k21,k22=k22,
                                          k31=k31,k32=k32,k41=k41,k42=k42,part=1)

                            job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                          'worker_replicas': job.worker_replicas,
                                          'training_step': job.training_step,
                                          'batch_size': job.batch_size,
                                          'interval': job.interval,
                                          'task_id': job.task_id, 'rtimes': job.rtimes,
                                          'tag': job.tag, 'bot': job.bot, 'block1': job.block1,
                                          'block2': job.block2,
                                          'block3': job.block3,
                                          'block4': job.block4, 'channel1': job.channel1, 'channel2': job.channel2,
                                          'channel3': job.channel3, 'channel4': job.channel4,'rate1': job.rate1,'rate2':job.rate2,'rate3':job.rate3,
                                          'rate4':job.rate4,'k0': job.k0,'k11': job.k11,'k12':job.k12,'k21':job.k21,'k22':job.k22,'k31':job.k31,'k32':job.k32,
                                          'k41':job.k41,'k42':job.k42,'retry': job.retry,'part': job.part}
                            dict = {'batch_size': job.real_batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                                    'channel4': channel4,
                                    'block1': layer1, 'block2': layer2,
                                    'block3': layer3, 'block4': layer4, 'bot': bot,'rate1': rate1,'rate2':rate2,'rate3':rate3,'rate4':rate4,
                                    'k0':k0,'k11':k11,'k12':k12,'k21':k21,'k22':k22,'k31':k31,'k32':k32,'k41':k41,'k42':k42}


                        measure = job.measure
                        # lock.acquire()
                        # tasks['base'] = job.name
                        # lock.release()
                    else:
                        job_base_name = tasks['base']
                        job_base_name_list = job_base_name.split('-')
                        if job_base_name_list[0] == 'vgg':
                            template_id = 1
                        elif job_base_name_list[0] == 'res':
                            template_id = 2
                        lock.acquire()
                        tmp1 = tasks['task_id']
                        tmp1[template_id - 1] += 1
                        tasks['task_id'] = tmp1
                        tmp2 = tasks['rtimes']
                        tmp2[template_id - 1] += 1
                        tasks['rtimes'] = tmp2
                        lock.release()
                        tmp_task_id = tmp1[template_id - 1]
                        job = reload_jobs(job_base_name, task_id=tmp_task_id)
                        job.retry = 0

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
                                          'num_layer5': job.num_layer5,
                                          'unit1': job.unit1,
                                          'unit2': job.unit2,
                                          'kernel': job.kernel,
                                          'retry': job.retry,
                                          'part': job.part}

                            dict = {'batch': job.real_batch, 'channel1': job.channel1, 'channel2': job.channel2,
                                    'channel3': job.channel3,
                                    'channel4': job.channel4,
                                    'channel5': job.channel5, 'num_layer1': job.num_layer1, 'num_layer2': job.num_layer2,
                                    'num_layer3': job.num_layer3, 'num_layer4': job.num_layer4, 'num_layer5': job.num_layer4,
                                    'kernel': job.kernel, 'unit1': job.unit1, 'unit2': job.unit2}

                        elif template_id == 2:
                            job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                         'worker_replicas': job.worker_replicas,
                                         'training_step': job.training_step,
                                         'batch_size': job.batch_size,
                                         'interval': job.interval,
                                         'task_id': job.task_id, 'rtimes': job.rtimes,
                                         'tag': job.tag, 'bot': job.bot, 'block1': job.block1,
                                         'block2': job.block2,
                                         'block3': job.block3,
                                         'block4': job.block4, 'channel1': job.channel1, 'channel2': job.channel2,
                                         'channel3': job.channel3, 'channel4': job.channel4, 'rate1': job.rate1,
                                         'rate2': job.rate2, 'rate3': job.rate3,
                                         'rate4': job.rate4, 'k0': job.k0, 'k11': job.k11, 'k12': job.k12,
                                         'k21': job.k21, 'k22': job.k22, 'k31': job.k31, 'k32': job.k32,
                                         'k41': job.k41, 'k42': job.k42, 'retry': job.retry, 'part': job.part}
                            dict = {'batch': job.real_batch, 'channel1': job.channel1, 'channel2': job.channel2, 'channel3': job.channel3,
                                    'channel4': job.channel4,
                                    'block1': job.block1, 'block2': job.block2,
                                    'block3': job.block3, 'block4': job.block4, 'bot': job.bot, 'rate1': job.rate1,
                                    'rate2': job.rate2, 'rate3': job.rate3, 'rate4': job.rate4,
                                    'k0': job.k0, 'k11': job.k11, 'k12': job.k12, 'k21': job.k21, 'k22': job.k22, 'k31': job.k31, 'k32': job.k32,
                                    'k41': job.k41, 'k42': job.k42}
                        measure = job.measure
                    lock.acquire()
                    tmp_tasks_count = tasks['count']
                    tmp_tasks_buffercount =  tasks['buffercount']
                    lock.release()
                    # lock.acquire()
                    if tmp_tasks_count < tasks['size'] or tasks['buffercount'] < max_buffer_size:
                        # loss_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        # loss_client.connect(ADDR)
                        client_pre = influxdb.InfluxDBClient(host=job.dbhost, port=8086, username='admin',
                                                             password='admin',
                                                             database="PREDICT")
                        pre_list = measure.split(" ")
                        # measure_s = pre_list[0] + 'S' + pre_list[-1]
                        measure_t = pre_list[0] + 'T' + pre_list[-1]
                        save_config_dir = task_submit.check_path(job.name)
                        save_job_path = '/data/tfdata/k8snfs/%s/%s.json' % (job.name, job.name)

                        pre_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        pre_client.connect(ADDR2)
                        pre_client.send(bytes(measure, 'utf-8'))
                        connect_try = 5
                        try_times = 1
                        connected = False
                        msg_from_server_str = ''
                        while True:
                            if try_times > connect_try:
                                break
                            msg_from_server = pre_client.recv(4096)
                            if not msg_from_server:
                                break
                            msg_from_server_str = str(msg_from_server.decode('utf-8'))
                            msg_from_server_list = msg_from_server_str.split(" ")
                            if msg_from_server_list[0] == '400':
                                connected = True
                                break
                            pre_client.send(bytes(measure, 'utf-8'))
                            try_times = try_times + 1

                        if not connected:
                            print("Connected or send message error!")
                            pre_client.close()
                            # lock.acquire()
                            tmp1 = tasks['task_id']
                            tmp1[template_id - 1] -= 1
                            tasks['task_id'] = tmp1
                            tmp2 = tasks['rtimes']
                            tmp2[template_id - 1] -= 1
                            tasks['rtimes'] = tmp2
                            # lock.release()
                            try:
                                command0 = 'rm %s' % save_job_path
                                aek = os.system(command0)
                                command0 = 'rm %s' % allow_path
                                ask = os.system(command0)
                            except Exception as eee0:
                                print(eee0)
                            continue
                        print(msg_from_server_str)
                        print("connected success!")
                        dict_json = json.dumps(dict)
                        pre_client.send(bytes(dict_json, 'utf-8'))
                        ress = pre_client.recv(4096)
                        ress_str = str(ress.decode('utf-8'))
                        ress_lists = ress_str.split(' ')
                        if ress_lists[0] == '400':
                            batch_res = int(ress_lists[1])
                            flops_res = int(ress_lists[2])
                            params_res = int(ress_lists[3])
                            part = int(ress_lists[-1])
                            if part < 0 or part >= 14:  
                                res_to_server = '0'
                                pre_client.send(bytes(res_to_server, 'utf-8'))
                                print("send response success!!")
                                time.sleep(6)
                                pre_client.close()
                                print("some time later to try again!!")
                                tmp1 = tasks['task_id']
                                tmp1[template_id - 1] -= 1
                                tasks['task_id'] = tmp1
                                tmp2 = tasks['rtimes']
                                tmp2[template_id - 1] -= 1
                                tasks['rtimes'] = tmp2
                                # lock.release()
                                try:
                                    command0 = 'rm %s' % save_job_path
                                    aek = os.system(command0)
                                    command0 = 'rm %s' % allow_path
                                    ask = os.system(command0)
                                except Exception as eee0:
                                    print(eee0)
                                time.sleep(5)
                                continue
                            res_to_server = '1'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                        else:
                            res_to_server = '0'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                            print("send response success!!")
                            time.sleep(6)
                            pre_client.close()
                            print("some time later to try again!!")
                            tmp1 = tasks['task_id']
                            tmp1[template_id - 1] -= 1
                            tasks['task_id'] = tmp1
                            tmp2 = tasks['rtimes']
                            tmp2[template_id - 1] -= 1
                            tasks['rtimes'] = tmp2
                            lock.release()
                            try:
                                command0 = 'rm %s' % save_job_path
                                aek = os.system(command0)
                                command0 = 'rm %s' % allow_path
                                ask = os.system(command0)
                            except Exception as eee0:
                                print(eee0)
                            time.sleep(30)
                            continue
                        pre_client.close()
                        tmp_reload = tasks['reload']
                        if tmp_reload == 0:
                            # alpha = 1
                            # beta = 1
                            alpha = random.randint(0,7)*0.1+0.5
                            beta = random.randint(0,18)*0.1+0.875
                        else:
                            alpha = random.randint(2, 12) * 0.1 + 0.6
                            beta = random.randint(0, 10) * 0.1 + 1
                        alpha = 1
                        beta = 1
                        job.set_batch(job.batch_size,part2=part)
                        # save_job_change_resource(job.name,job.batch_size,job.batch_size,part)
                        # job.set_resource(cpu_source=(math.ceil(cpu_base * alpha)),
                        #                  mem_source=(math.ceil(mem_base * beta)))
                        job_config['part'] = part
                        job.worker_replicas = job.worker_replicas*part
                        job_config['worker_replicas'] = job.worker_replicas
                        save_config(job_config, save_job_path)
                        allow_read = {}
                        allow_read['OK'] = True
                        allow_read['retry'] = 0
                        allow_p = check_path(measure_t)
                        allow_path = '/data/tfdata/k8snfs/%s/%s.json' % (job.name, measure_t)
                        save_config(allow_read, allow_path)
                        mini_batch = predict_min_first(rfr=rfr,batch=batch_res,flops=flops_res,params=params_res,template=job.template_id)
                        mini_batch = float(mini_batch)
                        deadline = mini_batch*job.training_step*(random.randint(4,48)*0.2)+(3000*random.randint(8,96)/16)*(min([(now_create+1),26])/(random.randint(5,8)))
                        print(deadline)
                        print(type(deadline))
                        # deadline = random.randint(3600, 18000)
                        start_time = '%.3f' % time.time()
                        start_time = float(start_time)
                        job.set_deadline(deadline=deadline, start_time=start_time)

                        job_res_config = {'deadline': job.deadline, 'start_time': job.starttime,'cpu_source': job.cpu_allocate,
                                          'real_batch': job.real_batch, 'batch_res': batch_res, 'mem_source': job.memory_allocate, 'cpu_high': job.cpu_allocate,
                        'memory_base': job.memory_allocate,
                                          'flops_res': flops_res, 'params_res': params_res, 'step_base': 0,'part':part,
                                          'reloadtime': []}
                        save_config_dir = task_submit.check_path(job.name)
                        save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                        # save_config(job_config, save_job_path)
                        save_config(job_res_config, save_res_path)
                        save_job_change_resource(job.name,job.batch_size,job.batch_size,job.part)
                        now_create = now_create+1
                        np.save('nowcreate.npy', now_create)


                        if tasks['count'] < tasks['size'] and tasks['buffercount'] == 0:
                            worker_need = math.ceil(
                                job.training_step * job.worker_replicas * mini_batch / (job.deadline * job.part))
                            worker_need_total = worker_need * part
                            print(worker_need_total)
                            print(part)
                            if worker_need_total > 5:
                                worker_need_total = 5
                            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                            cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,
                                                                                                  cpu_base=cpu_nodes,
                                                                                                  memory_base=memory_nodes,
                                                                                                  total_cpu_base=total_cpu_use,
                                                                                                  total_memory_base=total_mem_use)
                            node_index_gpu,k8s_monitor,index_node_gpu = job_basic.select_k8s_gpu()
                            catch_worker2 = 0
                            node_using = list(node_index_gpu.keys())
                            total_ava = 0
                            top_ava = 0
                            for i in range(len(index_node_gpu)):
                                total_ava+=k8s_monitor[index_node_gpu[i]]['avail']
                                if i<=2:
                                    top_ava+=k8s_monitor[index_node_gpu[i]]['avail']

                            if worker_need_total <= top_ava:
                                catch_worker2 = worker_need_total
                            elif worker_need_total <= total_ava:
                                if top_ava:
                                    catch_worker2 = top_ava
                                else:
                                    catch_worker2 = 0
                            else:
                                if not total_ava:
                                    catch_worker2 = 0
                                else:
                                    if total_ava > 1:
                                        catch_worker2 = total_ava - 1
                                    else:
                                        catch_worker2 = 1

                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas

                            if catch_worker2 > 0:
                                job.worker_replicas = catch_worker2

                            if cpu_value < 0.4:
                                catch_tmp_ps_re = math.ceil(catch_worker2/2)
                            elif cpu_value < 0.7:
                                catch_tmp_ps_re = math.ceil(catch_worker2 / 3)
                            else:
                                catch_tmp_ps_re = math.ceil(catch_worker2 / 4)


                            # catch_tmp_ps_re = random.randint(math.floor(job.worker_replicas / 4),
                            #                                  math.ceil(job.worker_replicas / 2))
                            if catch_tmp_ps_re < 1:
                                catch_tmp_ps_re = 1
                            job.ps_replicas = catch_tmp_ps_re
                            # job.ps_replicas = catch_tmp_ps_re
                            # job.worker_replicas = catch_worker2

                            # job.training_step = math.ceil(job.training_step * worker_need_total / )
                            # 
                            # save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, job.training_step)

                            mem_need = job.total_mem * total_mem_use + job.worker_replicas * job.memory_allocate + 2048 * job.ps_replicas
                            cpu_need = job.total_cpu * total_cpu_use + job.worker_replicas * job.cpu_allocate + 750 * job.ps_replicas
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
                                        if can_use_cpu - 2048> 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 2048
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
                                            if can_use_cpu - 2048 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 2048
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
                                if catch_ps >= catch_tmp_ps_re:
                                    reach_ps = True
                                if catch_worker >= catch_worker2:
                                    reach_worker = True
                                if catch_ps >= catch_tmp_ps_re and catch_worker >= catch_worker2:
                                    break
                            print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                            catch_ps = min([catch_ps,catch_tmp_ps_re])
                            catch_worker = min([catch_worker,catch_worker2])
                            if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                                tmp_ps = job.ps_replicas
                                tmp_worker = job.worker_replicas
                                if catch_ps > 0 and catch_worker > 0:
                                    if catch_worker > worker_need_total:
                                        catch_worker = worker_need_total
                                    if catch_worker > job.worker_replicas:
                                        catch_worker = job.worker_replicas
                                    if catch_ps > job.ps_replicas:
                                        catch_ps = job.ps_replicas
                                    job.ps_replicas = catch_ps
                                    job.worker_replicas = catch_worker
                                    job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                                    save_job_change_layout(job.name, catch_ps, catch_worker, job.training_step)
                                    job.update_step()
                                    job.update_batch()
                                    write_step_meg(job.name)
                                    connected = False
                                    try_times = 1
                                    while True:
                                        if try_times > 5:
                                            break
                                        connected = loss_server_conn(ADDR, job.measure)
                                        if connected:
                                            break
                                        else:
                                            try_times += 1
                                    if not connected:
                                        print("Conncet error!!Try again Later!!")
                                        # lock.release()
                                        continue
                                    submit_time_now = time.time()
                                    tongji_waiting_queue(job.name, submit_time_now)
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
                                    lock.release()

                                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                    # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                                    # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                                    # 'cpu_high':cpu_base,'batch_res':batch_res,
                                    # 'flops_res':flops_res,'params_res':params_res}
                                    res_config = load_config(save_res_path)
                                    batch_res = res_config['batch_res']
                                    flops_res = res_config['flops_res']
                                    params_res = res_config['params_res']
                                    real_batch = res_config['real_batch']

                                    pool.apply_async(catch_node_step_msg,
                                                     args=(
                                                     jobs, job.name, tasks, lock, batch_res, flops_res, params_res,real_batch, 1))
                                else:
                                    job.ps_replicas = 1
                                    job.worker_replicas = 1
                                    job.training_step = job.training_step * tmp_worker_replicas
                                    save_job_change_layout(job.name, 1, 1, job.training_step)
                                    lock.acquire()
                                    tmp_next = tasks['next']
                                    tmp_next.append(job.name)
                                    tmp_next_time_config = tasks['nexttimes']
                                    tmp_next_time_config[job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config
                                    tasks['next'] = tmp_next
                                    lock.release()
                                    # tasks['next'] = job.name
                            else:
                                job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                                save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas,job.training_step)
                                job.update_step()
                                job.update_batch()
                                write_step_meg(job.name)
                                connected = False
                                try_times = 1
                                while True:
                                    if try_times > 5:
                                        break
                                    connected = loss_server_conn(ADDR, job.measure)
                                    if connected:
                                        break
                                    else:
                                        try_times += 1
                                if not connected:
                                    print("Conncet error!!Try again Later!!")
                                    # lock.release()
                                    continue
                                submit_time_now = time.time()
                                tongji_waiting_queue(job.name, submit_time_now)
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
                                lock.release()
                                save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                                # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                                # 'cpu_high':cpu_base,'batch_res':batch_res,
                                # 'flops_res':flops_res,'params_res':params_res}
                                res_config = load_config(save_res_path)
                                batch_res = res_config['batch_res']
                                flops_res = res_config['flops_res']
                                params_res = res_config['params_res']
                                real_batch = res_config['real_batch']

                                pool.apply_async(catch_node_step_msg,
                                                 args=(
                                                 jobs, job.name, tasks, lock, batch_res, flops_res, params_res,real_batch,1))

                        elif tasks['count'] >= tasks['size']:
                            worker_buffer = tasks['buffer']
                            worker_buffer.append(job.name)
                            tasks['buffer'] = worker_buffer
                            tmp_buffer_count = tasks['buffercount']
                            tmp_buffer_count = tmp_buffer_count + 1
                            tasks['buffercount'] = tmp_buffer_count

                        else:
                            worker_buffer = tasks['buffer']
                            worker_buffer.append(job.name)
                            tmp_buffer_count = tasks['buffercount']
                            tmp_buffer_count = tmp_buffer_count + 1
                            tasks['buffercount'] = tmp_buffer_count
                            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                            cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,
                                                                                                  cpu_base=cpu_nodes,
                                                                                                  memory_base=memory_nodes,
                                                                                                  total_cpu_base=total_cpu_use,
                                                                                                  total_memory_base=total_mem_use)

                            node_index_gpu, k8s_monitor, index_node_gpu = job_basic.select_k8s_gpu()
                            catch_worker2 = 0
                            node_using = list(node_index_gpu.keys())
                            total_ava = 0
                            top_ava = 0
                            total_total = 0
                            top_total = 0
                            for i in range(len(index_node_gpu)):
                                total_ava += k8s_monitor[index_node_gpu[i]]['avail']
                                total_total+= k8s_monitor[index_node_gpu[i]]['total']
                                if i <= 2:
                                    top_ava += k8s_monitor[index_node_gpu[i]]['avail']
                                    top_total += k8s_monitor[index_node_gpu[i]]['total']

                            base = 0.6*((top_total - top_ava)/top_total)+0.4*((total_total - total_ava)/total_total)
                            if base < 0.5:
                                selected = False
                                selected_job_name = ''
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
                                # lock.acquire()
                                tasks['buffer'] = worker_buffer[:]
                                # tmp_buffer_size =
                                max_free_heap.clear()
                                if selected:
                                    tasks['buffercount'] = max_buffer_size
                                else:
                                    tmp_buffer_count = tmp_buffer_count - 1
                                    tasks['buffercount'] = tmp_buffer_count
                                # lock.release()
                            else:
                                selected = False
                                selected_job_name = ''
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
                            selected_res_config_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (
                            selected_job_name, selected_job_name)
                            selected_res_config2 = load_config(selected_res_config_path)
                            # "flops_res": 1000000000000,
                            # "params_res"
                            # "flops_res": 4130467255,
                            # "params_res": 458728224,

                            using_flops = selected_res_config2['flops_res']
                            using_param = selected_res_config2["params_res"]
                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas
                            mini_batch = predict_min_first(rfr=rfr, batch=job.real_batch, flops=using_flops,
                                                           params=using_param,template=job.template_id)
                            mini_batch = float(mini_batch)
                            tmp_rest = job.deadline + job.starttime - time.time()
                            if tmp_rest > 0:
                                worker_need = math.ceil(
                                    job.training_step * job.worker_replicas * mini_batch / ((tmp_rest) * job.part))
                                worker_need_total = worker_need * job.part
                            else:
                                if base < 0.5:
                                    worker_need_total = random.randint(2, 4)
                                elif base < 0.7:
                                    worker_need_total = random.randint(1, 3)
                                else:
                                    worker_need_total = random.randint(1, 2)
                            print(worker_need_total)
                            print(job.part)
                            if worker_need_total > 5:
                                worker_need_total = 5
                            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                            cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,
                                                                                                  cpu_base=cpu_nodes,
                                                                                                  memory_base=memory_nodes,
                                                                                                  total_cpu_base=total_cpu_use,
                                                                                                  total_memory_base=total_mem_use)
                            node_index_gpu, k8s_monitor, index_node_gpu = job_basic.select_k8s_gpu()
                            catch_worker2 = 0
                            node_using = list(node_index_gpu.keys())
                            total_ava = 0
                            top_ava = 0
                            for i in range(len(index_node_gpu)):
                                total_ava += k8s_monitor[index_node_gpu[i]]['avail']
                                if i <= 2:
                                    top_ava += k8s_monitor[index_node_gpu[i]]['avail']

                            if worker_need_total <= top_ava:
                                catch_worker2 = worker_need_total
                            elif worker_need_total <= total_ava:
                                if top_ava:
                                    catch_worker2 = top_ava
                                else:
                                    catch_worker2 = 0
                            else:
                                if not total_ava:
                                    catch_worker2 = 0
                                else:
                                    if total_ava > 1:
                                        catch_worker2 = total_ava - 1
                                    else:
                                        catch_worker2 = 1

                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas

                            if catch_worker2 > 0:
                                job.worker_replicas = catch_worker2

                            if cpu_value < 0.4:
                                catch_tmp_ps_re = math.ceil(worker_need_total / 2)
                            elif cpu_value < 0.7:
                                catch_tmp_ps_re = math.ceil(worker_need_total / 3)
                            else:
                                catch_tmp_ps_re = math.ceil(worker_need_total / 4)
                            if catch_tmp_ps_re < 1:
                                catch_tmp_ps_re = 1
                            job.ps_replicas = catch_tmp_ps_re
                            mem_need = job.total_mem * total_mem_use + job.worker_replicas * job.memory_allocate + 2048 * job.ps_replicas
                            cpu_need = job.total_cpu * total_cpu_use + job.worker_replicas * job.cpu_allocate + 2000 * job.ps_replicas
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
                                        if can_use_cpu - 2048 > 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 2048
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
                                            if can_use_cpu - 2048 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 2048
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
                                if catch_ps >= catch_tmp_ps_re:
                                    reach_ps = True
                                if catch_worker >= catch_worker2:
                                    reach_worker = True
                                if catch_ps >= catch_tmp_ps_re and catch_worker >= catch_worker2:
                                    break
                            print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                            catch_ps = min([catch_ps, catch_tmp_ps_re])
                            catch_worker = min([catch_worker, catch_worker2])
                            if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                                tmp_ps = job.ps_replicas
                                tmp_worker = job.worker_replicas
                                if catch_ps > 0 and catch_worker > 0:
                                    if catch_worker > worker_need_total:
                                        catch_worker = worker_need_total
                                    if catch_worker > job.worker_replicas:
                                        catch_worker = job.worker_replicas
                                    if catch_ps > job.ps_replicas:
                                        catch_ps = job.ps_replicas
                                    job.ps_replicas = catch_ps
                                    job.worker_replicas = catch_worker
                                    job.training_step = math.ceil(
                                        job.training_step * tmp_worker_replicas / job.worker_replicas)
                                    save_job_change_layout(job.name, catch_ps, catch_worker, job.training_step)
                                    job.update_step()
                                    job.update_batch()
                                    write_step_meg(job.name)
                                    connected = False
                                    try_times = 1
                                    while True:
                                        if try_times > 5:
                                            break
                                        connected = loss_server_conn(ADDR, job.measure)
                                        if connected:
                                            break
                                        else:
                                            try_times += 1
                                    if not connected:
                                        print("Conncet error!!Try again Later!!")
                                        # lock.release()
                                        continue
                                    submit_time_now = time.time()
                                    tongji_waiting_queue(job.name, submit_time_now)
                                    lock.acquire()
                                    job.create_tf()
                                    ns_tmp = tasks['ns']
                                    ns_tmp.append(job.name)
                                    tasks['ns'] = ns_tmp
                                    is_layout = tasks['nslayout']
                                    is_layout[job.name] = False
                                    tasks['nslayout'] = is_layout
                                    jobs.append(job.name)
                                    tasks['count'] += 1
                                    lock.release()
                                    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)

                                    res_config = load_config(save_res_path)
                                    batch_res = res_config['batch_res']
                                    flops_res = res_config['flops_res']
                                    params_res = res_config['params_res']
                                    real_batch = res_config['real_batch']

                                    pool.apply_async(catch_node_step_msg,
                                                     args=(
                                                         jobs, job.name, tasks, lock, batch_res, flops_res, params_res,
                                                         real_batch, 1))
                                else:
                                    job.ps_replicas = 1
                                    job.worker_replicas = 1
                                    job.training_step = job.training_step * tmp_worker_replicas
                                    save_job_change_layout(job.name, 1, 1, job.training_step)
                                    lock.acquire()
                                    tmp_next = tasks['next']
                                    tmp_next.append(job.name)
                                    tmp_next_time_config = tasks['nexttimes']
                                    tmp_next_time_config[job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config
                                    tasks['next'] = tmp_next
                                    lock.release()
                                    # tasks['next'] = job.name
                                    # lock.release()
                            else:
                                job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                                save_job_change_layout(job.name,job.ps_replicas,job.worker_replicas,job.training_step)
                                job.update_step()
                                job.update_batch()
                                write_step_meg(job.name)
                                connected = False
                                try_times = 1
                                while True:
                                    if try_times > 5:
                                        break
                                    connected = loss_server_conn(ADDR, job.measure)
                                    if connected:
                                        break
                                    else:
                                        try_times += 1
                                if not connected:
                                    print("Conncet error!!Try again Later!!")
                                    # lock.release()
                                    continue
                                submit_time_now = time.time()
                                tongji_waiting_queue(job.name, submit_time_now)
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
                                save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                res_config = load_config(save_res_path)
                                batch_res = res_config['batch_res']
                                flops_res = res_config['flops_res']
                                params_res = res_config['params_res']
                                real_batch = res_config['real_batch']
                                lock.release()
                                pool.apply_async(catch_node_step_msg,
                                                 args=(
                                                 jobs, job.name, tasks, lock, batch_res, flops_res, params_res, real_batch,1))

                        tmp_reload = tasks['reload']
                        tmp_reload = 0
                        tasks['reload'] = tmp_reload
                    # lock.release()
                    break
            global_count += 1
        if global_count % 7 == 0 and global_count%10!=0:
            # global_count += 1
            # continue
            for iter0 in range(2):
                aim_assign_config = {}
                mode1 = 0
                time10 = time.time()
                try:
                    lock.acquire()
                    tasks['modulate'] = True
                    lock.release()
                    # aim_assign_config, mode1 = assign_jobs(tasks, rfr=rfr, lock=lock)
                    try:
                        aim_assign_config,mode1 = assign_jobs(tasks,rfr=rfr,lock=lock)
                    except Exception as e00:
                        print("The error exist in dynamic modulation:")
                        print(e00)
                    print(aim_assign_config)
                    print(mode1)
                    lock.acquire()
                    tasks['modulate'] = False
                    lock.release()
                except Exception as e:
                    print(e)
                    # lock.release()
                    time.sleep(30)
                    continue
                print(aim_assign_config)
                print("Mode is %d" % mode1)
                if mode1 == 0:
                    continue
                elif mode1 == -1:
                    continue
                elif not aim_assign_config:
                    continue
                else:
                    assign_key = list(aim_assign_config.keys())
                    print(assign_key)
                    if not assign_key:
                        continue
                    jinxing = False
                    aim_ns = []
                    for assign in assign_key:
                        lock.acquire()
                        tmp_ns0 = tasks['ns']
                        lock.release()
                        # pod_status = [i.status.phase for i in v1.list_namespaced_pod(job.name).items]
                        # run_result00 = pd.value_counts(pod_status00)
                        # run_result_dict00 = dict(run_result00)
                        # print(run_result_dict00)
                        # elif 'Succeeded' in pod_status or 'Failed' in pod_status:
                        if (aim_assign_config[assign]) and (assign in tmp_ns0):
                            pod_status00 = [ps.status.phase for ps in v1.list_namespaced_pod(assign).items]
                            if pod_status00:
                                if (not ('Succeeded' in pod_status00 or 'Failed' in pod_status00)):
                                    jinxing = True
                                    aim_ns.append(assign)
                    print("At last the aim can be decided as:")
                    print(aim_ns)
                    if jinxing:
                        lock.acquire()
                        tmp_retry_ns = tasks['retry']
                        tmp_retry_solution = tasks['solution']
                        is_layout = tasks['nslayout']
                        if mode1 == 2:
                            try:
                                for iaim in range(len(aim_ns)-1,-1,-1):
                                    tmp_retry_ns.append(aim_ns[iaim])
                                    tmp_retry_solution[aim_ns[iaim]] = aim_assign_config[aim_ns[iaim]]
                                    is_layout[aim_ns[iaim]] = False
                            except Exception as ex0:
                                print(ex0)
                                for aim in aim_ns:
                                    if aim in tmp_retry_ns:
                                        tmp_retry_ns.remove(aim)
                                        tmp_retry_solution.pop(aim)
                                        is_layout[aim] = True
                                for aim in aim_ns:
                                    tmp_retry_ns.append(aim)
                                    tmp_retry_solution[aim] = aim_assign_config[aim]
                                    is_layout[aim] = False
                        else:
                            for aim in aim_ns:
                                tmp_retry_ns.append(aim)
                                tmp_retry_solution[aim] = aim_assign_config[aim]
                                is_layout[aim] = False
                        tasks['retry'] = tmp_retry_ns
                        tasks['solution'] = tmp_retry_solution
                        tasks['nslayout'] = is_layout
                        lock.release()
                        tongji_adjust_number(aim_ns)
                time20 = time.time()

                print("Modulation once cost %f" % float(time20 - time10))
                if (mode1==1 or mode1==4) and (iter0>=1):
                    break
                time.sleep(22*2)
            global_count+=1

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
    try:
        task2 = load_config('through.json')
        task3 = load_config('buffer.json')
    # aa = 0
    except Exception as eee:
        task2 = {}
        task3 = {}
        task2['through'] = {}
        task3['buffer'] = {}
        print(eee)
    while True:
        if tasks['start']==True:
            time.sleep(60)
            lock.acquire()
            tmp_count1 = tasks['count']
            tmp_bucount = tasks['buffercount']
            tmp_nextcount = len(tasks['next'])
            save_config(tasks,'system_info.json')
            tmp_buffer = tasks["buffer"]
            lock.release()
            print('saved configs')
            try:
                tmp_time = time.time()
                tmp_throughput = task2['through']
                tmp_throughput[tmp_time] = {'count': tmp_count1, 'buf': tmp_bucount, 'next': tmp_nextcount}
                task2['through'] = tmp_throughput
                tmp_buffer_cond = task3['buffer']
                tmp_buffer_cond[tmp_time] = tmp_buffer
                task3['buffer'] = tmp_buffer_cond
                save_config(task2,'through.json')
                save_config(task3,'buffer.json')
            except Exception as eeee:
                print(eeee)
            time.sleep(60)
        else:
            break

def save_job_change_layout(job_name,ps_n,worker_n,training_step,mode=0):
    save_job_path = '/data/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    job_config = load_config(save_job_path)
    save_change_path = '/data/tfdata/k8snfs/%s/%s_pw.json' % (job_name, job_name)
    try:
        job_res_config = load_config(save_change_path)
    except Exception as e:
        job_res_config = {}
        job_res_config['changen'] = {}
        save_config(job_res_config,save_change_path)
        job_res_config = load_config(save_change_path)
    # 'ps_replicas': job.ps_replicas,'worker_replicas': job.worker_replicas
    timenow = time.time()
    tmp_changen = job_res_config['changen']
    tmp_changen[timenow] = {'psbefore': job_config['ps_replicas'],'wbefore': job_config['worker_replicas'],'stepbefore': job_config['training_step'],'psnow':ps_n,'wnow':worker_n,'stepnow': training_step}
    if 'retry' not in job_config:
        job_config['retry'] = 0
    if mode != 0:
        job_config['retry'] = job_config['retry']+1
    job_config['ps_replicas'] = ps_n
    job_config['worker_replicas'] = worker_n
    job_config['training_step'] = training_step
    job_res_config['changen'] = tmp_changen
    save_config(job_res_config,save_change_path)
    save_config(job_config, save_job_path)

def save_job_change_resource(job_name,batch_before,batch_now,part):
    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    save_change_path = '/data/tfdata/k8snfs/%s/%s_change.json' % (job_name,job_name)
    change_dir = {}
    try:
        change_dir = load_config(save_change_path)
    except Exception as eek:
        change_dir['changer'] = {}
        change_dir['part'] = part
        change_dir['batch'] = batch_before
        save_config(change_dir,save_change_path)
    # keyy = list(job_change_config.keys())
    # if 'changer' not in keyy:
    #     job_res_config['changer'] = {}
    tmp_changer = change_dir['changer']
    timenow = time.time()
    tmp_changer[timenow] = {'batch_before': change_dir['batch'],'batch_now': batch_now}
    change_dir['batch'] = batch_now
    change_dir['part'] = part
    change_dir['changer'] = tmp_changer
    job_res_config['part'] = part
    job_res_config['batch_res'] = batch_now
    job_res_config['real_batch'] = int(batch_now // part)
    save_config(job_res_config,save_res_path)

    save_config(change_dir, save_change_path)


def read_step_base(job_name):
    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    key = job_res_config.keys()
    key_list = list(key)
    if 'step_base' not in key_list:
        job_res_config['step_base'] = 0
    step_base = job_res_config['step_base']
    return int(step_base)

def write_step_base(job_name,step_base):
    save_res_path = '/data/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    job_res_config['step_base'] = step_base
    save_config(job_res_config,save_res_path)
    print("save step base successfully!!!")




    # job_name_list = job_name.split('-')
    # job = VGGTask()





if __name__ == '__main__':
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    est_gpu = joblib.load('est_gpu.pkl')
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
    tasks['through'] = {}
    tasks['start'] = True

    url = 'https://172.16.190.97:6443/apis/metrics.k8s.io/v1beta1/nodes'
    args = parse()
    client = influxdb.InfluxDBClient('172.16.190.97', port=8086, username='admin', password='admin',
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
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjob/job/'+ns+'.yaml'
                        os.system(command)
                        deletehelp2(ns, v1)
                        # v1.delete_namespace(ns)
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
                        finishes = tasks['finish']
                        finishes.append(ns)
                        tasks['finish'] = finishes
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