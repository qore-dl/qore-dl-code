import influxdb
import json
from task_submit_fix import SubTask,VGGTask,RESTask,RETask,XCETask,DENTask
step_influx = influxdb.InfluxDBClient(host='192.168.128.10', port=8086, username='admin', password='admin',
                                              database="PREDICT")

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

def reload_jobs_aim(job_name,task_id):
    #full_flie_name = '/tfdata/tfcnn/expjob/%s.yaml' % job_name
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

import time

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

tasks = load_config("system_info.json")

kk = tasks['aim']
a = 0
for item in kk:
    rejob = reload_jobs_aim(item,-1)
    measure = rejob.measure
    pre_list = rejob.measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    measure_u = pre_list[0] + 'U' + pre_list[-1]
    measure_w = pre_list[0] + 'W' + pre_list[-1]
    try:
        step_influx.drop_measurement(measure_s)
        step_influx.drop_measurement(measure_t)
        step_influx.drop_measurement(measure_u)
        step_influx.drop_measurement(measure_w)
    except Exception as e:
        print(e)
    a += 1
    print(a)
    time.sleep(1.0)
