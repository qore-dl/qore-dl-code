import numpy as np
import yaml
import json
import kubernetes
import random
from task_submit import VGGTask,RESTask,RETask,DENTask,XCETask
import influxdb
# from random_job3 import load_config,save_config,reload_jobs
import time
import math

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

def reload_jobs(job_name,task_id):
    #full_flie_name = '/tfdata/tfcnn/expjob/%s.yaml' % job_name
    # save_job_path = '/tfdata/k8snfs/%s/%s.json' % (job_name, job_name)
    # save_res_path = '/tfdata/k8snfs/%s/%s_res.json' % (job_name, job_name)
    save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (job_name, job_name)
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (job_name, job_name)
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
    job_reload.cpu_allocate = job_res_config['cpu_source']
    job_reload.memory_allocate = job_res_config['mem_source']
    job_reload.deadline = job_res_config['deadline']
    job_reload.starttime = job_res_config['start_time']
    return job_reload

def value_free_load(item):
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (item, item)
    job_res_config = load_config(save_res_path)
    #job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
    # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,'cpu_high':cpu_base,
    #'batch_res':batch_res,'flops_res':flops_res,'params_res':params_res}
    now_time = time.time()
    last_for_time = now_time - job_res_config['start_time']
    rest_time = job_res_config['deadline'] - last_for_time
    cpu_need = job_res_config['cpu_source']
    mem_need = job_res_config['mem_source']
    save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (item, item)
    job_config = load_config(save_job_path)
    worker_replicas = job_config['worker_replicas']
    alpha = 0.9
    alpha2 = 0.85
    beta = 0.78
    theta = 0.75
    if rest_time > 0:
        rest_value = (-1)*(rest_time)
    else:
        rest_value = (-1)*(rest_time)
    item_job = reload_jobs(item,-1)
    source_value = (theta*cpu_need*worker_replicas/item_job.total_cpu)+((1-theta)*(mem_need)*worker_replicas/item_job.total_mem)
    combined_value = rest_value/source_value
    if random.random() < 0.1:
        combined_value = combined_value - 0.1*(theta*cpu_need*worker_replicas+(1-theta)*(mem_need)*worker_replicas)
    return combined_value

def value_weight_load(item):
    save_res_path = '/tfdata/k8snfs/setbase/%s/%s_res.json' % (item, item)
    job_res_config = load_config(save_res_path)
    # job_res_config = {'deadline':job.deadline,'start_time':job.starttime,
    # 'cpu_source':job.cpu_allocate,'mem_source':job.memory_allocate,'cpu_high':cpu_base,
    # 'batch_res':batch_res,'flops_res':flops_res,'params_res':params_res}
    now_time = time.time()
    last_for_time = now_time - job_res_config['start_time']
    rest_time = job_res_config['deadline'] - last_for_time
    cpu_need = job_res_config['cpu_source']
    mem_need = job_res_config['mem_source']
    save_job_path = '/tfdata/k8snfs/setbase/%s/%s.json' % (item, item)
    job_config = load_config(save_job_path)
    worker_replicas = job_config['worker_replicas']
    alpha = 0.9
    alpha2 = 0.85
    beta = 0.78
    theta = 0.75
    if rest_time > 0:
        rest_value = (-1) * (rest_time)
    else:
        rest_value = (-1) * (rest_time)
    item_job = reload_jobs(item, -1)
    source_value = (theta * cpu_need * worker_replicas / item_job.total_cpu) + (
                (1 - theta) * (mem_need) * worker_replicas / item_job.total_mem)
    combined_value = rest_value*source_value
    # combined_value = beta * rest_value + (1 - beta) * source_value
    return combined_value
