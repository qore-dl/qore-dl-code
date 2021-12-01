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
POP_SIZE = 8
N_GENERATIONS = 4
sleep_last_length = (70/3)*3
pop_total = []
GPU_EST = joblib.load("est_gpu.pkl")
'''
修改：动态调整策略，发布频率，监控代码迁移,资源配置
'''

rfr2 = joblib.load('rfr_batch.pkl')
def load_config(config_file):
    f = open(config_file,encoding='utf-8')
    res = f.read()
    config_content = json.loads(res)
    f.close()
    return config_content
def reload_jobs(job_name,task_id):
    save_job_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (job_name, job_name)
    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job_name, job_name)
    save_batch_path = '/data/tfdata/k8snfs/raw/%s/%s_change.json' % (job_name,job_name)

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
    if task_id != -1 and task_id != -2 and task_id != -3:
        params_dic['task_id'] = task_id
        params_dic['rtimes'] = task_id
    if job_config['template_id'] == 1:
        job_reload = VGGTask(**params_dic)
        job_reload.measure = "VGG %d" % job_reload.task_id
    elif job_config['template_id'] == 2:
        job_reload = RESTask(**params_dic)
        job_reload.measure = "RES %d" % job_reload.task_id
    job_reload.cpu_allocate = job_res_config['cpu_source']
    job_reload.memory_allocate = job_res_config['mem_source']
    job_reload.deadline = job_res_config['deadline']
    if task_id == -2:
        job_reload.starttime = job_res_config['start_time2']
    elif task_id == -3:
        job_reload.starttime = job_res_config['start_time3']
    else:
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
    job_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job_name, job_name)
    job_config_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (job_name, job_name)
    job_change_path = '/data/tfdata/k8snfs/raw/%s/%s_change.json' % (job_name, job_name)
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

# def make_new_pop(inpop):

def catch_task_gpu(job_name,k8s_monitor_x):
    using_job = reload_jobs(job_name,-3)
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

def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/data/tfdata/nodedata', help='save path')
    parser.add_argument('--database',default="NODEMESSAGE",help="save database")
    parser.add_argument('--derivation',default=10,help='sampling rate')
    parser.add_argument('--measurement',default="NODEMESSAGE",help="save measurement")

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
            job = reload_jobs(job_name,-3)
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
        print(job.ps_replicas)
        print(job.worker_replicas)
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
                fp = open('/data/tfdata/k8snfs/raw/' + job_name + '/layout.json', 'w', encoding='utf-8')
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
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config_keys = list(res_job_config.keys())
                    if 'endtimeraw' not in res_job_config_keys:
                        res_job_config['endtimeraw'] = time.time() - 10
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
                        exit_path = '/data/tfdata/k8snfs/raw/%s/exit_reason.json' % ns
                        exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                        fw_exit = open(exit_path, 'w', encoding='utf-8')
                        fw_exit.write(exit_json)
                        fw_exit.close()
                    except Exception as e:
                        print(e)
                    time.sleep(3)
                    lock.acquire()
                    command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/' + job.name + '.yaml'
                    os.system(command)
                    try:
                        deletehelp2(job.name, v1)
                    except Exception as we0:
                        print(we0)
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
                    if 'Failed' in pod_status:
                        fails = tasks['fail']
                        fails.append(job.name)
                        tasks['fail'] = fails
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
                    fp = open('/data/tfdata/k8snfs/raw/' + job_name + '/layout.json', 'w', encoding='utf-8')
                    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    fp.write(dicc_json)
                    fp.close()
            save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
            save_batch_path =  '/data/tfdata/k8snfs/raw/%s/%s_change.json' % (job.name, job.name)
            res_config = load_config(save_res_path)
            batch_config = load_config(save_batch_path)
            keys_res = res_config.keys()
            if 'reloadtime' not in keys_res:
                res_config['reloadtime'] = []
            # 'cpu_high': cpu_base, 'memory_base': mem_base
            if (job.worker_replicas > 0 and job.ps_replicas > 0):
                if count2 >= 5:
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])*int(result_items[0]['worker'])
                    print(aim_step)
                    save_job_change_layout(job.name, 1, 1, aim_step, mode=1)
                    lock.acquire()
                    command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/' + job.name + '.yaml'
                    os.system(command)
                    try:
                        deletehelp2(job.name, v1)
                    except Exception as we0:
                        print(we0)
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
                    time.sleep(15)
                    jieshu = True
                    print("Exception exit! Pending Problem!")
                    return
                else:
                    count2 +=1
                    time.sleep(21.5)
        elif run_result_dict['Running'] == 1:
            save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
                aim_step = math.ceil(int(result_items[0]['training_step'])*int(result_items[0]['worker'])/(job.worker_replicas+1))
                print(aim_step)
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
                time.sleep(21.5)
        elif not run_result_dict:
            ceshi_tmp_ns = tasks['ns']
            if job.name not in ceshi_tmp_ns:
                if count111 <= 4:
                    count111+=1
                    time.sleep(19)
                else:
                    return
            if count >= 8:
                jieshu = True
                print("Exception exit! Creating Problem!")
                save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
            time.sleep(19)
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
            save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
                    fp = open('/data/tfdata/k8snfs/raw/' + job_name + '/layout.json', 'w', encoding='utf-8')
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
                if count000 <= 3:
                    time.sleep(15.5)
                    count000+=1
                else:
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config_keys = list(res_job_config.keys())
                    if 'endtimeraw' not in res_job_config_keys:
                        res_job_config['endtimeraw'] = time.time() - 10
                    save_config(res_job_config, save_res_path)
                    time.sleep(3)
                    if (job.name not in tmp_retrys) and not tasks['modulate']:
                        try:
                            exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                                           v1.list_namespaced_pod(job.name).items]
                            print(exit_reason)
                            exit_ict = {'reasons': exit_reason}
                            exit_path = '/data/tfdata/k8snfs/raw/%s/exit_reason.json' % ns
                            exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                            fw_exit = open(exit_path, 'w', encoding='utf-8')
                            fw_exit.write(exit_json)
                            fw_exit.close()
                        except Exception as e:
                            print(e)
                        time.sleep(5)

                        lock.acquire()
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/' + job.name + '.yaml'
                        os.system(command)
                        print("delete this job %s!!!" % job.name)
                        try:
                            deletehelp2(job.name, v1)
                        except Exception as we0:
                            print(we0)
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
                        if 'Failed' in pod_status2:
                            fails = tasks['fail']
                            fails.append(job.name)
                            tasks['fail'] = fails
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
                        fp = open('/data/tfdata/k8snfs/raw/' + job_name + '/layout.json', 'w', encoding='utf-8')
                        # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                        dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                        fp.write(dicc_json)
                        fp.close()
                save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
                res_config = load_config(save_res_path)
                keys_res = res_config.keys()
                if 'reloadtime' not in keys_res:
                    res_config['reloadtime'] = []
               
                if (job.worker_replicas > 0 and job.ps_replicas > 0):
                    if count22 >= 5:
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])*int(result_items[0]['worker'])
                        tmp_replicas = job.worker_replicas
                        # aim_step = aim_step * tmp_replicas
                        print(aim_step)
                        #save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas - 1, aim_step, mode=1)
                        save_job_change_layout(job.name, 1, 1, aim_step, mode=1)
                        lock.acquire()
                        tmp_retry_job = tasks['retry']
                        tmp_retry_job.append(job.name)
                        tasks['retry'] = tmp_retry_job
                        time1 = time.time()
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/' + job.name + '.yaml'
                        os.system(command)
                        try:
                            deletehelp2(job.name, v1)
                        except Exception as we0:
                            print(we0)


                elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                    if count22 > 8:
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])*int(result_items[0]['worker'])
                        print(aim_step)
                        save_job_change_layout(job.name, 1, 1, aim_step, mode=1)

                        lock.acquire()
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/' + job.name + '.yaml'
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
                        time.sleep(15)
                        jieshu = True
                        print("Exception exit! Pending Problem!")
                        count22 += 1
                        return
                    else:
                        count22 += 1
                        time.sleep(19)
            elif run_result_dict2['Running'] == 1:
                if countt00 < 3:
                    countt00 += 1
                    time.sleep(15)
                else:
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
                    aim_step = math.ceil(int(result_items[0]['training_step'])*int(result_items[0]['worker'])/(job.worker_replicas+1))
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
                    time.sleep(19.5)
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
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config['errtime'] = time.time() - 5
                    save_config(res_job_config, save_res_path)
                    lock.acquire()
                    command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/' + job.name + '.yaml'
                    os.system(command)
                    try:
                        deletehelp2(job.name,v1)
                    except Exception as we0:
                        print(we0)
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
                time.sleep(15)

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
    train_dir = os.path.join('/data/tfdata/k8snfs/raw/', name)
    print(train_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    return train_dir

def write_step_meg(job_name):
    job = reload_jobs(job_name,-3)
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
        save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job0, job0)
        res_config = load_config(save_res_path)
        batch_res = res_config['batch_res']
        flops_res = res_config['flops_res']
        params_res = res_config['params_res']
        real_batch = res_config['real_batch']
        pool.apply_async(catch_node_step_msg,args=(jobs,job0,tasks,lock,batch_res,flops_res,params_res,real_batch,-1))
    global_count = 1


    while True:
        print("Global Count is :%d" % global_count)
        if tasks['start']==False:
            break
        tmp_aim_set = tasks['aim']
        tmp_next_set = tasks['next']
        tmp_ns_set = tasks['ns']
        if not tmp_aim_set and not tmp_next_set and tasks['buffercount'] <= 0:
            if not tmp_ns_set:
                break
        if global_count > 2 and global_count%10 != 0:
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
                job = reload_jobs(job_name, -3)
                print("%s in next reload!" % job_name)
                node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                # gpu_node_index,k8s_monitor,index_node_gpu = job_basic.select_k8s_gpu()
                catch_worker = 0
                catch_ps = 0
                catch_worker2 = 0
                node_keys = cpu_nodes.keys()
                node_index_gpu, k8s_monitor, index_node_gpu = job_basic.select_k8s_gpu()
                catch_worker2 = 0
                node_using = list(node_index_gpu.keys())
                total_ava = 0
                top_ava = 0
                for i in range(len(index_node_gpu)):
                    total_ava += k8s_monitor[index_node_gpu[i]]['avail']
                    if i <= 2:
                        top_ava += k8s_monitor[index_node_gpu[i]]['avail']

                catch_worker2 = total_ava
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
                    if catch_ps >= job.ps_replicas and catch_worker >= job.worker_replicas:
                        break
                # if catch_worker2 <= catch_worker:
                #     catch_worker = catch_worker2
                catch_worker = np.min([catch_worker2,catch_worker])
                catch_worker = catch_worker2
                print("In next catch ps: %d,worker:%d" % (catch_ps, catch_worker))
                if catch_ps >= job.ps_replicas and catch_worker > job.worker_replicas:
                    # lock.acquire()
                    job.update_step()
                    print("in next update step success!!")
                    write_step_meg(job.name)
                    job.update_batch()
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
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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

                    if catch_tmp_ps_re_job_name >=2 and tmp_buffer_count0 < max_buffer_size:
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
                        tasks['next'] = tmp_next
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
                    selected_job_name = worker_buffer[0]
                    print(selected_job_name)
                    ceshi_name = worker_buffer.pop(0)
                    print(ceshi_name)
                    # worker_buffer = max_free_heap.items
                    print(worker_buffer)
                    tasks['buffer'] = worker_buffer[:]
                    tmp_buffer_count = tmp_buffer_count - 1
                    tasks['buffercount'] = tmp_buffer_count
                else:
                    selected_job_name = worker_buffer[0]
                    print(selected_job_name)
                    ceshi_name = worker_buffer.pop(0)
                    print(ceshi_name)
                    # worker_buffer = max_free_heap.items
                    print(worker_buffer)
                    tasks['buffer'] = worker_buffer[:]
                    tmp_buffer_count = tmp_buffer_count - 1
                    tasks['buffercount'] = tmp_buffer_count
                job = reload_jobs(selected_job_name, -3)
                selected_res_config_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (selected_job_name,selected_job_name)
                selected_res_config2 = load_config(selected_res_config_path)
                tmp_ps_replicas = job.ps_replicas
                tmp_worker_replicas = job.worker_replicas
                pre_list = job.measure.split(" ")
                measure_s = pre_list[0] + 'S' + pre_list[-1]
                measure_t = pre_list[0] + 'T' + pre_list[-1]
                measure_b = pre_list[0]+'B'+pre_list[-1]

                node_index_gpu, k8s_monitor, index_node_gpu = job_basic.select_k8s_gpu()
                catch_worker2 = 0
                node_using = list(node_index_gpu.keys())
                total_ava = 0
                top_ava = 0
                for i in range(len(index_node_gpu)):
                    total_ava += k8s_monitor[index_node_gpu[i]]['avail']
                    if i <= 2:
                        top_ava += k8s_monitor[index_node_gpu[i]]['avail']

                catch_worker2 = total_ava

                # tmp_ps_replicas = job.ps_replicas
                # tmp_worker_replicas = job.worker_replicas

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
                    if catch_ps >= job.ps_replicas:
                        reach_ps = True
                    if catch_worker >= catch_worker2:
                        reach_worker = True
                    if catch_ps >= job.ps_replicas and catch_worker >= catch_worker2:
                        break
                print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                # catch_ps = min([catch_ps, catch_tmp_ps_re])
                catch_worker = min([catch_worker, catch_worker2])
                catch_worker = catch_worker2
                if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                    tmp_ps = job.ps_replicas
                    tmp_worker = job.worker_replicas
                    if catch_ps > 0 and catch_worker > 0:
                        if catch_worker > job.worker_replicas:
                            catch_worker = job.worker_replicas
                        if catch_ps > job.ps_replicas:
                            catch_ps = job.ps_replicas
                        job.ps_replicas = catch_ps
                        job.worker_replicas = catch_worker
                        job.training_step = math.ceil(job.training_step * tmp_worker / job.worker_replicas)
                        save_job_change_layout(job.name, catch_ps, catch_worker, job.training_step)
                        job.update_step()
                        job.update_batch()
                        write_step_meg(job.name)
                        lock.acquire()

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
                        lock.release()

                        save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
                        res_config = load_config(save_res_path)
                        batch_res = job.batch_size
                        flops_res = res_config['flops_res']
                        params_res = res_config['params_res']
                        real_batch = job.real_batch

                        pool.apply_async(catch_node_step_msg,
                                         args=(
                                             jobs, job.name, tasks, lock, batch_res, flops_res, params_res, real_batch,
                                             1))
                    else:
                        # Selection 2!!!
                        # xuanze = random.randint(1,3)
                        # if xuanze == 1:
                        #     job.ps_replicas = 1
                        #     job.worker_replicas = 1
                        #     job.training_step = math.ceil(tmp_worker_replicas*job.training_step)
                        #     save_job_change_layout(job.name, 1, 1, training_step=job.training_step)
                        #     tasks['next'].append(job.name)
                        lock.acquire()
                        tmp_next = tasks['next']
                        tmp_next.append(job.name)
                        tmp_next_time_config = tasks['nexttimes']
                        tmp_next_time_config[job.name] = 0
                        tasks['nexttimes'] = tmp_next_time_config
                        tasks['next'] = tmp_next
                        lock.release()
                else:
                    # job.training_step = math.ceil(job.training_step*tmp_worker_replicas / job.worker_replicas)
                    # save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, job.training_step)
                    job.update_step()
                    job.update_batch()
                    write_step_meg(job.name)
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
                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    batch_res = res_config['batch_res']
                    flops_res = res_config['flops_res']
                    params_res = res_config['params_res']
                    real_batch = res_config['real_batch']
                    lock.release()
                    pool.apply_async(catch_node_step_msg,
                                     args=(
                                         jobs, job.name, tasks, lock, batch_res, flops_res, params_res,real_batch, 1))

            global_count+=1
            time.sleep(sleep_last_length)
        if global_count % 10 == 0 or global_count<=2:
            print('start to submit a job!!')
            tmp_jobs0 = tasks['aim']
            if not tmp_jobs0:
                global_count += 1
                continue
            for _ in range(10):
                lock.acquire()
                counts = tasks['count']
                bufer_count = tasks['buffercount']
                lock.release()
                if ((counts >= tasks['size']) and (bufer_count >= max_buffer_size)):
                    time.sleep(float(random.randint(7,9)))
                    pass
                else:
                    print('select a job!!')
                    time.sleep(40)
                    # template_id = random.randint(1,2)
                    if tasks['aim']:
                        tmp_jobs = tasks['aim']
                        aim_job0 = tmp_jobs[0]
                        tmp_jobs.pop(0)
                        tasks['aim'] = tmp_jobs
                        aim_job = reload_jobs(aim_job0, -1)
                        aim_job.retry = aim_job.retry + 1
                        save_job_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (aim_job.name, aim_job.name)
                        aim_job_config = load_config(save_job_path)
                        aim_job_config['retry'] = aim_job.retry
                        save_config(aim_job_config, save_job_path)


                        pre_list = aim_job.measure.split(" ")
                        measure_s = pre_list[0] + 'S' + pre_list[-1]
                        measure_t = pre_list[0] + 'T' + pre_list[-1]
                        measure_write = pre_list[0] + 'W' + pre_list[-1]
                        measure_up = pre_list[0] + 'U' + pre_list[-1]
                        measure_b = pre_list[0]+'B'+pre_list[-1]

                        influx_client = influxdb.InfluxDBClient(host='172.16.190.97', port=8086, username='admin',
                                                                password='admin',
                                                                database="PREDICT")
                        batch_client = influxdb.InfluxDBClient(host='172.16.190.97', port=8086, username='admin',
                                                               password='admin', database="BATCH")
                        result = influx_client.query("select * from " + measure_t + " order by asc limit 1")
                        batch_result = batch_client.query("select * from " + measure_b + " order by asc limit 1")
                        key = result.keys()
                        print(key)
                        result_inter = result[key[0]]
                        result_items = list(result_inter)
                        print(result_items)
                        key2 = list(batch_result.keys())
                        result_inter2 = batch_result[key2[0]]
                        result_items2 = list(result_inter2)
                        batch_size0 = int(result_items2[0]['base'])
                        real_batch0 = int(result_items2[0]['batch'])
                        part0 = int(result_items2[0]['part'])
                        trains_step = int(result_items[0]['training_step'])
                        tmp_worker_replicas = int(result_items[0]['worker'])
                        tmp_ps_replicas = int(result_items[0]['ps'])
                        save_job_change_resource(aim_job.name,aim_job.batch_size,batch_size0,part0)
                        aim_job.set_batch(batch_size0,part2=1)
                        aim_job.training_step = math.ceil(trains_step*tmp_worker_replicas/part0)


                        worker_need_total = aim_job.worker_replicas
                        print(worker_need_total)
                        print(aim_job.part)

                        allow_read = {}
                        allow_read['OK'] = True
                        allow_read['retry'] = aim_job.retry
                        # allow_p = check_path(measure_t)
                        allow_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (aim_job.name, measure_t)
                        save_config(allow_read, allow_path)
                        lock.acquire()
                        tasks['base'] = aim_job.name
                        lock.release()
                    else:
                        break
                    lock.acquire()
                    tmp_tasks_count = tasks['count']
                    tmp_tasks_buffercount =  tasks['buffercount']
                    lock.release()
                    if tmp_tasks_count < tasks['size'] or tasks['buffercount'] < max_buffer_size:
                        # loss_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        # loss_client.connect(ADDR)
                        client_pre = influxdb.InfluxDBClient(host=aim_job.dbhost, port=8086, username='admin',
                                                             password='admin',
                                                             database="PREDICT")
                        save_config_dir = task_submit.check_path(aim_job.name)
                        save_job_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (aim_job.name, aim_job.name)
                        save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (aim_job.name, aim_job.name)
                        aim_res_config = load_config(save_res_path)
                        aim_job_config = load_config(save_job_path)
                        pre_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        pre_client.connect(ADDR2)
                        pre_client.send(bytes(aim_job.measure, 'utf-8'))
                        pre_list = aim_job.measure.split(" ")
                        # measure_s = pre_list[0] + 'S' + pre_list[-1]
                        measure_t = pre_list[0] + 'T' + pre_list[-1]
                        save_config_dir = task_submit.check_path(aim_job.name)
                        save_job_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (aim_job.name, aim_job.name)

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
                            pre_client.send(bytes(aim_job.measure, 'utf-8'))
                            try_times = try_times + 1

                        if not connected:
                            print("Connected or send message error!")
                            pre_client.close()
                            continue
                        print(msg_from_server_str)
                        print("connected success!")
                        start_time = '%.3f' % time.time()
                        start_time = float(start_time)

                        if aim_job.template_id == 1:
                            dict = {'batch_size': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                                    'channel3': aim_job.channel3,
                                    'channel4': aim_job.channel4,
                                    'channel5': aim_job.channel5, 'num_layer1': aim_job.num_layer1, 'num_layer2': aim_job.num_layer2,
                                    'num_layer3': aim_job.num_layer3, 'num_layer4': aim_job.num_layer4, 'num_layer5': aim_job.num_layer5, 'kernel': aim_job.kernel,
                                    'unit1': aim_job.unit1, 'unit2': aim_job.unit2}
                        else:
                            dict = {'batch_size': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                                    'channel3': aim_job.channel3,
                                    'channel4': aim_job.channel4,
                                    'block1': aim_job.block1, 'block2': aim_job.block2,
                                    'block3': aim_job.block3, 'block4': aim_job.block4, 'bot': aim_job.bot, 'rate1': aim_job.rate1, 'rate2': aim_job.rate2,
                                    'rate3': aim_job.rate3, 'rate4': aim_job.rate4,
                                    'k0': aim_job.k0, 'k11': aim_job.k11, 'k12': aim_job.k12, 'k21': aim_job.k21, 'k22': aim_job.k22, 'k31': aim_job.k31, 'k32': aim_job.k32,
                                    'k41': aim_job.k41, 'k42': aim_job.k42}

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
                            suiji = random.random()
                            part00 = part
                            if suiji < 0.33:
                                # suiji2 = random.random()
                                # if suiji2 <=0.4:
                                #     pianyi = random.randint(1,part)
                                #     part = int(part - pianyi)
                                pianyi = random.randint(1,2)
                                part = int(part+pianyi)
                            suiji = random.random()
                            if suiji < 0.1:
                                pianyi = random.randint(1,part00)
                                part = int(part-pianyi)

                            if part <= 0:
                                part = 1
                            if part >= 14:
                                part = 14
                            res_to_server = '1'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                        else:
                            res_to_server = '0'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                            print("send response success!!")
                            time.sleep(6)
                            pre_client.close()
                            print("some time later to try again!!")
                            time.sleep(30)
                            continue
                        pre_client.close()
                        tmp_reload = tasks['reload']
                        tmp_batch = aim_job.batch_size
                        aim_job.set_batch(aim_job.batch_size,part2=part)
                        save_job_change_resource(aim_job.name,tmp_batch,aim_job.batch_size,part)

                        aim_job_config['part'] = part
                        tmp_ree = aim_job.worker_replicas
                        aim_job.worker_replicas = random.randint(1,3)
                        aim_job.ps_replicas = random.randint(1,3)
                        aim_job.worker_replicas = aim_job.worker_replicas*part
                        aim_job_config['worker_replicas'] = aim_job.worker_replicas
                        aim_job.training_step = math.ceil(aim_job.training_step*aim_job.part/aim_job.worker_replicas)
                        tmp_start_time_before = aim_job.starttime
                        aim_job.set_deadline(aim_job.deadline,start_time)
                        save_job_change_layout(aim_job.name,aim_job.ps_replicas,aim_job.worker_replicas,aim_job.training_step)
                        save_config(aim_job_config, save_job_path)
                        allow_read = {}
                        allow_read['OK'] = True
                        allow_read['retry'] = 0
                        allow_p = check_path(measure_t)
                        allow_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (aim_job.name, measure_t)
                        save_config(allow_read, allow_path)
                        mini_batch = predict_min_first(rfr=rfr,batch=batch_res,flops=flops_res,params=params_res,template=aim_job.template_id)
                        mini_batch = float(mini_batch)

                        job_res_config = {'deadline': aim_job.deadline, 'start_time':tmp_start_time_before,'start_time3': aim_job.starttime,'cpu_source': aim_job.cpu_allocate,
                                          'real_batch': aim_job.real_batch, 'batch_res': aim_job.batch_size, 'mem_source': aim_job.memory_allocate, 'cpu_high': aim_job.cpu_allocate,
                        'memory_base': aim_job.memory_allocate,
                                          'flops_res': flops_res, 'params_res': params_res, 'step_base': 0,'part':part,
                                          'reloadtime': []}
                        save_config_dir = task_submit.check_path(aim_job.name)
                        save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (aim_job.name, aim_job.name)
                        # save_config(job_config, save_job_path)
                        save_config(job_res_config, save_res_path)
                        save_job_change_resource(aim_job.name,aim_job.batch_size,aim_job.batch_size,aim_job.part)
                        # now_create = now_create+1
                        # np.save('nowcreate.npy', now_create)


                        if tasks['count'] < tasks['size'] and tasks['buffercount'] == 0:

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

                            catch_worker2 = total_ava

                            tmp_ps_replicas = aim_job.ps_replicas
                            tmp_worker_replicas = aim_job.worker_replicas

                            mem_need = aim_job.total_mem * total_mem_use + aim_job.worker_replicas * aim_job.memory_allocate + 2048 * aim_job.ps_replicas
                            cpu_need = aim_job.total_cpu * total_cpu_use + aim_job.worker_replicas * aim_job.cpu_allocate + 750 * aim_job.ps_replicas
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
                                can_use_cpu = aim_job.node_cpu[key] * (1 - cpu_nodes[key])
                                can_use_mem = aim_job.node_memory[key] * (1 - memory_nodes[key])
                                first_try = True
                                endcpu = False
                                endmem = False
                                while (not endcpu) or (not endmem):
                                    if first_try:
                                        if can_use_cpu - 2048> 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 2048
                                        else:
                                            if can_use_cpu - aim_job.cpu_allocate > 0 and not reach_worker:
                                                catch_worker_c += 1
                                                can_use_cpu = can_use_cpu - aim_job.cpu_allocate
                                        if can_use_mem - 2048 > 0 and not reach_ps:
                                            catch_ps_m += 1
                                            can_use_mem = can_use_mem - 2048
                                        else:
                                            if can_use_mem - aim_job.memory_allocate > 0 and not reach_worker:
                                                catch_worker_m += 1
                                                can_use_mem = can_use_mem - aim_job.memory_allocate
                                        first_try = False
                                    else:
                                        if can_use_cpu - aim_job.cpu_allocate > 0 and not reach_worker:
                                            catch_worker_c += 1
                                            can_use_cpu = can_use_cpu - aim_job.cpu_allocate
                                        else:
                                            if can_use_cpu - 2048 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 2048
                                            else:
                                                endcpu = True

                                        if can_use_mem - aim_job.memory_allocate > 0 and not reach_worker:
                                            catch_worker_m += 1
                                            can_use_mem = can_use_mem - aim_job.memory_allocate
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
                                if catch_ps >= aim_job.ps_replicas:
                                    reach_ps = True
                                if catch_worker >= aim_job.worker_replicas:
                                    reach_worker = True
                                if catch_ps >= aim_job.ps_replicas and catch_worker >= aim_job.worker_replicas:
                                    break

                            # catch_ps = min([catch_ps,catch_tmp_ps_re])
                            catch_worker = min([catch_worker,catch_worker2])
                            catch_worker = catch_worker2
                            print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                            if catch_ps < aim_job.ps_replicas or catch_worker < aim_job.worker_replicas:
                                tmp_ps = aim_job.ps_replicas
                                tmp_worker = aim_job.worker_replicas
                                if catch_ps > 0 and catch_worker > 0:
                                    if catch_worker > aim_job.worker_replicas:
                                        catch_worker = aim_job.worker_replicas
                                    if catch_ps > aim_job.ps_replicas:
                                        catch_ps = aim_job.ps_replicas
                                    aim_job.ps_replicas = catch_ps
                                    aim_job.worker_replicas = catch_worker
                                    aim_job.training_step = math.ceil(aim_job.training_step * tmp_worker/ aim_job.worker_replicas)
                                    save_job_change_layout(aim_job.name, catch_ps, catch_worker, aim_job.training_step)
                                    aim_job.update_step()
                                    aim_job.update_batch()
                                    write_step_meg(aim_job.name)
                                    submit_time_now = time.time()
                                    tongji_waiting_queue(aim_job.name, submit_time_now)
                                    lock.acquire()
                                    aim_job.create_tf()
                                    ns_tmp = tasks['ns']
                                    ns_tmp.append(aim_job.name)
                                    tasks['ns'] = ns_tmp
                                    # job_tmp = tasks['job']
                                    # job_tmp[job.name] = job
                                    # tasks['job'] = job_tmp
                                    is_layout = tasks['nslayout']
                                    is_layout[aim_job.name] = False
                                    tasks['nslayout'] = is_layout
                                    jobs.append(aim_job.name)
                                    tasks['count'] += 1
                                    lock.release()

                                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (aim_job.name, aim_job.name)
                                  
                                    res_config = load_config(save_res_path)
                                    batch_res = res_config['batch_res']
                                    flops_res = res_config['flops_res']
                                    params_res = res_config['params_res']
                                    real_batch = res_config['real_batch']

                                    pool.apply_async(catch_node_step_msg,
                                                     args=(
                                                     jobs, aim_job.name, tasks, lock, batch_res, flops_res, params_res,real_batch, 1))
                                else:
                                    # xuanze = random.randint(1,3)
                                    # # selection 1!!!!
                                    # if xuanze == 1:
                                    #     aim_job.ps_replicas = 1
                                    #     aim_job.worker_replicas = 1
                                    #     aim_job.training_step = aim_job.training_step * tmp_worker
                                    #     save_job_change_layout(aim_job.name, 1, 1, aim_job.training_step)
                                    lock.acquire()
                                    tmp_next = tasks['next']
                                    tmp_next.append(aim_job.name)
                                    tmp_next_time_config = tasks['nexttimes']
                                    tmp_next_time_config[aim_job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config
                                    tasks['next'] = tmp_next
                                    lock.release()
                                    
                            else:
                                # aim_job.training_step = math.ceil(aim_job.training_step * tmp_worker_replicas / aim_job.worker_replicas)
                                # save_job_change_layout(aim_job.name, aim_job.ps_replicas, aim_job.worker_replicas,aim_job.training_step)
                                aim_job.update_step()
                                aim_job.update_batch()
                                write_step_meg(aim_job.name)
                                submit_time_now = time.time()
                                tongji_waiting_queue(aim_job.name, submit_time_now)
                                lock.acquire()
                                aim_job.create_tf()
                                ns_tmp = tasks['ns']
                                ns_tmp.append(aim_job.name)
                                tasks['ns'] = ns_tmp
                              
                                is_layout = tasks['nslayout']
                                is_layout[aim_job.name] = False
                                tasks['nslayout'] = is_layout
                                jobs.append(aim_job.name)
                                tasks['count'] += 1
                                lock.release()
                                save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (aim_job.name, aim_job.name)
                                
                                res_config = load_config(save_res_path)
                                batch_res = res_config['batch_res']
                                flops_res = res_config['flops_res']
                                params_res = res_config['params_res']
                                real_batch = res_config['real_batch']

                                pool.apply_async(catch_node_step_msg,
                                                 args=(
                                                 jobs, aim_job.name, tasks, lock, batch_res, flops_res, params_res,real_batch,1))

                        elif tasks['count'] >= tasks['size']:
                            worker_buffer = tasks['buffer']
                            worker_buffer.append(aim_job.name)
                            tasks['buffer'] = worker_buffer
                            tmp_buffer_count = tasks['buffercount']
                            tmp_buffer_count = tmp_buffer_count + 1
                            tasks['buffercount'] = tmp_buffer_count

                        else:
                            worker_buffer = tasks['buffer']
                            worker_buffer.append(aim_job.name)
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
                                tmp_buffers = tasks['buffer']
                                selected_job_name = tmp_buffers[0]
                                print(selected_job_name)
                                # worker_buffer = max_free_heap.items
                                print(worker_buffer)
                                ceshi_name = worker_buffer.pop(0)
                                print(ceshi_name)
                                tasks['buffer'] = worker_buffer[:]
                                tmp_buffer_count = tmp_buffer_count - 1
                                tasks['buffercount'] = tmp_buffer_count
                            else:
                                tmp_buffers = tasks['buffer']
                                selected_job_name = tmp_buffers[0]
                                print(selected_job_name)
                                # worker_buffer = max_free_heap.items
                                print(worker_buffer)
                                ceshi_name = worker_buffer.pop(0)
                                print(ceshi_name)
                                tasks['buffer'] = worker_buffer[:]
                                tmp_buffer_count = tmp_buffer_count - 1
                                tasks['buffercount'] = tmp_buffer_count
                            job = reload_jobs(selected_job_name, -3)
                            selected_res_config_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (
                            selected_job_name, selected_job_name)
                            selected_res_config2 = load_config(selected_res_config_path)

                            using_flops = selected_res_config2['flops_res']
                            using_param = selected_res_config2["params_res"]
                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas
                            mini_batch = predict_min_first(rfr=rfr, batch= job.real_batch, flops=using_flops,
                                                           params=using_param,template= job.template_id)
                            mini_batch = float(mini_batch)
                            tmp_rest = job.deadline + job.starttime - time.time()
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

                            catch_worker2 = total_ava

                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas

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
                                if catch_ps >= job.ps_replicas:
                                    reach_ps = True
                                if catch_worker >= job.worker_replicas:
                                    reach_worker = True
                                if catch_ps >= job.ps_replicas and catch_worker >= job.worker_replicas:
                                    break
                            print("catch_ps: %d catch_worker: %d" % (catch_ps, catch_worker))
                            # catch_ps = min([catch_ps, catch_tmp_ps_re])
                            catch_worker = min([catch_worker, catch_worker2])
                            catch_worker = catch_worker2
                            if catch_ps < job.ps_replicas or catch_worker < job.worker_replicas:
                                tmp_ps = job.ps_replicas
                                tmp_worker = job.worker_replicas
                                if catch_ps > 0 and catch_worker > 0:
                                    if catch_worker > job.worker_replicas:
                                        catch_worker = job.worker_replicas
                                    if catch_ps > job.ps_replicas:
                                        catch_ps = job.ps_replicas
                                    job.ps_replicas = catch_ps
                                    job.worker_replicas = catch_worker
                                    job.training_step = math.ceil(
                                        job.training_step * tmp_worker / job.worker_replicas)
                                    save_job_change_layout(job.name, catch_ps, catch_worker, job.training_step)
                                    job.update_step()
                                    job.update_batch()
                                    write_step_meg(job.name)
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
                                    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)

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
                                    # job.ps_replicas = 1
                                    # job.worker_replicas = 1
                                    # job.training_step = job.training_step * tmp_worker
                                    # save_job_change_layout(job.name, 1, 1, job.training_step)
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
                                # job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                                # save_job_change_layout(job.name,job.ps_replicas,job.worker_replicas,job.training_step)
                                job.update_step()
                                job.update_batch()
                                write_step_meg(job.name)
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
                                save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job.name, job.name)
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
    save_job_path = '/data/tfdata/k8snfs/raw/%s/%s.json' % (job_name, job_name)
    job_config = load_config(save_job_path)
    save_change_path = '/data/tfdata/k8snfs/raw/%s/%s_pw.json' % (job_name, job_name)
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
    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    save_change_path = '/data/tfdata/k8snfs/raw/%s/%s_change.json' % (job_name,job_name)
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
    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    key = job_res_config.keys()
    key_list = list(key)
    if 'step_base' not in key_list:
        job_res_config['step_base'] = 0
    step_base = job_res_config['step_base']
    return int(step_base)

def write_step_base(job_name,step_base):
    save_res_path = '/data/tfdata/k8snfs/raw/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    job_res_config['step_base'] = step_base
    save_config(job_res_config,save_res_path)
    print("save step base successfully!!!")

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
    submit_p = multiprocessing.Process(target=Submit_job,args=(tasks,lock,v1,jobs))
    monitor_p = multiprocessing.Process(target=Monitor_job,args=(tasks,lock,v1,jobs))
    jiance_p = multiprocessing.Process(target=jiance, args=(tasks, lock))

    # derivation
    node_p.daemon = True
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
                        command = 'kubectl delete -f /data/tfdata/tfcnn/expjobraw/job/'+ns+'.yaml'
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