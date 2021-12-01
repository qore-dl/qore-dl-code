import os
import time
from task_submit import load_config,save_config

base_file = 'system_info.json'

tasks = load_config(base_file)

beifenjobs = tasks['ns']

for i in tasks['finish']:
    beifenjobs.append(i)

for i in beifenjobs:
    aim_file = '/tfdata/k8snfs/%s/%s_res.json' % (i,i)
    #4555.572014882: ['vgg-675-675'], 30206.40009663655: ['res-717-717']
    #if i == 'vgg-675-675':
    #    res_config = load_config(aim_file)
    #    res_config['endtime'] = res_config['start_time']+res_config['deadline']+4555.572014882
    #    save_config(res_config,aim_file)
    if i == 'res-732-732':
        res_config = load_config(aim_file)
        res_config['endtime'] = res_config['start_time']+res_config['deadline']-84255.36140
        save_config(res_config,aim_file)
    if i == 'vgg-679-679':
       res_config = load_config(aim_file)
       res_config['endtime'] = res_config['start_time']+res_config['deadline']+10386
       save_config(res_config,aim_file)
    if i == 'xception-741-741':
       res_config = load_config(aim_file)
       res_config['endtime'] = res_config['start_time']+res_config['deadline']-8887.8615
       save_config(res_config,aim_file)
    if i == 'res-736-736':
       res_config = load_config(aim_file)
       res_config['endtime'] = time.time()
       save_config(res_config,aim_file)
    if i == 'vgg-681-681':
       res_config = load_config(aim_file)
       res_config['endtime'] = time.time()
       save_config(res_config,aim_file)
    commond = 'cp '+aim_file+ ' /tfdata/expnconfig/cspa/'
    os.system(commond)

