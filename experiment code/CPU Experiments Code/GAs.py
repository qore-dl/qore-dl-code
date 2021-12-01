from random_job3 import reload_jobs
import time
import influxdb
import numpy as np
from sklearn.externals import joblib
from random_job3 import load_config,save_config
import math

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
    mem_base = job_config['mem_base']
    cpu_alpha = cpu/ cpu_high
    mem_alpha = mem/ mem_base
    #     bfp = list(zip(list(res['batch']),list(res['flops']),list(res['params']),list(res['cpu_alpha']),list(res['mem_alpha'])))
    data = np.array([batch, flops, params, cpu_alpha, mem_alpha])
    data = np.mat(data)
    data = data.A
    iteration = rfr.predict(data)
    return iteration

def choice_jobs(tasks,rfr):
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
    # lock.acquire()
    tmp_ns = tasks['ns']
    tmp_layout = tasks['nslayout']
    # lock.release()
    piotential = []
    tmp_layout_key = tmp_layout.keys()
    for i in tmp_ns:
        if (i in tmp_layout_key) and tmp_layout[i]:
            piotential.append(i)
    aim1 = ''
    aim2 = ''
    mode = 0
    if piotential:
        aim = {}
        for i in piotential:
            reload_tmp = reload_jobs(i, -1)
            res_path = '/tfdata/k8snfs/%s/%s_res.json' % (i,i)
            res_config = load_config(res_path)
            pod_status = [j.status.phase for j in reload_tmp.v1.list_namespaced_pod(i).items]
            if 'Succeeded' in pod_status or 'Failed' in pod_status:
                continue
            tmp_re = reload_tmp.deadline - (time.time() - reload_tmp.starttime)
            tmp_iter = reload_tmp.get_remain(mode=1)
            reload_iter = reload_tmp.get_remain(mode=0)
            pre_list = reload_tmp.measure.split(" ")
            measure_s = pre_list[0] + 'S' + pre_list[-1]
            measure_t = pre_list[0] + 'T' + pre_list[-1]
            res = step_influx_client.query(
                "select * from " + measure_s + " group by nodes order by asc limit 5")
            keys = res.keys()
            node_list = [b['nodes'] for a, b in keys]
            dic_msg = {}
            time_avg = []
            for node in node_list:
                for k in range(len(keys)):
                    _, no = keys[k]
                    if no['nodes'] == node:
                        dic_msg[node] = list(res[keys[k]])
                        time_avg_list = [float(p['time_d']) for p in dic_msg[node]]
                        time_avg_node = np.mean(time_avg_list)
                        time_avg.append(time_avg_node)

            now_mini = max(time_avg)
            need_time = tmp_iter * now_mini
            res_config['need'] = need_time
            res_config['remain_time'] = tmp_re
            res_config['mini'] = now_mini
            res_config['remain_iter'] = tmp_iter
            res_config['reload_iter'] = reload_iter
            save_config(res_config,res_path)
            rescha = need_time - tmp_re
            aim_keys = list(aim.keys())
            if rescha not in aim_keys:
                aim[rescha] = []
            aim[rescha].append(i)
        aim_time = list(aim.keys())
        aim1 = ''
        aim2 = ''
        mode = 0
        if aim_time:
            list.sort(aim_time)
            if aim_time[-1]<=0:
                #都可以完成，考虑增大资源，提高资源利用率，其中要提升的也是离deadline最近的任务和对于资源最敏感的任务
                if len(aim_time)==1 and len(aim[aim_time[-1]])==1:
                    aim1 = aim[aim_time[-1]][0]
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[-1]][0]
                    aim_time_po = []
                    up_limit = min([3, len(aim_time)])
                    up_limit = 0 - up_limit
                    for i in range(up_limit, 0):
                        for j in aim[aim_time[i]]:
                            aim_time_po.append(j)
                    aim_mingan = {}
                    for j in aim_time_po:
                        reload_tmp = reload_jobs(j, -1)
                        res_path = '/tfdata/k8snfs/%s/%s_res.json' % (j, j)
                        res_config = load_config(res_path)
                        cpu_per = math.ceil((reload_tmp.cpu_allocate) / (reload_tmp.worker_replicas))
                        mem_per = math.ceil((reload_tmp.memory_allocate) / (reload_tmp.worker_replicas))
                        sco1 = (res_config['mini'] - predict_min(job_name=j, cpu=(reload_tmp.cpu_allocate + cpu_per),
                                                                 mem=(reload_tmp.memory_allocate + mem_per),rfr=rfr)) / (
                               (0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu)+(0.3*reload_tmp.memory_allocate/reload_tmp.total_mem))
                        sco2 = (res_config['mini']*(reload_tmp.get_remain(mode=1)-((reload_tmp.get_remain(mode=0)*reload_tmp.worker_replicas)/(reload_tmp.worker_replicas+1))))/(reload_tmp.get_remain(mode=1))
                        sco2 = sco2/((0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu)+(0.3*reload_tmp.memory_allocate/reload_tmp.total_mem))
                        sco = max([sco1,sco2])
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
            elif aim_time[0]<0:
                #有任务完不成，有任务可以完成，考虑减少资源和增大资源，减少离deadline最远且对资源最不敏感的任务，增大超时最严重的任务
                #返回任务
                #增加资源的任务为超时最严重的任务，没有疑问，减少资源的任务则为离deadline较远且对资源最不敏感的任务，即剥夺资源带来的影响最小：
                if len(aim_time)==1 and len(aim[aim_time[-1]])==1:
                    aim1 = aim[aim_time[-1]][0]
                    aim2 = ''
                else:
                    aim1 = aim[aim_time[-1]][0]
                    aim_time_po = []
                    up_limit = min([3, len(aim_time)])
                    # up_limit = 0 - up_limit
                    for i in range(0,up_limit):
                        if aim_time[i]>=0:
                            break
                        for j in aim[aim_time[i]]:
                            aim_time_po.append(j)
                    aim_mingan = {}
                    for j in aim_time_po:
                        reload_tmp = reload_jobs(j, -1)
                        res_path = '/tfdata/k8snfs/%s/%s_res.json' % (j, j)
                        res_config = load_config(res_path)
                        cpu_per = math.ceil((reload_tmp.cpu_allocate) / (reload_tmp.worker_replicas))
                        mem_per = math.ceil((reload_tmp.memory_allocate) / (reload_tmp.worker_replicas))
                        sco1 = (predict_min(job_name=j, cpu=(reload_tmp.cpu_allocate - cpu_per),mem=(reload_tmp.memory_allocate - mem_per),rfr=rfr)-res_config['mini']) / (
                                       (0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                           0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                        sco2 = (res_config['mini'] * ((
                                    (reload_tmp.get_remain(mode=0) * reload_tmp.worker_replicas) / (
                                        reload_tmp.worker_replicas - 1))-reload_tmp.get_remain(mode=1))) / (reload_tmp.get_remain(mode=1))
                        sco2 = sco2 / ((0.7 * reload_tmp.cpu_allocate / reload_tmp.total_cpu) + (
                                    0.3 * reload_tmp.memory_allocate / reload_tmp.total_mem))
                        sco = min([abs(sco1), abs(sco2)])
                        mingan_key = list(aim_mingan.keys())
                        # if sco not in mingan_key:
                        #     aim_mingan[sco] = []
                        aim_mingan[sco] = j
                    mingan_key = list(aim_mingan.keys())
                    list.sort(mingan_key)
                    if mingan_key[-1] < 0:
                        aim2 = ''
                    else:
                        aim2 = aim_mingan[mingan_key[0]]
                        if aim2 == aim1:
                            aim2 = ''
                mode = 2
            elif aim_time[0]>=0:
                if len(aim_time)==1 and len(aim[aim_time[-1]])==1:
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

    return aim1,aim2,mode








#工具性函数：