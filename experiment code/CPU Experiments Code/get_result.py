import numpy as np

import json

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

task = load_config("system_info.json")
import os
try:
    os.mkdir("results")
except Exception as e:
    print(e)
# /tfdata/k8snfs/vgg-953-953/worker0
for job in task['aim']:
    os.mkdir("results/%s/" % job)
    jobl = os.listdir("/tfdata/k8snfs/%s/" % job)
    print(jobl)
    for j in jobl:
        print('worker' in j)
        if 'worker' in j:
            print("cp /tfdata/k8snfs/%s/%s/resource_monitor.csv results/%s/%s.csv" % (job,j,job,j))
            os.system("cp /tfdata/k8snfs/%s/%s/resource_monitor.csv results/%s/%s.csv" % (job,j,job,j))
    os.system("cp /tfdata/k8snfs/%s/%s_res.json results/%s/" % (job,job,job))
    os.system("cp /tfdata/k8snfs/%s/%s_mod.json results/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/%s/%s.json results/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/%s/%s_pw.json results/%s/" % (job, job, job))
try:
    os.mkdir("fixres")
except Exception as e:
    print(e)

for job in task['aim']:
    os.mkdir("fixres/%s/" % job)
    jobl = os.listdir("/tfdata/k8snfs/setfix/%s/" % job)
    for j in jobl:
        if 'worker' in j:
            os.system("cp /tfdata/k8snfs/setfix/%s/%s/resource_monitor.csv fixres/%s/%s.csv" % (job, j, job, j))
    os.system("cp /tfdata/k8snfs/setfix/%s/%s_res.json fixres/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/setfix/%s/%s_mod.json fixres/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/setfix/%s/%s.json fixres/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/setfix/%s/%s_pw.json fixres/%s/" % (job, job, job))
try:
    os.mkdir("dycres")
except Exception as e:
    print(e)
for job in task['aim']:
    os.mkdir("dycres/%s/" % job)
    jobl = os.listdir("/tfdata/k8snfs/setdyc/%s/" % job)
    for j in jobl:
        print('worker' in j)
        if 'worker' in j:
            os.system("cp /tfdata/k8snfs/setdyc/%s/%s/resource_monitor.csv dycres/%s/%s.csv" % (job, j, job, j))
    os.system("cp /tfdata/k8snfs/setdyc/%s/%s_res.json dycres/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/setdyc/%s/%s_mod.json dycres/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/setdyc/%s/%s.json dycres/%s/" % (job, job, job))
    os.system("cp /tfdata/k8snfs/setdyc/%s/%s_pw.json dycres/%s/" % (job, job, job))