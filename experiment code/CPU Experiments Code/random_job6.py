# 1584927559
import task_submit_fix
from task_submit_fix import VGGTask,RESTask,RETask,DENTask,XCETask
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

np.set_printoptions(suppress=True)        #设置print选项的参数
'''
初始配置节点数量实验，对于节点资源分配，因为手动分配会造成错误，我认为统计本方法资源效率即可证明了
本设置为不考虑资源情况，仅考虑完成率的问题
'''
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
LOSSHOST = '192.168.128.5'
LOSSPORT = 12527
DNA_SIZE = 3
XBOUND = [0.765,1.36]    #1.6
XBOUND2 = [0.5,0.95]
YBOUND2 = [0.725,0.95]
YBOUND = [1,1.4]    #1.72
CROSSOVER_RATE = 0.8
CROSS_RATE=0.8
POP_SIZE = 8
N_GENERATIONS = 4
# 205.7142857
sleep_last_length = (78.6/3)
pop_total = []

rfr2 = joblib.load('rfr_batch.pkl')
def load_config(config_file):
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
def reload_jobs_aim(job_name,task_id):
    save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    save_mod_path = '/tfdata/k8snfs/%s/%s_mod.json' % (job_name,job_name)
   # with open(full_flie_name,'r') as yaml_job:
        #job_obj = yaml.load(yaml_job.read())

    job_config = load_config(save_job_path)
    job_res_config = load_config(save_res_path)
    try:
        job_mod_config = load_config(save_mod_path)
    except Exception as ee1:
        print(ee1)
        job_mod_config = {'mod': -1, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                          '3': [], '4': [], '5': [],
                          '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
        save_config(job_mod_config,save_mod_path)
    params_dic = {}
    params_dic['mod'] = job_mod_config['mod']
    keys = job_config.keys()
    for key in keys:
        params_dic[key] = job_config[key]
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
    elif job_config['template_id'] == 3:
        job_reload = RETask(**params_dic)
        job_reload.measure = "RE %d" % job_reload.task_id
    elif job_config['template_id'] == 4:
        job_reload = XCETask(**params_dic)
        job_reload.measure = "XCE %d" % job_reload.task_id
    else:
        job_reload = DENTask(**params_dic)
        job_reload.measure = "DEN %d" % job_reload.task_id
   # job_reload.template = job_obj
    #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,'cpu_source':job.cpu_allocate,
    # 'mem_source':job.memory_allocate,'cpu_high':cpu_base}
    job_reload.cpu_allocate = job_res_config['cpu_source']
    job_reload.memory_allocate = job_res_config['mem_source']
    job_reload.deadline = job_res_config['deadline']
    job_reload.starttime = job_res_config['start_time']

    return job_reload

def reload_jobs(job_name,task_id):
    save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job_name, job_name)
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    save_mod_path = '/tfdata/k8snfs/setbase/%s/%s_mod.json' % (job_name,job_name)
   # with open(full_flie_name,'r') as yaml_job:
        #job_obj = yaml.load(yaml_job.read())

    job_config = load_config(save_job_path)
    job_res_config = load_config(save_res_path)
    try:
        job_mod_config = load_config(save_mod_path)
    except Exception as ee1:
        print(ee1)
        job_mod_config = {'mod': -1, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                          '3': [], '4': [], '5': [],
                          '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
        save_config(job_mod_config,save_mod_path)
    params_dic = {}
    params_dic['mod'] = job_mod_config['mod']
    keys = job_config.keys()
    for key in keys:
        params_dic[key] = job_config[key]
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
    elif job_config['template_id'] == 3:
        job_reload = RETask(**params_dic)
        job_reload.measure = "RE %d" % job_reload.task_id
    elif job_config['template_id'] == 4:
        job_reload = XCETask(**params_dic)
        job_reload.measure = "XCE %d" % job_reload.task_id
    else:
        job_reload = DENTask(**params_dic)
        job_reload.measure = "DEN %d" % job_reload.task_id
   # job_reload.template = job_obj
    #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,'cpu_source':job.cpu_allocate,
    # 'mem_source':job.memory_allocate,'cpu_high':cpu_base}
    job_reload.cpu_allocate = job_res_config['cpu_source']
    job_reload.memory_allocate = job_res_config['mem_source']
    job_reload.deadline = job_res_config['deadline']
    job_reload.starttime = job_res_config['start_time']

    return job_reload

job_basic0 = reload_jobs_aim("res-292-292",-1)
basic_job_cpu = job_basic0.total_cpu
basic_job_mem = job_basic0.total_mem

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
    command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
    try:
        command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
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
    x_pop = pop[:,1::2]#从第1列开始，步进为2
    y_pop = pop[:,::2]#从第0列开始，步进为2
    # #pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)完成解码:二进制码求相应十进制值然后压缩到相应范围内即可完成解码
    x = x_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(XBOUND[-1] - XBOUND[0])+XBOUND[0]
    y = y_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(YBOUND[-1] - YBOUND[0])+YBOUND[0]
    # print("a translateDNA process finished")
    return x,y

def existss(pop_total,gene,init=1):
    if init == 0:
        gene10 = gene.dot(2 ** np.arange(2 * DNA_SIZE)[::-1])
        pop_total = list(gene10)
        return pop_total
    else:
        gene10 = int(gene.dot(2 ** np.arange(2 * DNA_SIZE)[::-1]))
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
    # print("a translateDNA2 process finished")
    return x, y

def predict_min_map1(job_exp):
    job_name = job_exp['name']
    cpu = job_exp['cpu']
    mem = job_exp['mem']
    ps = job_exp['ps']
    worker = job_exp['worker']
    global rfr2
    global basic_job_cpu
    global basic_job_mem
    job_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    job_config = load_config(job_path)
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
    pred = (0 - iteration) * (
                (ps * 720 + worker * cpu) / basic_job_cpu + (ps * 2048 + worker * mem) / basic_job_mem)
    return pred

def predict_min_map3(job_exp):
    job_name = job_exp['name']
    cpu = job_exp['cpu']
    mem = job_exp['mem']
    global rfr2
    global basic_job_cpu
    global basic_job_mem
    job_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    job_config = load_config(job_path)

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
    job_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    job_config = load_config(job_path)
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
    return score

def  get_fitness1(aim,pop,cpu_now,mem_now,cpu_base,mem_base,worker,ps):
    global XBOUND,YBOUND
    cpu_alpha,mem_alpha = translateDNA(pop)
    # print("catch cpu_alpha:")
    # print(cpu_alpha)
    # cpu_pre = cpu_now*cpu_alpha
    cpu_pre = cpu_now*cpu_alpha
    # print(type(cpu_pre))
    # mem_pre = mem_base*mem_alpha
    cpu_pre_limit = math.ceil(XBOUND[-1]*1.478*cpu_base)
    mem_pre = mem_now*mem_alpha
    mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * mem_base)
    for i in range(len(cpu_pre)):
        if cpu_pre[i] > cpu_pre_limit:
            cpu_pre[i] = cpu_pre_limit
        if mem_pre[i] > mem_pre_limit:
            mem_pre[i] = mem_pre_limit

    job_exp_list = []
    # job_name = job_exp['name']
    # cpu = job_exp['cpu']
    # mem = job_exp['mem']

    for i in range(len(cpu_pre)):
        # if cpu_pre[i] > cpu_pre_limit and mem_pre[i] <= mem_pre_limit:
        job_exp_list.append({'name':aim,'cpu':cpu_pre[i],'mem':mem_pre[i],'ps':ps,'worker':worker})
    # pred = []
    pool_fit = multiprocessing.Pool(6)
    # print("start to a get_fitness1 map")
    pred = pool_fit.map(predict_min_map1,job_exp_list)
    # print("end a get_fitness1 map")
    pool_fit.close()
    pool_fit.join()
    pred = np.array(pred)
    # print("a get_fitness1 procedure end!")
    # pred = mini_batch
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

def get_fitness3(aim,pop,cpu_now,mem_now,cpu_base,mem_base):
    #任务完成不了了，所以直接看minbatch可以减少多少而不是资源利用
    global XBOUND, YBOUND
    cpu_alpha, mem_alpha = translateDNA(pop)
    cpu_pre = cpu_now * cpu_alpha
    # print(type(cpu_pre))
    # mem_pre = mem_base*mem_alpha
    cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * cpu_base)
    mem_pre = mem_now * mem_alpha
    mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * mem_base)

    for i in range(len(cpu_pre)):
        if cpu_pre[i] > cpu_pre_limit:
            cpu_pre[i] = cpu_pre_limit
        if mem_pre[i] > mem_pre_limit:
            mem_pre[i] = mem_pre_limit
    job_exp_list = []
    for i in range(len(cpu_pre)):
        job_exp_list.append({'name':aim,'cpu':cpu_pre[i],'mem':mem_pre[i]})
    pool_fit = multiprocessing.Pool(6)
    # print("start to a get_fitness3 map")
    pred = pool_fit.map(predict_min_map3, job_exp_list)
    # print("end a get_fitness3 map")
    pool_fit.close()
    pool_fit.join()

    pred = np.array(pred)
    # print("a get_fitness3 process finished")
    # pred = mini_batch
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

def get_fitness4(aim,pop,cpu_base,mem_base,cpu_allocate,mem_allocate,worker,mini0):
    #任务可以完成，现在要减少资源，当然就是看减少资源的总量和减少资源造成的minibatch之间的权衡
    cpu_alpha,mem_alpha = translateDNA2(pop)
    # print("catch cpu_alpha:")
    # print(cpu_alpha)
    cpu_pre = cpu_allocate*cpu_alpha
    # print(type(cpu_pre))
    mem_pre = mem_allocate*mem_alpha
    job_exp_list = []
    for i in range(len(cpu_pre)):
        if cpu_pre[i] < 0.475 * cpu_base:
            cpu_pre[i] = math.ceil(0.475 * cpu_base)
        if mem_pre[i] < 1.03 * mem_base:
            mem_pre[i] = math.ceil(1.03 * mem_base)
        job_exp_list.append({'name': aim, 'cpu': cpu_pre[i], 'mem': mem_pre[i],'worker':worker,'mini0':mini0,'callo':cpu_allocate,'mallo':mem_allocate})
    pool_fit = multiprocessing.Pool(6)
    # print("start to get_fitness4 map")
    pred = pool_fit.map(predict_min_map4, job_exp_list)
    # print("end get_fitness4 map")
    pool_fit.close()
    pool_fit.join()
    pred = np.array(pred)
    # print("a get_fitness4 is finished")
    return (pred - min(pred)) + 1e-4

def select(pop,fitness):
    global POP_SIZE
    idx = np.random.choice(np.arange(pop.shape[0]),size=POP_SIZE,replace=True,p=fitness/fitness.sum())
#     不熟悉numpy的朋友可以查阅一下这个函数，主要是使用了choice里的最后一个参数p，参数p描述了从np.arange(POP_SIZE)里选择每一个元素的概率，
#     概率越高约有可能被选中，最后返回被选中的个体即可。

    return pop[idx]

def predict_min_first(rfr,cpu_alpha,mem_alpha,batch,flops,params):
    data = np.array([batch, flops, params, cpu_alpha, mem_alpha])
    data = np.mat(data)
    data = data.A
    iteration = rfr.predict(data)
    iteration = float(iteration)
    return iteration

def predict_min(job_name,cpu,mem, rfr):
    job_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    job_config = load_config(job_path)
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
    iteration = rfr.predict(data)
    iteration = float(iteration)
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
        cross_points = np.random.randint(low=0, high=DNA_SIZE * 2)  # 随机产生交叉的点
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
        mutate_point = np.random.randint(0, 2*DNA_SIZE-1)	#随机产生一个实数，代表要变异基因的位置
        child[mutate_point] = child[mutate_point]^1 	#将变异点的二进制为反转

def kongxian(res_cpu,res_mem,cpu_allocae,mem_allocate,cpu_base,mem_base,layout_config,pop):
    cpu_alpha,mem_alpha = translateDNA(pop)
    layout_key = layout_config.keys()
    delete_pop = []
    for i in range(len(cpu_alpha)):
        for lay in layout_key:
            if res_cpu[lay]+layout_config[lay]['worker']*(cpu_allocae-math.ceil(cpu_alpha[i]*cpu_allocae)) > 0 and res_mem[lay]+layout_config[lay]['worker']*(mem_allocate-mem_alpha[i]*mem_allocate)>0:
                continue
            else:
                delete_pop.append(i)
                break

    return delete_pop



def kongxian2(node_list,res_cpu,res_mem,ps,cpu_allocate,mem_allocate):
    res_load = [res_cpu[i] for i in node_list]
    list.sort(res_load)
    if res_load[-1] >= cpu_allocate:
        res_load[-1] = res_load[-1] - cpu_allocate
        list.sort(res_load)
        if res_load[-1] > 500*ps:
            return  True
        else:
            return False
    else:
        return False

def finish(res_iter,pop,res_time,cpu_allocate,mem_allocate,cpu_base,mem_base,rfr,aim):
    cpu_alpha,mem_alpha = translateDNA2(pop)
    delete_pop = []
    cpu_pre = cpu_allocate*cpu_alpha
    mem_pre = mem_allocate*mem_alpha
    for i in range(len(cpu_pre)):
        if cpu_pre[i] < 0.475 * cpu_base:
            cpu_pre[i] = math.ceil(0.475 * cpu_base)
        if mem_pre[i] < 1.03 * mem_base:
            mem_pre[i] = math.ceil(1.03 * mem_base)
        mini_batch = predict_min(aim,cpu_pre[i],mem_pre[i],rfr)
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


def assign_jobs(tasks, rfr, lock):
    global DNA_SIZE, POP_SIZE, N_GENERATIONS
    global XBOUND, YBOUND
    global pop_total
    # 选择标准有两个：
    '''
    1.对于每次选择，选择无法按时完成的任务，使用deadline
    为保证规模并不过分高，则每次选择的是最紧急的任务要进行调整
    2.对于系统负载而言，如果系统资源负载不高的话，则可以考虑调整资源，使其负载率较高
    3.对于系统而言，如果资源利用率持续低于某个阈值的话可以考虑增加某个任务的负载
    4.每次在调增任务时尝试选择调减任务，然后减少其资源的分配

    :return:
    '''
    step_influx_client = influxdb.InfluxDBClient(host='192.168.128.10', username='admin', password='admin',
                                                 database='PREDICT')

    piotential = []
    job_basic = reload_jobs_aim(tasks['last'], -1)
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
        layout_file = '/tfdata/k8snfs/setbase/%s/layout.json' % i
        res_file = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (i, i)
        job_file = '/tfdata/k8snfs/setbase/%s/%s.json' % (i, i)
        res_config = load_config(res_file)
        job_config = load_config(job_file)
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
                tmp_layout_config[tmp_config[tk]] = {'ps': 0, 'worker': 0}
            for tk in tmp_key:
                if 'ps' in tk:
                    tmp_cpu[tmp_config[tk]] += 750
                    tmp_mem[tmp_config[tk]] += 2048
                    tmp_layout_config[tmp_config[tk]]['ps'] += 1
                else:
                    # "cpu_source": 6046,
                    # "mem_source": 19225,
                    tmp_cpu[tmp_config[tk]] += res_config['cpu_source']
                    tmp_mem[tmp_config[tk]] += res_config['mem_source']
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
        return {}, -1
    assign_config = {}
    # for i in piotential:
    #     assign_config[i] = {}
    aim1 = ''
    aim2 = ''
    mode = 0
    aim = {}
    if not piotential:
        print("Do not have jobs!!")
        return {}, -1
    for i in piotential:
        reload_tmp = reload_jobs(i, -1)
        lock.acquire()
        tmp_ns2 = tasks['ns']
        lock.release()
        if i not in tmp_ns2:
            piotential.remove(i)
            key00 = layout_config0[i].keys()
            for ke00 in key00:
                res_cpu[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['cpu_source']
                res_mem[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['mem_source']
                res_cpu[ke00] += layout_config0[i][ke00]['ps'] * 650
                res_mem[ke00] += layout_config0[i][ke00]['ps'] * 1536
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
                res_cpu[ke00] += layout_config0[i][ke00]['ps'] * 650
                res_mem[ke00] += layout_config0[i][ke00]['ps'] * 15
            continue
        tmp_re = reload_tmp.deadline - (time.time() - reload_tmp.starttime)
        tmp_iter, total_step, _ = reload_tmp.get_remain(mode=1)
        reload_iter, _, reload_point = reload_tmp.get_remain(mode=0)
        pre_list = reload_tmp.measure.split(" ")
        measure_s = pre_list[0] + 'S' + pre_list[-1]
        measure_t = pre_list[0] + 'T' + pre_list[-1]
        res = step_influx_client.query(
            "select * from " + measure_s + " group by nodes order by desc limit 5")
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
                # now_mini = max(time_avg)
                now_mini = np.mean(time_avg)
            else:
                now_mini = predict_min(i, reload_tmp.cpu_allocate, reload_tmp.memory_allocate, rfr)
        else:
            now_mini = predict_min(i, reload_tmp.cpu_allocate, reload_tmp.memory_allocate, rfr)
        need_time = tmp_iter * now_mini
        res_config0[i]['need'] = need_time
        res_config0[i]['remain_time'] = tmp_re
        res_config0[i]['mini'] = now_mini
        res_config0[i]['remain_iter'] = tmp_iter
        res_config0[i]['reload_iter'] = reload_iter
        res_config0[i]['total_step'] = total_step
        res_config0[i]['reload_point'] = reload_point
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
            # 所有任务都可以完成
            relise_cpu = 0
            relise_mem = 0
            for node in node_list_global:
                relise_cpu += res_cpu[node]
                relise_mem += res_mem[node]
            relise_cpu = relise_cpu / job_basic.total_cpu
            relise_mem = relise_mem / job_basic.total_mem
            relise = 0.75 * relise_cpu + 0.25 * relise_mem
            if relise > 0.4:
                # 若资源空闲
                # 都可以完成，考虑增大资源，提高资源利用率，其中要提升的也是离deadline最近的任务和对于资源最敏感的任务
                if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                    aim1 = aim[aim_time[-1]][0]
                    print(aim1)
                    cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                    mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                    if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                            res_config0[aim1]['mem_source'] >= mem_pre_limit:
                        aim1 = ''
                    aim2 = ''
                else:
                    aim1 = ''
                    ttll = len(aim_time)
                    print("aim_time length % d" % ttll)
                    tmp_rank = -1
                    for atkk in range(ttll - 1, -1, -1):
                        for using_aim in aim[aim_time[atkk]]:
                            print(using_aim)
                            cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[using_aim]['cpu_high'])
                            mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[using_aim]['memory_base'])
                            if res_config0[using_aim]['worker'] > 8 and res_config0[using_aim][
                                'cpu_source'] >= cpu_pre_limit and res_config0[using_aim][
                                'mem_source'] >= mem_pre_limit:
                                continue
                            else:
                                aim1 = using_aim
                                tmp_rank = atkk
                                break
                        if tmp_rank >= 0:
                            break
                    aim_time_po = []
                    print(tmp_rank)
                    # up_limit = min(3, len(aim_time))
                    # up_limit = min(3, 0)
                    if tmp_rank >= 0:
                        up_limit = min(3, tmp_rank + 1)
                        # up_limit = 0 - (up_limit)
                        up_limit = tmp_rank - ttll + 1 - up_limit
                        print(up_limit)
                        for i in range(up_limit, tmp_rank - ttll + 1):
                            for j in aim[aim_time[i]]:
                                aim_time_po.append(j)
                        aim_mingan = {}
                        for j in aim_time_po:
                            print(j)
                            cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[j]['cpu_high'])
                            mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[j]['memory_base'])
                            if res_config0[j]['worker'] > 8 and res_config0[j]['cpu_source'] >= cpu_pre_limit and \
                                    res_config0[j]['mem_source'] >= mem_pre_limit:
                                continue
                            reload_tmp = reload_jobs(j, -1)
                            cpu_per = math.ceil((reload_tmp.cpu_allocate) / (reload_tmp.worker_replicas))
                            mem_per = math.ceil((reload_tmp.memory_allocate) / (reload_tmp.worker_replicas))
                            remain0, total0, atmp0 = reload_tmp.get_remain(mode=0)
                            remain1, _, _ = reload_tmp.get_remain(mode=1)
                            sco1 = (res_config0[j]['mini'] - predict_min(job_name=j,
                                                                         cpu=(reload_tmp.cpu_allocate + cpu_per),
                                                                         mem=(reload_tmp.memory_allocate + mem_per),
                                                                         rfr=rfr)) / (
                                           (0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                           0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                            if remain1 == 0:
                                sco2 = float('-inf')
                            else:
                                sco2 = (res_config0[j]['mini'] * (remain1 - (
                                        (total0 * reload_tmp.worker_replicas) / (
                                        reload_tmp.worker_replicas + 1) - atmp0))) / (remain1)
                                sco2 = sco2 / ((0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                        0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                            if remain1 == 0:
                                sco = float('-inf')
                            else:
                                # sco = max([sco1, sco2])
                                if res_config0[j]['worker'] > 8:
                                    sco = sco1
                                elif res_config0[j]['cpu_source'] >= cpu_pre_limit and res_config0[j][
                                    'mem_source'] >= mem_pre_limit:
                                    sco = sco2
                                else:
                                    sco = sco1
                                    if sco2 > sco1:
                                        sco = sco2
                            # mingan_key = list(aim_mingan.keys())
                            # if sco not in mingan_key:
                            #     aim_mingan[sco] = []
                            aim_mingan[sco] = j
                        mingan_key = list(aim_mingan.keys())
                        list.sort(mingan_key)
                        if mingan_key[-1] < 0:
                            aim2 = ''
                        else:
                            aim2 = aim_mingan[mingan_key[-1]]
                            if aim2 == aim1:
                                aim2 = ''
                    else:
                        aim2 = ''
                mode = 1
            else:
                # 资源比较紧张，此时考虑减少距离deadline最远且对资源最不敏感的任务
                if len(aim_time) == 1 and len(aim[aim_time[0]]) == 1:
                    aim1 = aim[aim_time[0]][0]
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[0]][0]

                    aim_time_po = []
                    up_limit = min(3, len(aim_time))
                    print("up_limit mode 4: %d" % up_limit)
                    # up_limit = min(3, len(aim_time) - tmp_rank - 1)
                    # up_limit = 0 - up_limit
                    # for i in range(tmp_rank, tmp_rank + up_limit):
                    for i in range(0, up_limit):
                        if aim_time[i] >= 0:
                            break
                        for j in aim[aim_time[i]]:
                            aim_time_po.append(j)
                    aim_mingan = {}
                    for j in aim_time_po:
                        reload_tmp = reload_jobs(j, -1)
                        cpu_per = math.ceil((reload_tmp.cpu_allocate) / (reload_tmp.worker_replicas))
                        mem_per = math.ceil((reload_tmp.memory_allocate) / (reload_tmp.worker_replicas))
                        remain0, total0, atmp0 = reload_tmp.get_remain(mode=0)
                        remain1, _, _ = reload_tmp.get_remain(mode=1)

                        sco1 = (predict_min(job_name=j, cpu=(reload_tmp.cpu_allocate - cpu_per),
                                            mem=(reload_tmp.memory_allocate - mem_per), rfr=rfr) - res_config0[j][
                                    'mini']) / (
                                       (0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                       0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))

                        if remain1 == 0 or (reload_tmp.worker_replicas - 1) == 0:
                            sco2 = float('inf')
                        else:
                            sco2 = (res_config0[j]['mini'] * (((total0 * reload_tmp.worker_replicas) / (
                                    reload_tmp.worker_replicas - 1) - atmp0) - remain1)) / (remain1)
                            sco2 = sco2 / ((0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                    0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                        if remain1 == 0:
                            sco = -10
                        else:
                            # if res_config0[j]['worker'] > 8:
                            #     sco = abs(sco1)
                            # elif res_config0[j]['cpu_source'] >= cpu_pre_limit and res_config0[j][
                            #     'mem_source'] >= mem_pre_limit:
                            #     sco = sco2
                            sco = min(abs(sco1), abs(sco2))
                            sco = sco / ((0.7 * (
                                    reload_tmp.cpu_allocate * reload_tmp.worker_replicas + reload_tmp.ps_replicas * 640) / reload_tmp.total_cpu) + (
                                                 0.3 * (
                                                 reload_tmp.memory_allocate * reload_tmp.worker_replicas + reload_tmp.ps_replicas * 1536) / reload_tmp.total_mem))
                        aim_mingan[sco] = j
                    mingan_key = list(aim_mingan.keys())
                    list.sort(mingan_key)
                    if mingan_key[-1] < 0:
                        aim2 = ''
                    else:
                        for ss in mingan_key:
                            if ss < 0:
                                mingan_key.remove(ss)
                        aim2 = aim_mingan[mingan_key[0]]
                        if aim2 == aim1:
                            aim2 = ''
                    mode = 4


        elif aim_time[0] < 0:
            # 有任务完不成，有任务可以完成，考虑减少资源和增大资源，减少离deadline最远且对资源最不敏感的任务，增大超时最严重的任务
            # 返回任务
            # 增加资源的任务为超时最严重的任务，没有疑问，减少资源的任务则为离deadline较远且对资源最不敏感的任务，即剥夺资源带来的影响最小：
            if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                # aim1 = aim[aim_time[-1]][0]
                # aim2 = ''
                aim1 = aim[aim_time[-1]][0]
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    aim1 = ''
                aim2 = ''
            else:
                # aim1 = aim[aim_time[-1]][0]
                aim1 = ''
                ttll = len(aim_time)
                print("aim_time length % d" % ttll)
                tmp_rank = -1
                for atkk in range(ttll - 1, -1, -1):
                    print("into loop")

                    for using_aim in aim[aim_time[atkk]]:
                        print(using_aim)
                        cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[using_aim]['cpu_high'])
                        mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[using_aim]['memory_base'])
                        if res_config0[using_aim]['worker'] > 8 and res_config0[using_aim][
                            'cpu_source'] >= cpu_pre_limit and res_config0[using_aim][
                            'mem_source'] >= mem_pre_limit:
                            continue
                        else:
                            aim1 = using_aim
                            tmp_rank = atkk
                            break
                    if tmp_rank >= 0:
                        break
                aim_time_po = []
                print("tmp rank:%d" % tmp_rank)
                up_limit = min(3, len(aim_time))
                # up_limit = 0 - up_limit
                for i in range(0, up_limit):
                    if aim_time[i] >= 0:
                        break
                    for j in aim[aim_time[i]]:
                        aim_time_po.append(j)
                aim_mingan = {}
                for j in aim_time_po:
                    reload_tmp = reload_jobs(j, -1)
                    cpu_per = math.ceil((reload_tmp.cpu_allocate) / (reload_tmp.worker_replicas))
                    mem_per = math.ceil((reload_tmp.memory_allocate) / (reload_tmp.worker_replicas))
                    remain0, total0, atmp0 = reload_tmp.get_remain(mode=0)
                    remain1, _, _ = reload_tmp.get_remain(mode=1)
                    sco1 = (predict_min(job_name=j, cpu=(reload_tmp.cpu_allocate - cpu_per),
                                        mem=(reload_tmp.memory_allocate - mem_per), rfr=rfr) - res_config0[j][
                                'mini']) / (
                                   (0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                   0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                    if remain1 == 0 or (reload_tmp.worker_replicas - 1) == 0:
                        sco2 = float('inf')
                    else:
                        sco2 = (res_config0[j]['mini'] * (((total0 * reload_tmp.worker_replicas) / (
                                reload_tmp.worker_replicas - 1) - atmp0) - remain1)) / (remain1)
                        sco2 = sco2 / ((0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                    if remain1 == 0:
                        sco = -10
                    else:
                        sco = min(abs(sco1), abs(sco2))
                        sco = sco / ((0.7 * (
                                reload_tmp.cpu_allocate * reload_tmp.worker_replicas + reload_tmp.ps_replicas * 500) / reload_tmp.total_cpu) + (
                                             0.3 * (
                                             reload_tmp.memory_allocate * reload_tmp.worker_replicas + reload_tmp.ps_replicas * 1536) / reload_tmp.total_mem))
                    aim_mingan[sco] = j
                mingan_key = list(aim_mingan.keys())
                list.sort(mingan_key)
                if mingan_key[-1] < 0:
                    aim2 = ''
                else:
                    for ss in mingan_key:
                        if ss < 0:
                            mingan_key.remove(ss)
                    aim2 = aim_mingan[mingan_key[0]]
                    if aim2 == aim1:
                        aim2 = ''
            mode = 2
        elif aim_time[0] >= 0:
            if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                aim1 = aim[aim_time[-1]][0]
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    aim1 = ''
                aim2 = ''
            else:
                # 都完不成，则返回超时最严重的两个任务，开始启发式评估方案
                # aim1 = aim[aim_time[-1]][0]
                aim1 = ''
                ttll = len(aim_time)
                print("aim_time length % d" % ttll)
                tmp_rank = -1
                tmp_inter_at_last = 0
                for atkk in range(ttll - 1, -1, -1):
                    tmp_inter_at = 0
                    for using_aim in aim[aim_time[atkk]]:
                        print(using_aim)
                        cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[using_aim]['cpu_high'])
                        mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[using_aim]['memory_base'])
                        if res_config0[using_aim]['worker'] > 8 and res_config0[using_aim][
                            'cpu_source'] >= cpu_pre_limit and res_config0[using_aim][
                            'mem_source'] >= mem_pre_limit:
                            tmp_inter_at += 1
                            continue
                        else:
                            aim1 = using_aim
                            tmp_inter_at_last = tmp_inter_at
                            tmp_rank = atkk
                            break
                    if tmp_rank >= 0:
                        break
                if tmp_rank >= 0:
                    if len(aim[aim_time[tmp_rank]]) > tmp_inter_at_last + 1:
                        aim2 = aim[aim_time[tmp_rank]][tmp_inter_at_last + 1]
                    else:
                        if tmp_rank > 0:
                            aim2 = aim[aim_time[tmp_rank - 1]][0]
                        else:
                            aim2 = ''

            mode = 3
    print('The mode will be used: %d' % mode)
    print('The first aim and second aim:')
    print(aim1)
    print(aim2)

    if mode == 0:
        print("Mode %d Do not find fit job to get modluation!!" % mode)
        return {}, mode
    elif mode == 1:
        if not aim1 and not aim2:
            print("Mode %d Do not find aim1 and aim2 to get modulateion!!" % mode)
            return {}, mode
        # 具体实施方案，则为两种选择，修改节点数和增加每个节点的资源，在这里评估指标变为节约的时间/资源
        # 可选方案：增加1个节点/添加相应的资源，判断方法：节约的时间/添加的资源，如果资源超过范围则丢弃该方案，直到找到合适的方案，备选方案为
        # job_aim1 = reload_jobs(aim1, -1)
        if aim1:
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
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
                # fitness = get_fitness1(aim1, pop,res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'],res_config0[aim1]['worker'],res_config0[aim1]['ps'])
                fitness = get_fitness1(aim1, pop, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                print("a fitness1:")
                print(fitness)
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 1, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])

            delete_pop = kongxian(res_cpu, res_mem, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                  res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], layout_config0[aim1],
                                  pop)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                if res_config0[aim1]['worker'] > 8:
                    assign_config[aim1] = {}
                else:
                    assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1][
                    'cpu_source'] >= cpu_pre_limit and res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    # fitness = get_fitness1(aim1, pop_new,res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                    #                        res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                    fitness = get_fitness1(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'],
                                           res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                           res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}

                    assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    fitness = get_fitness1(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'],
                                           res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                           res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}

                    best_min_batch = predict_min(aim1, aim1_cpu, aim1_mem, rfr)
                    # method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}

                    sco1 = res_config0[aim1]['need'] + 25 - (math.ceil(
                        res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (
                                1 + res_config0[aim1]['worker'])) -
                                                             res_config0[aim1]['reload_point'] + 1) * res_config0[aim1][
                               'mini']
                    sco1 = sco1 / (0.75 * ((res_config0[aim1]['ps'] + method1['ps']) * 720 + (
                            method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                                               'cpu_source']) / job_basic.total_cpu + 0.25 * (
                                           (res_config0[aim1]['ps'] + method1['ps']) * 1600 + (
                                           method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                                               'mem_source']) / job_basic.total_mem)
                    sco2 = res_config0[aim1]['need'] - best_min_batch * res_config0[aim1]['remain_iter']
                    sco2 = sco2 / (0.75 * (res_config0[aim1]['ps'] * 720 + res_config0[aim1][
                        'worker'] * aim1_cpu) / job_basic.total_cpu + 0.25 * (
                                           res_config0[aim1]['ps'] * 1600 + res_config0[aim1][
                                       'worker'] * aim1_mem) / job_basic.total_mem)
                    # max([sco2, sco1])
                    if res_config0[aim1]['worker'] > 8:
                        if sco2 > 0:
                            assign_config[aim1] = method2
                        else:
                            assign_config[aim1] = {}
                    elif res_config0[aim1]['cpu_source'] >= cpu_pre_limit and res_config0[aim1][
                        'mem_source'] >= mem_pre_limit:
                        if sco1 > 0:
                            assign_config[aim1] = method1
                        else:
                            assign_config[aim1] = {}
                    else:
                        sco_tmp0 = sco1
                        if sco2 > sco1:
                            sco_tmp0 = sco2
                        if sco_tmp0 < 0:
                            print('Mode %d: Can not find useful method!!' % mode)
                            assign_config[aim1] = {}
                        else:
                            if sco1 > sco2:
                                assign_config[aim1] = method1
                            else:
                                assign_config[aim1] = method2

            if assign_config[aim1]:
                if assign_config[aim1]['type'] == 1:
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
                    if assign_config[aim1]['ps'] != 0:
                        list.sort(res_load)
                        deal_node = res_condition[res_load[-1]]
                        res_cpu[deal_node] -= 650
                        res_mem[deal_node] -= 1792
                        aim1_tmp_layout = layout_config0[aim1]
                        aim1_tlk = list(aim1_tmp_layout.keys())
                        if deal_node in aim1_tlk:
                            layout_config0[aim1][deal_node]['ps'] += 1
                        else:
                            layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}
                else:
                    update_layouts = layout_config0[aim1]
                    update_lay_key = list(update_layouts.keys())
                    for ulk in update_lay_key:
                        # method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                        res_cpu[ulk] = res_cpu[ulk] + update_layouts[ulk]['worker'] * (
                                res_config0[aim1]['cpu_source'] - assign_config[aim1]['cpu'])
                        res_mem[ulk] = res_mem[ulk] + update_layouts[ulk]['worker'] * (
                                res_config0[aim1]['mem_source'] - assign_config[aim1]['mem'])
                    res_config0[aim1]['cpu_source'] = assign_config[aim1]['cpu']
                    res_config0[aim1]['mem_source'] = assign_config[aim1]['mem']
        else:
            assign_config[aim1] = {}
        if not aim2:
            assign_config[aim2] = {}
        else:
            aim1 = aim2

            # old code

            # job_aim2 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)
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
                # fitness = get_fitness1(aim1, pop,res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                #                        res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                fitness = get_fitness1(aim1, pop, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 1, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            # "cpu_high": 8991,
            # "memory_base": 8706,
            delete_pop = kongxian(res_cpu, res_mem, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                  res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], layout_config0[aim1],
                                  pop)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim2!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                if res_config0[aim1]['worker'] > 8:
                    assign_config[aim1] = {}
                else:
                    assign_config[aim1] = method1
                # assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['cpu_source'] >= cpu_pre_limit and res_config0[aim1][
                    'mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                # fitness = get_fitness1(aim1, pop_new,res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                #                        res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                else:
                    fitness = get_fitness1(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'], res_config0[aim1]['cpu_high'],
                                           res_config0[aim1]['memory_base'],
                                           res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    # aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
                    # aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    fitness = get_fitness1(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'], res_config0[aim1]['cpu_high'],
                                           res_config0[aim1]['memory_base'],
                                           res_config0[aim1]['worker'], res_config0[aim1]['ps'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    # aim1_cpu = cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high']
                    # aim1_mem = mem_mod[max_fitness_index] * res_config0[aim1]['memory_base']
                    aim1_cpu = cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source']
                    aim1_mem = mem_mod[max_fitness_index] * res_config0[aim1]['mem_source']
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    best_min_batch = predict_min(aim1, aim1_cpu, aim1_mem, rfr)
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    sco1 = res_config0[aim1]['need'] + 25 - (
                            math.ceil(res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (
                                    1 + res_config0[aim1]['worker'])) -
                            res_config0[aim1]['reload_point'] + 1) * res_config0[aim1]['mini']
                    sco1 = sco1 / (0.75 * ((res_config0[aim1]['ps'] + method1['ps']) * 720 + (
                            method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                                               'cpu_source']) / job_basic.total_cpu + 0.25 * (
                                           (res_config0[aim1]['ps'] + method1['ps']) * 1600 + (
                                           method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                                               'mem_source']) / job_basic.total_mem)
                    sco2 = res_config0[aim1]['need'] - best_min_batch * res_config0[aim1]['remain_iter']
                    sco2 = sco2 / (0.75 * (res_config0[aim1]['ps'] * 720 + res_config0[aim1][
                        'worker'] * aim1_cpu) / job_basic.total_cpu + 0.25 * (
                                           res_config0[aim1]['ps'] * 1600 + res_config0[aim1][
                                       'worker'] * aim1_mem) / job_basic.total_mem)

                    if res_config0[aim1]['worker'] > 8:
                        if sco2 > 0:
                            assign_config[aim1] = method2
                        else:
                            assign_config[aim1] = {}
                    elif res_config0[aim1]['cpu_source'] >= cpu_pre_limit and res_config0[aim1][
                        'mem_source'] >= mem_pre_limit:
                        if sco1 > 0:
                            assign_config[aim1] = method1
                        else:
                            assign_config[aim1] = {}
                    else:
                        if max(sco2, sco1) < 0:
                            print('Mode %d: Can not find useful method!!' % mode)
                            assign_config[aim1] = {}
                        else:
                            if sco1 > sco2:
                                assign_config[aim1] = method1
                            else:
                                assign_config[aim1] = method2

    elif mode == 2:
        # 一增一减，结合4和3即可轻松给出了
        # 首先对于aim1,增加资源：
        if not aim1 and not aim2:
            print("Mode %d Do not find aim1 and aim2 to get modulateion!!" % mode)
            return {}, mode

        if aim1:
            # job_aim1 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)

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
                # fitness = get_fitness3()
                # fitness = get_fitness3(aim1, pop, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                fitness = get_fitness3(aim1, pop, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 1, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])

            if not change_number:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            # "cpu_high": 8991,
            # "memory_base": 8706,
            delete_pop = kongxian(res_cpu, res_mem, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                  res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], layout_config0[aim1],
                                  pop)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                if res_config0[aim1]['worker'] > 8:
                    assign_config[aim1] = {}
                else:
                    assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1][
                    'cpu_source'] >= cpu_pre_limit and res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    # fitness = get_fitness3(aim1, pop_new,res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                    fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'],
                                           res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    # aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
                    # aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    # fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                    fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'],
                                           res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    # aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
                    # aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    best_min_batch = predict_min(aim1, aim1_cpu, aim1_mem, rfr)
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    # sco1 = res_config0[aim1]['ne']
                    # res_config0[i]['need'] = need_time
                    # res_config0[i]['remain_time'] = tmp_re
                    # res_config0[i]['mini'] = now_mini
                    # res_config0[i]['remain_iter'] = tmp_iter
                    # res_config0[i]['reload_iter'] = reload_iter
                    # res_config0[i]['total_step'] = total_step
                    # res_config0[i]['ps'] = job_config["ps_replicas"]
                    # res_config0[i]['worker'] = job_config["worker_replicas"]
                    # "cpu_source": 6046,
                    # "mem_source": 19225,
                    sco1 = res_config0[aim1]['need'] + 25 - (math.ceil(
                        res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (
                                1 + res_config0[aim1]['worker'])) -
                                                             res_config0[aim1][
                                                                 'reload_point'] + 1) * res_config0[aim1]['mini']
                    # sco1 = sco1 / (0.75 * ((res_config0[aim1]['ps'] + method1['ps']) * 1000 + (
                    #             method1['worker1'] + res_config0[aim1]['worker']) * res_config0[aim1][
                    #                            'cpu_source']) / job_basic.total_cpu + 0.25 * (
                    #                            (res_config0[aim1]['ps'] + method1['ps']) * 2048 + (
                    #                                method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                    #                                'mem_source']) / job_basic.total_mem)
                    sco2 = res_config0[aim1]['need'] - best_min_batch * res_config0[aim1]['remain_iter']
                    # sco2 = sco2 / (0.75 * (res_config0[aim1]['ps'] * 1000 + res_config0[aim1][
                    #     'worker'] * aim1_cpu) / job_basic.total_cpu + 0.25 * (
                    #                            res_config0[aim1]['ps'] * 2048 + res_config0[aim1][
                    #                        'worker'] * aim1_mem) / job_basic.total_mem)
                    if res_config0[aim1]['worker'] > 8:
                        if sco2 > 0:
                            assign_config[aim1] = method2
                        else:
                            assign_config[aim1] = {}
                    elif res_config0[aim1]['cpu_source'] >= cpu_pre_limit and res_config0[aim1][
                        'mem_source'] >= mem_pre_limit:
                        if sco1 > 0:
                            assign_config[aim1] = method1
                        else:
                            assign_config[aim1] = {}
                    else:
                        if max(sco2, sco1) < 0:
                            print('Mode %d: Can not find useful method!!' % mode)
                            assign_config[aim1] = {}
                        else:
                            if sco1 > sco2:
                                assign_config[aim1] = method1
                            else:
                                assign_config[aim1] = method2

                    # print("最优的基因型：", pop[max_fitness_index])
                    # print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))

            if assign_config[aim1]:
                if assign_config[aim1]['type'] == 1:
                    res_condition = {}
                    res_load = [res_cpu[i] for i in node_list_global]
                    for no_k0 in node_list_global:
                        res_condition[res_cpu[no_k0]] = no_k0
                    print("Now res_condition:")
                    print(res_condition)
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    print("Add a worker to %s" % deal_node)
                    res_cpu[deal_node] -= res_config0[aim1]['cpu_source']
                    res_mem[deal_node] -= res_config0[aim1]['mem_source']
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
                    if assign_config[aim1]['ps'] != 0:
                        list.sort(res_load)
                        deal_node = res_condition[res_load[-1]]
                        print("Add a worker to %s" % deal_node)
                        res_cpu[deal_node] -= 650
                        res_mem[deal_node] -= 1792
                        aim1_tmp_layout = layout_config0[aim1]
                        aim1_tlk = list(aim1_tmp_layout.keys())
                        if deal_node in aim1_tlk:
                            layout_config0[aim1][deal_node]['ps'] += 1
                        else:
                            layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}
                else:
                    update_layouts = layout_config0[aim1]
                    # update_lay_key = list(update_layouts.keys())
                    update_lay_key = list(update_layouts.keys())
                    for ulk in update_lay_key:
                        # method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                        res_cpu[ulk] = res_cpu[ulk] + update_layouts[ulk]['worker'] * (
                                res_config0[aim1]['cpu_source'] - assign_config[aim1]['cpu'])
                        res_mem[ulk] = res_mem[ulk] + update_layouts[ulk]['worker'] * (
                                res_config0[aim1]['mem_source'] - assign_config[aim1]['mem'])
                    res_config0[aim1]['cpu_source'] = assign_config[aim1]['cpu']
                    res_config0[aim1]['mem_source'] = assign_config[aim1]['mem']

        if not aim2:
            assign_config[aim2] = {}
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)

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
                # fitness = get_fitness3()
                fitness = get_fitness4(aim1, pop, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['mini'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False

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
            delete_pop = finish(res_config0[aim1]['remain_iter'], pop, res_config0[aim1]['remain_time'],
                                res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], rfr, aim1)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                fitness = get_fitness4(aim1, pop_new, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'], res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.475 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.475 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 1.03 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(1.03 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                fitness = get_fitness4(aim1, pop_new, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.475 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.475 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 1.03 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(1.03 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                sco1 = 0.75 * (abs(method1['ps']) * 720 + abs(method1['worker']) * res_config0[aim1][
                    'cpu_source']) / job_basic.total_cpu + 0.25 * (
                               abs(method1['ps']) * 1792 + abs(method1['worker']) * res_config0[aim1][
                           'mem_source']) / job_basic.total_mem
                sco2 = 0.75 * (res_config0[aim1]['worker'] * (
                        res_config0[aim1]['cpu_source'] - aim1_cpu)) / job_basic.total_cpu + 0.25 * (
                               res_config0[aim1]['worker'] * (
                               res_config0[aim1]['mem_source'] - aim1_mem)) / job_basic.total_mem
                if sco1 > sco2:
                    assign_config[aim1] = method1
                else:
                    assign_config[aim1] = method2

    elif mode == 3:
        if not aim1 and not aim2:
            print("Mode %d Do not find aim1 and aim2 to get modulateion!!" % mode)
            return {}, mode
        # 具体实施方案，则为两种选择，修改节点数和增加每个节点的资源，在这里评估指标变为节约的时间/资源
        # 可选方案：增加1个节点/添加相应的资源，判断方法：节约的时间/添加的资源，如果资源超过范围则丢弃该方案，直到找到合适的方案，备选方案为
        # job_aim1 = reload_jobs(aim1, -1)
        if aim1:
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)

            for _ in range(N_GENERATIONS):
                input_pop = []
                for father in pop:
                    mother = pop[np.random.randint(POP_SIZE)]
                    input_pop.append([father, mother])
                pool_cross = multiprocessing.Pool(6)
                pop_tmp = pool_cross.map(crossover_and_mutation, input_pop)
                # pop = crossover_and_mutation(input_pop)
                pool_cross.close()
                pool_cross.join()
                pop = []
                for item in pop_tmp:
                    for item2 in item:
                        pop.append(item2)
                pop = np.array(pop)
                fitness = get_fitness3(aim1, pop, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 1, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])

            if not change_number:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            # "cpu_high": 8991,
            # "memory_base": 8706,
            delete_pop = kongxian(res_cpu, res_mem, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                  res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], layout_config0[aim1],
                                  pop)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                if res_config0[aim1]['worker'] > 8:
                    assign_config[aim1] = {}
                else:
                    assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1][
                    'cpu_source'] >= cpu_pre_limit and res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'],
                                           res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)

                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'],
                                           res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)

                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    best_min_batch = predict_min(aim1, aim1_cpu, aim1_mem, rfr)
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}

                    sco1 = res_config0[aim1]['need'] + 25 - (math.ceil(
                        res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (
                                1 + res_config0[aim1]['worker'])) -
                                                             res_config0[aim1][
                                                                 'reload_point'] + 1) * res_config0[aim1]['mini']
                    # sco1 = sco1 / (0.75 * ((res_config0[aim1]['ps'] + method1['ps']) * 1000 + (
                    #             method1['worker1'] + res_config0[aim1]['worker']) * res_config0[aim1][
                    #                            'cpu_source']) / job_basic.total_cpu + 0.25 * (
                    #                            (res_config0[aim1]['ps'] + method1['ps']) * 2048 + (
                    #                                method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                    #                                'mem_source']) / job_basic.total_mem)
                    sco2 = res_config0[aim1]['need'] - best_min_batch * res_config0[aim1]['remain_iter']
                    # sco2 = sco2 / (0.75 * (res_config0[aim1]['ps'] * 1000 + res_config0[aim1][
                    #     'worker'] * aim1_cpu) / job_basic.total_cpu + 0.25 * (
                    #                            res_config0[aim1]['ps'] * 2048 + res_config0[aim1][
                    #    remain_iter
                    #                        'worker'] * aim1_mem) / job_basic.total_mem)
                    if res_config0[aim1]['worker'] > 8:
                        if sco2 > 0:
                            assign_config[aim1] = method2
                        else:
                            assign_config[aim1] = {}
                    elif res_config0[aim1]['cpu_source'] >= cpu_pre_limit and res_config0[aim1][
                        'mem_source'] >= mem_pre_limit:
                        if sco1 > 0:
                            assign_config[aim1] = method1
                        else:
                            assign_config[aim1] = {}
                    else:
                        if max(sco2, sco1) < 0:
                            print('Mode %d: Can not find useful method!!' % mode)
                            assign_config[aim1] = {}
                        else:
                            if sco1 > sco2:
                                assign_config[aim1] = method1
                            else:
                                assign_config[aim1] = method2

                    # print("最优的基因型：", pop[max_fitness_index])
                    # print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))
            if assign_config[aim1]:
                if assign_config[aim1]['type'] == 1:
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
                    if assign_config[aim1]['ps'] != 0:
                        list.sort(res_load)
                        deal_node = res_condition[res_load[-1]]
                        res_cpu[deal_node] -= 650
                        res_mem[deal_node] -= 1792
                        aim1_tmp_layout = layout_config0[aim1]
                        aim1_tlk = list(aim1_tmp_layout.keys())
                        if deal_node in aim1_tlk:
                            layout_config0[aim1][deal_node]['ps'] += 1
                        else:
                            layout_config0[aim1][deal_node] = {'ps': 1, 'worker': 0}

                else:
                    update_layouts = layout_config0[aim1]
                    # update_lay_key = list(update_layouts)
                    update_lay_key = list(update_layouts.keys())
                    for ulk in update_lay_key:
                        # method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                        res_cpu[ulk] = res_cpu[ulk] + update_layouts[ulk]['worker'] * (
                                res_config0[aim1]['cpu_source'] - assign_config[aim1]['cpu'])
                        res_mem[ulk] = res_mem[ulk] + update_layouts[ulk]['worker'] * (
                                res_config0[aim1]['mem_source'] - assign_config[aim1]['mem'])
                    res_config0[aim1]['cpu_source'] = assign_config[aim1]['cpu']
                    res_config0[aim1]['mem_source'] = assign_config[aim1]['mem']
        else:
            assign_config[aim1] = {}
        if not aim2:
            assign_config[aim2] = {}
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)
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

                fitness = get_fitness3(aim1, pop, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False
            if res_config0[aim1]['ps'] < math.ceil(res_config0[aim1]['worker'] / 4):
                method1 = {'type': 1, 'ps': 1, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 1, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            else:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])

            if not change_number:
                method1 = {'type': 1, 'ps': 0, 'worker': 1}
                change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                          res_config0[aim1]['mem_source'])
            delete_pop = kongxian(res_cpu, res_mem, res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                  res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], layout_config0[aim1],
                                  pop)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                if res_config0[aim1]['worker'] > 8:
                    assign_config[aim1] = {}
                else:
                    assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1][
                    'cpu_source'] >= cpu_pre_limit and res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'], res_config0[aim1]['cpu_high'],
                                           res_config0[aim1]['memory_base'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)
                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                cpu_pre_limit = math.ceil(XBOUND[-1] * 1.478 * res_config0[aim1]['cpu_high'])
                mem_pre_limit = math.ceil(YBOUND[-1] * 1.682 * res_config0[aim1]['memory_base'])
                if res_config0[aim1]['worker'] > 8 and res_config0[aim1]['cpu_source'] >= cpu_pre_limit and \
                        res_config0[aim1]['mem_source'] >= mem_pre_limit:
                    assign_config[aim1] = {}
                else:
                    fitness = get_fitness3(aim1, pop_new, res_config0[aim1]['cpu_source'],
                                           res_config0[aim1]['mem_source'], res_config0[aim1]['cpu_high'],
                                           res_config0[aim1]['memory_base'])
                    max_fitness_index = np.argmax(fitness)
                    print("max_fitness:", fitness[max_fitness_index])
                    cpu_mod, mem_mod = translateDNA(pop_new)

                    aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                    aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                    if aim1_cpu > cpu_pre_limit:
                        aim1_cpu = cpu_pre_limit
                    if aim1_mem > mem_pre_limit:
                        aim1_mem = mem_pre_limit
                    best_min_batch = predict_min(aim1, aim1_cpu, aim1_mem, rfr)
                    method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                    sco1 = res_config0[aim1]['need'] + 25 - (
                            math.ceil(res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (
                                    1 + res_config0[aim1]['worker'])) -
                            res_config0[aim1]['reload_point'] + 1) * res_config0[aim1]['mini']
                    # sco1 = sco1 / (0.75 * ((res_config0[aim1]['ps'] + method1['ps']) * 1000 + (
                    #         method1['worker1'] + res_config0[aim1]['worker']) * res_config0[aim1][
                    #                            'cpu_source']) / job_basic.total_cpu + 0.25 * (
                    #                        (res_config0[aim1]['ps'] + method1['ps']) * 2048 + (
                    #                        method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                    #                            'mem_source']) / job_basic.total_mem)
                    sco2 = res_config0[aim1]['need'] - best_min_batch * res_config0[aim1]['remain_iter']
                    # sco2 = sco2 / (0.75 * (res_config0[aim1]['ps'] * 1000 + res_config0[aim1][
                    #     'worker'] * aim1_cpu) / job_basic.total_cpu + 0.25 * (
                    #                        res_config0[aim1]['ps'] * 2048 + res_config0[aim1][
                    #                    'worker'] * aim1_mem) / job_basic.total_mem)
                    if res_config0[aim1]['worker'] > 8:
                        if sco2 > 0:
                            assign_config[aim1] = method2
                        else:
                            assign_config[aim1] = {}

                    elif res_config0[aim1]['cpu_source'] >= cpu_pre_limit and res_config0[aim1][
                        'mem_source'] >= mem_pre_limit:
                        if sco1 > 0:
                            assign_config[aim1] = method1
                        else:
                            assign_config[aim1] = {}
                    else:
                        if max(sco2, sco1) < 0:
                            print('Mode %d: Can not find useful method!!' % mode)
                            assign_config[aim1] = {}
                        else:
                            if sco1 > sco2:
                                assign_config[aim1] = method1
                            else:
                                assign_config[aim1] = method2


    elif mode == 4:
        if not aim1 and not aim2:
            print("Mode %d Do not find aim1 and aim2 to get modulateion!!" % mode)
            return {}, mode

        if aim1:
            # job_aim1 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)

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
                # fitness = get_fitness3()
                fitness = get_fitness4(aim1, pop, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['mini'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False

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
            delete_pop = finish(res_config0[aim1]['remain_iter'], pop, res_config0[aim1]['remain_time'],
                                res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], rfr, aim1)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                fitness = get_fitness4(aim1, pop_new, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.475 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.475 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 1.03 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(1.03 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                fitness = get_fitness4(aim1, pop_new, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.475 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.475 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 1.03 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(1.03 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                sco1 = 0.75 * (abs(method1['ps']) * 740 + abs(method1['worker']) * res_config0[aim1][
                    'cpu_source']) / job_basic.total_cpu + 0.25 * (
                               abs(method1['ps']) * 1800 + abs(method1['worker']) * res_config0[aim1][
                           'mem_source']) / job_basic.total_mem
                sco2 = 0.75 * (res_config0[aim1]['worker'] * (
                        res_config0[aim1]['cpu_source'] - aim1_cpu)) / job_basic.total_cpu + 0.25 * (
                               res_config0[aim1]['worker'] * (
                               res_config0[aim1]['mem_source'] - aim1_mem)) / job_basic.total_mem
                if sco1 > sco2:
                    assign_config[aim1] = method1
                else:
                    assign_config[aim1] = method2
        else:
            assign_config[aim1] = {}
        if not aim2:
            assign_config[aim2] = {}
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)

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
                # fitness = get_fitness3()
                fitness = get_fitness4(aim1, pop, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['mini'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False

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
            delete_pop = finish(res_config0[aim1]['remain_iter'], pop, res_config0[aim1]['remain_time'],
                                res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'], rfr, aim1)
            print("Unfit index are:")
            print(delete_pop)
            delete_pop = list(delete_pop)
            # ac = np.delete(ac,[1,3,5],axis=0)
            pop_new = np.delete(pop, delete_pop, axis=0)
            if pop_new.size == 0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size == 0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size > 0:
                fitness = get_fitness4(aim1, pop_new, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'], res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.475 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.475 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 1.03 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(1.03 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size > 0:
                fitness = get_fitness4(aim1, pop_new, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.475 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.475 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 1.03 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(1.03 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                sco1 = 0.75 * (abs(method1['ps']) * 740 + abs(method1['worker']) * res_config0[aim1][
                    'cpu_source']) / job_basic.total_cpu + 0.25 * (
                               abs(method1['ps']) * 1800 + abs(method1['worker']) * res_config0[aim1][
                           'mem_source']) / job_basic.total_mem
                sco2 = 0.75 * (res_config0[aim1]['worker'] * (
                        res_config0[aim1]['cpu_source'] - aim1_cpu)) / job_basic.total_cpu + 0.25 * (
                               res_config0[aim1]['worker'] * (
                               res_config0[aim1]['mem_source'] - aim1_mem)) / job_basic.total_mem
                if sco1 > sco2:
                    assign_config[aim1] = method1
                else:
                    assign_config[aim1] = method2
    else:
        print("Mode %d Do not find fit job to get modluation!!" % mode)
        return {}, mode

    return assign_config, mode

def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/tfdata/nodebase', help='save path')
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

def make_label_to_nodes(tasks2,base_job_name):
    print("start a labeling function!!!")
    base_job = reload_jobs_aim(base_job_name,-1)
    print("reload success!!!")
    try:
        tasks2["label"] = True
        print("start to label nodes!!!")
        point_base, cpu_base, memory_base, point_base_list = base_job.schedule_label()
        # tasks2[(str())]
        keyss = list(point_base.keys())
        tmp_tasks = tasks2['rank']
        tmp_task2 = tasks2['cpu']
        tmp_task3 = tasks2['mem']
        for kk in keyss:
            tmp_tasks[kk] = point_base_list.index(point_base[kk])
            tmp_task2[kk] = base_job.node_cpu[kk] - cpu_base[kk]*base_job.node_cpu[kk]
            tmp_task3[kk] = base_job.node_memory[kk] - memory_base[kk]*base_job.node_memory[kk]
        tasks2['rank'] = tmp_tasks
        tasks2['cpu'] = tmp_task2
        tasks2['mem'] = tmp_task3

        time.sleep(1.5)
        tasks2["label"] = False
        print("finish a label procedure")
        time.sleep(30.5)
    except Exception as eee:
        print("label nodes have errors:" + str(eee))
        # print(eee)
        tasks2["label"] = False
        # time.sleep(45)
        print("try with err again!!!")
    while True:
        time.sleep(72)
        try:
            tasks2["label"] = True
            print("start to label nodes!!!")
            point_base, cpu_base, memory_base, point_base_list = base_job.schedule_label()
            # tasks2[(str())]
            keyss = list(point_base.keys())
            tmp_tasks = tasks2['rank']
            tmp_task2 = tasks2['cpu']
            tmp_task3 = tasks2['mem']
            for kk in keyss:
                tmp_tasks[kk] = point_base_list.index(point_base[kk])
                tmp_task2[kk] = base_job.node_cpu[kk] - cpu_base[kk]*base_job.node_cpu[kk]
                tmp_task3[kk] = base_job.node_memory[kk] - memory_base[kk]*base_job.node_memory[kk]
            tasks2['rank'] = tmp_tasks
            tasks2['cpu'] = tmp_task2
            tasks2['mem'] = tmp_task3

            time.sleep(1.5)
            tasks2["label"] = False
            print("finish a label procedure")
            time.sleep(72)
        except Exception as eee:
            print("label nodes have errors:"+str(eee))
            # print(eee)
            tasks2["label"] = False
            time.sleep(45)
            print("try with err again!!!")

def generate_item(response,measurement):
    node_cpu = {}
    node_cpu['k8s-master'] = 64000 - 2500
    node_cpu['k8s-worker0'] = 24000 - 240
    node_cpu['k8s-worker2'] = 24000 - 650
    node_cpu['k8s-worker1'] = 16000 - 300
    node_cpu['k8s-worker3'] = 24000 - 360
    node_cpu['k8s-worker4'] = 24000 - 360
    node_cpu['k8s-worker5'] = 32000 - 320
    node_cpu['k8s-worker6'] = 24000 - 240
    node_cpu['k8s-worker7'] = 24000 - 240
    node_cpu['k8s-worker8'] = 24000 - 240
    # node_cpu['k8s-worker9'] = 16000 - 240
    node_cpu['k8s-worker10'] = 24000 - 200
    node_cpu['k8s-worker11'] = 24000 - 200
    node_cpu['k8s-worker12'] = 24000 - 240
    node_cpu['k8s-worker13'] = 24000 - 240
    node_cpu['k8s-worker14'] = 24000 - 240
    node_cpu['k8s-worker15'] = 32000 - 220
    node_cpu['k8s-worker16'] = 24000 - 240
    node_cpu['k8s-worker17'] = 24000 - 210
    # node_cpu['k8s-worker18'] = 16000 - 150
    node_cpu['k8s-worker19'] = 32000 - 240
    # node_cpu['k8s-worker20'] = 24000 - 150

    node_memory = {}

    node_memory['k8s-master'] = float(251 * 1024 - 12000)
    node_memory['k8s-worker0'] = float(94 * 1024 - 1400)
    node_memory['k8s-worker2'] = float(94 * 1024 - 4200)
    node_memory['k8s-worker1'] = float(125 * 1024 - 1200)
    node_memory['k8s-worker3'] = float(94 * 1024 - 1800)
    node_memory['k8s-worker4'] = float(188 * 1024 - 1000)
    node_memory['k8s-worker5'] = float(125 * 1024 - 1800)
    node_memory['k8s-worker6'] = float(94 * 1024 - 1200)
    node_memory['k8s-worker7'] = float(94 * 1024 - 3000)
    node_memory['k8s-worker8'] = float(94 * 1024 - 1250)
    # node_memory['k8s-worker9'] = float(62 * 1024 - 1600)
    node_memory['k8s-worker10'] = float(94 * 1024 - 1200)
    node_memory['k8s-worker11'] = float(94 * 1024 - 1400)
    # node_memory['k8s-worker12'] = float(62 * 1024 - 2000)
    # node_memory['k8s-worker13'] = float(62 * 1024 - 2000)
    node_memory['k8s-worker12'] = float(94 * 1024 - 1500)
    node_memory['k8s-worker13'] = float(94 * 1024 - 1400)
    node_memory['k8s-worker14'] = float(94 * 1024 - 1800)
    # node_memory['k8s-worker15'] = float(62 * 1024 - 2000)
    node_memory['k8s-worker15'] = float(125 * 1024 - 1800)
    # node_memory['k8s-worker16'] = float(62 * 1024 - 2000)
    node_memory['k8s-worker16'] = float(94 * 1024 - 1800)
    # node_memory['k8s-worker17'] = float(94 * 1024 - 2000)
    node_memory['k8s-worker17'] = float(94 * 1024 - 1400)
    # node_memory['k8s-worker18'] = float(62 * 1024 - 2000)
    node_memory['k8s-worker19'] = float(125 * 1024 - 1400)
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
        self.node_cpu['k8s-master'] = 64000 - 2500
        self.node_cpu['k8s-worker0'] = 24000 - 240
        self.node_cpu['k8s-worker2'] = 24000 - 650
        self.node_cpu['k8s-worker1'] = 16000 - 300
        self.node_cpu['k8s-worker3'] = 24000 - 360
        self.node_cpu['k8s-worker4'] = 24000 - 360
        self.node_cpu['k8s-worker5'] = 32000 - 320
        self.node_cpu['k8s-worker6'] = 24000 - 240
        self.node_cpu['k8s-worker7'] = 24000 - 240
        self.node_cpu['k8s-worker8'] = 24000 - 240
        # self.node_cpu['k8s-worker9'] = 16000 - 240
        self.node_cpu['k8s-worker10'] = 24000 - 200
        self.node_cpu['k8s-worker11'] = 24000 - 200
        self.node_cpu['k8s-worker12'] = 24000 - 240
        self.node_cpu['k8s-worker13'] = 24000 - 240
        self.node_cpu['k8s-worker14'] = 24000 - 240
        self.node_cpu['k8s-worker15'] = 32000 - 220
        self.node_cpu['k8s-worker16'] = 24000 - 240
        self.node_cpu['k8s-worker17'] = 24000 - 210
        # node_cpu['k8s-worker18'] = 16000 - 150
        self.node_cpu['k8s-worker19'] = 32000 - 240
        self.node_memory = {}
        self.node_memory['k8s-master'] = float(251 * 1024 - 10000)
        self.node_memory['k8s-worker0'] = float(94 * 1024 - 1400)
        self.node_memory['k8s-worker2'] = float(94 * 1024 - 3200)
        self.node_memory['k8s-worker1'] = float(125 * 1024 - 1600)
        self.node_memory['k8s-worker3'] = float(94 * 1024 - 1200)
        self.node_memory['k8s-worker4'] = float(188 * 1024 - 1200)
        self.node_memory['k8s-worker5'] = float(125 * 1024 - 1800)
        self.node_memory['k8s-worker6'] = float(94 * 1024 - 1200)
        self.node_memory['k8s-worker7'] = float(94 * 1024 - 1400)
        self.node_memory['k8s-worker8'] = float(94 * 1024 - 1250)
        # self.node_memory['k8s-worker9'] = float(62 * 1024 - 1600)
        self.node_memory['k8s-worker10'] = float(94 * 1024 - 1200)
        self.node_memory['k8s-worker11'] = float(94 * 1024 - 1400)
        # node_memory['k8s-worker12'] = float(62 * 1024 - 2000)
        # node_memory['k8s-worker13'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker12'] = float(94 * 1024 - 1500)
        self.node_memory['k8s-worker13'] = float(94 * 1024 - 1400)
        self.node_memory['k8s-worker14'] = float(94 * 1024 - 1800)
        # node_memory['k8s-worker15'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker15'] = float(125 * 1024 - 1800)
        # node_memory['k8s-worker16'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker16'] = float(94 * 1024 - 1800)
        # node_memory['k8s-worker17'] = float(94 * 1024 - 2000)
        self.node_memory['k8s-worker17'] = float(94 * 1024 - 1400)
        # node_memory['k8s-worker18'] = float(62 * 1024 - 2000)
        self.node_memory['k8s-worker19'] = float(125 * 1024 - 1400)

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
            try:
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
                    self.cpu_per[item['metadata']['name']].append(
                        float(match_cpu(item['usage']['cpu']) / self.node_cpu[item['metadata']['name']]))
                    self.memory_per[item['metadata']['name']].append(
                        float(match_memory(item['usage']['memory']) / self.node_memory[item['metadata']['name']]))
                self.client.write_points(generate_item(response, self.measurement), 's', database=self.database)
                if len(self.time_mess['creation']) % 45 == 0 and len(self.time_mess['creation']) > 0:
                    frame_key = list(self.time_mess.keys())
                    frame_lens = [len(self.time_mess[fkey]) for fkey in frame_key]
                    frame_len = min(frame_lens)
                    for fk in frame_key:
                        self.time_mess[fk] = self.time_mess[fk][-frame_len:]
                    data_frame = pd.DataFrame(self.time_mess)
                    data_frame.to_csv(self.save_path + '/' + 'struct2.csv', mode='a+', index=False, sep=',')
                    print(self.cpu_mess)
                    print(len(self.cpu_mess))
                    for keyss in self.cpu_mess:
                        print(keyss + ": " + str(len(self.cpu_mess[keyss])))
                    frame_key = list(self.cpu_mess.keys())
                    frame_lens = [len(self.cpu_mess[fkey]) for fkey in frame_key]
                    frame_len = min(frame_lens)
                    for fk in frame_key:
                        self.cpu_mess[fk] = self.cpu_mess[fk][-frame_len:]
                    data_frame2 = pd.DataFrame(self.cpu_mess)
                    data_frame2.to_csv(self.save_path + '/' + 'node6_cpu.csv', mode='a+', index=False, sep=',')
                    frame_key = list(self.memory_mess.keys())
                    frame_lens = [len(self.memory_mess[fkey]) for fkey in frame_key]
                    frame_len = min(frame_lens)
                    for fk in frame_key:
                        self.memory_mess[fk] = self.memory_mess[fk][-frame_len:]
                    data_frame3 = pd.DataFrame(self.memory_mess)
                    data_frame3.to_csv(self.save_path + '/' + 'node6_memory.csv', mode='a+', index=False, sep=',')

                    frame_key = list(self.cpu_per.keys())
                    frame_lens = [len(self.cpu_per[fkey]) for fkey in frame_key]
                    frame_len = min(frame_lens)
                    for fk in frame_key:
                        self.cpu_per[fk] = self.cpu_per[fk][-frame_len:]
                    data_frame4 = pd.DataFrame(self.cpu_per)
                    data_frame4.to_csv(self.save_path + '/' + 'node6_cpu_per.csv', mode='a+', index=False, sep=',')

                    frame_key = list(self.memory_per.keys())
                    frame_lens = [len(self.memory_per[fkey]) for fkey in frame_key]
                    frame_len = min(frame_lens)
                    for fk in frame_key:
                        self.memory_per[fk] = self.memory_per[fk][-frame_len:]
                    data_frame5 = pd.DataFrame(self.memory_per)
                    data_frame5.to_csv(self.save_path + '/' + 'node6_memory_per.csv', mode='a+', index=False, sep=',')
                    f1 = open('/tfdata/nodebase/node6.json', 'r', encoding='utf-8')
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
                    f2 = open('/tfdata/nodebase/node6.json', 'w', encoding='utf-8')
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
            except Exception as exeee:
                print(exeee)
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

def catch_node_step_msg(jobs,job_name,tasks,lock,batch,flops,params,mode,task2):
    node_influx_client = influxdb.InfluxDBClient(host='192.168.128.10',username='admin',password='admin',database='NODEMESSAGE')
    step_influx_client = influxdb.InfluxDBClient(host='192.168.128.10',username='admin',password='admin',database='PREDICT')
    global XBOUND,XBOUND2
    global YBOUND,YBOUND2
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
    count23 = 0
    count000 = 0
    count0000 = 0
    countt00 = 0
    count111 = 0
    job.set_mod(11)
    save_mode_change(11,job.name,float(time.time()))
    time.sleep(10.5)
    tktkt = -1
    # tktkm =
    while True:
        pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job.name).items]
        run_result = pd.value_counts(pod_status)
        run_result_dict = dict(run_result)
        run_result_dict_c = run_result_dict.copy()
        run_result_dict['job'] = job.name
        print(run_result_dict)
        print(run_result_dict_c)
        if 'Running' in pod_status and run_result_dict['Running'] == (job.ps_replicas + job.worker_replicas):
            if int(job.mod) != 5:
                job.set_mod(5)
                save_mode_change(5, job.name, float(time.time()))

            count2 = 0
            count000 = 0
            countt00 = 0
            count111 = 0
            count = 0

            time.sleep(4.4)
            lock.acquire()
            print("Select the loayout!")
            tmp_layout = tasks['nslayout']
            tmp_keys = list(tmp_layout.keys())
            if job_name in tmp_keys and tmp_layout[job_name] == False:
                tmp_layout_config = {}
                for i in job.v1.list_namespaced_pod(job_name).items:
                    tmp_layout_config[i.metadata.name] = i.spec.node_name
                fp = open('/tfdata/k8snfs/setbase/' + job_name + '/layout.json', 'w', encoding='utf-8')
                # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                fp.write(dicc_json)
                fp.close()
                tmp_layout[job_name] = True
                tasks['nslayout'] = tmp_layout
            lock.release()
            break
        # elif 'Running' in pod_status:
        elif 'Succeeded' in pod_status or 'Failed' in pod_status:
            countt00 = 0
            count111 = 0
            count = 0
            if 'Pending' not in pod_status:
                count2 = 0
            if 'Succeeded' in pod_status:
                tktkt = 1
            if count000 <= 6:
                count000+=1
                time.sleep(4.32)
                print("slepp waiting success or failed")
                continue
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
                    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config_keys = list(res_job_config.keys())
                    if 'endtime' not in res_job_config_keys:
                        res_job_config['endtime'] = time.time() - 30
                    save_config(res_job_config, save_res_path)
                    if int(job.mod) != 6 and int(job.mod)!=7:
                        if tktkt:
                            job.set_mod(6)
                            save_mode_change(6, job.name, float(res_job_config['endtime']))
                        else:
                            job.set_mod(7)
                            save_mode_change(7, job.name, float(res_job_config['endtime']))
                    print("save end time success!!")
                except Exception as eee:
                    print("Delete Problem:")
                    print(eee)
                time.sleep(3.2)
                if job.name not in tmp_reload_ns and not tasks['modulate']:
                    time.sleep(3.8)
                    try:
                        exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                                       v1.list_namespaced_pod(job.name).items]
                        print(exit_reason)
                        exit_ict = {'reasons': exit_reason}
                        exit_path = '/tfdata/k8snfs/setbase/%s/exit_reason.json' % ns
                        exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                        fw_exit = open(exit_path, 'w', encoding='utf-8')
                        fw_exit.write(exit_json)
                        fw_exit.close()
                    except Exception as e:
                        print(e)
                    time.sleep(3.2)
                    lock.acquire()
                    try:
                        try:
                            command = 'kubectl delete -f /tfdata/tfcnn/expjobbase/' + job.name + '.yaml'
                            os.system(command)
                        except Exception as ess2:
                            print(ess2)
                        deletehelp2(job.name, v1)
                        # v1.delete_namespace(job.name)
                        ns_tmp = tasks['ns']
                        ns_tmp.remove(job.name)
                        tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        is_layout.pop(job.name)
                        if job.name in jobs:
                            jobs.remove(job.name)
                        tasks['nslayout'] = is_layout
                        tasks['count'] -= 1
                        if 'Failed' in pod_status and 'Succeeded' not in pod_status:
                            fails = tasks['fail']
                            fails.append(job.name)
                            tasks['fail'] = fails
                        finishes = tasks['finish']
                        finishes.append(job.name)
                        tasks['finish'] = finishes
                        print("finish remove %s from jobs!" % job.name)
                        lock.release()
                    except Exception as ee33:
                        print(ee33)
                        ns_tmp = tasks['ns']
                        if job.name in ns_tmp:
                            ns_tmp.remove(job.name)
                            tasks['ns'] = ns_tmp
                        is_layout = tasks['nslayout']
                        if job.name in list(is_layout.keys()):
                            is_layout.pop(job.name)
                            tasks['nslayout'] = is_layout
                        # if job.name in jobs:
                        #     jobs.remove(job.name)
                        if job.name in jobs:
                            jobs.remove(job.name)
                        ns_tmp = tasks['ns']
                        tasks['count'] = len(ns_tmp)
                        if 'Failed' in pod_status and 'Succeeded' not in pod_status:
                            fails = tasks['fail']
                            fails.append(job.name)
                            tasks['fail'] = fails
                        finishes = tasks['finish']
                        if job.name not in finishes:
                            finishes.append(job.name)
                            tasks['finish'] = finishes
                        print("finish remove %s from jobs!" % job.name)
                        lock.release()
                    return
                else:
                    time.sleep(3.6)
        elif 'Pending' in pod_status and 'Succeeded' not in pod_status and 'Failed' not in pod_status:
            countt00 = 0
            count111 = 0
            count = 0
            # count000
            if 'Succeeded' not in pod_status and 'Failed' not in pod_status:
                count000 = 0
            # pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
            tmp_layout = tasks['nslayout']
            tmp_keys = list(tmp_layout.keys())
            if job_name in tmp_keys:
                tmp_layout_config = {}
                for i in job.v1.list_namespaced_pod(job_name).items:
                    if i.status.phase == 'Running':
                        tmp_layout_config[i.metadata.name] = i.spec.node_name
                if tmp_layout_config:
                    fp = open('/tfdata/k8snfs/setbase/' + job_name + '/layout.json', 'w', encoding='utf-8')
                    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    fp.write(dicc_json)
                    fp.close()
            if int(job.mod)!=4:
                job.set_mod(4)
                save_mode_change(4, job.name, float(time.time()))
            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
            res_config = load_config(save_res_path)
            keys_res = res_config.keys()
            if 'reloadtime' not in keys_res:
                res_config['reloadtime'] = []
            # 'cpu_high': cpu_base, 'memory_base': mem_base
            if count2 < 3:
                count23 = count23 + 1
                if count2 == 0:
                    time.sleep(1.3)
                if count23 % 5 == 0:
                    print("apply resource!")
                    if job.cpu_allocate > res_config['cpu_high']:
                        if math.ceil(job.cpu_allocate * 0.892) >= res_config['cpu_high']:
                            kpk = random.randint(2, 7) / 100
                            # job.retry
                            # job.repeat
                            tmp_mem_using = math.ceil(job.memory_allocate * (1 + kpk))
                            if job.retry <= 1:
                                if tmp_mem_using > res_config['memory_base'] * 1.22:
                                    tmp_mem_using = math.ceil(res_config['memory_base'] * 1.22)
                                save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.892), tmp_mem_using)
                                job.assignment_resource(math.ceil(job.cpu_allocate * 0.892), tmp_mem_using)
                            else:
                                if tmp_mem_using > res_config['memory_base'] * YBOUND[-1]:
                                    tmp_mem_using = math.ceil(res_config['memory_base'] * YBOUND[-1])
                                save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.892), tmp_mem_using)
                                job.assignment_resource(math.ceil(job.cpu_allocate * 0.892), tmp_mem_using)

                        else:
                            if job.retry <= 1:
                                kpk = random.randint(2, 7) / 100
                                tmp_mem_using = math.ceil(job.memory_allocate * (1 + kpk))
                                if tmp_mem_using > res_config['memory_base'] * 1.22:
                                    tmp_mem_using = math.ceil(res_config['memory_base'] * 1.22)
                                save_job_change_resource(job.name, res_config['cpu_high'], tmp_mem_using)
                                job.assignment_resource(res_config['cpu_high'], tmp_mem_using)
                            else:
                                kpk = random.randint(2, 7) / 100
                                tmp_mem_using = math.ceil(job.memory_allocate * (1 + kpk))
                                if tmp_mem_using > res_config['memory_base'] * YBOUND[-1]:
                                    tmp_mem_using = math.ceil(res_config['memory_base'] * YBOUND[-1])
                                save_job_change_resource(job.name, res_config['cpu_high'], tmp_mem_using)
                                job.assignment_resource(res_config['cpu_high'], tmp_mem_using)
                    else:
                        kpk = random.randint(2, 7) / 100
                        tmp_mem_using = math.ceil(job.memory_allocate * (1 + kpk))
                        if job.retry <= 1:
                            if tmp_mem_using > res_config['memory_base'] * 1.22:
                                tmp_mem_using = math.ceil(res_config['memory_base'] * 1.22)
                        else:
                            if tmp_mem_using > res_config['memory_base'] * YBOUND[-1]:
                                tmp_mem_using = math.ceil(res_config['memory_base'] * YBOUND[-1])
                        tmp_cpu_using = math.ceil(job.cpu_allocate * 0.925)
                        if tmp_cpu_using <= math.ceil(0.475 * res_config['cpu_high']):
                            tmp_cpu_using = math.ceil(0.475 * res_config['cpu_high'])
                        save_job_change_resource(job.name, tmp_cpu_using, tmp_mem_using)
                        job.assignment_resource(tmp_cpu_using, tmp_mem_using)
                    print("modulate the cpu!!")
                    if job.memory_allocate > 1.15 * res_config['memory_base']:
                        #  "cpu_high": 15780,
                        #     "memory_base": 32113,
                        if math.ceil(job.memory_allocate * 0.92) >= 1.15 * res_config['memory_base']:
                            save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                            job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                        elif math.ceil(job.memory_allocate * 0.95) >= 1.15 * res_config['memory_base']:
                            save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.95))
                            job.assignment_resource(job.cpu_allocate, math.floor(job.memory_allocate * 0.95))
                        else:
                            save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.985))
                            job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.985))
                        print("modulate the memory!!")
                    else:
                        tmp_memo_allo = math.ceil(job.memory_allocate * 0.985)
                        if tmp_memo_allo < math.ceil(res_config['memory_base']) * 1.077:
                            tmp_memo_allo = math.ceil(res_config['memory_base'] * 1.077)
                        # else:
                        #     tmp_memo_allo = math.ceil(job.memory_allocate * 0.98)
                        save_job_change_resource(job.name, job.cpu_allocate, tmp_memo_allo)
                        job.assignment_resource(job.cpu_allocate, tmp_memo_allo)
                    time.sleep(5.1)
                    count2 += 1
                if count2 != 0:
                    time.sleep(3.58)
            elif count2 == 3:
                count23 = count23 + 1
                if count23 % 5 == 0:
                    print("reschedule try!!")
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, aim_step, mode=1)
                    # aim_step = aim_step
                    time_1 = 0
                    # lock.acquire()
                    while True:
                        lock.acquire()
                        if not task2['label']:
                            tmp_retry_job = tasks['retry']
                            tmp_retry_job.append(job.name)
                            tasks['retry'] = tmp_retry_job
                            tmp_layout = tasks['nslayout']
                            tmp_layout[job.name] = False
                            tasks['nslayout'] = tmp_layout
                            time1 = time.time()
                            job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, job.worker_replicas,
                                         (job.ps_replicas),mode=1)
                            time2 = time.time()
                            tmp_retry_job = tasks['retry']
                            tmp_retry_job.remove(job.name)
                            tasks['retry'] = tmp_retry_job
                            tmp_reload = res_config['reloadtime']
                            tmp_reload.append((time2 - time1))
                            res_config['reloadtime'] = tmp_reload
                            save_config(res_config, save_res_path)
                            lock.release()
                            break
                        else:
                            lock.release()
                            time.sleep(2.8)
                    time.sleep(4.8)
                    job.write_retry(mode=0)
                    count2 += 1
                    print("reschedule again done!")
                    time.sleep(2.2)
                    # if count2 != 3:
                time.sleep(3.58)
            elif job.worker_replicas > 1:
                count23 = count23+1
                if count23 % 5 == 0:
                    if job.ps_replicas > 1:
                        tmp_ps_rep = job.ps_replicas
                        if job.ps_replicas > job.worker_replicas:
                            tmp_ps_rep = job.worker_replicas
                        tmp_replicas = job.worker_replicas
                        print("reduce worker number!!")
                        bili = math.floor(job.worker_replicas / tmp_ps_rep)
                        aim_tmp_replicas = int(job.worker_replicas - bili)
                        if tmp_ps_rep > 1:
                            if aim_tmp_replicas >= 4 * (tmp_ps_rep - 1):
                                aim_tmp_replicas = 4 * (tmp_ps_rep - 1)
                            if aim_tmp_replicas <= tmp_ps_rep - 1:
                                aim_tmp_replicas = tmp_ps_rep - 1
                        else:
                            if aim_tmp_replicas >= 4:
                                aim_tmp_replicas = 4
                            if aim_tmp_replicas <= 1:
                                aim_tmp_replicas = 1
                        if aim_tmp_replicas < 1:
                            aim_tmp_replicas = 1
                        # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])
                        print(aim_step)
                        # aim_step = math.ceil((aim_step * tmp_replicas) / (job.worker_replicas - 1))
                        aim_step = math.ceil((aim_step * tmp_replicas) / (aim_tmp_replicas))
                        if tmp_ps_rep > 1:
                            save_job_change_layout(job.name, tmp_ps_rep - 1, (aim_tmp_replicas), aim_step, mode=1)
                        else:
                            save_job_change_layout(job.name, 1, (aim_tmp_replicas), aim_step, mode=1)
                        # lock.acquire()
                        while True:
                            lock.acquire()
                            if not task2['label']:
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.append(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_layout = tasks['nslayout']
                                tmp_layout[job.name] = False
                                tasks['nslayout'] = tmp_layout
                                time1 = time.time()
                                job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, (aim_tmp_replicas),
                                             tmp_ps_rep - 1)
                                time2 = time.time()
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.remove(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_reload = res_config['reloadtime']
                                tmp_reload.append((time2 - time1))
                                res_config['reloadtime'] = tmp_reload
                                save_config(res_config, save_res_path)
                                lock.release()
                                break
                            else:
                                lock.release()
                                time.sleep(2.8)

                        time.sleep(4.9)
                        job.write_retry(mode=0)
                        # count2 += 1
                        print("reduce worker number successfully!!")
                    else:
                        tmp_replicas = job.worker_replicas
                        print("reduce worker number!!")
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])
                        print(aim_step)
                        aim_step = math.ceil((aim_step * tmp_replicas) / (job.worker_replicas - 1))
                        aim_worker_replicas2 = job.worker_replicas - 1
                        if aim_worker_replicas2 < 1:
                            aim_worker_replicas2 = 1
                        save_job_change_layout(job.name, 1, aim_worker_replicas2, aim_step, mode=1)
                        # lock.acquire()
                        while True:
                            lock.acquire()
                            if not task2['label']:
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.append(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_layout = tasks['nslayout']
                                tmp_layout[job.name] = False
                                tasks['nslayout'] = tmp_layout
                                time1 = time.time()
                                job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, aim_worker_replicas2,1)
                                time2 = time.time()
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.remove(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_reload = res_config['reloadtime']
                                tmp_reload.append((time2 - time1))
                                res_config['reloadtime'] = tmp_reload
                                save_config(res_config, save_res_path)
                                lock.release()
                                break
                            else:
                                lock.release()
                                time.sleep(2.8)

                        time.sleep(4.9)
                        job.write_retry(mode=0)
                        # count2 += 1
                        print("reduce worker number successfully!!")
                time.sleep(3.38)
            elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                count23 = count23+1
                if count23 % 5 == 0:
                    if count2 < 6:
                        kpk = random.randint(1, 4) / 100
                        # save_job_change_resource(job.name, math.ceil(job.cpu_allocate*0.9), math.ceil(job.memory_allocate*(1+kpk)))
                        tmp_reuse_mem = math.ceil(job.memory_allocate * (1 + kpk))
                        if tmp_reuse_mem > 1.15 * res_config['memory_base']:
                            tmp_reuse_mem = math.floor(1.15 * res_config['memory_base'])
                        tmp_reuse_cpu = math.ceil(job.cpu_allocate * 0.95)
                        if tmp_reuse_cpu <= 0.475 * res_config['cpu_high']:
                            tmp_reuse_cpu = math.ceil(0.475 * res_config['cpu_high'])

                        save_job_change_resource(job.name, tmp_reuse_cpu, tmp_reuse_mem)
                        job.assignment_resource(tmp_reuse_cpu, tmp_reuse_mem)
                        count2+=1
                        time.sleep(3.0)
                        print("modulate CPU before goto Next count2: %d" % count2)
                    if count2 == 6:
                        print("reschedule try before next!!")
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])
                        print(aim_step)
                        save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, aim_step, mode=1)
                        # aim_step = aim_step
                        time_1 = 0
                        # lock.acquire()
                        while True:
                            lock.acquire()
                            if not task2['label']:
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.append(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_layout = tasks['nslayout']
                                tmp_layout[job.name] = False
                                tasks['nslayout'] = tmp_layout
                                time1 = time.time()
                                job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, job.worker_replicas,
                                             (job.ps_replicas), mode=1)
                                time2 = time.time()
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.remove(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_reload = res_config['reloadtime']
                                tmp_reload.append((time2 - time1))
                                res_config['reloadtime'] = tmp_reload
                                save_config(res_config, save_res_path)
                                lock.release()
                                break
                            else:
                                lock.release()
                                time.sleep(2.8)
                        time.sleep(4.8)
                        job.write_retry(mode=0)
                        count2 += 1
                        print("reschedule again done before next!")
                        time.sleep(2.2)
                    if count2 > 6:
                        try:
                            aim_steps = step_influx_client.query(
                                "select training_step from " + measure_t + " order by desc limit 1")
                            aim_key = aim_steps.keys()
                            result_inter = aim_steps[aim_key[0]]
                            result_items = list(result_inter)
                            aim_step = int(result_items[0]['training_step'])
                            print(aim_step)
                            save_job_change_layout(job.name, 1, 1, aim_step, mode=1)
                        except Exception as ee32:
                            print(ee32)

                        lock.acquire()
                        try:
                            command = 'kubectl delete -f /tfdata/tfcnn/expjobbase/' + job.name + '.yaml'
                            os.system(command)
                            deletehelp2(job.name, v1)
                            # v1.delete_namespace(job.name)
                            ns_tmp = tasks['ns']
                            ns_tmp.remove(job.name)
                            tasks['ns'] = ns_tmp
                            is_layout = tasks['nslayout']
                            is_layout.pop(job.name)
                            if job.name in jobs:
                                jobs.remove(job.name)
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
                        except Exception as ee33:
                            ns_tmp = tasks['ns']
                            if job.name in ns_tmp:
                                ns_tmp.remove(job.name)
                                tasks['ns'] = ns_tmp
                            is_layout = tasks['nslayout']
                            if job.name in list(is_layout.keys()):
                                is_layout.pop(job.name)
                                tasks['nslayout'] = is_layout

                            if job.name in jobs:
                                jobs.remove(job.name)
                            ns_tmp = tasks['ns']
                            # job_tmp.pop(ns)
                            # tasks['job'] = job_tmp
                            tasks['count'] = len(ns_tmp)
                            tmp_next = tasks['next']
                            if job.name not in tmp_next:
                                tmp_next.append(job.name)
                                tasks['next'] = tmp_next
                            tmp_next_time_config = tasks['nexttimes']
                            if job.name not in list(tmp_next_time_config.keys()):
                                tmp_next_time_config[job.name] = 0
                                tasks['nexttimes'] = tmp_next_time_config
                            lock.release()
                            print(ee33)
                        time.sleep(5.7)
                        jieshu = True
                        print("Exception exit! Pending Problem!")
                        count2 += 1
                        return
                    else:
                        count2 += 1
                    # time.sleep(17.9)
                time.sleep(3.58)
        else:
            print("%s no condition, sleep!!" % job.name)
            time.sleep(10.2)
    count11 = 0
    countt00 = 0
    count22 = 0
    count223 = 0
    count000 = 0
    count0000 = 0
    count111 = 0
    tktkt = -1
    while True:
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
            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
            res_job_config = load_config(save_res_path)
            res_job_config_keys = list(res_job_config.keys())
            if (not pod_status) or 'Succeeded' in pod_status or 'Failed' in pod_status:
                # if 'Succeeded' in pod_status:
                #     tktkt = 1
                if count0000 <= 3:
                    time.sleep(3.2)
                    count0000+=1
                    continue
                else:
                    lock.acquire()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.remove(job.name)
                    tasks['retry'] = tmp_retry_job
                    tmp_retry_solution3 = tasks['solution']
                    tmp_retry_solution3.pop(job.name)
                    tasks['solution'] = tmp_retry_solution3
                    lock.release()
            else:
                count0000 = 0
                if int(solution['type']) == 2:
                    save_job_change_resource(job.name, math.ceil(solution['cpu']), math.ceil(solution['mem']))
                    job.set_mod(9)
                    save_mode_change(9,job.name,float(time.time()))
                    lock.acquire()
                    # method2 = {'type':2,'cpu':aim1_cpu,'mem':aim1_mem}
                    job.assignment_resource(math.ceil(solution['cpu']), math.ceil(solution['mem']))
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.remove(job.name)
                    tasks['retry'] = tmp_retry_job
                    tmp_retry_solution3 = tasks['solution']
                    tmp_retry_solution3.pop(job.name)
                    tasks['solution'] = tmp_retry_solution3
                    lock.release()
                    if int(job.mod) != 5:
                        job.set_mod(5)
                        save_mode_change(5, job.name, float(time.time()))
                elif int(solution['type']) == 1:
                    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                    # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                    # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                    # 'cpu_high':cpu_base,'batch_res':batch_res,
                    # 'flops_res':flops_res,'params_res':params_res}
                    res_config = load_config(save_res_path)
                    keys_res = res_config.keys()
                    if 'reloadtime' not in keys_res:
                        res_config['reloadtime'] = []
                    tmp_replicas = job.worker_replicas
                    aim_steps = step_influx_client.query(
                        "select training_step from " + measure_t + " order by desc limit 1")
                    aim_key = aim_steps.keys()
                    result_inter = aim_steps[aim_key[0]]
                    result_items = list(result_inter)
                    aim_step = int(result_items[0]['training_step'])
                    print(aim_step)
                    aim_worker_replicas = job.worker_replicas + int(solution['worker'])
                    if aim_worker_replicas <= 0:
                        aim_worker_replicas = 1
                    aim_step = math.ceil((aim_step * tmp_replicas) / (aim_worker_replicas))
                    aim_ps_replicas = job.ps_replicas + int(solution['ps'])
                    if aim_ps_replicas <= 0:
                        aim_ps_replicas = 1
                    if aim_worker_replicas <= 0:
                        aim_worker_replicas = 1
                    save_job_change_layout(job.name, aim_ps_replicas, aim_worker_replicas, aim_step, mode=1)
                    job.set_mod(8)
                    save_mode_change(8,job.name,float(time.time()))
                    # lock.acquire()
                    while True:
                        lock.acquire()
                        if not task2['label']:
                            time1 = time.time()
                            job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, aim_worker_replicas,
                                         aim_ps_replicas)
                            time2 = time.time()
                            tmp_retry_job = tasks['retry']
                            tmp_retry_job.remove(job.name)
                            tasks['retry'] = tmp_retry_job
                            tmp_retry_solution3 = tasks['solution']
                            tmp_retry_solution3.pop(job.name)
                            tasks['solution'] = tmp_retry_solution3
                            time.sleep(2.7)
                            lock.release()
                            tmp_reload = res_config['reloadtime']
                            tmp_reload.append((time2 - time1))
                            res_config['reloadtime'] = tmp_reload
                            save_config(res_config, save_res_path)
                            break
                        else:
                            lock.release()
                            time.sleep(2.8)
                    # method1 = {'type': 1, 'ps': 0, 'worker': 1}

                    time.sleep(3.8)
                    count33 = 0
                    while count33 < 36:
                        pod_status3 = [i.status.phase for i in v1.list_namespaced_pod(job.name).items]
                        run_result3 = pd.value_counts(pod_status3)
                        run_result_dict3 = dict(run_result3)
                        run_result_dict_c3 = run_result_dict3.copy()
                        run_result_dict3['job'] = job.name
                        print("Retry assignmenting for pods:")
                        print(run_result_dict3)
                        if 'Running' in pod_status3 and run_result_dict3['Running'] == (
                                job.ps_replicas + job.worker_replicas):
                            if int(job.mod) != 5:
                                job.set_mod(5)
                                save_mode_change(5, job.name, float(time.time()))
                            break
                        else:
                            count33+=1
                            time.sleep(2.72)
                    job.write_retry(mode=0)
        else:
            count0000 = 0
            pod_status2 = [i.status.phase for i in v1.list_namespaced_pod(job.name).items]
            run_result2 = pd.value_counts(pod_status2)
            run_result_dict2 = dict(run_result2)
            run_result_dict_c2 = run_result_dict2.copy()
            run_result_dict2['job'] = job.name
            print(run_result_dict2)
            if 'Running' in pod_status2 and run_result_dict2['Running'] == (job.ps_replicas + job.worker_replicas) and run_result_dict2['Running']>1:
                if int(job.mod) != 5:
                    job.set_mod(5)
                    save_mode_change(5, job.name, float(time.time()))
                count22 = 0
                count000 = 0
                countt00 = 0
                count111 = 0
                count11 = 0
                time.sleep(5.6)
                lock.acquire()
                print("Select the loayout!")
                tmp_layout = tasks['nslayout']
                lock.release()
                tmp_keys = list(tmp_layout.keys())
                if job_name in tmp_keys and tmp_layout[job_name] == False:
                    tmp_layout_config = {}
                    for i in job.v1.list_namespaced_pod(job_name).items:
                        tmp_layout_config[i.metadata.name] = i.spec.node_name
                    fp = open('/tfdata/k8snfs/setbase/' + job_name + '/layout.json', 'w', encoding='utf-8')
                    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    fp.write(dicc_json)
                    fp.close()
                    tmp_layout[job_name] = True
                    lock.acquire()
                    tasks['nslayout'] = tmp_layout
                    lock.release()
                else:
                    time.sleep(6.9)
            elif ('Succeeded' in pod_status2 or 'Failed' in pod_status2):
                countt00 = 0
                count111 = 0
                count11 = 0

                if 'Pending' not in pod_status2:
                    count22 = 0

                if 'Succeeded' in pod_status2:
                    tktkt = 1
                if count000 <= 6:
                    time.sleep(3.8)
                    count000+=1
                    print("slepp waiting success or failed")
                    continue
                else:
                    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config_keys = list(res_job_config.keys())
                    if 'endtime' not in res_job_config_keys:
                        res_job_config['endtime'] = time.time() - 10
                    save_config(res_job_config, save_res_path)
                    if int(job.mod) != 6 and int(job.mod)!=7:
                        if tktkt:
                            job.set_mod(6)
                            save_mode_change(6, job.name, float(res_job_config['endtime']))
                        else:
                            job.set_mod(7)
                            save_mode_change(7, job.name, float(res_job_config['endtime']))

                    time.sleep(3)
                    if (job.name not in tmp_retrys) and not tasks['modulate']:
                        try:
                            exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                                           v1.list_namespaced_pod(job.name).items]
                            print(exit_reason)
                            exit_ict = {'reasons': exit_reason}
                            exit_path = '/tfdata/k8snfs/setbase/%s/exit_reason.json' % ns
                            exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                            fw_exit = open(exit_path, 'w', encoding='utf-8')
                            fw_exit.write(exit_json)
                            fw_exit.close()
                        except Exception as e:
                            print(e)
                        time.sleep(5)
                        lock.acquire()
                        try:
                            command = 'kubectl delete -f /tfdata/tfcnn/expjobbase/' + job.name + '.yaml'
                            os.system(command)
                            print("delete this job %s!!!" % job.name)
                            deletehelp2(job.name, v1)
                            # v1.delete_namespace(job.name)
                            ns_tmp = tasks['ns']
                            ns_tmp.remove(job.name)
                            tasks['ns'] = ns_tmp
                            is_layout = tasks['nslayout']
                            is_layout.pop(job.name)
                            # for i in range(len(jobs)):
                            #     if jobs[i] == job.name:
                            #         jobs.pop(i)
                            #         break
                            if job.name in jobs:
                                jobs.remove(job.name)
                            tasks['nslayout'] = is_layout
                            tasks['count'] -= 1
                            # jobs_tmp = jobs
                            # jobs_tmp.remove(job.name)
                            # jobs = jobs_tmp
                            if 'Failed' in pod_status2 and 'Succeeded' not in pod_status2:
                                fails = tasks['fail']
                                fails.append(job.name)
                                tasks['fail'] = fails
                            finishes = tasks['finish']
                            finishes.append(job.name)
                            tasks['finish'] = finishes
                            lock.release()
                        except Exception as eess:
                            ns_tmp = tasks['ns']
                            if job.name in ns_tmp:
                                ns_tmp.remove(job.name)
                                tasks['ns'] = ns_tmp
                            is_layout = tasks['nslayout']
                            if is_layout in list(is_layout.keys()):
                                is_layout.pop(job.name)
                                tasks['nslayout'] = is_layout
                            if job.name in jobs:
                                jobs.remove(job.name)
                            ns_tmp = tasks['ns']
                            tasks['count']  = len(ns_tmp)
                            if 'Failed' in pod_status2 and 'Succeeded' not in pod_status2:
                                fails = tasks['fail']
                                fails.append(job.name)
                                tasks['fail'] = fails
                            finishes = tasks['finish']
                            if job.name not in finishes:
                                finishes.append(job.name)
                                tasks['finish'] = finishes
                            lock.release()
                            print(eess)
                        break
            elif 'Pending' in pod_status2 and 'Succeeded' not in pod_status2 and 'Failed' not in pod_status2:
                # pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job_name).items]
                tmp_layout = tasks['nslayout']
                tmp_keys = list(tmp_layout.keys())
                countt00 = 0
                count111 = 0
                count11 = 0

                if 'Succeeded' not in pod_status2 and 'Failed' not in pod_status2:
                    count000 = 0
                if job_name in tmp_keys:
                    lock.acquire()
                    tmp_layout[job_name] = False
                    tasks['nslayout'] = tmp_layout
                    lock.release()
                    tmp_layout_config = {}
                    for i in job.v1.list_namespaced_pod(job_name).items:
                        if i.status.phase == 'Running':
                            tmp_layout_config[i.metadata.name] = i.spec.node_name
                    if tmp_layout_config:
                        fp = open('/tfdata/k8snfs/setbase/' + job_name + '/layout.json', 'w', encoding='utf-8')
                        # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                        dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                        fp.write(dicc_json)
                        fp.close()
                if int(job.mod) != 4:
                    job.set_mod(4)
                    save_mode_change(4, job.name, float(time.time()))
                save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                res_config = load_config(save_res_path)
                keys_res = res_config.keys()
                if 'reloadtime' not in keys_res:
                    res_config['reloadtime'] = []
                # 'cpu_high': cpu_base, 'memory_base': mem_base
                if count22 < 4:
                    count223 = count223 + 1
                    if count22 == 0:
                        time.sleep(1.3)
                    if count223 % 5 == 0:
                        print("apply resource!")
                        if job.cpu_allocate > res_config['cpu_high']:
                            if math.ceil(job.cpu_allocate * 0.892) >= res_config['cpu_high']:
                                kpk = random.randint(1, 6) / 100
                                tmp_mem_using = math.ceil(job.memory_allocate * (1 + kpk))
                                # YBOUND[-1] * 1.92 * mem_base
                                if tmp_mem_using > res_config['memory_base'] * YBOUND[-1] * 1.8:
                                    tmp_mem_using = math.ceil(res_config['memory_base'] * YBOUND[-1] * 1.8)
                                tmp_cpu_using = math.ceil(job.cpu_allocate * 0.892)
                                if tmp_cpu_using <= res_config['cpu_high'] * 0.475:
                                    tmp_cpu_using = math.ceil(res_config['cpu_high'] * 0.475)
                                save_job_change_resource(job.name, tmp_cpu_using, tmp_mem_using)
                                job.assignment_resource(tmp_cpu_using, tmp_mem_using)
                            else:
                                save_job_change_resource(job.name, res_config['cpu_high'], job.memory_allocate)
                                job.assignment_resource(res_config['cpu_high'], job.memory_allocate)
                        else:
                            tmp_cpu_using = math.ceil(job.cpu_allocate * 0.925)
                            if tmp_cpu_using <= res_config['cpu_high'] * 0.475:
                                tmp_cpu_using = math.ceil(res_config['cpu_high'] * 0.475)
                            kpk = random.randint(1, 4) / 100
                            tmp_mem_using = math.ceil(job.memory_allocate * (1 + kpk))
                            if tmp_mem_using > res_config['memory_base'] * YBOUND[-1] * 1.525:
                                tmp_mem_using = math.ceil(res_config['memory_base'] * YBOUND[-1] * 1.525)
                            # save_job_change_resource(job.name, tmp_cpu_using, tmp_mem_using)
                            # job.assignment_resource(tmp_cpu_using, tmp_mem_using)
                            save_job_change_resource(job.name, tmp_cpu_using, tmp_mem_using)
                            job.assignment_resource(tmp_cpu_using, tmp_mem_using)
                        print("modulate the cpu!!")
                        if job.memory_allocate > 1.15 * res_config['memory_base']:
                            #  "cpu_high": 15780,
                            #     "memory_base": 32113,
                            if math.ceil(job.memory_allocate * 0.92) >= 1.15 * res_config['memory_base']:
                                save_job_change_resource(job.name, job.cpu_allocate,
                                                         math.ceil(job.memory_allocate * 0.92))
                                job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                            elif math.ceil(job.memory_allocate * 0.95) >= 1.15 * res_config['memory_base']:
                                save_job_change_resource(job.name, job.cpu_allocate,
                                                         math.ceil(job.memory_allocate * 0.95))
                                job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.95))
                            else:
                                save_job_change_resource(job.name, job.cpu_allocate,
                                                         math.ceil(job.memory_allocate * 0.982))
                                job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.982))
                            print("modulate the memory!!")
                        else:
                            # save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                            # job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                            tmp_memo_allo = math.ceil(job.memory_allocate * 0.985)
                            if tmp_memo_allo < math.ceil(res_config['memory_base']) * 1.077:
                                tmp_memo_allo = math.ceil(res_config['memory_base'] * 1.077)
                            save_job_change_resource(job.name, job.cpu_allocate, tmp_memo_allo)
                            job.assignment_resource(job.cpu_allocate, tmp_memo_allo)
                        count22 += 1
                    if count22 != 0:
                        time.sleep(4)
                elif count22 == 4:
                    count223 = count223 + 1
                    if count223 % 5 == 0:
                        print("reschedule try!!")
                        # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                        aim_steps = step_influx_client.query(
                            "select training_step from " + measure_t + " order by desc limit 1")
                        aim_key = aim_steps.keys()
                        result_inter = aim_steps[aim_key[0]]
                        result_items = list(result_inter)
                        aim_step = int(result_items[0]['training_step'])
                        print(aim_step)
                        save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, aim_step, mode=1)
                        while True:
                            lock.acquire()
                            if not task2['label']:
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.append(job.name)
                                tasks['retry'] = tmp_retry_job
                                time1 = time.time()
                                job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, job.worker_replicas,
                                             (job.ps_replicas),mode=1)
                                time2 = time.time()
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.remove(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_reload = res_config['reloadtime']
                                tmp_reload.append((time2 - time1))
                                res_config['reloadtime'] = tmp_reload
                                save_config(res_config, save_res_path)
                                lock.release()
                                break
                            else:
                                lock.release()
                                time.sleep(2.8)
                        time.sleep(4.7)
                        job.write_retry(mode=0)
                        count22 += 1
                        time.sleep(2.3)
                        print("reschedule again done!")
                    time.sleep(4)
                elif job.worker_replicas > 1:
                    count223 = count223 + 1
                    if count223 % 5 == 0:
                        tmp_ps_rep = job.ps_replicas
                        if tmp_ps_rep > job.worker_replicas:
                            tmp_ps_rep = job.worker_replicas
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
                        aim_tmp_replicas = job.worker_replicas - 1
                        if aim_tmp_replicas < 1:
                            aim_tmp_replicas = 1
                        if (aim_tmp_replicas / tmp_ps_rep) <= 2:
                            tmp_ps_rep = math.floor(aim_tmp_replicas/2)
                        if tmp_ps_rep < 1:
                            tmp_ps_rep = 1
                        aim_step = math.ceil((aim_step * tmp_replicas) / aim_tmp_replicas)
                        save_job_change_layout(job.name, tmp_ps_rep, aim_tmp_replicas, aim_step, mode=1)
                        # lock.acquire()
                        while True:
                            lock.acquire()
                            if not task2['label']:
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.append(job.name)
                                tasks['retry'] = tmp_retry_job
                                time1 = time.time()
                                job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, aim_tmp_replicas,
                                             tmp_ps_rep)
                                time2 = time.time()
                                tmp_retry_job = tasks['retry']
                                tmp_retry_job.remove(job.name)
                                tasks['retry'] = tmp_retry_job
                                tmp_reload = res_config['reloadtime']
                                tmp_reload.append((time2 - time1))
                                res_config['reloadtime'] = tmp_reload
                                save_config(res_config, save_res_path)
                                lock.release()
                                break
                            else:
                                lock.release()
                                time.sleep(2.8)
                        time.sleep(5.2)
                        job.write_retry(mode=0)
                        # count22 += 1
                        print("reduce worker number successfully!!")
                    time.sleep(4)
                # time.sleep(17.9)
                elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                    count223 = count223+1
                    if count223 % 5 == 0:
                        if count22 < 6:
                            kpk = random.randint(1, 4) / 100
                            tmp_reuse_mem = math.ceil(job.memory_allocate * (1 + kpk))
                            if tmp_reuse_mem > res_config['memory_base'] * YBOUND[-1]:
                                tmp_reuse_mem = math.floor(res_config['memory_base'] * YBOUND[-1])
                            tmp_reuse_cpu = math.ceil(job.cpu_allocate * 0.95)
                            if tmp_reuse_cpu <= 0.475 * res_config['cpu_high']:
                                tmp_reuse_cpu = 0.475 * res_config['cpu_high']
                            save_job_change_resource(job.name, tmp_reuse_cpu, tmp_reuse_mem)
                            job.assignment_resource(tmp_reuse_cpu, tmp_reuse_mem)
                            print("modulate CPU before goto Next next22: %d" % count22)
                            count22+=1
                        if count22 == 6:
                            print("reschedule try before go to next!!")
                            # aim_step = step_influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
                            aim_steps = step_influx_client.query(
                                "select training_step from " + measure_t + " order by desc limit 1")
                            aim_key = aim_steps.keys()
                            result_inter = aim_steps[aim_key[0]]
                            result_items = list(result_inter)
                            aim_step = int(result_items[0]['training_step'])
                            print(aim_step)
                            save_job_change_layout(job.name, 1, 1, aim_step, mode=1)
                            # aim_step = aim_step
                            time_1 = 0
                            # lock.acquire()
                            while True:
                                lock.acquire()
                                if not task2['label']:
                                    tmp_retry_job = tasks['retry']
                                    tmp_retry_job.append(job.name)
                                    tasks['retry'] = tmp_retry_job
                                    time1 = time.time()
                                    job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, 1,
                                                 1, mode=1)
                                    time2 = time.time()
                                    tmp_retry_job = tasks['retry']
                                    tmp_retry_job.remove(job.name)
                                    tasks['retry'] = tmp_retry_job
                                    tmp_reload = res_config['reloadtime']
                                    tmp_reload.append((time2 - time1))
                                    res_config['reloadtime'] = tmp_reload
                                    save_config(res_config, save_res_path)
                                    lock.release()
                                    break
                                else:
                                    lock.release()
                                    time.sleep(2.8)
                            time.sleep(4.7)
                            job.write_retry(mode=0)
                            count22 += 1
                            time.sleep(2.3)
                            print("reschedule again done before go to next!")
                        if count22 >= 7:
                            aim_steps = step_influx_client.query(
                                "select training_step from " + measure_t + " order by desc limit 1")
                            aim_key = aim_steps.keys()
                            result_inter = aim_steps[aim_key[0]]
                            result_items = list(result_inter)
                            aim_step = int(result_items[0]['training_step'])
                            print(aim_step)
                            save_job_change_layout(job.name, 1, 1, aim_step, mode=1)
                            lock.acquire()
                            try:
                                command = 'kubectl delete -f /tfdata/tfcnn/expjobbase/' + job.name + '.yaml'
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
                            except Exception as eess:
                                ns_tmp = tasks['ns']
                                if job.name in ns_tmp:
                                    ns_tmp.remove(job.name)
                                    tasks['ns'] = ns_tmp
                                is_layout = tasks['nslayout']
                                if job.name in list(is_layout.keys()):
                                    is_layout.pop(job.name)
                                    tasks['nslayout'] = is_layout

                                if job.name in jobs:
                                    jobs.remove(job.name)
                                # for i in range(len(jobs)):
                                #     if jobs[i] == job.name:
                                #         jobs.pop(i)
                                #         break
                                ns_tmp = tasks['ns']
                                tasks['count'] = len(ns_tmp)
                                tmp_next = tasks['next']
                                if job.name not in tmp_next:
                                    tmp_next.append(job.name)
                                    tasks['next'] = tmp_next

                                tmp_next_time_config = tasks['nexttimes']
                                if job.name not in list(tmp_next_time_config.keys()):
                                    tmp_next_time_config[job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config

                                lock.release()
                                print(eess)
                            time.sleep(6.5)
                            jieshu = True
                            print("Exception exit! Pending Problem!")
                            count22 += 1
                            return
                        else:
                            count22 += 1
                            # time.sleep(17.5)
                    time.sleep(4)
            else:
                print("%s no condition, just sleep!!!" % job.name)
                time.sleep(10.2)

def get_load_value(node_index,cpu_base,memory_base,total_cpu_base,total_memory_base):
    keys = node_index.keys()
    alpha = 0.675
    cpu_score = 0
    memory_score = 0
    node_use = []
    node_cpu = []
    node_mem = []
    for key in keys:
        if node_index[key] <=11:
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
    cpu_score = cpu_score / 0.834
    memory_score = memory_score / 0.834
    return cpu_score,memory_score,node_cpu,node_mem

def check_path(name):
    train_dir = os.path.join('/tfdata/k8snfs/setbase/', name)
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
                'ps': job.ps_replicas
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

def save_mode_change(mod,job_name,happen_time):
    save_mod_path = '/tfdata/k8snfs/setbase/%s/%s_mod.json' % (job_name, job_name)
    try:
        job_mod_config = load_config(save_mod_path)
    except Exception as e1:
        job_mod_config = {'mod': mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                          '3': [], '4': [], '5': [],
                          '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
    job_mod_config['mod'] = mod
    try:
        job_mod_config[str(mod)].append(happen_time)
    except Exception as e2:
        job_mod_config[str(mod)] = []
        job_mod_config[str(mod)].append(happen_time)
    save_config(job_mod_config,save_mod_path)

def Submit_job(tasks,lock,v1,jobs,task2):
    try:
        rfr = joblib.load('rfr_batch.pkl')
    except Exception as e0:
        print(e0)
    print('start to reload')
    print(jobs)
    global LOSSHOST,LOSSPORT,sleep_last_length
    ADDR = (LOSSHOST,LOSSPORT)
    PREHOST = '192.168.128.5'
    PREPORT = 12529
    ADDR2 = (PREHOST,PREPORT)
    max_buffer_size = 38
    job_basic = reload_jobs_aim(tasks['last'],-1)
    max_free_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_free_load)
    max_wight_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_weight_load)
    worker_buffer = tasks['buffer']
    first_reload = False
    time.sleep(14)
    if worker_buffer:
        first_reload = True
    pool = multiprocessing.Pool(processes=32)
    for job0 in jobs:
        save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job0, job0)
        res_config = load_config(save_res_path)
        batch_res = res_config['batch_res']
        flops_res = res_config['flops_res']
        params_res = res_config['params_res']
        job01 = reload_jobs(job0,-1)
        # catch_node_step_msg(jobs=,job_name=,tasks=,lock=,batch=,flops=,params=,mode=)
        loss_server_conn(ADDR,job01.measure)
        pool.apply_async(catch_node_step_msg,args=(jobs,job0,tasks,lock,batch_res,flops_res,params_res,-1,task2))

    try:
        now_create = np.load('nowcreate.npy')
    except Exception as ee00:
        now_create = 0
        # np.save('nowcreate.npy')
        np.save('nowcreate.npy',now_create)
    global_count = 45
    need_s = load_config("modify.json")
    need_buffer = need_s['pool']
    try:
        makebuf = np.load("makebuf.npy")
    except Exception as eee011:
        makebuf = 0
        np.save("makebuf.npy",makebuf)

    if makebuf < 1:
        print('start to make a buffer pool!!')
        for bfjob in need_buffer:
            aim_job = reload_jobs_aim(bfjob, -1)
            save_change_path = '/tfdata/k8snfs/%s/%s_pw.json' % (aim_job.name, aim_job.name)
            aim_job_step_base = load_config(save_change_path)
            his_step_key = list(aim_job_step_base["changen"].keys())
            his_step = []
            for hsk in his_step_key:
                his_step.append(float(hsk))

            # list.sort(his_step)
            aim_job_step_base_pre = aim_job_step_base["changen"][str(min(his_step))]
            tmp_step0 = aim_job_step_base_pre["stepbefore"]
            ps_r = aim_job_step_base_pre["psbefore"]
            worker_r = aim_job_step_base_pre["wbefore"]
            if aim_job.template_id == 1:
                # def __init__(self,v1,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,repeat,channel1,channel2,channel3,channel4,channel5,channel6,channel7,channel8,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                #                  update_end=0.75, update_delay=2.0):
                job = VGGTask(template_id=aim_job.template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tmp_step0,
                              batch_size=aim_job.batch_size,
                              interval=aim_job.interval,
                              task_id=aim_job.task_id,
                              rtimes=aim_job.rtimes,
                              tag=aim_job.tag, channel1=aim_job.channel1, channel2=aim_job.channel2,
                              channel3=aim_job.channel3, channel4=aim_job.channel4, channel5=aim_job.channel5,
                              num_layer1=aim_job.num_layer1, num_layer2=aim_job.num_layer2,
                              num_layer3=aim_job.num_layer3,
                              num_layer4=aim_job.num_layer4, num_layer5=aim_job.num_layer5
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
                              'retry': job.retry}

                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                  '3': [], '4': [], '5': [],
                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                          'channel3': aim_job.channel3,
                          'channel4': aim_job.channel4,
                          'channel5': aim_job.channel5, 'num_layer1': aim_job.num_layer1,
                          'num_layer2': aim_job.num_layer2,
                          'num_layer3': aim_job.num_layer3, 'num_layer4': aim_job.num_layer4,
                          'num_layer5': aim_job.num_layer5}

            elif aim_job.template_id == 2:
                job = RESTask(template_id=aim_job.template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tmp_step0,
                              batch_size=aim_job.batch_size,
                              interval=aim_job.interval,
                              task_id=aim_job.task_id,
                              rtimes=aim_job.rtimes,
                              tag=aim_job.tag, bottle=aim_job.bottle, layer1=aim_job.layer1,
                              layer2=aim_job.layer2,
                              layer3=aim_job.layer3,
                              layer4=aim_job.layer4, channel1=aim_job.channel1, channel2=aim_job.channel2,
                              channel3=aim_job.channel3,
                              channel4=aim_job.channel4)

                job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                              'worker_replicas': job.worker_replicas,
                              'training_step': job.training_step,
                              'batch_size': job.batch_size,
                              'interval': job.interval,
                              'task_id': job.task_id, 'rtimes': job.rtimes,
                              'tag': job.tag, 'bottle': job.bottle, 'layer1': job.layer1,
                              'layer2': job.layer2,
                              'layer3': job.layer3,
                              'layer4': job.layer4, 'channel1': job.channel1, 'channel2': job.channel2,
                              'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry}

                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                  '3': [], '4': [], '5': [],
                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                          'channel3': aim_job.channel3,
                          'channel4': aim_job.channel4,
                          'layer1': aim_job.layer1, 'layer2': aim_job.layer2,
                          'layer3': aim_job.layer3, 'layer4': aim_job.layer4, 'bottle': aim_job.bottle}

            elif aim_job.template_id == 3:
                job = RETask(template_id=aim_job.template_id, ps_replicas=ps_r,
                             worker_replicas=worker_r,
                             training_step=tmp_step0,
                             batch_size=aim_job.batch_size,
                             interval=aim_job.interval,
                             task_id=aim_job.task_id,
                             rtimes=aim_job.rtimes,
                             tag=aim_job.tag, stack=aim_job.stack, channel1=aim_job.channel1,
                             channel2=aim_job.channel2,
                             channel3=aim_job.channel3, channel4=aim_job.channel4
                             )
                dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                          'channel3': aim_job.channel3,
                          'channel4': aim_job.channel4, 'stack_num': aim_job.stack}

                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                  '3': [], '4': [], '5': [],
                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                job_config = {
                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                    'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                    'batch_size': job.batch_size, 'interval': job.interval,
                    'task_id': job.task_id, 'rtimes': job.rtimes,
                    'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1,
                    'channel2': job.channel2,
                    'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry
                }

            elif aim_job.template_id == 4:

                job = XCETask(template_id=aim_job.template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tmp_step0,
                              batch_size=aim_job.batch_size,
                              interval=aim_job.interval,
                              task_id=aim_job.task_id,
                              rtimes=aim_job.rtimes,
                              tag=aim_job.tag,
                              repeat=aim_job.repeat,
                              channel1=aim_job.channel1, channel2=aim_job.channel2, channel3=aim_job.channel3,
                              channel4=aim_job.channel4, channel5=aim_job.channel5, channel6=aim_job.channel6,
                              channel7=aim_job.channel7,
                              channel8=aim_job.channel8)

                job_config = {
                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                    'worker_replicas': job.worker_replicas,
                    'training_step': job.training_step,
                    'batch_size': job.batch_size,
                    'interval': job.interval,
                    'task_id': job.task_id,
                    'rtimes': job.rtimes, 'tag': job.tag, 'repeat': job.repeat,
                    'channel1': job.channel1,
                    'channel2': job.channel2, 'channel3': job.channel3, 'channel4': job.channel4,
                    'channel5': job.channel5,
                    'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8,
                    'retry': job.retry
                }

                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                  '3': [], '4': [], '5': [],
                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                          'channel3': aim_job.channel3,
                          'channel4': aim_job.channel4, 'channel5': aim_job.channel5, 'channel6': aim_job.channel6,
                          'channel7': aim_job.channel7,
                          'channel8': aim_job.channel8, 'repeat': aim_job.repeat}

            else:
                job = DENTask(template_id=aim_job.template_id, ps_replicas=ps_r,
                              worker_replicas=worker_r,
                              training_step=tmp_step0,
                              batch_size=aim_job.batch_size,
                              interval=aim_job.interval,
                              task_id=aim_job.task_id,
                              rtimes=aim_job.rtimes,
                              tag=aim_job.tag, L=aim_job.L, k=aim_job.k, BC=aim_job.BC)

                job_config = {
                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                    'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                    'batch_size': job.batch_size, 'interval': job.interval, 'task_id': job.task_id,
                    'rtimes': job.rtimes,
                    'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC, 'retry': job.retry
                }

                # batch, flops, params = denfpmodel.denfp(batch=256, BC=0, k=24, L=100, num_classes=10)
                dict12 = {'batch': aim_job.batch_size, 'BC': aim_job.BC, 'k': aim_job.k, 'L': aim_job.L,
                          'num_classes': 10}

                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                  '3': [], '4': [], '5': [],
                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
            measure = job.measure
            time.sleep(1.5)

            pre_list = measure.split(" ")
            measure_t = pre_list[0] + 'T' + pre_list[-1]
            allow_p = check_path(measure_t)

            save_config_dir = task_submit_fix.check_path(job.name)
            save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job.name, job.name)
            allow_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job.name, measure_t)

            pre_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pre_client.connect(ADDR2)
            pre_client.send(bytes(measure, 'utf-8'))
            connect_try = 5
            try_times = 1
            connected = False
            msg_from_server_str = ''
            # while True:
            #     if try_times > connect_try:
            #         break
            #     msg_from_server = pre_client.recv(4096)
            #     if not msg_from_server:
            #         break
            #     msg_from_server_str = str(msg_from_server.decode('utf-8'))
            #     msg_from_server_list = msg_from_server_str.split(" ")
            #     if msg_from_server_list[0] == '400':
            #         connected = True
            #         break
            #     pre_client.send(bytes(measure, 'utf-8'))
            #     try_times = try_times + 1

            # if not connected:
            #     print("Connected or send message error!")
            #     pre_client.close()
                # lock.acquire()
                # if kkppkk == 0:
                #     tmp1 = tasks['task_id']
                #     tmp1[job.template_id - 1] -= 1
                #     tasks['task_id'] = tmp1
                #     tmp2 = tasks['rtimes']
                #     tmp2[job.template_id - 1] -= 1
                #     tasks['rtimes'] = tmp2
                # lock.release()
                # try:
                #     command0 = 'rm %s' % save_job_path
                #     aek = os.system(command0)
                #     command0 = 'rm %s' % allow_path
                #     ask = os.system(command0)
                # except Exception as eee0:
                #     print(eee0)
                # # lock.release()
                # continue
            # print(msg_from_server_str)
            # print("connected success!")
            # dict_json = json.dumps(dict12)
            # pre_client.send(bytes(dict_json, 'utf-8'))
            # ress = pre_client.recv(4096)
            # ress_str = str(ress.decode('utf-8'))
            # ress_lists = ress_str.split(' ')
            # if ress_lists[0] == '400':
            resource_allocation_base = '/tfdata/tfcnn/queue/%s_res.json' % bfjob
            resource_allocation = load_config(resource_allocation_base)
            # "flops_res": 109867927,
            #     "params_res": 15861810,
            batch_res = int(resource_allocation["batch_res"])
            flops_res = int(resource_allocation["flops_res"])
            params_res = int(resource_allocation["params_res"])
            # cpu_predict = float(ress_lists[-2])
            # "cpu_source": 6420,
            #     "mem_source": 14287,
            #     "cpu_high": 6420,
            #     "memory_base": 14287,
            cpu_base = math.ceil(resource_allocation["cpu_high"])
            mem_base = math.ceil(resource_allocation["memory_base"])
            # if job.template_id != 4:
            #     mem_base = math.ceil(1.672 * mem_predict)
            # else:
            #     mem_base = math.ceil(1.872 * mem_predict)
            #     res_to_server = '1'
            #     pre_client.send(bytes(res_to_server, 'utf-8'))
            # else:
            #     res_to_server = '0'
            #     pre_client.send(bytes(res_to_server, 'utf-8'))
            #     print("send response success!!")
            #     time.sleep(5.3)
            #     pre_client.close()
            #     print("some time later to try again!!")

                # if kkppkk == 0:
                #     tmp1 = tasks['task_id']
                #     tmp1[job.template_id - 1] -= 1
                #     tasks['task_id'] = tmp1
                #     tmp2 = tasks['rtimes']
                #     tmp2[job.template_id - 1] -= 1
                #     tasks['rtimes'] = tmp2
                #
                # try:
                #     command0 = 'rm %s' % save_job_path
                #     aek = os.system(command0)
                #     command0 = 'rm %s' % allow_path
                #     ask = os.system(command0)
                # except Exception as eee0:
                #     print(eee0)
                # time.sleep(27)
                # continue
            # pre_client.close()
            tmp_reload = tasks['reload']
            if tmp_reload == 0:
                alpha = random.randint(0, 7) * 0.1 + 0.5
                beta = random.randint(0, 18) * 0.1 + 0.875
            else:
                alpha = random.randint(2, 12) * 0.1 + 0.6
                beta = random.randint(0, 10) * 0.1 + 1
            alpha = 1
            beta = 1
            job.set_resource(cpu_source=(math.ceil(cpu_base * alpha)),
                             mem_source=(math.ceil(mem_base * beta)))

            save_config(job_config, save_job_path)
            allow_read = {}
            allow_read['OK'] = True
            allow_read['retry'] = 0
            allow_p = check_path(measure_t)

            save_config(allow_read, allow_path)

            mini_batch = predict_min_first(rfr=rfr, cpu_alpha=alpha, mem_alpha=beta, batch=batch_res,
                                           flops=flops_res, params=params_res)
            mini_batch = float(mini_batch)
            # if kkppkk == 0:
            #     deadline = mini_batch * job.training_step * (random.randint(66, 244) * 0.01) + 750
            # else:
            #     deadline = float(aim_job.deadline)
            deadline = float(resource_allocation["deadline"])
            print(deadline)
            print(type(deadline))
            # deadline = random.randint(3600, 18000)
            start_time = '%.3f' % time.time()
            start_time = float(start_time)
            job.set_deadline(deadline=deadline, start_time=start_time)
            job.set_mod(new_mod=0)
            job_mod_config['0'].append(start_time)
            job.set_mod(0)
            job_res_config = {'deadline': job.deadline, 'start_time': job.starttime,
                              'cpu_source': job.cpu_allocate,
                              'mem_source': job.memory_allocate, 'cpu_high': cpu_base,
                              'memory_base': mem_base, 'batch_res': batch_res,
                              'flops_res': flops_res, 'params_res': params_res, 'step_base': 0,
                              'reloadtime': []}
            save_config_dir = task_submit_fix.check_path(job.name)

            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)

            save_mod_path = '/tfdata/k8snfs/setbase/%s/%s_mod.json' % (job.name, job.name)
            save_config(job_res_config, save_res_path)
            save_config(job_mod_config, save_mod_path)
            now_create = now_create + 1
            np.save('nowcreate.npy', now_create)
            time.sleep(1.5)
            job.set_mod(2)
            save_mode_change(2, job.name, float(time.time()))
            lock.acquire()
            worker_buffer = tasks['buffer']
            worker_buffer.append(job.name)
            tasks['buffer'] = worker_buffer
            tmp_buffer_count = tasks['buffercount']
            tmp_buffer_count = tmp_buffer_count + 1
            tasks['buffercount'] = tmp_buffer_count
            lock.release()
            print("add %d job into waiting pool success!!" % tmp_buffer_count)
            time.sleep(sleep_last_length-2)

    makebuf = 1
    np.save("makebuf.npy",makebuf)
    while True:
        print("Global Count is :%d" % global_count)
        if tasks['start']==False:
            break
        # and global_count%45 > 1
        tmp_aim_set = tasks['aim']
        tmp_next_set = tasks['next']
        ymp_ns_set = tasks['ns']
        #and global_count % 45 > 1
        #and global_count % 45 > 1
        # and global_count % 45 > 1
        # and global_count % 45 > 1
        if global_count > 4 and global_count % 11 != 0 and global_count%9 != 0 and global_count % 45 > 1:
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
                job_next_time_job_name = job_next_time_job_name + 1
                job_next_time[job_name] = job_next_time_job_name
                tasks['nexttimes'] = job_next_time
                tasks['next'] = tmp_next
                lock.release()
                job = reload_jobs(job_name, -1)
                job.set_mod(1)
                save_mode_change(1,job.name,float(time.time()))
                print("%s in next reload!" % job_name)
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
                    count_trys = 0
                    while (not endcpu) or (not endmem):
                        if first_try:
                            if can_use_cpu - 720 > 0:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 720
                            else:
                                if can_use_cpu - job.cpu_allocate > 0:
                                    catch_worker_c += 1
                                    can_use_cpu = can_use_cpu - job.cpu_allocate

                            if can_use_mem - 2000 > 0:
                                catch_ps_m += 1
                                can_use_mem = can_use_mem - 2000
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
                                if can_use_cpu - 720 > 0:
                                    catch_ps_c += 1
                                    can_use_cpu = can_use_cpu - 720
                                else:
                                    endcpu = True

                            if can_use_mem - job.memory_allocate > 0:
                                catch_worker_m += 1
                                can_use_mem = can_use_mem - job.memory_allocate
                            else:
                                if can_use_mem - 2000 > 0:
                                    catch_ps_m += 1
                                    can_use_mem = can_use_mem - 2000
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

                    if catch_ps >= 1 and catch_worker >= 1:
                        break
                print("In next catch ps: %d,worker:%d" % (catch_ps, catch_worker))
                if catch_ps > 0 and catch_worker > 0:
                    # lock.acquire()
                    job.update_step()
                    print("in next update step success!!")
                    write_step_meg(job.name)
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
                    tmpk_next = tasks['next']
                    while True:
                        lock.acquire()
                        if job.mod != 10:
                            job.set_mod(10)
                            save_mode_change(10, job.name, float(time.time()))
                        if not task2['label']:
                            if len(tmpk_next) >= 1 and tasks['size'] - tasks['count']>=2 and (global_count+1)%9!=0 and (global_count+1)%11!=0:
                                job.create_tf(mode=1)
                            else:
                                job.create_tf(mode=1)
                            submit_time_now = time.time()
                            tongji_waiting_queue(job.name, submit_time_now)
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
                            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                            res_config = load_config(save_res_path)
                            lock.release()
                            batch_res = res_config['batch_res']
                            flops_res = res_config['flops_res']
                            params_res = res_config['params_res']
                            pool.apply_async(catch_node_step_msg,
                                             args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1,task2))
                            # tasks['next'] = ''
                            break
                        else:
                            lock.release()
                            time.sleep(2.9)
                else:
                    lock.acquire()
                    tmp_buffer_count0 = tasks['buffercount']
                    catch_tmp_nexttimes = tasks['nexttimes']
                    catch_tmp_ps_re_job_name = catch_tmp_nexttimes[job_name]
                    # tasks['nexttimes'][job.name]
                    if catch_tmp_ps_re_job_name >=3 and tmp_buffer_count0 < max_buffer_size:
                        tmp_buffer_pool = tasks['buffer']
                        tmp_buffer_pool.append(job.name)
                        job.set_mod(2)
                        save_mode_change(2,job.name,float(time.time()))
                        tasks['buffer'] = tmp_buffer_pool
                        tmp_buffer_count0+=1
                        tasks['buffercount'] = tmp_buffer_count0
                        tmp_next_time_config = tasks['nexttimes']
                        tmp_next_time_config.pop(job.name)
                        tasks['nexttimes'] =  tmp_next_time_config
                    else:
                        tmp_next = tasks['next']
                        tmp_next.append(job.name)
                        tasks['next'] = tmp_next
                    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                    # save_res_path = '/tfdata/tfcnn'
                    res_config = load_config(save_res_path)
                    if job.cpu_allocate > math.ceil(0.515*res_config['cpu_high']):
                        if math.ceil(job.cpu_allocate * 0.85) >= math.ceil(0.515*res_config['cpu_high']):
                            save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.85),
                                                     job.memory_allocate)
                        else:
                            save_job_change_resource(job.name, math.ceil(0.515*res_config['cpu_high']), job.memory_allocate)
                        # job.assignment_resource(res_config['cpu_high'], job.memory_allocate)
                        print("modulate the cpu!!")
                    else:
                        if job.memory_allocate > res_config['memory_base']:
                            save_job_change_resource(job.name, job.cpu_allocate, 1.093*res_config['memory_base'])
                            # job.assignment_resource(job.cpu_allocate, res_config['memory_base'])
                            print("modulate the memory!!")
                    lock.release()
                    time.sleep(18.5)
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
                if cpu_value < 0.4:
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
                job.set_mod(1)
                save_mode_change(1,job.name,float(time.time()))
                tmp_ps_replicas = job.ps_replicas
                tmp_worker_replicas = job.worker_replicas
                selected_res_config_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (selected_job_name, selected_job_name)
                selected_res_config2 = load_config(selected_res_config_path)

                using_flops = selected_res_config2['flops_res']
                using_param = selected_res_config2["params_res"]
                using_cpu_base = selected_res_config2['cpu_high']
                using_mem_base = selected_res_config2['memory_base']
                using_min_batch = predict_min_first(rfr=rfr,cpu_alpha=job.cpu_allocate/using_cpu_base,mem_alpha=job.memory_allocate/using_mem_base,batch=job.batch_size,flops=using_flops,params=using_param)

                using_min_batch = float(using_min_batch)
                tmp_rest = job.deadline + job.starttime - time.time()
                if tmp_rest > 0:
                    _,_,atmp = job.get_remain(mode=0)
                    worker_need = math.ceil(
                        (job.training_step - atmp) * job.worker_replicas * using_min_batch / ((tmp_rest)))
                    worker_need_total = worker_need
                    if job.training_step - atmp <= 2:
                        job.worker_replicas = 1
                    else:
                        job.worker_replicas = worker_need_total
                        if cpu_value < 0.4:
                            if worker_need >= 6:
                                job.worker_replicas = 6
                        elif cpu_value < 0.7:
                            if worker_need >= 4:
                                job.worker_replicas = 4
                        else:
                            if worker_need >= 2:
                                job.worker_replicas = 2
                    # job.get_remain()
                else:
                    if cpu_value < 0.4:
                        job.worker_replicas = random.randint(3, 5)
                    elif cpu_value < 0.7:
                        job.worker_replicas = random.randint(2, 3)
                    else:
                        job.worker_replicas = random.randint(1, 2)
                # job.worker_replicas = 2
                catch_tmp_ps_re = random.randint(math.floor(job.worker_replicas / 4),math.ceil(job.worker_replicas / 2))
                # catch_tmp_ps_re = 1
                if catch_tmp_ps_re < 1:
                    catch_tmp_ps_re = 1
                job.ps_replicas = catch_tmp_ps_re
                job.training_step = math.ceil(job.training_step * tmp_worker_replicas / job.worker_replicas)
                save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas, job.training_step)
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
                            if can_use_cpu - 720 > 0 and not reach_ps:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 720
                            else:
                                if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                    catch_worker_c += 1
                                    can_use_cpu = can_use_cpu - job.cpu_allocate
                            if can_use_mem - 2000 > 0 and not reach_ps:
                                catch_ps_m += 1
                                can_use_mem = can_use_mem - 2000
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
                                if can_use_cpu - 720 > 0 and not reach_ps:
                                    catch_ps_c += 1
                                    can_use_cpu = can_use_cpu - 720
                                else:
                                    endcpu = True

                            if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                catch_worker_m += 1
                                can_use_mem = can_use_mem - job.memory_allocate
                            else:
                                if can_use_mem - 2000 > 0 and not reach_ps:
                                    catch_ps_m += 1
                                    can_use_mem = can_use_mem - 2000
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
                        # lock.acquire()
                        save_job_change_layout(job.name, catch_ps, catch_worker, job.training_step)
                        job.update_step()
                        write_step_meg(job.name)
                        # lock.release()
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
                        while True:
                            lock.acquire()
                            if job.mod != 10:
                                job.set_mod(10)
                                save_mode_change(10, job.name, float(time.time()))
                            if not task2['label']:
                                if tasks['buffercount'] >= 2 and tasks['size']-tasks['count']>=2 and (global_count+1)%9!=0 and (global_count+1)%11!=0:
                                    job.create_tf(mode=1)
                                else:
                                    job.create_tf()
                                submit_time_now = time.time()
                                tongji_waiting_queue(job.name, submit_time_now)
                                ns_tmp = tasks['ns']
                                ns_tmp.append(job.name)
                                tasks['ns'] = ns_tmp
                                is_layout = tasks['nslayout']
                                is_layout[job.name] = False
                                tasks['nslayout'] = is_layout
                                jobs.append(job.name)
                                tasks['count'] += 1

                                save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                                res_config = load_config(save_res_path)
                                lock.release()
                                batch_res = res_config['batch_res']
                                flops_res = res_config['flops_res']
                                params_res = res_config['params_res']
                                pool.apply_async(catch_node_step_msg,
                                                 args=(
                                                     jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1,task2))
                                break
                            else:
                                lock.release()
                                time.sleep(2.9)

                    else:
                        job.ps_replicas = 1
                        job.worker_replicas = 1
                        job.training_step = job.training_step = math.ceil(job.training_step * tmp_worker)
                        save_job_change_layout(job.name, 1, 1, training_step=job.training_step)
                        job.set_mod(3)
                        save_mode_change(3,job.name,float(time.time()))

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
                    # lock.acquire()
                    job.update_step()
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
                    while True:
                        lock.acquire()
                        if job.mod != 10:
                            job.set_mod(10)
                            save_mode_change(10, job.name, float(time.time()))
                        if not task2['label']:
                            if tasks['buffercount'] >= 2 and tasks['size'] - tasks['count']>=2 and (global_count+1)%9!=0 and (global_count+1)%11!=0:
                                job.create_tf(mode=1)
                            else:
                                job.create_tf()
                            submit_time_now = time.time()
                            tongji_waiting_queue(job.name, submit_time_now)
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
                            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)
                            res_config = load_config(save_res_path)
                            lock.release()
                            batch_res = res_config['batch_res']
                            flops_res = res_config['flops_res']
                            params_res = res_config['params_res']
                            pool.apply_async(catch_node_step_msg,
                                             args=(
                                                 jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1,task2))
                            break
                        else:
                            lock.release()
                            time.sleep(2.9)

            global_count+=1
            time.sleep(sleep_last_length)
        #  or global_count%45==1
        # or global_count % 45 == 1
        #  or global_count % 45 == 1
        # or global_count % 45 == 1
        if global_count % 9 == 0 or global_count<=4 or global_count % 45 == 1:
            print('start to submit a job!!')
            for _ in range(10):
                lock.acquire()
                counts = tasks['count']
                bufer_count = tasks['buffercount']
                lock.release()
                if ((counts >= tasks['size']) and (bufer_count >= max_buffer_size)) or (now_create>=27 and (not tmp_aim_set)):
                    time.sleep(float(random.randint(2,3)))
                    pass

                else:
                    print('select a job!!')
                    time.sleep(29)
                    kkppkk = 0
                    if tasks['aim']:
                        kkppkk = 1
                        tmp_jobs = tasks['aim']
                        aim_job0 = tmp_jobs[0]
                        tmp_jobs.pop(0)
                        tasks['aim'] = tmp_jobs
                        aim_job = reload_jobs_aim(aim_job0, -1)
                        save_change_path = '/tfdata/k8snfs/%s/%s_pw.json' % (aim_job.name, aim_job.name)
                        aim_job_step_base = load_config(save_change_path)
                        his_step_key = list(aim_job_step_base["changen"].keys())
                        his_step = []
                        for hsk in his_step_key:
                           his_step.append(float(hsk))

                        # list.sort(his_step)
                        aim_job_step_base_pre = aim_job_step_base["changen"][str(min(his_step))]
                        # tmp_step0 = aim_job_step_base_pre["stepbefore"]*aim_job_step_base_pre["wbefore"]
                        # tmp_step0 = math.ceil(tmp_step0/2)
                        # ps_r = 1
                        # worker_r = 2
                        tmp_step0 = aim_job_step_base_pre["stepbefore"]
                        # tmp_step0 = aim_job_step_base_pre["stepbefore"]*aim_job_step_base_pre["wbefore"]
                        # tmp_step0 = math.ceil(tmp_step0/2)
                        # "psbefore"
                        ps_r = aim_job_step_base_pre["psbefore"]
                        worker_r = aim_job_step_base_pre["wbefore"]
                        if aim_job.template_id == 1:
                            # def __init__(self,v1,template_id,ps_replicas,worker_replicas,training_step,batch_size,interval,task_id,rtimes,tag,repeat,channel1,channel2,channel3,channel4,channel5,channel6,channel7,channel8,dbhost='192.168.128.10', retry=0, update_min_step=400, step_update=200, update_start=0.25,
                            #                  update_end=0.75, update_delay=2.0):
                            job = VGGTask(template_id=aim_job.template_id, ps_replicas=ps_r,
                                          worker_replicas=worker_r,
                                          training_step=tmp_step0,
                                          batch_size=aim_job.batch_size,
                                          interval=aim_job.interval,
                                          task_id=aim_job.task_id,
                                          rtimes=aim_job.rtimes,
                                          tag=aim_job.tag, channel1=aim_job.channel1, channel2=aim_job.channel2,
                                          channel3=aim_job.channel3,channel4=aim_job.channel4, channel5=aim_job.channel5,
                                          num_layer1=aim_job.num_layer1, num_layer2=aim_job.num_layer2, num_layer3=aim_job.num_layer3,
                                          num_layer4=aim_job.num_layer4,num_layer5=aim_job.num_layer5
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
                                          'retry': job.retry}

                            job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                              '3': [], '4': [], '5': [],
                                              '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                            dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                                      'channel3': aim_job.channel3,
                                      'channel4': aim_job.channel4,
                                      'channel5': aim_job.channel5, 'num_layer1': aim_job.num_layer1, 'num_layer2': aim_job.num_layer2,
                                      'num_layer3': aim_job.num_layer3, 'num_layer4': aim_job.num_layer4, 'num_layer5': aim_job.num_layer5}

                        elif aim_job.template_id == 2:
                            job = RESTask(template_id=aim_job.template_id, ps_replicas=ps_r,
                                          worker_replicas=worker_r,
                                          training_step=tmp_step0,
                                          batch_size=aim_job.batch_size,
                                          interval=aim_job.interval,
                                          task_id=aim_job.task_id,
                                          rtimes=aim_job.rtimes,
                                          tag=aim_job.tag, bottle=aim_job.bottle, layer1=aim_job.layer1,
                                          layer2=aim_job.layer2,
                                          layer3=aim_job.layer3,
                                          layer4=aim_job.layer4, channel1=aim_job.channel1, channel2=aim_job.channel2, channel3=aim_job.channel3,
                                          channel4=aim_job.channel4)

                            job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                          'worker_replicas': job.worker_replicas,
                                          'training_step': job.training_step,
                                          'batch_size': job.batch_size,
                                          'interval': job.interval,
                                          'task_id': job.task_id, 'rtimes': job.rtimes,
                                          'tag': job.tag, 'bottle': job.bottle, 'layer1': job.layer1,
                                          'layer2': job.layer2,
                                          'layer3': job.layer3,
                                          'layer4': job.layer4, 'channel1': job.channel1, 'channel2': job.channel2,
                                          'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry}

                            job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                              '3': [], '4': [], '5': [],
                                              '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                            dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                                      'channel3': aim_job.channel3,
                                      'channel4': aim_job.channel4,
                                      'layer1': aim_job.layer1, 'layer2': aim_job.layer2,
                                      'layer3': aim_job.layer3, 'layer4': aim_job.layer4, 'bottle': aim_job.bottle}

                        elif aim_job.template_id == 3:
                            job = RETask(template_id=aim_job.template_id, ps_replicas=ps_r,
                                         worker_replicas=worker_r,
                                         training_step=tmp_step0,
                                         batch_size=aim_job.batch_size,
                                         interval=aim_job.interval,
                                         task_id=aim_job.task_id,
                                         rtimes=aim_job.rtimes,
                                         tag=aim_job.tag, stack=aim_job.stack, channel1=aim_job.channel1,
                                         channel2=aim_job.channel2,
                                         channel3=aim_job.channel3, channel4=aim_job.channel4
                                         )
                            dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                                      'channel3': aim_job.channel3,
                                      'channel4': aim_job.channel4, 'stack_num': aim_job.stack}

                            job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                              '3': [], '4': [], '5': [],
                                              '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                            job_config = {
                                'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                                'batch_size': job.batch_size, 'interval': job.interval,
                                'task_id': job.task_id, 'rtimes': job.rtimes,
                                'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1,
                                'channel2': job.channel2,
                                'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry
                            }

                        elif aim_job.template_id == 4:

                            job = XCETask(template_id=aim_job.template_id, ps_replicas=ps_r,
                                          worker_replicas=worker_r,
                                          training_step=tmp_step0,
                                          batch_size=aim_job.batch_size,
                                          interval=aim_job.interval,
                                          task_id=aim_job.task_id,
                                          rtimes=aim_job.rtimes,
                                          tag=aim_job.tag,
                                          repeat=aim_job.repeat,
                                          channel1=aim_job.channel1, channel2=aim_job.channel2, channel3=aim_job.channel3,
                                          channel4=aim_job.channel4, channel5=aim_job.channel5, channel6=aim_job.channel6,
                                          channel7=aim_job.channel7,
                                          channel8=aim_job.channel8)

                            job_config = {
                                'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                'worker_replicas': job.worker_replicas,
                                'training_step': job.training_step,
                                'batch_size': job.batch_size,
                                'interval': job.interval,
                                'task_id': job.task_id,
                                'rtimes': job.rtimes, 'tag': job.tag, 'repeat': job.repeat,
                                'channel1': job.channel1,
                                'channel2': job.channel2, 'channel3': job.channel3, 'channel4': job.channel4,
                                'channel5': job.channel5,
                                'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8,
                                'retry': job.retry
                            }

                            job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                              '3': [], '4': [], '5': [],
                                              '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                            dict12 = {'batch': aim_job.batch_size, 'channel1': aim_job.channel1, 'channel2': aim_job.channel2,
                                      'channel3': aim_job.channel3,
                                      'channel4': aim_job.channel4, 'channel5': aim_job.channel5, 'channel6': aim_job.channel6,
                                      'channel7': aim_job.channel7,
                                      'channel8': aim_job.channel8, 'repeat': aim_job.repeat}

                        else:
                            job = DENTask(template_id=aim_job.template_id, ps_replicas=ps_r,
                                          worker_replicas=worker_r,
                                          training_step=tmp_step0,
                                          batch_size=aim_job.batch_size,
                                          interval=aim_job.interval,
                                          task_id=aim_job.task_id,
                                          rtimes=aim_job.rtimes,
                                          tag=aim_job.tag, L=aim_job.L, k=aim_job.k, BC=aim_job.BC)

                            job_config = {
                                'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                                'batch_size': job.batch_size, 'interval': job.interval, 'task_id': job.task_id,
                                'rtimes': job.rtimes,
                                'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC, 'retry': job.retry
                            }

                            # batch, flops, params = denfpmodel.denfp(batch=256, BC=0, k=24, L=100, num_classes=10)
                            dict12 = {'batch': aim_job.batch_size, 'BC': aim_job.BC, 'k': aim_job.k, 'L': aim_job.L, 'num_classes': 10}

                            job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                              '3': [], '4': [], '5': [],
                                              '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
                        measure = job.measure
                        time.sleep(2.5)
                        # aim_job.retry = 0

                    else:
                        template_id = random.randint(1, 4)
                        if tasks['reload'] == 0:
                            template_id = random.randint(1, 4)
                            if template_id <= 2:
                                template_id = 1
                            else:
                                template_id = 4
                                tmp_worker_replicas = 4
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
                            lock.release()
                            ps_r = random.randint(1, 3)
                            worker_r = random.randint(1, 5)
                            batch = random.randint(64, 1024)
                            measure = "VGG 1"
                            print(tasks)
                            if template_id == 1:
                                channels = [24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400,
                                            480, 512, 576]
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
                                              'num_layer5': job.num_layer5,
                                              'retry': job.retry}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                                dict12 = {'batch': batch, 'channel1': channel1, 'channel2': channel2,
                                          'channel3': channel3,
                                          'channel4': channel4,
                                          'channel5': channel5, 'num_layer1': num_layer1, 'num_layer2': num_layer2,
                                          'num_layer3': num_layer3, 'num_layer4': num_layer4, 'num_layer5': num_layer5}

                            elif template_id == 2:
                                bottle = random.randint(0, 1)
                                channels = [24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400,
                                            480, 512, 576]
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
                                              tag=tasks['tag'][template_id - 1], bottle=bottle, layer1=layer1,
                                              layer2=layer2,
                                              layer3=layer3,
                                              layer4=layer4, channel1=channel1, channel2=channel2, channel3=channel3,
                                              channel4=channel4)

                                job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                              'worker_replicas': job.worker_replicas,
                                              'training_step': job.training_step,
                                              'batch_size': job.batch_size,
                                              'interval': job.interval,
                                              'task_id': job.task_id, 'rtimes': job.rtimes,
                                              'tag': job.tag, 'bottle': job.bottle, 'layer1': job.layer1,
                                              'layer2': job.layer2,
                                              'layer3': job.layer3,
                                              'layer4': job.layer4, 'channel1': job.channel1, 'channel2': job.channel2,
                                              'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                                dict12 = {'batch': batch, 'channel1': channel1, 'channel2': channel2,
                                          'channel3': channel3,
                                          'channel4': channel4,
                                          'layer1': layer1, 'layer2': layer2,
                                          'layer3': layer3, 'layer4': layer4, 'bottle': bottle}

                            elif template_id == 3:
                                stack = random.randint(3, 16)
                                channels = [12, 16, 24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320,
                                            384,
                                            400,
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
                                             task_id=tasks['task_id'][template_id - 1],
                                             rtimes=tasks['rtimes'][template_id - 1],
                                             tag=tasks['tag'][template_id - 1], stack=stack, channel1=channel1,
                                             channel2=channel2,
                                             channel3=channel3, channel4=channel4
                                             )
                                dict12 = {'batch': batch, 'channel1': channel1, 'channel2': channel2,
                                          'channel3': channel3,
                                          'channel4': channel4, 'stack_num': stack}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                                job_config = {
                                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                    'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                                    'batch_size': job.batch_size, 'interval': job.interval,
                                    'task_id': job.task_id, 'rtimes': job.rtimes,
                                    'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1,
                                    'channel2': job.channel2,
                                    'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry
                                }

                            elif template_id == 4:
                                repeat = random.randint(4, 12)
                                channels = [12, 16, 24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320,
                                            384,
                                            400,
                                            480,
                                            512, 576, 640, 728, 856, 920, 960, 1024, 1280, 1408, 1536, 1600, 1728, 2048,
                                            2096]
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
                                              rtimes=tasks['rtimes'][template_id - 1],
                                              tag=tasks['tag'][template_id - 1],
                                              repeat=repeat,
                                              channel1=channel1, channel2=channel2, channel3=channel3,
                                              channel4=channel4, channel5=channel5, channel6=channel6,
                                              channel7=channel7,
                                              channel8=channel8)

                                job_config = {
                                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                    'worker_replicas': job.worker_replicas,
                                    'training_step': job.training_step,
                                    'batch_size': job.batch_size,
                                    'interval': job.interval,
                                    'task_id': job.task_id,
                                    'rtimes': job.rtimes, 'tag': job.tag, 'repeat': job.repeat,
                                    'channel1': job.channel1,
                                    'channel2': job.channel2, 'channel3': job.channel3, 'channel4': job.channel4,
                                    'channel5': job.channel5,
                                    'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8,
                                    'retry': job.retry
                                }

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                                dict12 = {'batch': batch, 'channel1': channel1, 'channel2': channel2,
                                          'channel3': channel3,
                                          'channel4': channel4, 'channel5': channel5, 'channel6': channel6,
                                          'channel7': channel7,
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
                                    'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC, 'retry': job.retry
                                }

                                # batch, flops, params = denfpmodel.denfp(batch=256, BC=0, k=24, L=100, num_classes=10)
                                dict12 = {'batch': batch, 'BC': BC, 'k': k, 'L': L, 'num_classes': 10}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
                            measure = job.measure
                            # lock.acquire()
                            #
                            # tasks['base'] = job.name
                            # lock.release()
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

                            lock.release()
                            tmp_task_id = tmp1[template_id - 1]
                            job = reload_jobs_aim(job_base_name, task_id=tmp_task_id)
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
                                              'num_layer5': job.num_layer5, 'retry': job.retry}

                                dict12 = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                                          'channel3': job.channel3,
                                          'channel4': job.channel4,
                                          'channel5': job.channel5, 'num_layer1': job.num_layer1,
                                          'num_layer2': job.num_layer2,
                                          'num_layer3': job.num_layer3, 'num_layer4': job.num_layer4,
                                          'num_layer5': job.num_layer5}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
                            elif template_id == 2:
                                job_config = {'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                              'worker_replicas': job.worker_replicas,
                                              'training_step': job.training_step,
                                              'batch_size': job.batch_size,
                                              'interval': job.interval,
                                              'task_id': job.task_id, 'rtimes': job.rtimes,
                                              'tag': job.tag, 'bottle': job.bottle, 'layer1': job.layer1,
                                              'layer2': job.layer2,
                                              'layer3': job.layer3,
                                              'layer4': job.layer4, 'channel1': job.channel1, 'channel2': job.channel2,
                                              'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}

                                dict12 = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                                          'channel3': job.channel3,
                                          'channel4': job.channel4,
                                          'layer1': job.layer1, 'layer2': job.layer2,
                                          'layer3': job.layer3, 'layer4': job.layer4, 'bottle': job.bottle}
                            elif template_id == 3:
                                dict12 = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                                          'channel3': job.channel3,
                                          'channel4': job.channel4, 'stack_num': job.stack}

                                job_config = {
                                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                    'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                                    'batch_size': job.batch_size, 'interval': job.interval,
                                    'task_id': job.task_id, 'rtimes': job.rtimes,
                                    'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1,
                                    'channel2': job.channel2,
                                    'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry
                                }

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
                            elif template_id == 4:
                                job_config = {
                                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                    'worker_replicas': job.worker_replicas,
                                    'training_step': job.training_step,
                                    'batch_size': job.batch_size,
                                    'interval': job.interval,
                                    'task_id': job.task_id,
                                    'rtimes': job.rtimes, 'tag': job.tag, 'repeat': job.repeat,
                                    'channel1': job.channel1,
                                    'channel2': job.channel2, 'channel3': job.channel3, 'channel4': job.channel4,
                                    'channel5': job.channel5,
                                    'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8,
                                    'retry': job.retry
                                }

                                dict12 = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                                          'channel3': job.channel3,
                                          'channel4': job.channel4, 'channel5': job.channel5, 'channel6': job.channel6,
                                          'channel7': job.channel7,
                                          'channel8': job.channel8, 'repeat': job.repeat}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
                            else:
                                job_config = {
                                    'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                    'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                                    'batch_size': job.batch_size, 'interval': job.interval, 'task_id': job.task_id,
                                    'rtimes': job.rtimes,
                                    'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC, 'retry': job.retry
                                }

                                dict12 = {'batch': job.batch_size, 'BC': job.BC, 'k': job.k, 'L': job.L,
                                          'num_classes': 10}

                                job_mod_config = {'mod': job.mod, '-1': [float(time.time())], '0': [], '1': [], '2': [],
                                                  '3': [], '4': [], '5': [],
                                                  '6': [], '7': [], '8': [], '9': [], '10': [], '11': []}
                            measure = job.measure
                    # lock.acquire()
                    if tasks['count'] < tasks['size'] or tasks['buffercount'] < max_buffer_size:
                        pre_list = measure.split(" ")
                        measure_t = pre_list[0] + 'T' + pre_list[-1]
                        allow_p = check_path(measure_t)

                        save_config_dir = task_submit_fix.check_path(job.name)
                        save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job.name, job.name)
                        allow_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job.name, measure_t)

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
                            if kkppkk == 0:
                                tmp1 = tasks['task_id']
                                tmp1[job.template_id - 1] -= 1
                                tasks['task_id'] = tmp1
                                tmp2 = tasks['rtimes']
                                tmp2[job.template_id - 1] -= 1
                                tasks['rtimes'] = tmp2
                            # lock.release()
                            try:
                                command0 = 'rm %s' % save_job_path
                                aek = os.system(command0)
                                command0 = 'rm %s' % allow_path
                                ask = os.system(command0)
                            except Exception as eee0:
                                print(eee0)
                            # lock.release()
                            continue
                        print(msg_from_server_str)
                        print("connected success!")
                        dict_json = json.dumps(dict12)
                        pre_client.send(bytes(dict_json, 'utf-8'))
                        ress = pre_client.recv(4096)
                        ress_str = str(ress.decode('utf-8'))
                        ress_lists = ress_str.split(' ')
                        if ress_lists[0] == '400':
                            batch_res = int(ress_lists[1])
                            flops_res = int(ress_lists[2])
                            params_res = int(ress_lists[3])
                            cpu_predict = float(ress_lists[-2])
                            cpu_base = math.ceil(1.03 * cpu_predict)
                            mem_predict = float(ress_lists[-1])
                            if job.template_id != 4:
                                mem_base = math.ceil(1.672 * mem_predict)
                            else:
                                mem_base = math.ceil(1.872 * mem_predict)
                            res_to_server = '1'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                        else:
                            res_to_server = '0'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                            print("send response success!!")
                            time.sleep(5.3)
                            pre_client.close()
                            print("some time later to try again!!")

                            if kkppkk == 0:
                                tmp1 = tasks['task_id']
                                tmp1[job.template_id - 1] -= 1
                                tasks['task_id'] = tmp1
                                tmp2 = tasks['rtimes']
                                tmp2[job.template_id - 1] -= 1
                                tasks['rtimes'] = tmp2

                            try:
                                command0 = 'rm %s' % save_job_path
                                aek = os.system(command0)
                                command0 = 'rm %s' % allow_path
                                ask = os.system(command0)
                            except Exception as eee0:
                                print(eee0)
                            time.sleep(27)
                            continue
                        pre_client.close()
                        tmp_reload = tasks['reload']
                        if tmp_reload == 0:
                            alpha = random.randint(0, 7) * 0.1 + 0.5
                            beta = random.randint(0, 18) * 0.1 + 0.875
                        else:
                            alpha = random.randint(2, 12) * 0.1 + 0.6
                            beta = random.randint(0, 10) * 0.1 + 1
                        alpha = 1
                        beta = 1
                        job.set_resource(cpu_source=(math.ceil(cpu_base * alpha)),
                                         mem_source=(math.ceil(mem_base * beta)))

                        save_config(job_config, save_job_path)
                        allow_read = {}
                        allow_read['OK'] = True
                        allow_read['retry'] = 0
                        allow_p = check_path(measure_t)

                        save_config(allow_read, allow_path)

                        mini_batch = predict_min_first(rfr=rfr, cpu_alpha=alpha, mem_alpha=beta, batch=batch_res,
                                                       flops=flops_res, params=params_res)
                        mini_batch = float(mini_batch)
                        if kkppkk == 0:
                            deadline = mini_batch * job.training_step * (random.randint(66, 244) * 0.01) + 750
                        else:
                            deadline = float(aim_job.deadline)
                        print(deadline)
                        print(type(deadline))
                        # deadline = random.randint(3600, 18000)
                        start_time = '%.3f' % time.time()
                        start_time = float(start_time)
                        job.set_deadline(deadline=deadline, start_time=start_time)
                        job.set_mod(new_mod=0)
                        job_mod_config['0'].append(start_time)
                        job.set_mod(0)
                        job_res_config = {'deadline': job.deadline, 'start_time': job.starttime,
                                          'cpu_source': job.cpu_allocate,
                                          'mem_source': job.memory_allocate, 'cpu_high': cpu_base,
                                          'memory_base': mem_base, 'batch_res': batch_res,
                                          'flops_res': flops_res, 'params_res': params_res, 'step_base': 0,
                                          'reloadtime': []}
                        save_config_dir = task_submit_fix.check_path(job.name)

                        save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job.name, job.name)

                        save_mod_path = '/tfdata/k8snfs/setbase/%s/%s_mod.json' % (job.name, job.name)
                        save_config(job_res_config, save_res_path)
                        save_config(job_mod_config, save_mod_path)
                        now_create = now_create + 1
                        np.save('nowcreate.npy', now_create)
                        if tasks['count'] < tasks['size'] and tasks['buffercount'] == 0:
                            save_mode_change(1, job.name, float(time.time()))
                            job.set_mod(1)
                            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                            cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(
                                node_index=node_index,
                                cpu_base=cpu_nodes,
                                memory_base=memory_nodes,
                                total_cpu_base=total_cpu_use,
                                total_memory_base=total_mem_use)
                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas

                            worker_need = math.ceil(
                                (job.training_step) * job.worker_replicas * mini_batch / ((job.deadline)))
                            worker_need_total = worker_need
                            if job.training_step <= 100:
                                job.worker_replicas = 1
                            else:
                                job.worker_replicas = worker_need_total
                                if cpu_value < 0.4:
                                    if worker_need >= 5:
                                        job.worker_replicas = 5
                                elif cpu_value < 0.7:
                                    if worker_need >= 4:
                                        job.worker_replicas = 4
                                else:
                                    if worker_need >= 2:
                                        job.worker_replicas = 2

                            catch_tmp_ps_re = random.randint(math.floor(job.worker_replicas / 4),
                                                             math.ceil(job.worker_replicas / 2))
                            if cpu_value < 0.4:
                                catch_tmp_ps_re = math.ceil(job.worker_replicas / 2)
                            elif cpu_value < 0.7:
                                catch_tmp_ps_re = math.ceil(job.worker_replicas / 3)
                            else:
                                catch_tmp_ps_re = math.ceil(job.worker_replicas / 4)
                            if catch_tmp_ps_re < 1:
                                catch_tmp_ps_re = 1
                            job.ps_replicas = catch_tmp_ps_re
                            # job.ps_replicas = 1
                            # job.worker_replicas = 2

                            job.training_step = math.ceil(
                                job.training_step * tmp_worker_replicas / job.worker_replicas)

                            save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas,
                                                   job.training_step)

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
                                        if can_use_cpu - 720 > 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 720
                                        else:
                                            if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                                catch_worker_c += 1
                                                can_use_cpu = can_use_cpu - job.cpu_allocate
                                        if can_use_mem - 2000 > 0 and not reach_ps:
                                            catch_ps_m += 1
                                            can_use_mem = can_use_mem - 2000
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
                                            if can_use_cpu - 720 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 720
                                            else:
                                                endcpu = True

                                        if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                            catch_worker_m += 1
                                            can_use_mem = can_use_mem - job.memory_allocate
                                        else:
                                            if can_use_mem - 2000 > 0 and not reach_ps:
                                                catch_ps_m += 1
                                                can_use_mem = can_use_mem - 2000
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
                                    while True:
                                        lock.acquire()
                                        if job.mod != 10:
                                            job.set_mod(10)
                                            save_mode_change(10, job.name, float(time.time()))
                                        if not task2['label']:
                                            if global_count == 2 or global_count == 3 or global_count % 45 == 1:
                                                job.create_tf(mode=1)
                                            else:
                                                job.create_tf()
                                            submit_time_now = time.time()
                                            tongji_waiting_queue(job.name, submit_time_now)
                                            ns_tmp = tasks['ns']
                                            ns_tmp.append(job.name)
                                            tasks['ns'] = ns_tmp
                                            is_layout = tasks['nslayout']
                                            is_layout[job.name] = False
                                            tasks['nslayout'] = is_layout
                                            jobs.append(job.name)
                                            tasks['count'] += 1

                                            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (
                                                job.name, job.name)
                                            res_config = load_config(save_res_path)
                                            lock.release()
                                            batch_res = res_config['batch_res']
                                            flops_res = res_config['flops_res']
                                            params_res = res_config['params_res']

                                            pool.apply_async(catch_node_step_msg,
                                                             args=(
                                                                 jobs, job.name, tasks, lock, batch_res, flops_res,
                                                                 params_res, 1, task2))
                                            break
                                        else:
                                            lock.release()
                                            time.sleep(2.9)

                                else:
                                    job.ps_replicas = 1
                                    job.worker_replicas = 1
                                    job.training_step = job.training_step * tmp_worker
                                    job.set_mod(new_mod=3)
                                    save_mode_change(3, job.name, float(time.time()))
                                    lock.acquire()
                                    save_job_change_layout(job.name, 1, 1, job.training_step)
                                    tmp_next = tasks['next']
                                    tmp_next.append(job.name)
                                    tmp_next_time_config = tasks['nexttimes']
                                    tmp_next_time_config[job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config
                                    tasks['next'] = tmp_next
                                    lock.release()
                                    # tasks['next'] = job.name
                            else:
                                job.update_step()
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
                                while True:
                                    lock.acquire()
                                    if job.mod != 10:
                                        job.set_mod(10)
                                        save_mode_change(10, job.name, float(time.time()))
                                    if not task2['label']:
                                        if global_count == 2 or global_count == 3 or global_count % 45 == 1:
                                            job.create_tf(mode=1)
                                        else:
                                            job.create_tf()
                                        submit_time_now = time.time()
                                        tongji_waiting_queue(job.name, submit_time_now)
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
                                        save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (
                                            job.name, job.name)

                                        res_config = load_config(save_res_path)
                                        lock.release()
                                        batch_res = res_config['batch_res']
                                        flops_res = res_config['flops_res']
                                        params_res = res_config['params_res']

                                        pool.apply_async(catch_node_step_msg,
                                                         args=(
                                                             jobs, job.name, tasks, lock, batch_res, flops_res,
                                                             params_res, 1, task2))
                                        break
                                    else:
                                        lock.release()
                                        time.sleep(2.9)


                        elif tasks['count'] >= tasks['size']:
                            job.set_mod(2)
                            save_mode_change(2, job.name, float(time.time()))
                            lock.acquire()
                            worker_buffer = tasks['buffer']
                            worker_buffer.append(job.name)
                            tasks['buffer'] = worker_buffer
                            tmp_buffer_count = tasks['buffercount']
                            tmp_buffer_count = tmp_buffer_count + 1
                            tasks['buffercount'] = tmp_buffer_count
                            lock.release()

                        else:
                            # lock.acquire()
                            job.set_mod(2)
                            save_mode_change(2, job.name, float(time.time()))
                            worker_buffer = tasks['buffer']
                            worker_buffer.append(job.name)
                            tmp_buffer_count = tasks['buffercount']
                            tmp_buffer_count = tmp_buffer_count + 1
                            tasks['buffercount'] = tmp_buffer_count
                            # lock.release()
                            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                            cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(
                                node_index=node_index,
                                cpu_base=cpu_nodes,
                                memory_base=memory_nodes,
                                total_cpu_base=total_cpu_use,
                                total_memory_base=total_mem_use)
                            if cpu_value < 0.4:
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
                                # lock.acquire()
                                tasks['buffer'] = worker_buffer[:]
                                # tmp_buffer_size =
                                max_wight_heap.clear()
                                if selected:
                                    tasks['buffercount'] = max_buffer_size
                                else:
                                    tmp_buffer_count = tmp_buffer_count - 1
                                    tasks['buffercount'] = tmp_buffer_count
                                # lock.release()

                            job = reload_jobs(selected_job_name, -1)
                            job.set_mod(1)
                            save_mode_change(1, selected_job_name, float(time.time()))
                            # selected_res_config2
                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas
                            selected_res_config_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (
                                selected_job_name, selected_job_name)
                            selected_res_config2 = load_config(selected_res_config_path)

                            using_flops = selected_res_config2['flops_res']
                            using_param = selected_res_config2["params_res"]
                            using_cpu_base = selected_res_config2['cpu_high']
                            using_mem_base = selected_res_config2['memory_base']
                            using_min_batch = predict_min_first(rfr=rfr,
                                                                cpu_alpha=job.cpu_allocate / using_cpu_base,
                                                                mem_alpha=job.memory_allocate / using_mem_base,
                                                                batch=job.batch_size, flops=using_flops,
                                                                params=using_param)

                            using_min_batch = float(using_min_batch)
                            tmp_rest = job.deadline + job.starttime - time.time()
                            # job.worker_replicas = 2
                            if tmp_rest > 0:
                                _, _, atmp = job.get_remain(mode=0)
                                worker_need = math.ceil(
                                    (job.training_step - atmp) * job.worker_replicas * using_min_batch / (
                                        (tmp_rest)))
                                worker_need_total = worker_need
                                if job.training_step - atmp <= 2:
                                    job.worker_replicas = 1
                                else:
                                    job.worker_replicas = worker_need_total
                                    if cpu_value < 0.4:
                                        if worker_need >= 6:
                                            job.worker_replicas = 6
                                    elif cpu_value < 0.7:
                                        if worker_need >= 4:
                                            job.worker_replicas = 4
                                    else:
                                        if worker_need >= 2:
                                            job.worker_replicas = 2
                                # job.get_remain()
                            else:
                                if cpu_value < 0.4:
                                    job.worker_replicas = random.randint(3, 5)
                                elif cpu_value < 0.7:
                                    job.worker_replicas = random.randint(2, 3)
                                else:
                                    job.worker_replicas = random.randint(1, 2)
                            catch_tmp_ps_re = random.randint(math.floor(job.worker_replicas / 4),
                                                             math.ceil(job.worker_replicas / 2))

                            # catch_tmp_ps_re = 1
                            if cpu_value < 0.4:
                                catch_tmp_ps_re = math.ceil(job.worker_replicas / 2)
                            elif cpu_value < 0.7:
                                catch_tmp_ps_re = math.ceil(job.worker_replicas / 3)
                            else:
                                catch_tmp_ps_re = math.ceil(job.worker_replicas / 4)

                            if catch_tmp_ps_re < 1:
                                catch_tmp_ps_re = 1

                            # if catch_tmp_ps_re < 1:
                            #     catch_tmp_ps_re = 1
                            job.ps_replicas = catch_tmp_ps_re

                            job.training_step = math.ceil(
                                job.training_step * tmp_worker_replicas / job.worker_replicas)
                            save_job_change_layout(job.name, job.ps_replicas, job.worker_replicas,
                                                   job.training_step)

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
                                        if can_use_cpu - 720 > 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 720
                                        else:
                                            if can_use_cpu - job.cpu_allocate > 0 and not reach_worker:
                                                catch_worker_c += 1
                                                can_use_cpu = can_use_cpu - job.cpu_allocate
                                        if can_use_mem - 2000 > 0 and not reach_ps:
                                            catch_ps_m += 1
                                            can_use_mem = can_use_mem - 2000
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
                                            if can_use_cpu - 750 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 750
                                            else:
                                                endcpu = True

                                        if can_use_mem - job.memory_allocate > 0 and not reach_worker:
                                            catch_worker_m += 1
                                            can_use_mem = can_use_mem - job.memory_allocate
                                        else:
                                            if can_use_mem - 2000 > 0 and not reach_ps:
                                                catch_ps_m += 1
                                                can_use_mem = can_use_mem - 2000
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
                                    while True:
                                        lock.acquire()
                                        if job.mod != 10:
                                            job.set_mod(10)
                                            save_mode_change(10, job.name, float(time.time()))
                                        if not task2['label']:
                                            if global_count == 2 or global_count == 3 or global_count % 45 == 1:
                                                job.create_tf(mode=1)
                                            else:
                                                job.create_tf()
                                            submit_time_now = time.time()
                                            tongji_waiting_queue(job.name, submit_time_now)
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
                                            save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (
                                                job.name, job.name)

                                            res_config = load_config(save_res_path)
                                            lock.release()
                                            batch_res = res_config['batch_res']
                                            flops_res = res_config['flops_res']
                                            params_res = res_config['params_res']
                                            pool.apply_async(catch_node_step_msg,
                                                             args=(
                                                                 jobs, job.name, tasks, lock, batch_res, flops_res,
                                                                 params_res, 1, task2))
                                            break
                                        else:
                                            lock.release()
                                            time.sleep(2.9)

                                else:
                                    job.ps_replicas = 1
                                    job.worker_replicas = 1
                                    job.training_step = job.training_step = math.ceil(
                                        job.training_step * tmp_worker)
                                    save_job_change_layout(job.name, 1, 1, training_step=job.training_step)
                                    job.set_mod(3)
                                    save_mode_change(3, job.name, float(time.time()))
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
                                job.update_step()
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
                                while True:
                                    lock.acquire()
                                    if job.mod != 10:
                                        job.set_mod(10)
                                        save_mode_change(10, job.name, float(time.time()))
                                    if not task2['label']:
                                        if global_count == 2 or global_count == 3 or global_count % 45 == 1:
                                            job.create_tf(mode=1)
                                        else:
                                            job.create_tf()
                                        submit_time_now = time.time()
                                        tongji_waiting_queue(job.name, submit_time_now)
                                        ns_tmp = tasks['ns']
                                        ns_tmp.append(job.name)
                                        tasks['ns'] = ns_tmp
                                        is_layout = tasks['nslayout']
                                        is_layout[job.name] = False
                                        tasks['nslayout'] = is_layout
                                        jobs.append(job.name)
                                        tasks['count'] += 1
                                        save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (
                                            job.name, job.name)

                                        res_config = load_config(save_res_path)
                                        lock.release()
                                        batch_res = res_config['batch_res']
                                        flops_res = res_config['flops_res']
                                        params_res = res_config['params_res']
                                        pool.apply_async(catch_node_step_msg,
                                                         args=(
                                                             jobs, job.name, tasks, lock, batch_res, flops_res,
                                                             params_res, 1, task2))
                                        break
                                    else:
                                        lock.release()
                                        time.sleep(3)

                        tmp_reload = tasks['reload']
                        tmp_reload = 0
                        tasks['reload'] = tmp_reload

                    break
            global_count += 1
        #   and global_count%45 > 1
        # and global_count%45 > 1
        # and global_count%45 > 1
        # and global_count % 45 > 1
        #  and global_count % 45 > 1
        if global_count % 11 == 0 and global_count%9!=0 and global_count % 45 > 1:
            for iter0 in range(2):
                aim_assign_config = {}
                mode1 = 0
                time10 = time.time()
                try:
                    lock.acquire()
                    tasks['modulate'] = True
                    lock.release()
                    try:
                        aim_assign_config,mode1 = assign_jobs(tasks,rfr=rfr,lock=lock)
                    except Exception as e00:
                        print("The error exist in dynamic modulation:")
                        print(e00)

                    print(aim_assign_config)
                    print(mode1)
                    # mode_saves = {}

                    lock.acquire()
                    tasks['modulate'] = False
                    lock.release()
                except Exception as e:
                    print(e)
                    # lock.release()
                    time.sleep(19.2)
                    continue
                time20 = time.time()
                print(aim_assign_config)
                print("Mode is %d" % mode1)
                if mode1 == 0:
                    if iter0 == 0:
                        try:
                            mode_saves = load_config("mode.json")
                        except Exception as sese:
                            mode_saves = {'ad': []}
                            save_config(mode_saves, "mode.json")
                        tmp_mode_save = mode_saves['ad'][:]
                        one_mess = {'time': float(time.time()), 'mode': mode1,'need':0}
                        tmp_mode_save.append(one_mess)
                        mode_saves['ad'] = tmp_mode_save
                        save_config(mode_saves, "mode.json")
                    continue
                elif mode1 == -1:
                    if iter0 == 0:
                        try:
                            mode_saves = load_config("mode.json")
                        except Exception as sese:
                            mode_saves = {'ad': []}
                            save_config(mode_saves, "mode.json")
                        tmp_mode_save = mode_saves['ad'][:]
                        one_mess = {'time': float(time.time()), 'mode': mode1,'need':0}
                        tmp_mode_save.append(one_mess)
                        mode_saves['ad'] = tmp_mode_save
                        save_config(mode_saves, "mode.json")
                    continue
                elif not aim_assign_config:
                    if iter0 == 0:
                        try:
                            mode_saves = load_config("mode.json")
                        except Exception as sese:
                            mode_saves = {'ad': []}
                            save_config(mode_saves, "mode.json")
                        tmp_mode_save = mode_saves['ad'][:]
                        one_mess = {'time': float(time.time()), 'mode': mode1, 'need': 0}
                        tmp_mode_save.append(one_mess)
                        mode_saves['ad'] = tmp_mode_save
                        save_config(mode_saves, "mode.json")
                    continue
                else:
                    assign_key = list(aim_assign_config.keys())
                    assign_key2 = []
                    for akk in assign_key:
                        if aim_assign_config[akk]:
                            assign_key2.append(akk)
                    assign_key = assign_key2
                    print(assign_key)
                    if not assign_key:
                        continue
                    jinxing = False
                    aim_ns = []
                    for assign in assign_key:
                        lock.acquire()
                        tmp_ns0 = tasks['ns']
                        lock.release()
                        if (aim_assign_config[assign]) and (assign in tmp_ns0):
                            pod_status00 = [ps.status.phase for ps in v1.list_namespaced_pod(assign).items]
                            if pod_status00:
                                if (not ('Succeeded' in pod_status00 or 'Failed' in pod_status00)):
                                    jinxing = True
                                    aim_ns.append(assign)
                    print("At last the aim can be decided as:")
                    print(aim_ns)
                    try:
                        mode_saves = load_config("mode.json")
                    except Exception as sese:
                        mode_saves = {'ad': []}
                        save_config(mode_saves, "mode.json")
                    tmp_mode_save = mode_saves['ad'][:]
                    one_mess = {'time': float(time.time()), 'mode': mode1, 'need': len(aim_ns)}
                    tmp_mode_save.append(one_mess)
                    mode_saves['ad'] = tmp_mode_save
                    save_config(mode_saves, "mode.json")
                    # if iter0 == 0:

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
                                # lock.release()
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



                print("Modulation once cost %f" % float(time20 - time10))
                if (mode1==1 or mode1==4) and (iter0>1):
                    break
                time.sleep(27)
            global_count+=1
        # if global_count == 5:
        #     need_s = load_config("modify.json")
        #     need_buffer = need_s['pool']
        #     for i




def jiance(tasks,lock,tasks2):
    try:
        task2 = load_config('through.json')
        task3 = load_config('buffer.json')
        task4 = load_config("noderes.json")
    # aa = 0
    except Exception as eee:
        task2 = {}
        task3 = {}
        task4 = {}
        task2['through'] = {}
        task3['buffer'] = {}
        task4['cpu'] = {}
        task4['mem'] = {}
        task4['rank'] = {}
        task4['time'] = []
        print("will create them")
        print(eee)
    while True:
        if tasks['start']==True:
            time.sleep(57)
            lock.acquire()
            tmp_count1 = tasks['count']
            tmp_bucount = tasks['buffercount']
            tmp_nextcount = len(tasks['next'])
            save_config(tasks,'system_info.json')

            save_config(tasks2,'node_label.json')
            tmp_cpu = tasks2['cpu']
            tmp_mem = tasks2['mem']
            tmp_rank = tasks2['rank']
            tmp_buffer = tasks["buffer"]
            tmp_jobs = tasks['ns']
            lock.release()

            pend_num = 0



            try:
                tmp_time = time.time()
                tmp_throughput = task2['through']
                for tns in tmp_jobs:
                    try:
                        pod_status2 = [i.status.phase for i in v1.list_namespaced_pod(tns).items]
                        if 'Pending' in pod_status2 and 'Succeeded' not in pod_status2 and 'Failed' not in pod_status2:
                            pend_num += 1
                    except Exception as eke:
                        print(eke)
                        continue
                tmp_throughput[tmp_time] = {'count': tmp_count1, 'buf': tmp_bucount, 'next': tmp_nextcount,'pend':pend_num}
                task2['through'] = tmp_throughput
                tmp_buffer_cond = task3['buffer']
                tmp_buffer_cond[tmp_time] = tmp_buffer
                task3['buffer'] = tmp_buffer_cond

                tck = list(tmp_cpu.keys())
                for tc in tck:
                    try:
                        task4['cpu'][tc].append(tmp_cpu[tc])
                    except Exception as tce:
                        task4['cpu'][tc] = []
                        task4['cpu'][tc].append(tmp_cpu[tc])

                tck = list(tmp_mem.keys())
                for tc in tck:
                    try:
                        task4['mem'][tc].append(tmp_mem[tc])
                    except Exception as tce:
                        task4['mem'][tc] = []
                        task4['mem'][tc].append(tmp_mem[tc])

                tck = list(tmp_rank.keys())
                for tc in tck:
                    try:
                        task4['rank'][tc].append(tmp_rank[tc])
                    except Exception as tce:
                        task4['rank'][tc] = []
                        task4['rank'][tc].append(tmp_rank[tc])

                task4['time'].append(float(time.time()))

                save_config(task2,'through.json')
                save_config(task3,'buffer.json')
                save_config(task4,'noderes.json')
            except Exception as eeee:
                print(eeee)
            print('saved configs')
            time.sleep(57)
        else:
            break

def save_job_change_layout(job_name,ps_n,worker_n,training_step,mode=0):
    save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job_name, job_name)

    save_change_path = '/tfdata/k8snfs/setbase/%s/%s_pw.json' % (job_name, job_name)
    try:
        job_res_config = load_config(save_change_path)
    except Exception as e:
        job_res_config = {}
        job_res_config['changen'] = {}
        job_config = load_config(save_job_path)
        job_res_config['ps'] = job_config['ps_replicas']
        job_res_config['worker'] = job_config['worker_replicas']
        job_res_config['training_step'] = job_config['training_step']
        save_config(job_res_config,save_change_path)
        job_res_config = load_config(save_change_path)

    timenow = time.time()
    tmp_changen = job_res_config['changen']
    tmp_changen[timenow] = {'psbefore': job_res_config['ps'], 'wbefore': job_res_config['worker'],
                            'stepbefore': job_res_config['training_step'], 'psnow': ps_n, 'wnow': worker_n,
                            'stepnow': training_step}
    job_res_config['ps'] = ps_n
    job_res_config['worker'] = worker_n
    job_res_config['training_step'] = training_step

    job_config = load_config(save_job_path)
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

def save_job_change_resource(job_name,cpu_allocate,mem_allocate):
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    save_change_path = '/tfdata/k8snfs/setbase/%s/%s_change.json' % (job_name, job_name)
    change_dir = {}

    try:
        change_dir = load_config(save_change_path)
    except Exception as eek:
        change_dir['changer'] = {}
        job_res_config = load_config(save_res_path)
        change_dir['cpu'] = job_res_config['cpu_source']
        change_dir['mem'] = job_res_config['mem_source']
    # tmp_changer = job_res_config['changer']
    tmp_changer = change_dir['changer']
    timenow = time.time()
    tmp_changer[timenow] = {"cpubefore":change_dir['cpu'],'membefore':change_dir['mem'],'memnow': mem_allocate,'cpunow':cpu_allocate}
    change_dir['cpu'] = cpu_allocate
    change_dir['mem'] = mem_allocate
    job_res_config = load_config(save_res_path)
    job_res_config['cpu_source'] = cpu_allocate
    job_res_config['mem_source'] = mem_allocate
    change_dir['changer'] = tmp_changer
    # job_res_config['changer'] = tmp_changer
    save_config(job_res_config, save_res_path)
    save_config(change_dir,save_change_path)

def read_step_base(job_name):
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    key = job_res_config.keys()
    key_list = list(key)
    if 'step_base' not in key_list:
        job_res_config['step_base'] = 0
    step_base = job_res_config['step_base']
    return int(step_base)

def write_step_base(job_name,step_base):
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
    job_res_config = load_config(save_res_path)
    job_res_config['step_base'] = step_base
    save_config(job_res_config,save_res_path)
    print("save step base successfully!!!")

if __name__ == '__main__':
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # v1.list_node()
    mgr = multiprocessing.Manager()
    tasks = mgr.dict()
    tasks2 = mgr.dict()
    lock = mgr.Lock()
    jobs = mgr.list()
    config_content = load_config('system_info.json')
    config_content2 = load_config('node_label.json')
    for key,value in config_content.items():
        tasks[key] = value
    for key,value in config_content2.items():
        tasks2[key] = value
    print(tasks)
    print(tasks2)
    for ns in tasks["ns"]:
        # job_reload = reload_jobs(ns,-1)
        jobs.append(ns)
   # tasks['ns'] = []
    # tasks['job'] = {}
    q = multiprocessing.Manager().Queue(maxsize=tasks['size'])
    tasks['through'] = {}
    tasks['start'] = True

    url = 'https://192.168.128.10:6443/apis/metrics.k8s.io/v1beta1/nodes'
    args = parse()
    client = influxdb.InfluxDBClient('192.168.128.10', port=8086, username='admin', password='admin',
                                     database=args.database)
    # node_p = Node_mess(url=url,derivation=10,args=args)
    node_p = Node_mess(url=url, args=args,tasks=tasks,v1=v1)
    base_job_name = 'vgg-732-732'
    submit_p = multiprocessing.Process(target=Submit_job,args=(tasks,lock,v1,jobs,tasks2))
    monitor_p = multiprocessing.Process(target=Monitor_job,args=(tasks,lock,v1,jobs))
    jiance_p = multiprocessing.Process(target=jiance, args=(tasks, lock,tasks2))
    label_p = multiprocessing.Process(target=make_label_to_nodes,args=(tasks2,base_job_name))

    # derivation
    node_p.daemon = True
    # submit_p.daemon = True
    # monitor_p.daemon = True
    jiance_p.daemon = True
    label_p.daemon = True
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
            label_p.start()
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
                        try:
                            ns_tmp = tasks['ns']
                            command = 'kubectl delete -f /tfdata/tfcnn/expjobbase/' + ns + '.yaml'
                            os.system(command)
                            deletehelp2(ns, v1)

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
                        except Exception as eess:
                            ns_tmp = tasks['ns']
                            if ns in ns_tmp:
                                ns_tmp.remove(ns)
                                tasks['ns'] = ns_tmp
                            is_layout = tasks['nslayout']
                            print("is layout: \n")
                            print(is_layout)
                            if ns in list(is_layout.keys()):
                                is_layout.pop(ns)
                                tasks['nslayout'] = is_layout
                            print("after deal: \n")
                            print(tasks['nslayout'])
                            tasks['count'] = len(ns_tmp)
                            finishes = tasks['finish']
                            if ns not in finishes:
                                finishes.append(ns)
                                tasks['finish'] = finishes
                            print(tasks['count'])
                            lock.release()
                            print(eess)
                    time.sleep(5)
            time_last = math.ceil(time.time())
            tmp_list = tasks['endtime']
            tmp_list.append(time_last)
            tasks["endtime"] = tmp_list
            save_config(tasks,filename='system_info.json')
            print('System end!')
            break