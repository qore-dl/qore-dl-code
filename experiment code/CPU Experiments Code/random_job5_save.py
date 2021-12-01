# 1584927559
import task_submit
from task_submit import VGGTask,RESTask,RETask,DENTask,XCETask
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
aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
aTokenw = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
LOSSHOST = '192.168.128.21'
LOSSPORT = 12527
DNA_SIZE = 4
XBOUND = [0.8,2]
XBOUND2 = [0.5,0.95]
YBOUND2 = [0.65,0.95]
YBOUND = [1,3]
CROSSOVER_RATE = 0.8
POP_SIZE = 16
N_GENERATIONS = 8
def translateDNA(pop):
    global DNA_SIZE,XBOUND,YBOUND
    print(pop.shape)
    #pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目：
    x_pop = pop[:,1::2]#从第1列开始，步进为2
    y_pop = pop[:,::2]#从第0列开始，步进为2
    # #pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)完成解码:二进制码求相应十进制值然后压缩到相应范围内即可完成解码
    x = x_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(XBOUND[-1] - XBOUND[0])+XBOUND[0]
    y = y_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(YBOUND[-1] - YBOUND[0])+YBOUND[0]
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
    return x, y


def get_fitness1(aim,pop,rfr,cpu_base,mem_base,worker,ps,total_cpu,total_memory):
    cpu_alpha,mem_alpha = translateDNA(pop)
    cpu_pre = cpu_base*cpu_alpha
    mem_pre = mem_base*mem_alpha
    pred = []
    for i in range(len(cpu_pre)):
        mini_batch = predict_min(aim,cpu_pre[i],mem_pre[i],rfr)
        mini_batch = float(mini_batch)
        pred.append((0-mini_batch)*((ps*700+worker*cpu_pre[i])/total_cpu+(ps*2048+worker*mem_pre[i])/total_memory))
    pred = np.array(pred)
    # pred = mini_batch
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

def get_fitness3(aim,pop,rfr,cpu_base,mem_base):
    #任务完成不了了，所以直接看minbatch可以减少多少而不是资源利用
    cpu_alpha,mem_alpha = translateDNA(pop)
    cpu_pre = cpu_base*cpu_alpha
    mem_pre = mem_base*mem_alpha
    pred = []
    for i in range(len(cpu_pre)):
        mini_batch = predict_min(aim,cpu_pre[i],mem_pre[i],rfr)
        mini_batch = float(mini_batch)
        pred.append((0-mini_batch))
    pred = np.array(pred)
    # pred = mini_batch
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

def get_fitness4(aim,pop,rfr,cpu_base,mem_base,cpu_allocate,mem_allocate,worker,total_cpu,total_mem,mini0):
    #任务可以完成，现在要减少资源，当然就是看减少资源的总量和减少资源造成的minibatch之间的权衡
    cpu_alpha,mem_alpha = translateDNA2(pop)
    cpu_pre = cpu_allocate*cpu_alpha
    mem_pre = mem_allocate*mem_alpha
    pred = []
    for i in range(len(cpu_pre)):
        if cpu_pre[i] < 0.55 * cpu_base:
            cpu_pre[i] = math.ceil(0.55 * cpu_base)
        if mem_pre[i] < 0.85 * mem_base:
            mem_pre[i] = math.ceil(0.85 * mem_base)
        mini_batch = predict_min(aim,cpu_pre[i],mem_pre[i],rfr)
        score = worker*(0.75*(cpu_allocate - cpu_pre[i])/total_cpu+0.25*(mem_allocate - mem_pre[i])/total_mem)
        minik = mini_batch/mini0
        score = score/minik
        pred.append(score)

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

def predict_min_first(rfr,cpu_alpha,mem_alpha,batch,flops,params):
    data = np.array([batch, flops, params, cpu_alpha, mem_alpha])
    data = np.mat(data)
    data = data.A
    iteration = rfr.predict(data)
    iteration = float(iteration)
    return iteration

def predict_min(job_name,cpu,mem, rfr):
    job_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
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
    iteration = rfr.predict(data)
    iteration = float(iteration)
    return iteration

def crossover_and_mutation(pop,pop_total,CROSS_RATE=0.8):
    global POP_SIZE,N_GENERATIONS
    new_pop = []
    i = 0
    pop_sizes = len(pop)
    for father in pop:
        # print(father)
        #遍历种群中的每一个个体，将该个体作为父亲
        #孩子先得到父亲的全部基因（这里我把一串二进制串的那些0，1称为基因）
        child = np.array(list(father)[:])
        i = i+1
        child2 = []
        # print(child.shape)
        cross = False
        if np.random.rand() < CROSS_RATE:
            cross = True
            # 产生子代时不是必然发生交叉，而是以一定的概率发生交叉
            mother = pop[np.random.randint(POP_SIZE)]#再种群中选择另一个个体，并将该个体作为母亲
            # if i == len(pop):
            #     i = 0
            # mother = pop[i]
            child2 = np.array(list(mother)[:])
            cross_points = np.random.randint(low=0,high=DNA_SIZE*2)#随机产生交叉的点
            child[cross_points:] = mother[cross_points:]#孩子得到位于交叉点后的母亲的基因
            child2[cross_points:] = father[cross_points:]
        mutation(child)  # 每个后代有一定的机率发生变异
        exist_res = existss(pop_total,child)
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
    return np.array(new_pop)

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
            if res_cpu[lay]+layout_config[lay]['worker']*(cpu_allocae-math.ceil(cpu_alpha[i]*cpu_base)) > 0 and res_mem[lay]+layout_config[lay]['worker']*(mem_allocate-mem_alpha[i]*mem_base)>0:
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
        if cpu_pre[i] < 0.55 * cpu_base:
            cpu_pre[i] = math.ceil(0.55 * cpu_base)
        if mem_pre[i] < 0.85 * mem_base:
            mem_pre[i] = math.ceil(0.85 * mem_base)
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

def assign_jobs(tasks,rfr,lock):
    global DNA_SIZE,POP_SIZE,N_GENERATIONS
    #选择标准有两个：
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
    job_basic = reload_jobs(tasks['last'], -1)
    print("reload a  job success!!")
    node_list_global = job_basic.node_list
    res_cpu = job_basic.node_cpu
    '''
    self.node_cpu['k8s-master'] = 32000
        self.node_cpu['k8s-worker0'] = 24000
        self.node_cpu['k8s-worker2'] = 24000
        self.node_cpu['k8sworker1'] = 16000
        self.node_cpu['k8s-worker3'] = 24000
        self.node_cpu['k8s-worker4'] = 16000
        self.node_cpu['k8s-worker5'] = 24000
    '''
    # res_cpu['k8s-master'] = 32000 - 1000
    # res_cpu['k8s-worker0'] = 24000 - 400
    # res_cpu['k8s-worker2'] = 24000 - 400
    # res_cpu['k8sworker1'] = 16000 - 600
    # res_cpu['k8s-worker3'] = 24000 - 200
    # res_cpu[]
    res_mem = job_basic.node_memory
    res_config0 = {}
    layout_config0 = {}
    lock.acquire()
    tmp_ns = tasks['ns']
    tmp_layout = tasks['nslayout']
    tmp_layout_key = tmp_layout.keys()
    for i in tmp_ns:
        layout_file = '/tfdata/k8snfs/%s/layout.json' % i
        res_file = '/tfdata/k8snfs/%s/%s_res.json' % (i,i)
        job_file = '/tfdata/k8snfs/%s/%s.json' % (i,i)
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
                tmp_layout_config[tmp_config[tk]] = {'ps':0,'worker':0}
            for tk in tmp_key:
                if 'ps' in tk:
                    tmp_cpu[tmp_config[tk]]+= 700
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
    for i in piotential:
        reload_tmp = reload_jobs(i, -1)
        # res_path = '/tfdata/k8snfs/%s/%s_res.json' % (i, i)
        # res_config = load_config(res_path)
        lock.acquire()
        tmp_ns2 = tasks['ns']
        lock.release()
        if i not in tmp_ns2:
            piotential.remove(i)
            res_cpu[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['cpu_source']
            res_mem[ke00] += layout_config0[i][ke00]['worker'] * res_config0[i]['mem_source']
            res_cpu[ke00] += layout_config0[i][ke00]['ps'] * 500
            res_mem[ke00] += layout_config0[i][ke00]['ps'] * 1024
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
                res_cpu[ke00] += layout_config0[i][ke00]['ps'] * 500
                res_mem[ke00] += layout_config0[i][ke00]['ps'] * 1024
            #         '''
            #         "deadline": 14843,
            #         "start_time": 1584816589.613,
            #         "cpu_source": 6046,
            #         "mem_source": 19225,
            #         "cpu_high": 8991,
            #         "memory_base": 8706,
            #         "batch_res": 785,
            #         "flops_res": 127834653,
            #         "params_res": 18273610,
            #          "step_base": 69,
            #            '''
            #         res_config0.pop(i)
            #         assign_config.pop(i)
            #         layout_config0.pop(i)
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
                now_mini = max(time_avg)
            else:
                now_mini = predict_min(i,reload_tmp.cpu_allocate,reload_tmp.memory_allocate,rfr)
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
            relise_cpu = 0
            relise_mem = 0
            for node in node_list_global:
                relise_cpu+=res_cpu[node]
                relise_mem +=res_mem[node]
            relise_cpu = relise_cpu/job_basic.total_cpu
            relise_mem = relise_mem/job_basic.total_mem
            relise = 0.75*relise_cpu+0.25*relise_mem
            if relise > 0.4:
                # 若资源空闲
                # 都可以完成，考虑增大资源，提高资源利用率，其中要提升的也是离deadline最近的任务和对于资源最敏感的任务
                if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                    aim1 = aim[aim_time[-1]][0]
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[-1]][0]
                    aim_time_po = []
                    up_limit = min(3, len(aim_time))
                    up_limit = 0 - up_limit
                    for i in range(up_limit, 0):
                        for j in aim[aim_time[i]]:
                            aim_time_po.append(j)
                    aim_mingan = {}
                    for j in aim_time_po:
                        reload_tmp = reload_jobs(j, -1)
                        # res_path = '/tfdata/k8snfs/%s/%s_res.json' % (j, j)
                        # res_config = load_config(res_path)
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
                            sco = sco1
                            if sco2 > sco1:
                                sco = sco2
                        mingan_key = list(aim_mingan.keys())
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
                mode = 1
            else:
                #资源比较紧张，此时考虑减少距离deadline最远且对资源最不敏感的任务
                if len(aim_time) == 1 and len(aim[aim_time[0]]) == 1:
                    aim1 = aim[aim_time[0]][0]
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[0]][0]
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
                        reload_tmp = reload_jobs(j, -1)
                        # res_path = '/tfdata/k8snfs/%s/%s_res.json' % (j, j)
                        # res_config = load_config(res_path)
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
                    mode = 4


        elif aim_time[0] < 0:
            # 有任务完不成，有任务可以完成，考虑减少资源和增大资源，减少离deadline最远且对资源最不敏感的任务，增大超时最严重的任务
            # 返回任务
            # 增加资源的任务为超时最严重的任务，没有疑问，减少资源的任务则为离deadline较远且对资源最不敏感的任务，即剥夺资源带来的影响最小：
            if len(aim_time) == 1 and len(aim[aim_time[-1]]) == 1:
                aim1 = aim[aim_time[-1]][0]
                aim2 = ''
            else:
                aim1 = aim[aim_time[-1]][0]
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
                    reload_tmp = reload_jobs(j, -1)
                    # res_path = '/tfdata/k8snfs/%s/%s_res.json' % (j, j)
                    # res_config = load_config(res_path)
                    cpu_per = math.ceil((reload_tmp.cpu_allocate) / (reload_tmp.worker_replicas))
                    mem_per = math.ceil((reload_tmp.memory_allocate) / (reload_tmp.worker_replicas))
                    remain0, total0, atmp0 = reload_tmp.get_remain(mode=0)
                    remain1, _, _ = reload_tmp.get_remain(mode=1)
                    sco1 = (predict_min(job_name=j, cpu=(reload_tmp.cpu_allocate - cpu_per),
                                        mem=(reload_tmp.memory_allocate - mem_per), rfr=rfr) - res_config0[j][
                                'mini']) / (
                                   (0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                   0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                    if remain1==0 or (reload_tmp.worker_replicas - 1)==0:
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
                aim2 = ''
            else:
                # 都完不成，则返回超时最严重的两个任务，开始启发式评估方案
                aim1 = aim[aim_time[-1]][0]
                if len(aim[aim_time[-1]][0]) > 1:
                    aim2 = aim[aim_time[-1]][1]
                else:
                    aim2 = aim[aim_time[-2]][0]
            mode = 3
    print('The mode will be used: %d' % mode)
    print('The first aim and second aim:')
    print(aim1)
    print(aim2)
    if mode == 0:
        print("Mode %d Do not find fit job to get modluation!!" % mode)
        return {},mode
    elif mode == 1:
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {},mode
        # 具体实施方案，则为两种选择，修改节点数和增加每个节点的资源，在这里评估指标变为节约的时间/资源
        # 可选方案：增加1个节点/添加相应的资源，判断方法：节约的时间/添加的资源，如果资源超过范围则丢弃该方案，直到找到合适的方案，备选方案为
        # job_aim1 = reload_jobs(aim1, -1)
        pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
        pop_total = []
        pop_total = existss(pop_total,pop,init=0)
        print(len(pop_total))
        '''
         "deadline": 14843,
        "start_time": 1584816589.613,
        "cpu_source": 6046,
        "mem_source": 19225,
        "cpu_high": 8991,
        "memory_base": 8706,
        "batch_res": 785,
        "flops_res": 127834653,
        "params_res": 18273610,
        "step_base": 69,
        '''
        for _ in range(N_GENERATIONS):
            pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
            pop = np.array(pop)
            fitness = get_fitness1(aim1, pop, rfr, res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'],res_config0[aim1]['worker'],res_config0[aim1]['ps'],job_basic.total_cpu,job_basic.total_mem)
            pop = select(pop, fitness)  # 选择生成新的种群
            if len(pop_total)>= 2**(2*DNA_SIZE)-1:
                break
        print(len(pop_total))
        method1 = {}
        method2 = {}
        if res_config0[aim1]['ps']< math.ceil(res_config0[aim1]['worker']/4):
            method1 = {'type':1,'ps':1,'worker':1}
            change_number = kongxian2(node_list_global,res_cpu,res_mem,1,res_config0[aim1]['cpu_source'],res_config0[aim1]['mem_source'])
        else:
            method1 = {'type':1,'ps':0,'worker':1}
            change_number = kongxian2(node_list_global, res_cpu, res_mem, 0, res_config0[aim1]['cpu_source'],
                                      res_config0[aim1]['mem_source'])
        # "cpu_high": 8991,
        # "memory_base": 8706,
        delete_pop = kongxian(res_cpu,res_mem,res_config0[aim1]['cpu_source'],res_config0[aim1]['mem_source'],res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'],layout_config0[aim1],pop)
        print("Unfit index are:")
        print(delete_pop)
        delete_pop = list(delete_pop)
        # ac = np.delete(ac,[1,3,5],axis=0)
        pop_new = np.delete(pop,delete_pop,axis=0)
        if pop_new.size==0 and not change_number:
            print("Mode %d Can not find a way to aim1!!" % mode)
            assign_config[aim1] = {}
        elif pop_new.size==0 and change_number:
            assign_config[aim1] = method1
        elif not change_number and pop_new.size>0:
            fitness = get_fitness1(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                   res_config0[aim1]['worker'], res_config0[aim1]['ps'], job_basic.total_cpu,
                                   job_basic.total_mem)
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index]*res_config0[aim1]['cpu_high'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index]*res_config0[aim1]['memory_base'])
            method2 = {'type':2,'cpu':aim1_cpu,'mem':aim1_mem}
            assign_config[aim1] = method2
        elif change_number and pop_new.size>0:
            fitness = get_fitness1(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                   res_config0[aim1]['worker'], res_config0[aim1]['ps'], job_basic.total_cpu,
                                   job_basic.total_mem)
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
            best_min_batch = predict_min(aim1,aim1_cpu,aim1_mem,rfr)
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
            #"cpu_source": 6046,
            #"mem_source": 19225,
            sco1 = res_config0[aim1]['need']+25 - (math.ceil(res_config0[aim1]['total_step']*res_config0[aim1]['worker']/(1+res_config0[aim1]['worker'])) - res_config0[aim1]['reload_point']+1)*res_config0[aim1]['mini']
            sco1 = sco1/(0.75*((res_config0[aim1]['ps']+method1['ps'])*700+(method1['worker']+res_config0[aim1]['worker'])*res_config0[aim1]['cpu_source'])/job_basic.total_cpu+0.25*((res_config0[aim1]['ps']+method1['ps'])*2048+(method1['worker']+res_config0[aim1]['worker'])*res_config0[aim1]['mem_source'])/job_basic.total_mem)
            sco2 = res_config0[aim1]['need'] - best_min_batch*res_config0[aim1]['remain_iter']
            sco2 = sco2/(0.75*(res_config0[aim1]['ps']*700+res_config0[aim1]['worker']*aim1_cpu)/job_basic.total_cpu+0.25*(res_config0[aim1]['ps']*2048+res_config0[aim1]['worker']*aim1_mem)/job_basic.total_mem)
            # max([sco2, sco1])
            sco_tmp0 = sco1
            if sco2 > sco1:
                sco_tmp0 = sco2
            if sco_tmp0 < 0:
                print('Mode %d: Can not find useful method!!'% mode)
                assign_config[aim1] = {}
            else:
                if sco1 > sco2:
                    assign_config[aim1] = method1
                else:
                    assign_config[aim1] = method2

            # print("最优的基因型：", pop[max_fitness_index])
            # print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))
        if assign_config[aim1]:
            if assign_config[aim1]['type']==1:
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
                if assign_config[aim1]['ps']!=0:
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    res_cpu[deal_node] -= 600
                    res_mem[deal_node] -= 2048
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
                    res_cpu[ulk]=res_cpu[ulk]+update_layouts[ulk]['worker']*(res_config0[aim1]['cpu_source']-assign_config[aim1]['cpu'])
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
                pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
                pop = np.array(pop)
                fitness = get_fitness1(aim1, pop, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['ps'], job_basic.total_cpu,
                                       job_basic.total_mem)
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
            if pop_new.size==0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size==0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size>0:
                fitness = get_fitness1(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['ps'], job_basic.total_cpu,
                                       job_basic.total_mem)
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size>0:
                fitness = get_fitness1(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['worker'], res_config0[aim1]['ps'], job_basic.total_cpu,
                                       job_basic.total_mem)
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA(pop_new)
                aim1_cpu = cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high']
                aim1_mem = mem_mod[max_fitness_index] * res_config0[aim1]['memory_base']
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
                sco1 = res_config0[aim1]['need'] + 25 - (
                            math.ceil(res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (1 + res_config0[aim1]['worker'])) -
                            res_config0[aim1]['reload_point'] + 1) * res_config0[aim1]['mini']
                sco1 = sco1 / (0.75 * ((res_config0[aim1]['ps'] + method1['ps']) * 700 + (
                            method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                                           'cpu_source']) / job_basic.total_cpu + 0.25 * (
                                           (res_config0[aim1]['ps'] + method1['ps']) * 2048 + (
                                               method1['worker'] + res_config0[aim1]['worker']) * res_config0[aim1][
                                               'mem_source']) / job_basic.total_mem)
                sco2 = res_config0[aim1]['need'] - best_min_batch * res_config0[aim1]['remain_iter']
                sco2 = sco2 / (0.75 * (res_config0[aim1]['ps'] * 700 + res_config0[aim1][
                    'worker'] * aim1_cpu) / job_basic.total_cpu + 0.25 * (
                                           res_config0[aim1]['ps'] * 2048 + res_config0[aim1][
                                       'worker'] * aim1_mem) / job_basic.total_mem)
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
    elif mode == 2:
        #一增一减，结合4和3即可轻松给出了
        #首先对于aim1,增加资源：
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {}, mode
        # job_aim1 = reload_jobs(aim1, -1)
        pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
        pop_total = []
        pop_total = existss(pop_total, pop, init=0)
        print(pop_total)
        '''
         "deadline": 14843,
        "start_time": 1584816589.613,
        "cpu_source": 6046,
        "mem_source": 19225,
        "cpu_high": 8991,
        "memory_base": 8706,
        "batch_res": 785,
        "flops_res": 127834653,
        "params_res": 18273610,
        "step_base": 69,
        '''
        for _ in range(N_GENERATIONS):
            pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
            pop = np.array(pop)
            # fitness = get_fitness3()
            fitness = get_fitness3(aim1, pop, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
            pop = select(pop, fitness)  # 选择生成新的种群
            if len(pop_total)>= 2**(2*DNA_SIZE)-1:
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
        if pop_new.size==0 and not change_number:
            print("Mode %d Can not find a way to aim1!!" % mode)
            assign_config[aim1] = {}
        elif pop_new.size==0 and change_number:
            assign_config[aim1] = method1
        elif not change_number and pop_new.size>0:
            fitness = get_fitness3(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
            method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
            assign_config[aim1] = method2
        elif change_number and pop_new.size>0:
            fitness = get_fitness3(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
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
                res_config0[aim1]['total_step'] * res_config0[aim1]['worker'] / (1 + res_config0[aim1]['worker'])) -
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
            if assign_config[aim1]['type']==1:
                res_condition = {}
                res_load = [res_cpu[i] for i in node_list_global]
                for no_k0 in node_list_global:
                    res_condition[res_cpu[no_k0]] = no_k0
                print("Now res_condition:")
                print(res_condition)
                list.sort(res_load)
                deal_node = res_condition[res_load[-1]]
                print("Add a worker to %s" % deal_node)
                res_cpu[deal_node]-=res_config0[aim1]['cpu_source']
                res_mem[deal_node]-=res_config0[aim1]['mem_source']
                aim1_tmp_layout = layout_config0[aim1]
                aim1_tlk = list(aim1_tmp_layout.keys())
                if deal_node in aim1_tlk:
                    layout_config0[aim1][deal_node]['worker']+=1
                else:
                    layout_config0[aim1][deal_node] = {'ps':0,'worker':1}
                res_condition.pop(res_load[-1])
                update_reload = res_load[-1]-res_config0[aim1]['cpu_source']
                res_condition[update_reload] = deal_node
                res_load[-1] = update_reload
                if assign_config[aim1]['ps']!=0:
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    print("Add a worker to %s" % deal_node)
                    res_cpu[deal_node] -= 600
                    res_mem[deal_node] -= 2048
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
                    res_cpu[ulk]=res_cpu[ulk]+update_layouts[ulk]['worker']*(res_config0[aim1]['cpu_source']-assign_config[aim1]['cpu'])
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
            '''
             "deadline": 14843,
            "start_time": 1584816589.613,
            "cpu_source": 6046,
            "mem_source": 19225,
            "cpu_high": 8991,
            "memory_base": 8706,
            "batch_res": 785,
            "flops_res": 127834653,
            "params_res": 18273610,
            "step_base": 69,
            '''
            for _ in range(N_GENERATIONS):
                pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
                pop = np.array(pop)
                # fitness = get_fitness3()
                fitness = get_fitness4(aim1, pop, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['worker'], job_basic.total_cpu, job_basic.total_mem,res_config0[aim1]['mini'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False

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
            if pop_new.size==0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size==0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size>0:
                fitness = get_fitness4(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'], res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       job_basic.total_cpu, job_basic.total_mem,res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.55 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.55 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 0.85 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(0.85 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size>0:
                fitness = get_fitness4(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       job_basic.total_cpu,
                                       job_basic.total_mem,res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.55 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.55 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 0.85 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(0.85 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                sco1 = 0.75 * (abs(method1['ps']) * 700 + abs(method1['worker']) * res_config0[aim1][
                    'cpu_source']) / job_basic.total_cpu + 0.25 * (
                               abs(method1['ps']) * 2048 + abs(method1['worker']) * res_config0[aim1][
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
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {}, mode
        # 具体实施方案，则为两种选择，修改节点数和增加每个节点的资源，在这里评估指标变为节约的时间/资源
        # 可选方案：增加1个节点/添加相应的资源，判断方法：节约的时间/添加的资源，如果资源超过范围则丢弃该方案，直到找到合适的方案，备选方案为
        # job_aim1 = reload_jobs(aim1, -1)
        pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
        pop_total = []
        pop_total = existss(pop_total, pop, init=0)
        print(pop_total)
        '''
         "deadline": 14843,
        "start_time": 1584816589.613,
        "cpu_source": 6046,
        "mem_source": 19225,
        "cpu_high": 8991,
        "memory_base": 8706,
        "batch_res": 785,
        "flops_res": 127834653,
        "params_res": 18273610,
        "step_base": 69,
        '''
        for _ in range(N_GENERATIONS):
            pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
            pop = np.array(pop)
            # fitness = get_fitness3()
            fitness = get_fitness3(aim1, pop, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
            pop = select(pop, fitness)  # 选择生成新的种群
            if len(pop_total)>= 2**(2*DNA_SIZE)-1:
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
        if pop_new.size==0 and not change_number:
            print("Mode %d Can not find a way to aim1!!" % mode)
            assign_config[aim1] = {}
        elif pop_new.size==0 and change_number:
            assign_config[aim1] = method1
        elif not change_number and pop_new.size>0:
            fitness = get_fitness3(aim1,pop_new,rfr,res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
            method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
            assign_config[aim1] = method2
        elif change_number and pop_new.size>0:
            fitness = get_fitness3(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
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
                res_config0[aim1]['total_step'] *res_config0[aim1]['worker'] / (1 + res_config0[aim1]['worker'])) - res_config0[aim1][
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
            if assign_config[aim1]['type']==1:
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
                if assign_config[aim1]['ps']!=0:
                    list.sort(res_load)
                    deal_node = res_condition[res_load[-1]]
                    res_cpu[deal_node] -= 600
                    res_mem[deal_node] -= 2048
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
                    res_cpu[ulk]=res_cpu[ulk]+update_layouts[ulk]['worker']*(res_config0[aim1]['cpu_source']-assign_config[aim1]['cpu'])
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
                pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
                pop = np.array(pop)
                fitness = get_fitness3(aim1, pop, rfr, res_config0[aim1]['cpu_high'],
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
            if pop_new.size==0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size==0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size>0:
                fitness = get_fitness3(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size>0:
                fitness = get_fitness3(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_high'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['memory_base'])
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
                if max(sco2, sco1) < 0:
                    print('Mode %d: Can not find useful method!!' % mode)
                    assign_config[aim1] = {}
                else:
                    if sco1 > sco2:
                        assign_config[aim1] = method1
                    else:
                        assign_config[aim1] = method2
    elif mode == 4:
        if not aim1:
            print("Mode %d Do not find aim1 to get modulateion!!" % mode)
            return {},mode
        # job_aim1 = reload_jobs(aim1, -1)
        pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
        pop_total = []
        pop_total = existss(pop_total, pop, init=0)
        print(pop_total)
        '''
         "deadline": 14843,
        "start_time": 1584816589.613,
        "cpu_source": 6046,
        "mem_source": 19225,
        "cpu_high": 8991,
        "memory_base": 8706,
        "batch_res": 785,
        "flops_res": 127834653,
        "params_res": 18273610,
        "step_base": 69,
        '''
        for _ in range(N_GENERATIONS):
            pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
            pop = np.array(pop)
            # fitness = get_fitness3()
            fitness = get_fitness4(aim1,pop,rfr,res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'],res_config0[aim1]['cpu_source'],res_config0[aim1]['mem_source'],res_config0[aim1]['worker'],job_basic.total_cpu,job_basic.total_mem,res_config0[aim1]['mini'])
            pop = select(pop, fitness)  # 选择生成新的种群
            if len(pop_total)>= 2**(2*DNA_SIZE)-1:
                break
        print(len(pop_total))
        method1 = {}
        method2 = {}
        change_number = False

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

        if res_config0[aim1]['ps'] > math.ceil(res_config0[aim1]['worker'] / 2):
            method1 = {'type': 1, 'ps': -1, 'worker': -1}
            change_number =finish2(res_config0[aim1]['total_step'],res_config0[aim1]['remain_time'],res_config0[aim1]['reload_point'],res_config0[aim1]['worker'],res_config0[aim1]['ps'],1,res_config0[aim1]['mini'])
        else:
            method1 = {'type': 1, 'ps': 0, 'worker': -1}
            change_number = finish2(res_config0[aim1]['total_step'], res_config0[aim1]['remain_time'],
                                    res_config0[aim1]['reload_point'], res_config0[aim1]['worker'],
                                    res_config0[aim1]['ps'], 0, res_config0[aim1]['mini'])
        delete_pop = finish(res_config0[aim1]['remain_iter'],pop,res_config0[aim1]['remain_time'],res_config0[aim1]['cpu_source'],res_config0[aim1]['mem_source'],res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'],rfr,aim1)
        print("Unfit index are:")
        print(delete_pop)
        delete_pop = list(delete_pop)
        # ac = np.delete(ac,[1,3,5],axis=0)
        pop_new = np.delete(pop, delete_pop, axis=0)
        if pop_new.size==0 and not change_number:
            print("Mode %d Can not find a way to aim1!!" % mode)
            assign_config[aim1] = {}
        elif pop_new.size==0 and change_number:
            assign_config[aim1] = method1
        elif not change_number and pop_new.size>0:
            fitness = get_fitness4(aim1,pop_new,rfr,res_config0[aim1]['cpu_high'],res_config0[aim1]['memory_base'],res_config0[aim1]['cpu_source'],
                                   res_config0[aim1]['mem_source'],res_config0[aim1]['worker'],job_basic.total_cpu,job_basic.total_mem,res_config0[aim1]['mini'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA2(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
            if aim1_cpu < 0.55 * res_config0[aim1]['cpu_high']:
                aim1_cpu = math.ceil(0.55 * res_config0[aim1]['cpu_high'])
            if aim1_mem < 0.85 * res_config0[aim1]['memory_base']:
                aim1_mem = math.ceil(0.85 * res_config0[aim1]['memory_base'])
            method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
            assign_config[aim1] = method2
        elif change_number and pop_new.size>0:
            fitness = get_fitness4(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                   res_config0[aim1]['cpu_source'],
                                   res_config0[aim1]['mem_source'], res_config0[aim1]['worker'], job_basic.total_cpu,
                                   job_basic.total_mem,res_config0[aim1]['mini'])
            max_fitness_index = np.argmax(fitness)
            print("max_fitness:", fitness[max_fitness_index])
            cpu_mod, mem_mod = translateDNA2(pop_new)
            aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
            aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
            if aim1_cpu < 0.55 * res_config0[aim1]['cpu_high']:
                aim1_cpu = math.ceil(0.55 * res_config0[aim1]['cpu_high'])
            if aim1_mem < 0.85 * res_config0[aim1]['memory_base']:
                aim1_mem = math.ceil(0.85 * res_config0[aim1]['memory_base'])
            method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
            sco1 = 0.75*(abs(method1['ps'])*700+abs(method1['worker'])*res_config0[aim1]['cpu_source'])/job_basic.total_cpu+0.25*(abs(method1['ps'])*2048+abs(method1['worker'])*res_config0[aim1]['mem_source'])/job_basic.total_mem
            sco2 = 0.75*(res_config0[aim1]['worker']*(res_config0[aim1]['cpu_source'] - aim1_cpu))/job_basic.total_cpu+0.25*(res_config0[aim1]['worker']*(res_config0[aim1]['mem_source'] - aim1_mem))/job_basic.total_mem
            if sco1 > sco2:
                assign_config[aim1] = method1
            else:
                assign_config[aim1] = method2

        if not aim2:
            assign_config[aim2] = {}
        else:
            aim1 = aim2
            # job_aim2 = reload_jobs(aim1, -1)
            pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))
            pop_total = []
            pop_total = existss(pop_total, pop, init=0)
            print(pop_total)
            '''
             "deadline": 14843,
            "start_time": 1584816589.613,
            "cpu_source": 6046,
            "mem_source": 19225,
            "cpu_high": 8991,
            "memory_base": 8706,
            "batch_res": 785,
            "flops_res": 127834653,
            "params_res": 18273610,
            "step_base": 69,
            '''
            for _ in range(N_GENERATIONS):
                pop = crossover_and_mutation(pop,pop_total,CROSSOVER_RATE)
                pop = np.array(pop)
                # fitness = get_fitness3()
                fitness = get_fitness4(aim1, pop, rfr, res_config0[aim1]['cpu_high'], res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'], res_config0[aim1]['mem_source'],
                                       res_config0[aim1]['worker'], job_basic.total_cpu,job_basic.total_mem,res_config0[aim1]['mini'])
                pop = select(pop, fitness)  # 选择生成新的种群
                if len(pop_total) >= 2 ** (2 * DNA_SIZE) - 1:
                    break
            print(len(pop_total))
            method1 = {}
            method2 = {}
            change_number = False

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
            if pop_new.size==0 and not change_number:
                print("Mode %d Can not find a way to aim1!!" % mode)
                assign_config[aim1] = {}
            elif pop_new.size==0 and change_number:
                assign_config[aim1] = method1
            elif not change_number and pop_new.size>0:
                fitness = get_fitness4(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'], res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       job_basic.total_cpu, job_basic.total_mem,res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.55 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.55 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 0.85 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(0.85 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                assign_config[aim1] = method2
            elif change_number and pop_new.size>0:
                fitness = get_fitness4(aim1, pop_new, rfr, res_config0[aim1]['cpu_high'],
                                       res_config0[aim1]['memory_base'],
                                       res_config0[aim1]['cpu_source'],
                                       res_config0[aim1]['mem_source'], res_config0[aim1]['worker'],
                                       job_basic.total_cpu,
                                       job_basic.total_mem,res_config0[aim1]['mini'])
                max_fitness_index = np.argmax(fitness)
                print("max_fitness:", fitness[max_fitness_index])
                cpu_mod, mem_mod = translateDNA2(pop_new)
                aim1_cpu = math.ceil(cpu_mod[max_fitness_index] * res_config0[aim1]['cpu_source'])
                aim1_mem = math.ceil(mem_mod[max_fitness_index] * res_config0[aim1]['mem_source'])
                if aim1_cpu < 0.55 * res_config0[aim1]['cpu_high']:
                    aim1_cpu = math.ceil(0.55 * res_config0[aim1]['cpu_high'])
                if aim1_mem < 0.85 * res_config0[aim1]['memory_base']:
                    aim1_mem = math.ceil(0.85 * res_config0[aim1]['memory_base'])
                method2 = {'type': 2, 'cpu': aim1_cpu, 'mem': aim1_mem}
                sco1 = 0.75 * (abs(method1['ps']) * 700 + abs(method1['worker']) * res_config0[aim1][
                    'cpu_source']) / job_basic.total_cpu + 0.25 * (
                                   abs(method1['ps']) * 2048 + abs(method1['worker']) * res_config0[aim1][
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

    return assign_config,mode


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
    node_cpu['k8s-master'] = 32000 - 1000
    node_cpu['k8s-worker0'] = 24000 - 400
    node_cpu['k8s-worker2'] = 24000 - 400
    node_cpu['k8sworker1'] = 16000 - 520
    node_cpu['k8s-worker3'] = 24000 - 150
    node_cpu['k8s-worker4'] = 16000 - 150
    node_cpu['k8s-worker5'] = 24000 - 150
    node_memory = {}
    node_memory['k8s-master'] = float(251 * 1024 - 20000)
    node_memory['k8s-worker0'] = float(94 * 1024 - 4000)
    node_memory['k8s-worker2'] = float(94 * 1024 - 3000)
    node_memory['k8sworker1'] = float(125 * 1024 - 4500)
    node_memory['k8s-worker3'] = float(94 * 1024 - 2200)
    node_memory['k8s-worker4'] = float(125 * 1024 - 2200)
    node_memory['k8s-worker5'] = float(94 * 1024 - 2200)
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
                # else:
                #     # print(b[0].status.container_statuses[0].state.terminated.reason)
                #     pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                #     lock.acquire()
                #     tmp_reload_ns = tasks['retry']
                #     lock.release()
                #     if ('Succeeded' in pod_status or 'Failed' in pod_status) and (ns not in tmp_reload_ns):
                #         # # print(b[0].status.container_statuses[0].state.terminated.reason)
                #         # pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                #         # ['OOMKilled']
                #         save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (ns,ns)
                #         res_job_config = load_config(save_res_path)
                #         res_job_config['endtime'] = time.time() - 10
                #         time.sleep(10)
                #         try:
                #             exit_reason = [i.status.container_statuses[0].state.terminated.reason for i in
                #                            v1.list_namespaced_pod(ns).items]
                #             print(exit_reason)
                #             exit_ict = {'reasons': exit_reason}
                #             exit_path = '/tfdata/k8snfs/%s/exit_reason.json' % ns
                #             exit_json = json.dumps(exit_ict, ensure_ascii=False, indent=4)
                #             fw_exit = open(exit_path, 'w', encoding='utf-8')
                #             fw_exit.write(exit_json)
                #             fw_exit.close()
                #         except Exception as e:
                #             print(e)
                #         time.sleep(6)
                #         lock.acquire()
                #         # job_tmp = tasks['job']
                #         # job = job_tmp[ns]
                #         # job.delete_tf()
                #         # command = 'kubectl delete -f /tfdata/tfcnn/expjob/'+ns+'.yaml'
                #         command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + ns + '.yaml'
                #         os.system(command)
                #         v1.delete_namespace(ns)
                #         ns_tmp = tasks['ns']
                #         ns_tmp.remove(ns)
                #         tasks['ns'] = ns_tmp
                #         is_layout = tasks['nslayout']
                #         is_layout.pop(ns)
                #         for i in range(len(jobs)):
                #             if jobs[i] == ns:
                #                 jobs.pop(i)
                #                 break
                #         tasks['nslayout'] = is_layout
                #         # job_tmp.pop(ns)
                #         # tasks['job'] = job_tmp
                #         tasks['count'] -= 1
                #         lock.release()
                #     time.sleep(4)

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
    job_measure = job.measure
    print("job measure: %s" % job.measure)
    pre_list = job_measure.split(' ')
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_load = pre_list[0] + 'L' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    count = 0
    count2 = 0
    while True:
        pod_status = [i.status.phase for i in job.v1.list_namespaced_pod(job.name).items]
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
        # elif 'Running' in pod_status:
        elif 'Succeeded' in pod_status or 'Failed' in pod_status:
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
                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
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
                time.sleep(3)
                lock.acquire()
                command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + job.name + '.yaml'
                os.system(command)
                v1.delete_namespace(job.name)
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
                    fp = open('/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                    # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                    dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                    fp.write(dicc_json)
                    fp.close()
            save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
            res_config = load_config(save_res_path)
            keys_res = res_config.keys()
            if 'reloadtime' not in keys_res:
                res_config['reloadtime'] = []
            # 'cpu_high': cpu_base, 'memory_base': mem_base
            if count2 < 4:
                print("apply resource!")
                if job.cpu_allocate > res_config['cpu_high']:
                    if math.ceil(job.cpu_allocate*0.85) >= res_config['cpu_high']:
                        save_job_change_resource(job.name, math.ceil(job.cpu_allocate*0.85), job.memory_allocate)
                        job.assignment_resource(math.ceil(job.cpu_allocate*0.85), job.memory_allocate)
                    else:
                        save_job_change_resource(job.name, res_config['cpu_high'], job.memory_allocate)
                        job.assignment_resource(res_config['cpu_high'], job.memory_allocate)
                else:
                    save_job_change_resource(job.name, math.ceil(job.cpu_allocate*0.9), job.memory_allocate)
                    job.assignment_resource(math.ceil(job.cpu_allocate*0.9), job.memory_allocate)
                print("modulate the cpu!!")
                if job.memory_allocate > res_config['memory_base']:
                    #  "cpu_high": 15780,
                    #     "memory_base": 32113,
                    if math.ceil(job.memory_allocate * 0.85) >= res_config['memory_base']:
                        save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.85))
                        job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.85))
                    else:
                        save_job_change_resource(job.name, job.cpu_allocate, res_config['memory_base'])
                        job.assignment_resource(job.cpu_allocate, res_config['memory_base'])
                    print("modulate the memory!!")
                else:
                    save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                    job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                count2+=1
                time.sleep(50)
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
                job.retry_tf(job.cpu_allocate,job.memory_allocate,aim_step,job.worker_replicas,(job.ps_replicas - 1))
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
                save_config(res_config,save_res_path)
                count2+=1
                time.sleep(38)
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
                job.retry_tf(job.cpu_allocate,job.memory_allocate,aim_step,job.worker_replicas-1,job.ps_replicas)
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
                save_config(res_config,save_res_path)
                count2+=1
                print("reduce worker number successfully!!")
                time.sleep(38)
            elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                if count2 <= 7:
                    save_job_change_resource(job.name, math.ceil(job.cpu_allocate*0.9), job.memory_allocate)
                    job.assignment_resource(math.ceil(job.cpu_allocate*0.9), job.memory_allocate)
                    print("modulate CPU before goto Next")
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
                    command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + job.name + '.yaml'
                    os.system(command)
                    v1.delete_namespace(job.name)
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
                    time.sleep(50)
        elif not run_result_dict:
            ceshi_tmp_ns = tasks['ns']
            if job.name not in ceshi_tmp_ns:
                return
            if count >= 8:
                jieshu = True
                print("Exception exit! Creating Problem!")
                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                res_job_config = load_config(save_res_path)
                res_job_config['errtime'] = time.time() - 5
                save_config(res_job_config, save_res_path)
                lock.acquire()
                # command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + job.name + '.yaml'
                # os.system(command)
                v1.delete_namespace(job.name)
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
            time.sleep(40)
        else:
            time.sleep(40)
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
            save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
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
                if int(solution['type']) == 2:
                    save_job_change_resource(job.name, math.ceil(solution['cpu']), math.ceil(solution['mem']))
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
                elif int(solution['type']) == 1:
                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
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
                    lock.acquire()
                    # method1 = {'type': 1, 'ps': 0, 'worker': 1}
                    time1 = time.time()
                    job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, aim_worker_replicas, aim_ps_replicas)
                    time2 = time.time()
                    tmp_retry_job = tasks['retry']
                    tmp_retry_job.remove(job.name)
                    tasks['retry'] = tmp_retry_job
                    tmp_retry_solution3 = tasks['solution']
                    tmp_retry_solution3.pop(job.name)
                    tasks['solution'] = tmp_retry_solution3
                    time.sleep(4)
                    lock.release()
                    tmp_reload = res_config['reloadtime']
                    tmp_reload.append((time2 - time1))
                    res_config['reloadtime'] = tmp_reload
                    save_config(res_config, save_res_path)
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
            if 'Running' in pod_status2 and run_result_dict2['Running'] == (job.ps_replicas + job.worker_replicas):
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
                    fp = open('/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
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
                # # print(b[0].status.container_statuses[0].state.terminated.reason)
                # pod_status = [i.status.phase for i in v1.list_namespaced_pod(ns).items]
                # ['OOMKilled']
                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                res_job_config = load_config(save_res_path)
                res_job_config_keys = list(res_job_config.keys())
                if 'endtime' not in res_job_config_keys:
                    res_job_config['endtime'] = time.time() - 10
                save_config(res_job_config, save_res_path)
                time.sleep(3)
                if (job.name not in tmp_retrys) and not tasks['modulate']:
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
                    time.sleep(5)
                    lock.acquire()
                    command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + job.name + '.yaml'
                    os.system(command)
                    print("delete this job %s!!!" % job.name)
                    v1.delete_namespace(job.name)
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
            # elif ('Succeeded' in pod_status or 'Failed' in pod_status):
            #     lock.acquire()
            #     save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
            #     res_job_config = load_config(save_res_path)
            #     res_job_config_keys = list(res_job_config.keys())
            #     lock.release()
            #     if 'endtime' not in res_job_config_keys:
            #         res_job_config['endtime'] = time.time() - 10
            #     save_config(res_job_config, save_res_path)
            #     time.sleep(6)
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
                        fp = open('/tfdata/k8snfs/' + job_name + '/layout.json', 'w', encoding='utf-8')
                        # ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
                        dicc_json = json.dumps(tmp_layout_config, ensure_ascii=False, indent=4)  # 字典转成json，字典转成字符串
                        fp.write(dicc_json)
                        fp.close()
                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                res_config = load_config(save_res_path)
                keys_res = res_config.keys()
                if 'reloadtime' not in keys_res:
                    res_config['reloadtime'] = []
                # 'cpu_high': cpu_base, 'memory_base': mem_base
                if count2 < 4:
                    print("apply resource!")
                    if job.cpu_allocate > res_config['cpu_high']:
                        if math.ceil(job.cpu_allocate * 0.85) >= res_config['cpu_high']:
                            save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.85), job.memory_allocate)
                            job.assignment_resource(math.ceil(job.cpu_allocate * 0.85), job.memory_allocate)
                        else:
                            save_job_change_resource(job.name, res_config['cpu_high'], job.memory_allocate)
                            job.assignment_resource(res_config['cpu_high'], job.memory_allocate)
                    else:
                        save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.9), job.memory_allocate)
                        job.assignment_resource(math.ceil(job.cpu_allocate * 0.9), job.memory_allocate)
                    print("modulate the cpu!!")
                    if job.memory_allocate > res_config['memory_base']:
                        #  "cpu_high": 15780,
                        #     "memory_base": 32113,
                        if math.ceil(job.memory_allocate * 0.85) >= res_config['memory_base']:
                            save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.85))
                            job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.85))
                        else:
                            save_job_change_resource(job.name, job.cpu_allocate, res_config['memory_base'])
                            job.assignment_resource(job.cpu_allocate, res_config['memory_base'])
                        print("modulate the memory!!")
                    else:
                        save_job_change_resource(job.name, job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                        job.assignment_resource(job.cpu_allocate, math.ceil(job.memory_allocate * 0.92))
                    count2 += 1
                    time.sleep(35)
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
                    job.retry_tf(job.cpu_allocate, job.memory_allocate, aim_step, job.worker_replicas,
                                 (job.ps_replicas - 1))
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
                    time.sleep(32)
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
                    tmp_reload = res_config['reloadtime']
                    tmp_reload.append((time2 - time1))
                    res_config['reloadtime'] = tmp_reload
                    save_config(res_config, save_res_path)
                    count2 += 1
                    print("reduce worker number successfully!!")
                    time.sleep(32)
                elif (job.worker_replicas == 1 and job.ps_replicas == 1):
                    if count2 <= 7:
                        save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.9), job.memory_allocate)
                        job.assignment_resource(math.ceil(job.cpu_allocate * 0.9), job.memory_allocate)
                        print("modulate CPU before goto Next")
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
                        command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + job.name + '.yaml'
                        os.system(command)
                        v1.delete_namespace(job.name)
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
                        count2 += 1
                        time.sleep(32)
            elif not run_result_dict2:
                ceshi_tmp_ns = tasks['ns']
                if job.name not in ceshi_tmp_ns:
                    return
                if count > 8:
                    jieshu = True
                    print("Exception exit! Creating Problem!")
                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_job_config = load_config(save_res_path)
                    res_job_config['errtime'] = time.time() - 5
                    save_config(res_job_config, save_res_path)
                    lock.acquire()
                    command = 'kubectl delete -f /tfdata/tfcnn/expjob/' + job.name + '.yaml'
                    os.system(command)
                    v1.delete_namespace(job.name)
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
                count += 1
                time.sleep(37)
            else:
                time.sleep(15)

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
        if node_index[key] <=4:
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

def check_path(name):
    train_dir = os.path.join('/tfdata/k8snfs/', name)
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

def Submit_job(tasks,lock,v1,jobs):
    try:
        rfr = joblib.load('rfr_batch.pkl')
    except Exception as e0:
        print(e0)
    # est_mem = joblib.load('est_mem.pkl')
    # est_cpu = joblib.load('est_cpu.pkl')
    print('start to reload')
    print(jobs)
    global LOSSHOST,LOSSPORT
    ADDR = (LOSSHOST,LOSSPORT)
    PREHOST = '192.168.128.21'
    PREPORT = 12529
    ADDR2 = (PREHOST,PREPORT)
    max_buffer_size = 5
    job_basic = reload_jobs(tasks['last'],-1)
    max_free_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_free_load)
    max_wight_heap = MaxHeap(max_size=max_buffer_size,fn=worker_queue.value_weight_load)
    worker_buffer = tasks['buffer']
    first_reload = False
    time.sleep(20)
    if worker_buffer:
        first_reload = True
    pool = multiprocessing.Pool(processes=10)
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
        job01 = reload_jobs(job0,-1)
        # catch_node_step_msg(jobs=,job_name=,tasks=,lock=,batch=,flops=,params=,mode=)
        loss_server_conn(ADDR,job01.measure)
        pool.apply_async(catch_node_step_msg,args=(jobs,job0,tasks,lock,batch_res,flops_res,params_res,-1))
    global_count = 1
    while True:
        print("Global Count is :%d" % global_count)
        if tasks['start']==False:
            break
        if global_count >3 and global_count % 7 != 0 and global_count%12 != 0:
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
                job_next_time = tasks['nexttimes'][job_name]
                job_next_time+=1
                tasks['nexttimes'][job_name] = job_next_time
                tasks['next'] = tmp_next
                lock.release()
                job = reload_jobs(job_name, -1)
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
                            if can_use_cpu - 750 > 0:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 750
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
                                if can_use_cpu - 750 > 0:
                                    catch_ps_c += 1
                                    can_use_cpu = can_use_cpu - 750
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

                    if catch_ps >= 1 and catch_worker >= 1:
                        break
                print("In next catch ps: %d,worker:%d" % (catch_ps, catch_worker))
                if catch_ps > 0 and catch_worker > 0:
                    lock.acquire()
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
                        lock.release()
                        continue
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
                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    batch_res = res_config['batch_res']
                    flops_res = res_config['flops_res']
                    params_res = res_config['params_res']
                    pool.apply_async(catch_node_step_msg,
                                     args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                    # tasks['next'] = ''
                    lock.release()
                else:
                    lock.acquire()
                    tmp_buffer_count0 = tasks['buffercount']
                    if tasks['nexttimes'][job.name] >=3 and tmp_buffer_count0 < max_buffer_size:
                        tmp_buffer_pool = tasks['buffer']
                        tmp_buffer_pool.append(job.name)
                        tasks['buffer'] = tmp_buffer_pool
                        tmp_buffer_count0+=1
                        tasks['buffercount'] = tmp_buffer_count0
                        tmp_next_time_config = tasks['nexttimes']
                        tmp_next_time_config.pop(job.name)
                        tasks['nexttimes'] =  tmp_next_time_config
                    else:
                        tmp_next = tasks['next']
                        tmp_next.append(job.name)
                        # tmp_next_time_config = tasks['nexttimes']
                        # tmp_next_time_config[job.name] = 0
                        # tasks['nexttimes'] = tmp_next_time_config
                        tasks['next'] = tmp_next
                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    # save_res_path = '/tfdata/tfcnn'
                    res_config = load_config(save_res_path)
                    if job.cpu_allocate > math.ceil(0.55*res_config['cpu_high']):
                        if math.ceil(job.cpu_allocate * 0.75) >= math.ceil(0.55*res_config['cpu_high']):
                            save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.85),
                                                     job.memory_allocate)
                        else:
                            save_job_change_resource(job.name, math.ceil(0.55*res_config['cpu_high']), job.memory_allocate)
                        # job.assignment_resource(res_config['cpu_high'], job.memory_allocate)
                        print("modulate the cpu!!")
                    else:
                        if job.memory_allocate > res_config['memory_base']:
                            save_job_change_resource(job.name, job.cpu_allocate, res_config['memory_base'])
                            # job.assignment_resource(job.cpu_allocate, res_config['memory_base'])
                            print("modulate the memory!!")
                    lock.release()
                    time.sleep(30)
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
                tmp_ps_replicas = job.ps_replicas
                tmp_worker_replicas = job.worker_replicas
                if cpu_value < 0.4:
                    job.worker_replicas = random.randint(4, 6)
                elif cpu_value < 0.7:
                    job.worker_replicas = random.randint(3, 4)
                else:
                    job.worker_replicas = random.randint(1, 2)
                job.ps_replicas = random.randint(math.ceil(job.worker_replicas / 4),
                                                 math.ceil(job.worker_replicas / 2))
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
                            if can_use_cpu - 750 > 0 and not reach_ps:
                                catch_ps_c += 1
                                can_use_cpu = can_use_cpu - 750
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
                                if can_use_cpu - 750 > 0 and not reach_ps:
                                    catch_ps_c += 1
                                    can_use_cpu = can_use_cpu - 750
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
                        lock.acquire()
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
                            lock.release()
                            continue
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
                        save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                        # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                        # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                        # 'cpu_high':cpu_base,'batch_res':batch_res,
                        # 'flops_res':flops_res,'params_res':params_res}
                        res_config = load_config(save_res_path)
                        batch_res = res_config['batch_res']
                        flops_res = res_config['flops_res']
                        params_res = res_config['params_res']
                        pool.apply_async(catch_node_step_msg,
                                         args=(
                                             jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                        lock.release()
                    else:
                        job.ps_replicas = 1
                        job.worker_replicas = 1
                        job.training_step = job.training_step = math.ceil(job.training_step * tmp_worker)
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
                    lock.acquire()
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
                        lock.release()
                        continue
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
                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                    res_config = load_config(save_res_path)
                    batch_res = res_config['batch_res']
                    flops_res = res_config['flops_res']
                    params_res = res_config['params_res']
                    pool.apply_async(catch_node_step_msg,
                                     args=(
                                         jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                    lock.release()
            global_count+=1
            time.sleep(83.3)
        if global_count % 12 == 0 or global_count<=3:
            print('start to submit a job!!')
            for _ in range(10):
                lock.acquire()
                counts = tasks['count']
                bufer_count = tasks['buffercount']
                lock.release()
                if (counts >= tasks['size']) and (bufer_count >= max_buffer_size):
                    time.sleep(float(random.randint(7,9)))
                    pass
                # elif tasks['next'] and counts < tasks['size']:
                #     print("panduan tasks in next")
                #     lock.acquire()
                #     tmp_next = tasks['next']
                #     job_name = tmp_next.pop(0)
                #     tasks['next'] = tmp_next
                #     lock.release()
                #     job = reload_jobs(job_name, -1)
                #     print("%s in next reload!" % job_name)
                #     node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                #     # mem_need = job.total_mem * total_mem_use + job.worker_replicas * job.memory_allocate + 2048 * job.ps_replicas
                #     # cpu_need = job.total_cpu * total_cpu_use + job.worker_replicas * job.cpu_allocate + 1000 * job.ps_replicas
                #     catch_worker = 0
                #     catch_ps = 0
                #
                #     node_keys = cpu_nodes.keys()
                #     for key in node_keys:
                #         catch_ps_c = 0
                #         catch_ps_m = 0
                #         catch_worker_c = 0
                #         catch_worker_m = 0
                #         can_use_cpu = job.node_cpu[key] * (1 - cpu_nodes[key])
                #         can_use_mem = job.node_memory[key] * (1 - memory_nodes[key])
                #         first_try = True
                #         endcpu = False
                #         endmem = False
                #         count_trys = 0
                #         while (not endcpu) or (not endmem):
                #             if first_try:
                #                 if can_use_cpu - 1000 > 0:
                #                     catch_ps_c += 1
                #                     can_use_cpu = can_use_cpu - 1000
                #                 else:
                #                     if can_use_cpu - job.cpu_allocate > 0:
                #                         catch_worker_c += 1
                #                         can_use_cpu = can_use_cpu - job.cpu_allocate
                #
                #                 if can_use_mem - 2048 > 0:
                #                     catch_ps_m += 1
                #                     can_use_mem = can_use_mem - 2048
                #                 else:
                #                     if can_use_mem - job.memory_allocate > 0:
                #                         catch_worker_m += 1
                #                         can_use_mem = can_use_mem - job.memory_allocate
                #                 first_try = False
                #             else:
                #                 if can_use_cpu - job.cpu_allocate > 0:
                #                     catch_worker_c += 1
                #                     can_use_cpu = can_use_cpu - job.cpu_allocate
                #                 else:
                #                     if can_use_cpu - 1000 > 0:
                #                         catch_ps_c += 1
                #                         can_use_cpu = can_use_cpu - 1000
                #                     else:
                #                         endcpu = True
                #
                #                 if can_use_mem - job.memory_allocate > 0:
                #                     catch_worker_m += 1
                #                     can_use_mem = can_use_mem - job.memory_allocate
                #                 else:
                #                     if can_use_mem - 2048 > 0:
                #                         catch_ps_m += 1
                #                         can_use_mem = can_use_mem - 2048
                #                     else:
                #                         endmem = True
                #
                #         if catch_worker_c < catch_worker_m:
                #             catch_worker += catch_worker_c
                #         else:
                #             catch_worker += catch_worker_m
                #
                #         if catch_ps_c < catch_ps_m:
                #             catch_ps += catch_ps_c
                #         else:
                #             catch_ps += catch_ps_m
                #
                #         if catch_ps >= 1 and catch_worker >= 1:
                #             break
                #     print("In next catch ps: %d,worker:%d" % (catch_ps, catch_worker))
                #     if catch_ps > 0 and catch_worker > 0:
                #         lock.acquire()
                #         job.update_step()
                #         print("in next update step success!!")
                #         write_step_meg(job.name)
                #         connected = False
                #         try_times = 1
                #         while True:
                #             if try_times > 5:
                #                 break
                #             print(job.measure)
                #             print(ADDR)
                #             connected = loss_server_conn(ADDR, job.measure)
                #             print("connect result:")
                #             print(connected)
                #             if connected:
                #                 break
                #             else:
                #                 try_times += 1
                #         if not connected:
                #             print("Conncet error!!Try again Later!!")
                #             lock.release()
                #             continue
                #         job.create_tf()
                #         ns_tmp = tasks['ns']
                #         ns_tmp.append(job.name)
                #         tasks['ns'] = ns_tmp
                #         # job_tmp = tasks['job']
                #         # job_tmp[job.name] = job
                #         # tasks['job'] = job_tmp
                #         is_layout = tasks['nslayout']
                #         is_layout[job.name] = False
                #         tasks['nslayout'] = is_layout
                #         jobs.append(job.name)
                #         tasks['count'] += 1
                #         save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                #         # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                #         # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                #         # 'cpu_high':cpu_base,'batch_res':batch_res,
                #         # 'flops_res':flops_res,'params_res':params_res}
                #         res_config = load_config(save_res_path)
                #         batch_res = res_config['batch_res']
                #         flops_res = res_config['flops_res']
                #         params_res = res_config['params_res']
                #         pool.apply_async(catch_node_step_msg,
                #                          args=(jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                #         # tasks['next'] = ''
                #         lock.release()
                #     else:
                #         # lock.acquire()
                #         tmp_next = tasks['next']
                #         tmp_next.append(job.name)
                #         tasks['next'] = tmp_next
                #         save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                #         # save_res_path = '/tfdata/tfcnn'
                #         res_config = load_config(save_res_path)
                #         if job.cpu_allocate > res_config['cpu_high']:
                #             if math.ceil(job.cpu_allocate * 0.85) >= res_config['cpu_high']:
                #                 save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.85),
                #                                          job.memory_allocate)
                #             else:
                #                 save_job_change_resource(job.name, res_config['cpu_high'], job.memory_allocate)
                #             # job.assignment_resource(res_config['cpu_high'], job.memory_allocate)
                #             print("modulate the cpu!!")
                #         else:
                #             if job.memory_allocate > res_config['memory_base']:
                #                 save_job_change_resource(job.name, job.cpu_allocate, res_config['memory_base'])
                #                 # job.assignment_resource(job.cpu_allocate, res_config['memory_base'])
                #                 print("modulate the memory!!")
                #             else:
                #                 save_job_change_resource(job.name, math.ceil(job.cpu_allocate * 0.9),
                #                                          job.memory_allocate)
                #         # lock.release()
                #         time.sleep(30)
                else:
                    print('select a job!!')
                    time.sleep(60)
                    template_id = random.randint(1,4)
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
                            channels = [24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400,
                                        480,
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
                                          'num_layer5': job.num_layer5,
                                          'retry': job.retry}

                            dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                                    'channel4': channel4,
                                    'channel5': channel5, 'num_layer1': num_layer1, 'num_layer2': num_layer2,
                                    'num_layer3': num_layer3, 'num_layer4': num_layer4, 'num_layer5': num_layer5}


                        elif template_id == 2:
                            bottle = random.randint(0, 1)
                            channels = [24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384, 400,
                                        480,
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

                            dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                                    'channel4': channel4,
                                    'layer1': layer1, 'layer2': layer2,
                                    'layer3': layer3, 'layer4': layer4, 'bottle': bottle}

                        elif template_id == 3:
                            stack = random.randint(3, 16)
                            channels = [12, 16, 24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384,
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
                            dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
                                    'channel4': channel4, 'stack_num': stack}

                            job_config = {
                                'template_id': job.template_id, 'ps_replicas': job.ps_replicas,
                                'worker_replicas': job.worker_replicas, 'training_step': job.training_step,
                                'batch_size': job.batch_size, 'interval': job.interval,
                                'task_id': job.task_id, 'rtimes': job.rtimes,
                                'tag': job.tag, 'stack': job.stack, 'channel1': job.channel1, 'channel2': job.channel2,
                                'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry
                            }

                        elif template_id == 4:
                            repeat = random.randint(4, 12)
                            channels = [12, 16, 24, 32, 40, 48, 64, 72, 80, 96, 120, 128, 160, 192, 240, 256, 320, 384,
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
                                'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8,
                                'retry': job.retry
                            }

                            dict = {'batch': batch, 'channel1': channel1, 'channel2': channel2, 'channel3': channel3,
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

                            dict = {'batch': job.batch_size, 'channel1': job.channel1, 'channel2': job.channel2,
                                    'channel3': job.channel3,
                                    'channel4': job.channel4,
                                    'channel5': job.channel5, 'num_layer1': job.num_layer1,
                                    'num_layer2': job.num_layer2,
                                    'num_layer3': job.num_layer3, 'num_layer4': job.num_layer4,
                                    'num_layer5': job.num_layer5}
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
                                'channel3': job.channel3, 'channel4': job.channel4, 'retry': job.retry
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
                                'channel6': job.channel6, 'channel7': job.channel7, 'channel8': job.channel8,
                                'retry': job.retry
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
                                'tag': job.tag, 'L': job.L, 'k': job.k, 'BC': job.BC, 'retry': job.retry
                            }

                            dict = {'batch': job.batch_size, 'BC': job.BC, 'k': job.k, 'L': job.L, 'num_classes': 10}
                        measure = job.measure
                    lock.acquire()
                    if tasks['count'] < tasks['size'] or tasks['buffercount'] < max_buffer_size:
                        # loss_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        # loss_client.connect(ADDR)
                        client_pre = influxdb.InfluxDBClient(host=job.dbhost, port=8086, username='admin',
                                                             password='admin',
                                                             database="PREDICT")
                        pre_list = measure.split(" ")
                        # measure_s = pre_list[0] + 'S' + pre_list[-1]
                        measure_t = pre_list[0] + 'T' + pre_list[-1]
                        save_config_dir = task_submit.check_path(job.name)
                        save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job.name, job.name)
                        # save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                        save_config(job_config, save_job_path)
                        allow_read = {}
                        allow_read['OK'] = True
                        allow_read['retry'] = 0
                        allow_p = check_path(measure_t)
                        allow_path = '/tfdata/k8snfs/%s/%s.json' % (job.name, measure_t)
                        save_config(allow_read, allow_path)
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
                            lock.release()
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
                            cpu_predict = float(ress_lists[-2])
                            cpu_base = math.ceil(1.12 * cpu_predict)
                            mem_predict = float(ress_lists[-1])
                            mem_base = math.ceil(1.35 * mem_predict)
                            res_to_server = '1'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                        else:
                            res_to_server = '0'
                            pre_client.send(bytes(res_to_server, 'utf-8'))
                            print("send response success!!")
                            time.sleep(6)
                            pre_client.close()
                            print("some time later to try again!!")
                            lock.release()
                            time.sleep(60)
                            continue
                        pre_client.close()
                        tmp_reload = tasks['reload']
                        if tmp_reload == 0:
                            # alpha = 1
                            # beta = 1
                            alpha = random.randint(0,7)*0.1+0.55
                            beta = random.randint(0,18)*0.1+0.875
                        else:
                            alpha = random.randint(2, 12) * 0.1 + 0.6
                            beta = random.randint(0, 10) * 0.1 + 1
                        # alpha = 1
                        # beta = 1
                        job.set_resource(cpu_source=(math.ceil(cpu_base * alpha)),
                                         mem_source=(math.ceil(mem_base * beta)))

                        mini_batch = predict_min_first(rfr=rfr,cpu_alpha=alpha,mem_alpha=beta,batch=batch_res,flops=flops_res,params=params_res)
                        mini_batch = float(mini_batch)
                        deadline = mini_batch*job.training_step*(random.randint(8,26)*0.1)+300
                        print(deadline)
                        print(type(deadline))
                        # deadline = random.randint(3600, 18000)
                        start_time = '%.3f' % time.time()
                        start_time = float(start_time)
                        job.set_deadline(deadline=deadline, start_time=start_time)
                        job_res_config = {'deadline': job.deadline, 'start_time': job.starttime,
                                          'cpu_source': job.cpu_allocate,
                                          'mem_source': job.memory_allocate, 'cpu_high': cpu_base,
                                          'memory_base': mem_base, 'batch_res': batch_res,
                                          'flops_res': flops_res, 'params_res': params_res, 'step_base': 0,
                                          'reloadtime': []}
                        save_config_dir = task_submit.check_path(job.name)
                        # save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job.name, job.name)
                        save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                        # save_config(job_config, save_job_path)
                        save_config(job_res_config, save_res_path)
                        if tasks['count'] < tasks['size'] and tasks['buffercount'] == 0:
                            node_index, cpu_nodes, memory_nodes, total_cpu_use, total_mem_use = job_basic.schedule_base()
                            cpu_value, mem_value, cpu_node_value, mem_node_value = get_load_value(node_index=node_index,
                                                                                                  cpu_base=cpu_nodes,
                                                                                                  memory_base=memory_nodes,
                                                                                                  total_cpu_base=total_cpu_use,
                                                                                                  total_memory_base=total_mem_use)
                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas

                            if cpu_value < 0.4:
                                job.worker_replicas = random.randint(4, 6)


                            elif cpu_value < 0.7:
                                job.worker_replicas = random.randint(3, 4)

                            else:
                                job.worker_replicas = random.randint(1, 2)

                            job.ps_replicas = random.randint(math.ceil(job.worker_replicas / 4),
                                                             math.ceil(job.worker_replicas / 2))

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
                                        if can_use_cpu - 750> 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 750
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
                                            if can_use_cpu - 750 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 750
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
                                        lock.release()
                                        continue
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

                                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                    # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                                    # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                                    # 'cpu_high':cpu_base,'batch_res':batch_res,
                                    # 'flops_res':flops_res,'params_res':params_res}
                                    res_config = load_config(save_res_path)
                                    batch_res = res_config['batch_res']
                                    flops_res = res_config['flops_res']
                                    params_res = res_config['params_res']

                                    pool.apply_async(catch_node_step_msg,
                                                     args=(
                                                     jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                                else:
                                    job.ps_replicas = 1
                                    job.worker_replicas = 1
                                    job.training_step = job.training_step * tmp_worker
                                    save_job_change_layout(job.name, 1, 1, job.training_step)
                                    # lock.acquire()
                                    tmp_next = tasks['next']
                                    tmp_next.append(job.name)
                                    tmp_next_time_config = tasks['nexttimes']
                                    tmp_next_time_config[job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config
                                    tasks['next'] = tmp_next
                                    # lock.release()
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
                                    lock.release()
                                    continue
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
                                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                                # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                                # 'cpu_high':cpu_base,'batch_res':batch_res,
                                # 'flops_res':flops_res,'params_res':params_res}
                                res_config = load_config(save_res_path)
                                batch_res = res_config['batch_res']
                                flops_res = res_config['flops_res']
                                params_res = res_config['params_res']

                                pool.apply_async(catch_node_step_msg,
                                                 args=(
                                                 jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))

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
                            tmp_ps_replicas = job.ps_replicas
                            tmp_worker_replicas = job.worker_replicas
                            if cpu_value < 0.4:
                                job.worker_replicas = random.randint(4, 6)
                            elif cpu_value < 0.7:
                                job.worker_replicas = random.randint(3, 4)
                            else:
                                job.worker_replicas = random.randint(1, 2)
                            job.ps_replicas = random.randint(math.ceil(job.worker_replicas / 4),
                                                             math.ceil(job.worker_replicas / 2))

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
                                        if can_use_cpu - 750 > 0 and not reach_ps:
                                            catch_ps_c += 1
                                            can_use_cpu = can_use_cpu - 750
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
                                            if can_use_cpu - 750 > 0 and not reach_ps:
                                                catch_ps_c += 1
                                                can_use_cpu = can_use_cpu - 750
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
                                        lock.release()
                                        continue
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
                                    save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                    # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                                    # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                                    # 'cpu_high':cpu_base,'batch_res':batch_res,
                                    # 'flops_res':flops_res,'params_res':params_res}
                                    res_config = load_config(save_res_path)
                                    batch_res = res_config['batch_res']
                                    flops_res = res_config['flops_res']
                                    params_res = res_config['params_res']
                                    pool.apply_async(catch_node_step_msg,
                                                     args=(
                                                     jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))
                                else:
                                    job.ps_replicas = 1
                                    job.worker_replicas = 1
                                    job.training_step = job.training_step = math.ceil(job.training_step * tmp_worker)
                                    save_job_change_layout(job.name, 1, 1, training_step=job.training_step)
                                    # tasks['next'] = job.name
                                    # lock.acquire()
                                    tmp_next = tasks['next']
                                    tmp_next.append(job.name)
                                    tmp_next_time_config = tasks['nexttimes']
                                    tmp_next_time_config[job.name] = 0
                                    tasks['nexttimes'] = tmp_next_time_config
                                    tasks['next'] = tmp_next
                                    # lock.release()
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
                                    lock.release()
                                    continue
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
                                save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job.name, job.name)
                                # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
                                # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,
                                # 'cpu_high':cpu_base,'batch_res':batch_res,
                                # 'flops_res':flops_res,'params_res':params_res}
                                res_config = load_config(save_res_path)
                                batch_res = res_config['batch_res']
                                flops_res = res_config['flops_res']
                                params_res = res_config['params_res']
                                pool.apply_async(catch_node_step_msg,
                                                 args=(
                                                 jobs, job.name, tasks, lock, batch_res, flops_res, params_res, 1))

                        tmp_reload = tasks['reload']
                        tmp_reload = 0
                        # tmp_reload = tmp_reload + 1
                        # if tmp_reload == 6:
                        #     tmp_reload = 0
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
                    break
            global_count += 1
        if global_count % 7 == 0:
            for iter0 in range(3):
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
                        for aim in aim_ns:
                            tmp_retry_ns.append(aim)
                            tmp_retry_solution[aim] = aim_assign_config[aim]
                            is_layout[aim] = False
                        tasks['retry'] = tmp_retry_ns
                        tasks['solution'] = tmp_retry_solution
                        tasks['nslayout'] = is_layout
                        lock.release()
                time20 = time.time()
                print("Modulation once cost %f" % float(time20 - time10))
                if (mode1==1 or mode1==4) and (iter0>=1):
                    break
                time.sleep(15)
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
    # aa = 0
    while True:
        if tasks['start']==True:
            time.sleep(120)
            lock.acquire()
            tmp_count1 = tasks['count']
            tmp_bucount = tasks['buffercount']
            tmp_nextcount = len(tasks['next'])
            tmp_time = time.time()
            tmp_throughput = tasks['through']
            tmp_throughput[tmp_time] = {'count': tmp_count1, 'buf': tmp_bucount, 'next': tmp_nextcount}
            tasks['through'] = tmp_throughput
            save_config(tasks,'system_info.json')
            lock.release()
            print('saved configs')
            time.sleep(120)
        else:
            break

def save_job_change_layout(job_name,ps_n,worker_n,training_step,mode=0):
    save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    job_config = load_config(save_job_path)
    # 'ps_replicas': job.ps_replicas,'worker_replicas': job.worker_replicas
    job_config['ps_replicas'] = ps_n
    job_config['worker_replicas'] = worker_n
    job_config['training_step'] = training_step
    keys = job_config.keys()
    if 'retry' not in job_config:
        job_config['retry'] = 0
    if mode != 0:
        job_config['retry'] = job_config['retry']+1

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