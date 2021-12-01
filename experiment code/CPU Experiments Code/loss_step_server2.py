import influxdb
import pandas as pd
import numpy as np
import kubernetes
import os
import math
import signal
import socket
import multiprocessing
import datetime as dt
from utils import Timer
import scipy.optimize as opt
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingRegressor
import time
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import optimizers
from keras.layers import LSTM,Dense,Activation,Dropout,Input,concatenate
from keras.models import Sequential,Model
from keras.callbacks import EarlyStopping, ModelCheckpoint,LearningRateScheduler,ReduceLROnPlateau
from keras.utils.vis_utils import plot_model
import matplotlib.pyplot as plt
import time
import json
import re
# from fps import vggfpmodel,resfpmodel,res2fpmodel,xcefpmodel,denfpmodel
from TimeoutException import Myhandler,TimeoutError

# def load_task(params_dict,template_id):
#     if template_id == 1:
#         try:
#             batch_size,flops,params = vggfpmodel.vggfp(**params_dict)
#         except:
#             print("报错")
#     elif template_id == 2:
#         try:
#             batch_size,flops,params = resfpmodel.resfp(**params_dict)
#         except Exception as e:
#             print(e)
#     elif template_id == 3:
#         try:
#             batch_size,flops,params = res2fpmodel.res2fp(**params_dict)
#         except Exception as e:
#             print(e)
#     else:
#         try:
#             batch_size,flops,params = xcefpmodel.xcefp(**params_dict)
#         except Exception as e:
#             print(e)
#
#     return batch_size,flops,params
def save_config(config,name):
    config_content = {}
    filename = "%s.json" % name
    for key,value in config.items():
        # if key != 'job' and key != 'ns':
        config_content[key] = value
        # task_content['task_id'] = tasks['task_id']
    fw = open(filename, 'w', encoding='utf-8')
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
    f.close()
    return config_content
def select_node(client,measure_s):
    res0 = client.query("select * from " + measure_s + " group by nodes order by desc limit 10")
    keys0 = res0.keys()
    node_list = [b['nodes'] for a, b in keys0]
    node_index = [int(p[6:]) for p in node_list]
    node_index.sort()
    selected_node = 'worker%d' % node_index[0]
    return selected_node
def load_data(min_steps,length,measure,db="PREDICT",host='192.168.128.10',first=True):
    # measure,db="PREDICT",host='192.168.128.10'
    aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
    aConfiguration = kubernetes.client.Configuration()
    aConfiguration.host = "https://192.168.128.10:6443"
    aConfiguration.verify_ssl = False
    aConfiguration.api_key = {"authorization": "Bearer " + aToken}
    aApiClient = kubernetes.client.ApiClient(aConfiguration)
    v1 = kubernetes.client.CoreV1Api(aApiClient)
    print("Start for db load data")
    client = influxdb.InfluxDBClient(host=host,port=8086,username='admin',password='admin',database=db)
    pre_list = measure.split(" ")
    measure_s = pre_list[0]+'S'+pre_list[-1]
    measure_t = pre_list[0]+'T'+pre_list[-1]
    measure_write = pre_list[0]+'W'+pre_list[-1]
    measure_up = pre_list[0] + 'U' + pre_list[-1]
    print(measure_s)
    catched_job = pre_list[0]
    catched_job = catched_job.lower()
    jieshu = False
    if catched_job == 'xce':
        aim_ns = 'xception-' + pre_list[-1] + '-' + pre_list[-1]
    else:
        aim_ns = catched_job + "-" + pre_list[-1] + "-" + pre_list[-1]
    if first:
        min_steps2 = min_steps
        yichang = False
        countt00 = 0
        while True:
            # selected_node = select_node(client,measure_s)
            res = client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
            print("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
            keys = res.keys()
            print(keys[:])
            while True:
                if keys:
                    break
                else:
                    time.sleep(10)
                res = client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
                keys = res.keys()
            print(keys[:])

            msg_inter = list(res[keys[0]])
            step_now = int(msg_inter[0]['step'])
            print(step_now)
            len_msg = len(msg_inter)
            interval_step = 0
            for i in range(len_msg):
                interval_step += msg_inter[i]['time_d']
            interval_step = (interval_step / len_msg)

            if step_now >= min_steps2:
                break
            else:
                ns_list = get_ns(v1)
                write_ss = client.query("select * from " + measure_write + " order by desc limit 1")
                key_write = write_ss.keys()
                print(key_write[:])
                write_inter = write_ss[key_write[0]]
                write_items = list(write_inter)
                print(write_items[:])
                write_now = int(write_items[0]['modulate'])
                if aim_ns not in ns_list and (write_now==0):
                    yichang = True
                    break
                pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
                print(pod_status)
                print("going on")
                print(measure)
                # print(math.ceil(step_to_train * 0.75))
                # print(step_now)
                write_ss = client.query("select * from " + measure_write + " order by desc limit 1")
                key_write = write_ss.keys()
                print(key_write[:])
                write_inter = write_ss[key_write[0]]
                write_items = list(write_inter)
                print(write_items[:])
                write_now = int(write_items[0]['modulate'])
                if ('Succeeded' in pod_status or 'Failed' in pod_status) and (write_now==0):
                    if countt00 <= 3:
                        countt00+=1
                    else:
                        print("Job is ended")
                        yichang = True
                        break
                div_num = min_steps2 - step_now + 1
                sleep_last = interval_step * div_num
                print(sleep_last)
                print(div_num)
                print(interval_step)
                result = client.query("select * from " + measure_t + " order by desc limit 1")
                key = result.keys()
                result_inter = result[key[0]]
                result_items = list(result_inter)
                trains_step = int(result_items[0]['training_step'])
                if step_now >= math.ceil(trains_step*0.85):
                    jieshu = True
                    break
                if step_now >= trains_step - 3:
                    print("This process is ended!!")
                    jieshu = True
                    break
                # allow path!!!
                # allow_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, measure_t)
                allow_path = '/tfdata/k8snfs/setfix/%s/%s.json' % (aim_ns, measure_t)
                retry_now = int(result_items[0]['retry'])
                allow_read = load_config(allow_path)
                print("Reload success!!")
                allow_read['retry'] = retry_now
                ps_now = int(result_items[0]['ps'])
                worker_now = int(result_items[0]['worker'])
                allow_read['worker'] = worker_now
                allow_read['ps'] = ps_now
                save_config2(allow_read, allow_path)
                print("save success!!")
                result2 = client.query("select * from " + measure_up + " order by desc limit 1")
                key2 = result2.keys()
                # print(key2)
                result_inter2 = result2[key2[0]]
                result_items2 = list(result_inter2)
                # print(result_items2)
                retry_top = int(result_items2[0]['retry'])
                if retry_top != retry_now:
                    new_ps = int(result_items2[0]['ps'])
                    new_worker = int(result_items2[0]['worker'])
                    trains_step = math.ceil(trains_step * worker_now / new_worker)
                    allow_read = load_config(allow_path)
                    allow_read['retry'] = retry_top
                    allow_read['ps'] = new_ps
                    allow_read['worker'] = new_worker
                    save_config2(allow_read, allow_path)
                    print("saved successful!!")
                    # print(trains_step)
                    step_items = [
                        {
                            'measurement': measure_t,
                            'tags': {
                                'task': int(pre_list[-1]),
                                'runtimes': int(pre_list[-1]),
                                'retry': int(retry_top)
                            },
                            'fields': {
                                'training_step': int(trains_step),
                                'ps': int(allow_read['ps']),
                                'worker': int(allow_read['worker'])
                            }
                        }
                    ]
                    print("saved in db")
                    client.write_points(step_items, time_precision="ms", database="PREDICT")
                    print("Writed in db")
                    min_steps2 = trains_step*0.2
                time.sleep(float(interval_step))
        if yichang:
            return [],0
        # selected_node = select_node(client,measure_s)
        result = client.query("select * from " + measure_s + " where nodes='worker0' order by desc")
    else:
        # selected_node = select_node(client,measure_s)
        result = client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit "+str(length))
        print("select * from " + measure_s + " where nodes='worker0' order by desc limit "+str(length))
    keys = result.keys()
    print(keys)
    msg_raw = list(result[keys[0]])
    print(msg_raw)
    print(first)
    print("Catched raw data")
    # msg = {}
    # tmp_step = []
    tmp_loss = {}
    for i in range(len(msg_raw)):
        # tmp_step.append(int(msg_raw[i]['step']))
        tmp = int(msg_raw[i]['step'])
        # tmp_loss.append(msg_raw[i]['loss'])
        if tmp in tmp_loss:
            tmp_loss[tmp].append(msg_raw[i]['loss'])
        else:
            tmp_loss[tmp] = [msg_raw[i]['loss']]
    steps = list(tmp_loss.keys())
    loss = []
    steps.sort()
    for i in steps:
        loss_per_step = np.mean(tmp_loss[i])
        loss.append(loss_per_step)

    step_high = steps[-1]
    step_low = steps[0]

    if first:
        config = {}
        loss_max = max(loss)
        config['high'] = step_high
        config['low'] = step_low
        config['loss_max'] = loss_max
        save_config(config,measure_s)
    else:
        filename = '%s.json' % measure_s
        config = load_config(filename)
        config['high'] = step_high
        config['low'] = step_low
        save_config(config,measure_s)
    print("saved config")
    max_loss = config['loss_max']
    print(loss)
    if jieshu:
        return loss, max_loss, 1
    else:
        return loss, max_loss, 0




    # tmp_step.reverse()
    # tmp_loss.reverse()
    # msg['step'] = tmp_step
    # msg['loss'] = tmp_loss
    # step_set = set(tmp_step)

def predict_nnls(data_in,step_x):
    w,theta = opt.nnls(data_in,step_x)
    return w

def predict_step_nnls(data_in,step_x,measure,top_step,low_step,threshold=0.01):
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    filename = '%s.json' % measure_s
    config = load_config(filename)
    step_now = config['high']+1
    w = predict_nnls(data_in,step_x)
    step_to_train = step_now
    tiaochu = False
    while step_now <= top_step+1:
        fed_in = [1/step_now,1]
        predict_result = float(np.array(fed_in).dot(w))
        if predict_result < threshold:
            step_to_train = predict_result
            tiaochu = True
            break
        step_now+=1

    if tiaochu:
        if step_now<=low_step+1:
            step_to_train = low_step+2
        return step_to_train
    else:
        step_to_train = top_step
        return step_to_train





def load_data_nnls(min_steps,length,measure,db="PREDICT",host='192.168.128.10',first=True):
    aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
    aConfiguration = kubernetes.client.Configuration()
    aConfiguration.host = "https://192.168.128.10:6443"
    aConfiguration.verify_ssl = False
    aConfiguration.api_key = {"authorization": "Bearer " + aToken}
    aApiClient = kubernetes.client.ApiClient(aConfiguration)
    v1 = kubernetes.client.CoreV1Api(aApiClient)
    print("Start for db load data")
    client = influxdb.InfluxDBClient(host=host, port=8086, username='admin', password='admin', database=db)
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    measure_write = pre_list[0] + 'W' + pre_list[-1]
    measure_up = pre_list[0] + 'U' + pre_list[-1]
    print(measure_s)
    catched_job = pre_list[0]
    catched_job = catched_job.lower()
    jieshu = False
    if catched_job == 'xce':
        aim_ns = 'xception-' + pre_list[-1] + '-' + pre_list[-1]
    else:
        aim_ns = catched_job + "-" + pre_list[-1] + "-" + pre_list[-1]
    if first:
        min_steps2 = min_steps
        yichang = False
        countt00 = 0
        while True:
            # selected_node = select_node(client, measure_s)
            res = client.query(
                "select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
            print("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
            keys = res.keys()
            print(keys[:])
            while True:
                if keys:
                    break
                else:
                    time.sleep(10)
                res = client.query(
                    "select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
                keys = res.keys()
            print(keys[:])

            msg_inter = list(res[keys[0]])
            step_now = int(msg_inter[0]['step'])
            print(step_now)
            len_msg = len(msg_inter)
            interval_step = 0
            for i in range(len_msg):
                interval_step += msg_inter[i]['time_d']
            interval_step = (interval_step / len_msg)

            if step_now >= min_steps2:
                break
            else:
                ns_list = get_ns(v1)
                write_ss = client.query("select * from " + measure_write + " order by desc limit 1")
                key_write = write_ss.keys()
                print(key_write[:])
                write_inter = write_ss[key_write[0]]
                write_items = list(write_inter)
                print(write_items[:])
                write_now = int(write_items[0]['modulate'])
                if aim_ns not in ns_list and (write_now == 0):
                    yichang = True
                    break
                pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
                print(pod_status)
                print("going on")
                print(measure)
                # print(math.ceil(step_to_train * 0.75))
                # print(step_now)
                write_ss = client.query("select * from " + measure_write + " order by desc limit 1")
                key_write = write_ss.keys()
                print(key_write[:])
                write_inter = write_ss[key_write[0]]
                write_items = list(write_inter)
                print(write_items[:])
                write_now = int(write_items[0]['modulate'])
                if ('Succeeded' in pod_status or 'Failed' in pod_status) and (write_now == 0):
                    if countt00 <= 3:
                        countt00+=1
                    else:
                        print("Job is ended")
                        yichang = True
                        break
                div_num = min_steps2 - step_now + 1
                sleep_last = interval_step * div_num
                print(sleep_last)
                print(div_num)
                print(interval_step)
                result = client.query("select * from " + measure_t + " order by desc limit 1")
                key = result.keys()
                result_inter = result[key[0]]
                result_items = list(result_inter)
                trains_step = int(result_items[0]['training_step'])
                if step_now >= math.ceil(trains_step * 0.85):
                    jieshu = True
                    break
                if step_now >= trains_step - 3:
                    print("This process is ended!!")
                    jieshu = True
                    break
                # allow path!!!
                # allow_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, measure_t)
                allow_path = '/tfdata/k8snfs/setfix/%s/%s.json' % (aim_ns, measure_t)
                # allow_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, measure_t)
                retry_now = int(result_items[0]['retry'])
                allow_read = load_config(allow_path)
                print("Reload success!!")
                allow_read['retry'] = retry_now
                ps_now = int(result_items[0]['ps'])
                worker_now = int(result_items[0]['worker'])
                allow_read['worker'] = worker_now
                allow_read['ps'] = ps_now
                save_config2(allow_read, allow_path)
                print("save success!!")
                result2 = client.query("select * from " + measure_up + " order by desc limit 1")
                key2 = result2.keys()
                # print(key2)
                result_inter2 = result2[key2[0]]
                result_items2 = list(result_inter2)
                # print(result_items2)
                retry_top = int(result_items2[0]['retry'])
                if retry_top != retry_now:
                    new_ps = int(result_items2[0]['ps'])
                    new_worker = int(result_items2[0]['worker'])
                    trains_step = math.ceil(trains_step * worker_now / new_worker)
                    allow_read = load_config(allow_path)
                    allow_read['retry'] = retry_top
                    allow_read['ps'] = new_ps
                    allow_read['worker'] = new_worker
                    save_config2(allow_read, allow_path)
                    print("saved successful!!")
                    # print(trains_step)
                    step_items = [
                        {
                            'measurement': measure_t,
                            'tags': {
                                'task': int(pre_list[-1]),
                                'runtimes': int(pre_list[-1]),
                                'retry': int(retry_top)
                            },
                            'fields': {
                                'training_step': int(trains_step),
                                'ps': int(allow_read['ps']),
                                'worker': int(allow_read['worker'])
                            }
                        }
                    ]
                    print("saved in db")
                    client.write_points(step_items, time_precision="ms", database="PREDICT")
                    print("Writed in db")
                    min_steps2 = trains_step * 0.2
                time.sleep(float(interval_step))
        if yichang:
            return [], 0
        # selected_node = select_node(client, measure_s)
        result = client.query("select * from " + measure_s + " where nodes='worker0' order by desc")
    else:
        # selected_node = select_node(client, measure_s)
        result = client.query("select * from " + measure_s + " where nodes='worker0' order by desc")
        print("select * from " + measure_s + " where nodes='worker0' order by desc")
    keys = result.keys()
    print(keys)
    msg_raw = list(result[keys[0]])
    print(msg_raw)
    print(first)
    print("Catched raw data")
    tmp_loss = {}
    for i in range(len(msg_raw)):
        # tmp_step.append(int(msg_raw[i]['step']))
        tmp = int(msg_raw[i]['step'])
        # tmp_loss.append(msg_raw[i]['loss'])
        if tmp in tmp_loss:
            tmp_loss[tmp].append(msg_raw[i]['loss'])
        else:
            tmp_loss[tmp] = [msg_raw[i]['loss']]
    steps = list(tmp_loss.keys())
    loss = []
    steps.sort()
    for i in steps:
        loss_per_step = np.mean(tmp_loss[i])
        loss.append(loss_per_step)

    step_high = steps[-1]
    step_low = steps[0]

    if first:
        config = {}
        loss_max = max(loss)

        config['high'] = step_high
        config['low'] = step_low
        config['loss_max'] = loss_max
        save_config(config, measure_s)
    else:
        filename = '%s.json' % measure_s
        config = load_config(filename)
        config['high'] = step_high
        config['low'] = step_low
        save_config(config, measure_s)
    print("saved config")
    max_loss = config['loss_max']
    # print(loss)

    if jieshu:
        return loss,max_loss,1
    else:
        return loss,max_loss,0

def normalization(loss,max_loss):
    loss_array = []
    for i in loss:
        tmp = i / max_loss
        loss_array.append(tmp)
    loss_array = np.asarray(loss_array)

    return loss_array

def make_dataset_nnls(data,max_loss):
    step_len = len(data)
    step_arrange = list(np.arange(step_len)+1)
    step_arrange.reverse()
    step_x = np.array([1/i for i in step_arrange])
    data = data.reverse()
    data_in = np.array([[i/max_loss,1] for i in data])
    return data_in,step_x

def make_dataset(data,max_loss,time_step,predict_step,intra):
    loss_array = normalization(data,max_loss)
    train = []
    total_length = len(loss_array)
    for i in range(0,total_length - time_step - predict_step,intra):
        train_slice = loss_array[i:i+time_step+predict_step]
        train.append(train_slice)

    train = np.array(train).astype(float)
    train_x = train[:,0:time_step]
    train_y = train[:,time_step:]
    train_twice_x = []
    train_twice_y = []
    gap = time_step // intra
    slice_length = len(train)
    for i in range(gap,slice_length):
        tmp_slice_twice = []
        tmp_slice_twice.append(train_x[i-gap])
        tmp_slice_twice.append(train_x[i])
        train_twice_x.append(tmp_slice_twice)
        train_twice_y.append(train_y[i])

    train_twice_x = np.array(train_twice_x).astype(float)
    train_twice_y = np.array(train_twice_y).astype(float)

    return train_x,train_y,train_twice_x,train_twice_y

def build_lstm_model(time_step,predict_step,input_dim):
    model = Sequential()
    model.add(LSTM(units=16,input_shape=(time_step,input_dim),return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=64,return_sequences=True))
    model.add(LSTM(units=128,return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=predict_step))
    model.add(Activation('linear'))
    model.summary()
    optimizer = optimizers.Adam()
    model.compile(loss="mse",optimizer=optimizer)

    return model


def build_twice_lstm_model(time_step,predict_step,input_dim):
    input_1 = Input(shape=(time_step,input_dim),dtype='float32',name='First_Time_Step')
    input_2 = Input(shape=(time_step,input_dim),dtype='float32',name='Pre_First_Time_Step')
    lstm1 = LSTM(units=16,input_shape=(time_step,input_dim),return_sequences=True)(input_1)
    lstm1 = Dropout(0.2)(lstm1)
    lstm2 = LSTM(units=16,input_shape=(time_step,input_dim),return_sequences=True)(input_2)
    lstm2 = Dropout(0.2)(lstm2)
    lstm = concatenate([lstm2,lstm1],axis=1)
    x1 = LSTM(units=64,return_sequences=True)(lstm)
    x1 = LSTM(units=128,return_sequences=False)(x1)
    x1 = Dense(units=predict_step)(x1)
    output = Activation('linear')(x1)
    model = Model(input=[input_1,input_2],output=output)
    model.summary()
    optimizer = optimizers.Adam()
    model.compile(loss='mse',optimizer=optimizer)

    return model



#加载模型
def load_model(filepath):
    print('[Model] Loading model from file %s' % filepath)
    model = keras.models.load_model(filepath)
    return model

def reshape_for_lstm(data):
    train = np.reshape(data,[data.shape[0],data.shape[1],1])
    return train

def divide_train_test(data,split):
    isplit = math.ceil(data.shape[0]*split)
    train_data = data[:isplit]
    test_data = data[isplit:]

    return train_data,test_data

def train(x, y, epochs, batch_size, save_dir, model,measure):
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    timer = Timer()
    timer.start()
    print('[Model] Training Started')
    print('[Model] %s epochs, %s batch size' % (epochs, batch_size))

    def scheduler(epoch):
        # 每隔100个epoch，学习率减小为原来的1/10
        if epoch % 100 == 0 and epoch != 0:
            lr = keras.backend.get_value(model.optimizer.lr)
            keras.backend.set_value(model.optimizer.lr, lr * 0.1)
            print("lr changed to {}".format(lr * 0.1))
        return keras.backend.get_value(model.optimizer.lr)

    #'%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs))
    save_fname = os.path.join(save_dir, '%s.h5' % measure_s)
    reduce_lr = LearningRateScheduler(scheduler)
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10),
        ModelCheckpoint(filepath=save_fname, monitor='val_loss', save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=10, verbose=0, mode='auto',
                          epsilon=0.001, cooldown=0, min_lr=0)
    ]
    # 当评价指标不在提升时，减少学习率
    #
    # 当学习停滞时，减少2倍或10倍的学习率常常能获得较好的效果。该回调函数检测指标的情况，如果在patience个epoch中看不到模型性能提升，则减少学习率
    # 参数
    #
    #     monitor：被监测的量
    #     factor：每次减少学习率的因子，学习率将以lr = lr*factor的形式被减少
    #     patience：当patience个epoch过去而模型性能不提升时，学习率减少的动作会被触发
    #     mode：‘auto’，‘min’，‘max’之一，在min模式下，如果检测值触发学习率减少。在max模式下，当检测值不再上升则触发学习率减少。
    #     epsilon：阈值，用来确定是否进入检测值的“平原区”
    #     cooldown：学习率减少后，会经过cooldown个epoch才重新进行正常操作
    #     min_lr：学习率的下限
    # ————————————————
    history = model.fit(
        x,
        y,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        validation_split=0.1
    )

    model.save(save_fname)

    print('[Model] Training Completed. Model saved as %s' % save_fname)
    timer.stop()
    return history, model

def train_twice(x1,x2, y, epochs, batch_size, save_dir, model,measure):
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    timer = Timer()
    timer.start()
    print('[Model] Training Started')
    print('[Model] %s epochs, %s batch size' % (epochs, batch_size))

    def scheduler(epoch):
        # 每隔100个epoch，学习率减小为原来的1/10
        if epoch % 100 == 0 and epoch != 0:
            lr = keras.backend.get_value(model.optimizer.lr)
            keras.backend.set_value(model.optimizer.lr, lr * 0.1)
            print("lr changed to {}".format(lr * 0.1))
        return keras.backend.get_value(model.optimizer.lr)

    save_fname = os.path.join(save_dir, '%s.h5' % measure_s)
    reduce_lr = LearningRateScheduler(scheduler)
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10),
        ModelCheckpoint(filepath=save_fname, monitor='val_loss', save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=10, verbose=0, mode='auto',
                          epsilon=0.001, cooldown=0, min_lr=0)
    ]
    # 当评价指标不在提升时，减少学习率
    #
    # 当学习停滞时，减少2倍或10倍的学习率常常能获得较好的效果。该回调函数检测指标的情况，如果在patience个epoch中看不到模型性能提升，则减少学习率
    # 参数
    #
    #     monitor：被监测的量
    #     factor：每次减少学习率的因子，学习率将以lr = lr*factor的形式被减少
    #     patience：当patience个epoch过去而模型性能不提升时，学习率减少的动作会被触发
    #     mode：‘auto’，‘min’，‘max’之一，在min模式下，如果检测值触发学习率减少。在max模式下，当检测值不再上升则触发学习率减少。
    #     epsilon：阈值，用来确定是否进入检测值的“平原区”
    #     cooldown：学习率减少后，会经过cooldown个epoch才重新进行正常操作
    #     min_lr：学习率的下限
    # ————————————————
    history = model.fit(
        {'First_Time_Step': x1,'Pre_First_Time_Step':x2},
        y,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        validation_split=0.1
    )

    model.save(save_fname)

    print('[Model] Training Completed. Model saved as %s' % save_fname)
    timer.stop()
    return history,model

def predict_once(data,model,input_dim,time_step,predict_step):
    data = np.reshape(data,(1,time_step,input_dim))
    predict_y = model.predict(data)
    predict_y = np.array(predict_y).astype(float)
    predict_y = np.reshape(predict_y,(predict_step,1))
    return predict_y

def predict_once_t(data1,data2,model,input_dim,time_step,predict_step):
    data1 = np.reshape(data1,(1,time_step,input_dim))
    data2 = np.reshape(data2,(1,time_step,input_dim))
    predict_y = model.predict([data1,data2])
    predict_y = np.array(predict_y).astype(float)
    predict_y = np.reshape(predict_y,(predict_step,1))
    return predict_y

def predict_multi(data,model,input_dim,time_step,predict_step,intra):
    iter = predict_step // intra
    predict = []
    for i in range(0,data.shape[0],iter):
        pone = predict_once(data[i],model,input_dim,time_step,predict_step)
        pone = np.array(pone).astype(float)
        pone = np.reshape(pone,(predict_step,))
        for p in pone:
            predict.append(p)
    predict = np.array(predict).astype(float)
    predict = np.reshape(predict,(len(predict),1))
    return predict

def predict_multi_t(data1,data2,model,input_dim,time_step,predict_step,intra):
    iter = predict_step // intra
    predict = []
    for i in range(0,data1.shape[0],iter):
        pone = predict_once_t(data1[i],data2[i],model,input_dim,time_step,predict_step)
        pone = np.array(pone).astype(float)
        pone = np.reshape(pone,(predict_step,))
        for p in pone:
            predict.append(p)
    predict = np.array(predict).astype(float)
    predict = np.reshape(predict,(len(predict),1))
    return predict

def derivation(x1,x2):
    xx = (x1 - x2)**2
    result = float((math.sqrt((xx))) / x1)
    return result

def step_predict(data,model,input_dim,predict_step,time_step,div,top_step,low_step,measure):
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    filename = '%s.json' % measure_s
    config = load_config(filename)
    # config['high'] = step_high
    # config['low'] = step_low
    # save_config(config, measure)
    #
    #
    # max_loss = config['loss_max']
    step_high = config['high']
    max_loss_read = config['loss_max']
    data_array = np.array(data).astype(float)
    data_array = data_array / max_loss_read
    data_use = list(data_array)


    fit_step = 0 - time_step - predict_step
    data_fit = data_use[fit_step:]
    data_list = list(data_fit[:])
    data_fit = np.array(data_fit[-time_step:]).astype(float)
    data_fit = np.reshape(data_fit,(1,time_step,input_dim))
    # data = np.reshape(data, (1, time_step, input_dim))
    predict_res = predict_once(data_fit,model,input_dim,time_step,predict_step)

    predict_res = np.squeeze(predict_res)
    step_to_train = predict_step
    tmp_base = 0 - 3*predict_step
    for i in range(predict_step):
        data_list.append(predict_res[i])
    while True:
        print(step_to_train)
        if step_to_train + step_high >= top_step:
            break
        data_div_pre = data_list[tmp_base:]
        print(data_div_pre)
        data_div_base = []
        for i in range(1,3*predict_step):
            tmp_div = derivation(data_div_pre[i-1],data_div_pre[i])
            data_div_base.append(tmp_div)
        der_base = np.mean(data_div_base)
        print(der_base)
        if der_base < div:
            break
        data_fit = data_list[fit_step:]
        data_list = list(data_fit[:])
        data_fit = np.array(data_fit[-time_step:]).astype(float)
        data_fit = np.reshape(data_fit, (1, time_step, input_dim))
        # data = np.reshape(data, (1, time_step, input_dim))
        predict_res = predict_once(data_fit, model, input_dim, time_step, predict_step)

        predict_res = np.squeeze(predict_res)
        step_to_train += predict_step
        for i in range(predict_step):
            data_list.append(predict_res[i])

    step_to_train = step_to_train+step_high
    if step_to_train <= low_step:
        step_to_train = low_step
    return step_to_train

# def step_predict_nnls(data,step_in):


def step_predict_twice(data,model,input_dim,predict_step,time_step,div,top_step,low_step,measure):
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    filename = '%s.json' % measure_s
    config = load_config(filename)
    # config['high'] = step_high
    # config['low'] = step_low
    # save_config(config, measure)
    #
    #
    # max_loss = config['loss_max']

    step_high = config['high']
    max_loss_read = config['loss_max']
    data_array = np.array(data).astype(float)
    data_array = data_array / max_loss_read
    data_use = list(data_array)
    fit_step = 0 - time_step - 2*predict_step
    data_fit = data_use[fit_step:]
    data_list = list(data_fit[:])
    data_fit_1 = np.array(data_fit[-time_step:]).astype(float)
    data_fit_2 = np.array(data_fit[-1*2*time_step:-time_step]).astype(float)
    data_fit_1 = np.reshape(data_fit_1,(1,time_step,input_dim))
    data_fit_2 = np.reshape(data_fit_2,(1,time_step,input_dim))
    # data = np.reshape(data, (1, time_step, input_dim))
    predict_res = predict_once_t(data_fit_1,data_fit_2,model,input_dim,time_step,predict_step)

    predict_res = np.squeeze(predict_res)
    step_to_train = predict_step
    tmp_base = 0 - 3*predict_step
    for i in range(predict_step):
        data_list.append(predict_res[i])
    while True:
        print(step_to_train)
        if step_to_train + step_high >= top_step:
            break
        data_div_pre = data_list[tmp_base:]
        print(data_div_pre)
        data_div_base = []
        for i in range(1,3*predict_step):
            tmp_div = derivation(data_div_pre[i-1],data_div_pre[i])
            data_div_base.append(tmp_div)
        der_base = np.mean(data_div_base)
        print(der_base)
        if der_base < div:
            break
        data_fit = data_list[fit_step:]
        data_list = list(data_fit[:])
        data_fit_1 = np.array(data_fit[-time_step:]).astype(float)
        data_fit_2 = np.array(data_fit[-1 * 2 * time_step:-time_step]).astype(float)
        data_fit_1 = np.reshape(data_fit_1, (1, time_step, input_dim))
        data_fit_2 = np.reshape(data_fit_2, (1, time_step, input_dim))
        # data = np.reshape(data, (1, time_step, input_dim))
        predict_res = predict_once_t(data_fit_1, data_fit_2, model, input_dim, time_step, predict_step)

        predict_res = np.squeeze(predict_res)
        step_to_train += predict_step
        for i in range(predict_step):
            data_list.append(predict_res[i])

    step_to_train = step_to_train+step_high
    if step_to_train <= low_step:
        step_to_train = low_step
    return step_to_train

def get_ns(v1):
    ns_list = []
    for i in v1.list_namespace().items:
        ns_list.append(i.metadata.name)
    return ns_list

def save_config2(config,filename):
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

def check_path(name):
    #check_path!!!
    # train_dir = os.path.join('/tfdata/k8snfs/', name)
    train_dir = os.path.join('/tfdata/k8snfs/setfix/', name)
    created = False
    print(train_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
        created = True
    return train_dir,created

def step_resource_predict_handle(conn,dictionary,lock,pool_size,connect_try=5,predict_fre=150):
    #measure,db="PREDICT",host='192.168.128.10'
    aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
    aConfiguration = kubernetes.client.Configuration()
    aConfiguration.host = "https://192.168.128.10:6443"
    aConfiguration.verify_ssl = False
    aConfiguration.api_key = {"authorization": "Bearer " + aToken}
    aApiClient = kubernetes.client.ApiClient(aConfiguration)
    v1 = kubernetes.client.CoreV1Api(aApiClient)
    try:
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp + 1
        dictionary['running_number'] = tmp
        lock.release()
    except Exception as e:
        print(e)
        lock.release()
    print("now running number is: %d" % tmp)

    influx_client = influxdb.InfluxDBClient(host='192.168.128.10',port=8086,username='admin',password='admin',database="PREDICT")
    try_times = 1
    legal_pattern = '\w+ \d+'
    msg_from_client = conn.recv(4096)
    matched = None
    while True:
        if try_times > connect_try:
            break
        msg_from_client_str = str(msg_from_client.decode('utf-8'))
        print(msg_from_client_str+" "+"try_time: "+str(try_times))
        # try_times = try_times + 1
        matched  = re.match(legal_pattern,msg_from_client_str)
        if matched is not None:
            break
        if not msg_from_client:
            break
        response = "403 "+"Message-error!"

        conn.send(bytes(response, 'utf-8'))

        msg_from_client = conn.recv(4096)
        try_times = try_times + 1

        # msg_from_client_str = str(msg_from_client.decode('utf-8'))

    if matched is None:
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        return
    print("connect success!")
    measure = matched.group()
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    measure_up = pre_list[0] + 'U' + pre_list[-1]
    measure_write = pre_list[0]+'W'+pre_list[-1]
    lock.acquire()
    # lock.release()
    tmp_running = dictionary['running_number']
    lock.release()
    res_pool = pool_size - tmp_running
    print("resuming pool size: %d" % res_pool)

    response = "400 "+pre_list[0]+" "+pre_list[-1]+" "+str(res_pool)
    conn.send(bytes(response,'utf-8'))
    catched_job = pre_list[0]
    catched_job = catched_job.lower()
    if catched_job == 'xce':
        aim_ns = 'xception-' + pre_list[-1] + '-' + pre_list[-1]
    else:
        aim_ns = catched_job + "-" + pre_list[-1] + "-" + pre_list[-1]
    print("this is work for %s" % (aim_ns))
    try:
        # job_con_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, aim_ns)
        job_con_path = "/tfdata/k8snfs/setfix/%s/%s.json" % (aim_ns, aim_ns)
        job_config = load_config(job_con_path)
        print("load job config success!!")
        # allow path!!!
        allow_path = '/tfdata/k8snfs/setfix/%s/%s.json' % (aim_ns, measure_t)
        # allow_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, measure_t)
    except Exception as e:
        print(e)
    # allow_path2 = "/tfdata/k8snfs/%s/%s_r.json" % (measure_t,measure_t)
    allow_p, created = check_path(aim_ns)
    print(allow_p)
    if created:
        allow_read = {}
        # allow_readr = {}
        allow_read['OK'] = True
        allow_read['retry'] = job_config['retry']
        save_config2(allow_read,allow_path)
        # save_config2(allow_readr,allow_path2)
    if not os.path.exists(allow_path):
        allow_read = {}
        # allow_readr = {}
        allow_read['OK'] = True
        allow_read['retry'] = job_config['retry']
        save_config2(allow_read, allow_path)

    ns_list = get_ns(v1)
    print(ns_list)
    print(aim_ns)
    print(aim_ns in ns_list)
    ceshi_count = 0
    ceshi_in = False
    while True:
        if ceshi_count > 210:
            break
        ns_list = get_ns(v1)
        write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
        key_write = write_ss.keys()
        print(key_write[:])
        write_inter = write_ss[key_write[0]]
        write_items = list(write_inter)
        print(write_items[:])
        write_now = int(write_items[0]['modulate'])
        if aim_ns not in ns_list and (write_now==0):
            ceshi_count+=1
            time.sleep(2.5)
        else:
            ceshi_in = True
            break
    if not ceshi_in:
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        print("namespace created error!")
        return
    result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
    key = result.keys()
    print(key)
    result_inter = result[key[0]]
    result_items = list(result_inter)
    print(result_items)
    trains_step = int(result_items[0]['training_step'])
    tmp_item = dict(result_items[0])
    key_tmp = list(tmp_item.keys())
    if 'retry' not in key_tmp:
        retry_now = int(job_config['retry'])
    else:
        retry_now = int(result_items[0]['retry'])

    allow_read = load_config(allow_path)
    print("Reload success!!")
    allow_read['retry'] = retry_now
    # 'ps_replicas': job.ps_replicas,
    # 'worker_replicas': job.worker_replicas
    if 'ps' not in key_tmp:
        ps_now = int(job_config['ps_replicas'])
    else:
        ps_now = int(result_items[0]['ps'])
    if 'worker' not in key_tmp:
        worker_now = int(job_config['worker_replicas'])
    else:
        worker_now = int(result_items[0]['worker'])
    allow_read['worker'] = worker_now
    allow_read['ps'] = ps_now
    save_config2(allow_read,allow_path)
    print("save success!!")

    result2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
    key2 = result2.keys()
    print(key2)
    result_inter2 = result2[key2[0]]
    result_items2 = list(result_inter2)
    print(result_items2)
    retry_top = int(result_items2[0]['retry'])
    print(retry_top)
    print(type(retry_top))
    print(retry_now)
    print(type(retry_now))
    if retry_top != retry_now:
        new_ps = int(result_items2[0]['ps'])
        new_worker = int(result_items2[0]['worker'])
        trains_step = math.ceil(trains_step*worker_now/new_worker)
        allow_read = load_config(allow_path)
        allow_read['retry'] = retry_top
        allow_read['ps'] = new_ps
        allow_read['worker'] = new_worker
        save_config2(allow_read,allow_path)
        print("saved successful!!")
    print(trains_step)
    modekk = 0
    if trains_step <= 200:
        step_items = [
            {
                'measurement': measure_t,
                'tags': {
                    'task': int(pre_list[-1]),
                    'runtimes': int(pre_list[-1]),
                    'retry': int(retry_top)
                },
                'fields': {
                    'training_step': int(trains_step),
                    'ps': int(allow_read['ps']),
                    'worker': int(allow_read['worker'])
                }
            }
        ]
        print("saved in db")
        print(trains_step)
        influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
        print("Writed in db")
        # conn.close()
        # lock.acquire()
        # # lock.release()
        # tmp = dictionary['running_number']
        # tmp = tmp - 1
        # dictionary['running_number'] = tmp
        # lock.release()
        print("Do not need to predict,return")
        modekk = 1
    min_steps = math.ceil(trains_step*0.2)
    length = math.ceil(min_steps*0.6)
    print("Initial Config Success!"+"min_steps:"+str(min_steps))
    time_start = time.time()
    print("start to load data")
    loss,max_loss,modekk_z = load_data(min_steps=min_steps,length=length,measure=measure,first=True)
    if not loss:
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        return
    # loss_array = normalization(loss,max_loss)
    result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
    key = result.keys()
    result_inter = result[key[0]]
    result_items = list(result_inter)
    trains_step = int(result_items[0]['training_step'])
    step_to_train = trains_step
    if trains_step<=200:
        modekk_z = 1
    if modekk_z!=1:
        print("Get data first time")
        data_x, data_y, data_twice_x, data_twice_y = make_dataset(loss[:], max_loss, 20, 10, 1)
        data_x_lstm = reshape_for_lstm(data_x[:])
        # data_y_lstm = reshape_for_lstm(data_y[:])
        # data_twice_x_1 = data_twice_x[:,1,:]
        # data_twice_x_2 = data_twice_x[:,0,:]
        # # data_twice_y = reshape_for_lstm(data_twice_y[:])
        # data_twice_x_1_lstm = reshape_for_lstm(data_twice_x_1[:])
        # data_twice_x_2_lstm = reshape_for_lstm(data_twice_x_2[:])
        print("Make dataset first time")
        # model = load_model('save_model/31122019-031018-e10.h5')
        if os.path.exists("save_model/%s.h5" % measure_s):
            model = load_model('save_model/%s.h5' % measure_s)
        else:
            model = build_lstm_model(time_step=20, predict_step=10, input_dim=1)
        print("Start to train")
        history, model = train(x=data_x_lstm, y=data_y, epochs=100, batch_size=64, save_dir='save_model', model=model,
                               measure=measure)
        step_to_train = step_predict(data=loss[:], model=model, input_dim=1, predict_step=10, time_step=20, div=0.01,
                                     top_step=trains_step, low_step=math.ceil(trains_step * 0.5), measure=measure)
    else:
        step_to_train = trains_step
    res1 = influx_client.query("select * from "+measure_up+" order by desc limit 1")
    key1 = res1.keys()
    res1_inter = res1[key1[0]]
    res1_items = list(res1_inter)
    retry = int(res1_items[0]['retry'])
    allow_read = load_config(allow_path)
    retry_now = int(allow_read['retry'])
    if retry_now != retry:
        new_ps = int(res1_items[0]['ps'])
        new_worker = int(res1_items[0]['worker'])
        step_to_train = math.ceil(step_to_train*int(allow_read['worker'])/new_worker)
        allow_read['retry'] = retry
        allow_read['ps'] = new_ps
        allow_read['worker'] = new_worker

        save_config2(allow_read,allow_path)
    step_items = [
        {
            'measurement': measure_t,
            'tags': {
                'task': int(pre_list[-1]),
                'runtimes': int(pre_list[-1]),
                'retry': int(retry)
            },
            'fields': {
                'training_step': step_to_train,
                'ps': int(allow_read['ps']),
                'worker': int(allow_read['worker'])
            }
        }
    ]
    print("saved in db")
    print(step_to_train)
    influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
    print("Writed in db")
    print("First prdict cost time: "+str(time.time() - time_start))
    iftrain = 0
    time_total = 0
    if modekk != 1:
        modekk = modekk_z
    countt00 = 0
    # iikk =0
    # tmp_panduan_key = -1
    while True:
        if modekk == 1:
            break
        # selected_node = select_node(influx_client,measure_s)
        res1 = influx_client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
        key1 = res1.keys()
        # print(key1[:])
        res1_inter = res1[key1[0]]
        res1_items = list(res1_inter)
        # print(res1_items[:])
        step_now = int(res1_items[0]['step'])
        time_mean_list = [float(i['time_d']) for i in res1_items]
        time_mean = np.mean(time_mean_list)
        # print(time_mean)
        # time_sleep = predict_fre * time_mean
        # print(step_now)
        ns_list = get_ns(v1)
        # print(ns_list)
        # print(aim_ns)
        # print(aim_ns in ns_list)
        write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
        key_write = write_ss.keys()
        # print(key_write[:])
        write_inter = write_ss[key_write[0]]
        write_items = list(write_inter)
        # print(write_items[:])
        write_now = int(write_items[0]['modulate'])
        if (aim_ns not in ns_list) and (write_now == 0):
            tmp_panduan_key = -1
            for iikk in range(32):
                time.sleep(1)
                ns_list = get_ns(v1)
                write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
                key_write = write_ss.keys()
                # print(key_write[:])
                write_inter = write_ss[key_write[0]]
                write_items = list(write_inter)
                # print(write_items[:])
                write_now = int(write_items[0]['modulate'])
                if (aim_ns not in ns_list) and (write_now == 0):
                    print("namespace is missing")
                else:
                    tmp_panduan_key = 1
                    break
            if tmp_panduan_key < 0:
                print("namespace has been missed")
                break
        pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
        # print(pod_status)
        print("going on")
        # print(measure)
        print(math.ceil(step_to_train*0.85))
        print(step_now)
        write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
        key_write = write_ss.keys()
        write_inter = write_ss[key_write[0]]
        write_items = list(write_inter)
        write_now = int(write_items[0]['modulate'])
        if ('Succeeded' in pod_status or 'Failed' in pod_status) and (write_now == 0):
            if countt00 <=16:
                countt00+=1
                time.sleep(1.5)
                continue
            else:
                print("Job is ended")
                break
        else:
            time.sleep(1.2)
            print("Job is going")
        # print(math.ceil(step_to_train*0.85))
        # print(step_now)
        panduan_going = math.ceil(step_to_train*0.85)
        # print(type(step_now))
        step_now = int(step_now)
        print(type(step_now))
        print(step_now)
        if step_now >= panduan_going:
            print("It need not to predict")
            modekk = 1
            break
        else:
            time.sleep(1.2)
            print("Job is going to load")
        time.sleep(2.2)
        print(measure)
        print(length)
        print(type(length))
        print("load data again")
        if time_total>= predict_fre:
            result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
            key = result.keys()
            result_inter = result[key[0]]
            result_items = list(result_inter)
            trains_step = int(result_items[0]['training_step'])
            if step_now >= trains_step - 3:
                print("This process is ended!!")
                break
            loss, max_loss = load_data(min_steps=min_steps, length=length, measure=measure, first=False)
            print("Start to load model!")
            try:
                model = load_model('save_model/%s.h5' % measure_s)
            except Exception as e:
                print(e)
                conn.close()
                lock.acquire()
                # lock.release()
                tmp = dictionary['running_number']
                tmp = tmp - 1
                dictionary['running_number'] = tmp
                lock.release()
                return
            print("get model successfully!")
            if iftrain > 0 and iftrain % 20 == 19:
                data_x, data_y, data_twice_x, data_twice_y = make_dataset(loss[:], max_loss, 20, 10, 1)
                data_x_lstm = reshape_for_lstm(data_x[:])
                # data_y_lstm = reshape_for_lstm(data_y[:])
                data_twice_x_1 = data_twice_x[:, 1, :]
                data_twice_x_2 = data_twice_x[:, 0, :]
                # data_twice_y = reshape_for_lstm(data_twice_y[:])
                data_twice_x_1_lstm = reshape_for_lstm(data_twice_x_1[:])
                data_twice_x_2_lstm = reshape_for_lstm(data_twice_x_2[:])
                history, model = train(x=data_x_lstm, y=data_y, epochs=10, batch_size=64, save_dir='save_model',
                                       model=model, measure=measure)
            step_to_train = step_predict(data=loss[:], model=model, input_dim=1, predict_step=10, time_step=20,
                                         div=0.005, top_step=trains_step, low_step=math.ceil(trains_step * 0.5),
                                         measure=measure)
            res2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
            key2 = list(res2.keys())
            res2_inter = res2[key2[0]]
            res2_items = list(res2_inter)
            retry = int(res2_items[0]['retry'])
            allow_read = load_config(allow_path)
            retry_now = int(allow_read['retry'])
            new_ps = int(allow_read['ps'])
            new_worker = int(allow_read['worker'])
            if retry_now != retry:
                new_ps = int(res2_items[0]['ps'])
                new_worker = int(res2_items[0]['worker'])
                step_to_train = math.ceil(step_to_train * int(allow_read['worker']) / new_worker)
                allow_read['retry'] = retry
                allow_read['worker'] = new_worker
                allow_read['ps'] = new_ps
                save_config2(allow_read, allow_path)

            step_items = [
                {
                    'measurement': measure_t,
                    'tags': {
                        'task': int(pre_list[-1]),
                        'runtimes': int(pre_list[-1]),
                        'retry': int(retry)
                    },
                    'fields': {
                        'training_step': step_to_train,
                        'ps': new_ps,
                        'worker': new_worker
                    }
                }
            ]
            print(step_to_train)
            influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
            print("Writed result in db")
            iftrain = iftrain + 1
            print("Predict " + str(iftrain) + " costs time: " + str(time.time() - time_start))
            time_total = 0
            time_total+=1
            time.sleep(float(time_mean))
        else:
            result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
            key = result.keys()
            result_inter = result[key[0]]
            result_items = list(result_inter)
            trains_step = int(result_items[0]['training_step'])
            if step_now >= trains_step - 3:
                print("This process is ended!!")
                break
            retry_now = int(result_items[0]['retry'])
            allow_read = load_config(allow_path)
            print("Reload success!!")
            allow_read['retry'] = retry_now
            ps_now = int(result_items[0]['ps'])
            worker_now = int(result_items[0]['worker'])
            allow_read['worker'] = worker_now
            allow_read['ps'] = ps_now
            save_config2(allow_read, allow_path)
            print("save success!!")
            result2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
            key2 = result2.keys()
            result_inter2 = result2[key2[0]]
            result_items2 = list(result_inter2)
            retry_top = int(result_items2[0]['retry'])
            if retry_top != retry_now:
                new_ps = int(result_items2[0]['ps'])
                new_worker = int(result_items2[0]['worker'])
                trains_step = math.ceil(trains_step * worker_now / new_worker)
                allow_read = load_config(allow_path)
                allow_read['retry'] = retry_top
                allow_read['ps'] = new_ps
                allow_read['worker'] = new_worker
                save_config2(allow_read, allow_path)
                print("saved successful!!")
                # print(trains_step)
                step_items = [
                    {
                        'measurement': measure_t,
                        'tags': {
                            'task': int(pre_list[-1]),
                            'runtimes': int(pre_list[-1]),
                            'retry': int(retry_top)
                        },
                        'fields': {
                            'training_step': int(trains_step),
                            'ps': int(allow_read['ps']),
                            'worker': int(allow_read['worker'])
                        }
                    }
                ]
                print("saved in db")
                influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
                print("Writed in db")
            time_total += 1
            step_to_train = trains_step
            time.sleep(float(time_mean))

    if modekk == 1:
        countt00 = 0
        while True:
            write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
            key_write = write_ss.keys()
            write_inter = write_ss[key_write[0]]
            write_items = list(write_inter)
            # print(write_items[:])
            write_now = int(write_items[0]['modulate'])
            pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
            if ('Succeeded' in pod_status or 'Failed' in pod_status) and (write_now == 0):
                if countt00 <= 16:
                    countt00+=1
                    time.sleep(1.5)
                    continue
                else:
                    print("Job is ended")
                    break
            write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
            ns_list = get_ns(v1)
            key_write = write_ss.keys()
            write_inter = write_ss[key_write[0]]
            write_items = list(write_inter)
            write_now = int(write_items[0]['modulate'])

            if (aim_ns not in ns_list) and (write_now == 0):
                tmp_panduan_key = -1
                for iikk in range(32):
                    time.sleep(1)
                    ns_list = get_ns(v1)
                    write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
                    key_write = write_ss.keys()
                    # print(key_write[:])
                    write_inter = write_ss[key_write[0]]
                    write_items = list(write_inter)
                    # print(write_items[:])
                    write_now = int(write_items[0]['modulate'])
                    if (aim_ns not in ns_list) and (write_now == 0):
                        print("namespace is missing")
                    else:
                        tmp_panduan_key = 1
                        break
                if tmp_panduan_key < 0:
                    print("namespace has been missed")
                    break
                # time.sleep(9)
                # ns_list = get_ns(v1)
                # write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
                # key_write = write_ss.keys()
                # # print(key_write[:])
                # write_inter = write_ss[key_write[0]]
                # write_items = list(write_inter)
                # # print(write_items[:])
                # write_now = int(write_items[0]['modulate'])
                # if (aim_ns not in ns_list) and (write_now == 0):
                #     print("namespace is missing")
                #     break
            # print(pod_status)
            print("going on")
            # print(measure)
            # print(math.ceil(step_to_train * 0.75))
            # print(step_now)
            # worker%d
            # selected_node = select_node(influx_client, measure_s)
            res1 = influx_client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 3")
            key1 = res1.keys()
            res1_inter = res1[key1[0]]
            res1_items = list(res1_inter)
            step_now = int(res1_items[0]['step'])
            time_mean_list = [float(i['time_d']) for i in res1_items]
            time_mean = np.mean(time_mean_list)
            result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
            key = result.keys()
            result_inter = result[key[0]]
            result_items = list(result_inter)
            trains_step = int(result_items[0]['training_step'])
            if step_now >= trains_step - 3:
                print("This process is ended!!")
                break
            retry_now = int(result_items[0]['retry'])
            allow_read = load_config(allow_path)
            print("Reload success!!")
            allow_read['retry'] = retry_now
            ps_now = int(result_items[0]['ps'])
            worker_now = int(result_items[0]['worker'])
            allow_read['worker'] = worker_now
            allow_read['ps'] = ps_now
            save_config2(allow_read, allow_path)
            print("save success!!")
            result2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
            key2 = result2.keys()
            # print(key2)
            result_inter2 = result2[key2[0]]
            result_items2 = list(result_inter2)
            # print(result_items2)
            retry_top = int(result_items2[0]['retry'])
            # print(retry_top)
            # print(type(retry_top))
            # print(retry_now)
            # print(type(retry_now))
            if retry_top != retry_now:
                new_ps = int(result_items2[0]['ps'])
                new_worker = int(result_items2[0]['worker'])
                trains_step = math.ceil(trains_step * worker_now / new_worker)
                allow_read = load_config(allow_path)
                allow_read['retry'] = retry_top
                allow_read['ps'] = new_ps
                allow_read['worker'] = new_worker
                save_config2(allow_read, allow_path)
                print("saved successful!!")
                # print(trains_step)
                step_items = [
                    {
                        'measurement': measure_t,
                        'tags': {
                            'task': int(pre_list[-1]),
                            'runtimes': int(pre_list[-1]),
                            'retry': int(retry_top)
                        },
                        'fields': {
                            'training_step': int(trains_step),
                            'ps': int(allow_read['ps']),
                            'worker': int(allow_read['worker'])
                        }
                    }
                ]
                print("saved in db")
                influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
                print("Writed in db")
                time.sleep(float(0.3*time_mean))
            else:
                time.sleep(float(time_mean))


    conn.close()
    lock.acquire()
    # lock.release()
    tmp = dictionary['running_number']
    tmp = tmp - 1
    dictionary['running_number'] = tmp
    lock.release()
    time_end = time.time()
    print(time_end - time_start)
    print("This prediction end!")

def step_nnls_predict_handle(conn,dictionary,lock,pool_size,connect_try=5,predict_fre=150):
    aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
    aConfiguration = kubernetes.client.Configuration()
    aConfiguration.host = "https://192.168.128.10:6443"
    aConfiguration.verify_ssl = False
    aConfiguration.api_key = {"authorization": "Bearer " + aToken}
    aApiClient = kubernetes.client.ApiClient(aConfiguration)
    v1 = kubernetes.client.CoreV1Api(aApiClient)
    lock.acquire()
    # lock.release()
    tmp = dictionary['running_number']
    tmp = tmp + 1
    dictionary['running_number'] = tmp
    lock.release()
    influx_client = influxdb.InfluxDBClient(host='192.168.128.10', port=8086, username='admin', password='admin',
                                            database="PREDICT")
    try_times = 1
    legal_pattern = '\w+ \d+'
    msg_from_client = conn.recv(4096)
    matched = None
    while True:
        if try_times > connect_try:
            break
        msg_from_client_str = str(msg_from_client.decode('utf-8'))
        print(msg_from_client_str + " " + "try_time: " + str(try_times))
        # try_times = try_times + 1
        matched = re.match(legal_pattern, msg_from_client_str)
        if matched is not None:
            break
        if not msg_from_client:
            break
        response = "403 " + "Message-error!"

        conn.send(bytes(response, 'utf-8'))

        msg_from_client = conn.recv(4096)
        try_times = try_times + 1

        # msg_from_client_str = str(msg_from_client.decode('utf-8'))

    if matched is None:
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        return
    print("connect success!")
    measure = matched.group()
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    measure_up = pre_list[0] + 'U' + pre_list[-1]
    measure_write = pre_list[0] + 'W' + pre_list[-1]
    lock.acquire()
    # lock.release()
    tmp_running = dictionary['running_number']
    lock.release()
    res_pool = pool_size - tmp_running
    response = "400 " + pre_list[0] + " " + pre_list[-1] + " " + str(res_pool)
    conn.send(bytes(response, 'utf-8'))
    catched_job = pre_list[0]
    catched_job = catched_job.lower()
    if catched_job == 'xce':
        aim_ns = 'xception-' + pre_list[-1] + '-' + pre_list[-1]
    else:
        aim_ns = catched_job + "-" + pre_list[-1] + "-" + pre_list[-1]
        #/tfdata/k8snfs/setfix/
    job_con_path = "/tfdata/k8snfs/setfix/%s/%s.json" % (aim_ns, aim_ns)
    # job_con_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, aim_ns)
    job_config = load_config(job_con_path)
    print("load job config success!!")
    # allow_path = "/tfdata/k8snfs/%s/%s.json" % (aim_ns, measure_t)
    allow_path = "/tfdata/k8snfs/setfix/%s/%s.json" % (aim_ns, measure_t)
    # allow_path2 = "/tfdata/k8snfs/%s/%s_r.json" % (measure_t,measure_t)
    allow_p, created = check_path(aim_ns)
    print(allow_p)
    if created:
        allow_read = {}
        # allow_readr = {}
        allow_read['OK'] = True
        allow_read['retry'] = job_config['retry']
        save_config2(allow_read, allow_path)
        # save_config2(allow_readr,allow_path2)
    if not os.path.exists(allow_path):
        allow_read = {}
        # allow_readr = {}
        allow_read['OK'] = True
        allow_read['retry'] = job_config['retry']
        save_config2(allow_read, allow_path)

    ns_list = get_ns(v1)
    ceshi_count = 0
    ceshi_in = False
    while True:
        if ceshi_count > 35:
            break
        ns_list = get_ns(v1)
        write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
        key_write = write_ss.keys()
        print(key_write[:])
        write_inter = write_ss[key_write[0]]
        write_items = list(write_inter)
        print(write_items[:])
        write_now = int(write_items[0]['modulate'])
        if aim_ns not in ns_list and (write_now == 0):
            ceshi_count += 1
            time.sleep(15)
        else:
            ceshi_in = True
            break
    if not ceshi_in:
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        print("namespace created error!")
        return
    result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
    key = result.keys()
    print(key)
    result_inter = result[key[0]]
    result_items = list(result_inter)
    print(result_items)
    trains_step = int(result_items[0]['training_step'])
    tmp_item = dict(result_items[0])
    key_tmp = tmp_item.keys()
    if 'retry' not in key_tmp:
        retry_now = int(job_config['retry'])
    else:
        retry_now = int(result_items[0]['retry'])

    allow_read = load_config(allow_path)
    print("Reload success!!")
    allow_read['retry'] = retry_now
    # 'ps_replicas': job.ps_replicas,
    # 'worker_replicas': job.worker_replicas
    if 'ps' not in key_tmp:
        ps_now = int(job_config['ps_replicas'])
    else:
        ps_now = int(result_items[0]['ps'])
    if 'worker' not in key_tmp:
        worker_now = int(job_config['worker_replicas'])
    else:
        worker_now = int(result_items[0]['worker'])
    allow_read['worker'] = worker_now
    allow_read['ps'] = ps_now
    save_config2(allow_read, allow_path)
    print("save success!!")
    result2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
    key2 = result2.keys()
    print(key2)
    result_inter2 = result2[key2[0]]
    result_items2 = list(result_inter2)
    print(result_items2)
    retry_top = int(result_items2[0]['retry'])
    print(retry_top)
    print(type(retry_top))
    print(retry_now)
    print(type(retry_now))
    if retry_top != retry_now:
        new_ps = int(result_items2[0]['ps'])
        new_worker = int(result_items2[0]['worker'])
        trains_step = math.ceil(trains_step * worker_now / new_worker)
        allow_read = load_config(allow_path)
        allow_read['retry'] = retry_top
        allow_read['ps'] = new_ps
        allow_read['worker'] = new_worker
        save_config2(allow_read, allow_path)
        print("saved successful!!")
    print(trains_step)
    modekk = 0
    if trains_step <= 200:
        step_items = [
            {
                'measurement': measure_t,
                'tags': {
                    'task': int(pre_list[-1]),
                    'runtimes': int(pre_list[-1]),
                    'retry': int(retry_top)
                },
                'fields': {
                    'training_step': int(trains_step),
                    'ps': int(allow_read['ps']),
                    'worker': int(allow_read['worker'])
                }
            }
        ]
        print("saved in db")
        print(trains_step)
        influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
        print("Writed in db")
        # conn.close()
        # lock.acquire()
        # # lock.release()
        # tmp = dictionary['running_number']
        # tmp = tmp - 1
        # dictionary['running_number'] = tmp
        # lock.release()
        print("Do not need to predict,return")
        modekk = 1
    min_steps = math.ceil(trains_step * 0.2)
    length = math.ceil(min_steps * 0.4)
    print("Initial Config Success!" + "min_steps:" + str(min_steps))
    time_start = time.time()
    print("start to load data")
    loss, max_loss, modekk_z = load_data_nnls(min_steps=min_steps, length=length, measure=measure, first=True)
    if not loss:
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        return
    # loss_array = normalization(loss,max_loss)
    result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
    key = result.keys()
    result_inter = result[key[0]]
    result_items = list(result_inter)
    trains_step = int(result_items[0]['training_step'])
    step_to_train = trains_step
    if trains_step <= 200:
        modekk_z = 1
    if modekk_z != 1:
        print("Get data first time")
        data_in, step_x = make_dataset_nnls(loss, max_loss)
        step_to_train = predict_step_nnls(data_in, step_x, measure, trains_step, math.ceil(trains_step * 0.5))
    else:
        step_to_train = trains_step
    res1 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
    key1 = res1.keys()
    res1_inter = res1[key1[0]]
    res1_items = list(res1_inter)
    retry = int(res1_items[0]['retry'])
    allow_read = load_config(allow_path)
    retry_now = int(allow_read['retry'])
    if retry_now != retry:
        new_ps = int(res1_items[0]['ps'])
        new_worker = int(res1_items[0]['worker'])
        step_to_train = math.ceil(step_to_train * int(allow_read['worker']) / new_worker)
        allow_read['retry'] = retry
        allow_read['ps'] = new_ps
        allow_read['worker'] = new_worker
        save_config2(allow_read, allow_path)
    step_items = [
        {
            'measurement': measure_t,
            'tags': {
                'task': int(pre_list[-1]),
                'runtimes': int(pre_list[-1]),
                'retry': int(retry)
            },
            'fields': {
                'training_step': step_to_train,
                'ps': int(allow_read['ps']),
                'worker': int(allow_read['worker'])
            }
        }
    ]
    print("saved in db")
    print(step_to_train)
    influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
    print("Writed in db")
    print("First prdict cost time: " + str(time.time() - time_start))
    iftrain = 0
    time_total = 0
    if modekk != 1:
        modekk = modekk_z
    while True:
        if modekk == 1:
            break
        # selected_node = select_node(influx_client, measure_s)
        res1 = influx_client.query(
            "select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
        key1 = res1.keys()
        print(key1[:])
        res1_inter = res1[key1[0]]
        res1_items = list(res1_inter)
        print(res1_items[:])
        step_now = int(res1_items[0]['step'])
        time_mean_list = [float(i['time_d']) for i in res1_items]
        time_mean = np.mean(time_mean_list)
        print(time_mean)
        # time_sleep = predict_fre * time_mean
        print(step_now)
        ns_list = get_ns(v1)
        print(ns_list)
        print(aim_ns)
        print(aim_ns in ns_list)
        write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
        key_write = write_ss.keys()
        print(key_write[:])
        write_inter = write_ss[key_write[0]]
        write_items = list(write_inter)
        print(write_items[:])
        write_now = int(write_items[0]['modulate'])
        if (aim_ns not in ns_list) and (write_now == 0):
            time.sleep(15)
            ns_list = get_ns(v1)
            write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
            key_write = write_ss.keys()
            # print(key_write[:])
            write_inter = write_ss[key_write[0]]
            write_items = list(write_inter)
            # print(write_items[:])
            write_now = int(write_items[0]['modulate'])
            if (aim_ns not in ns_list) and (write_now == 0):
                print("namespace is missing")
                break
        pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
        print(pod_status)
        print("going on")
        print(measure)
        print(math.ceil(step_to_train * 0.85))
        print(step_now)
        write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
        key_write = write_ss.keys()
        write_inter = write_ss[key_write[0]]
        write_items = list(write_inter)
        write_now = int(write_items[0]['modulate'])
        if ('Succeeded' in pod_status or 'Failed' in pod_status) and (write_now == 0):
            print("Job is ended")
            break
        else:
            time.sleep(3)
            print("Job is going")
        print(math.ceil(step_to_train * 0.85))
        print(step_now)
        panduan_going = math.ceil(step_to_train * 0.85)
        print(type(step_now))
        step_now = int(step_now)
        print(type(step_now))
        print(step_now)
        if step_now >= panduan_going:
            print("It need not to predict")
            modekk = 1
            break
        else:
            time.sleep(2)
            print("Job is going to load")
        time.sleep(2.5)
        print(measure)
        print(length)
        print(type(length))
        print("load data again")
        if time_total >= predict_fre:
            result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
            key = result.keys()
            result_inter = result[key[0]]
            result_items = list(result_inter)
            trains_step = int(result_items[0]['training_step'])
            if step_now >= trains_step - 3:
                print("This process is ended!!")
                break
            # loss, max_loss = load_data_nnls(min_steps=min_steps, length=length, measure=measure, first=False)
            loss,max_loss = load_data_nnls(min_steps=min_steps,length=length,measure=measure,first=False)
            print("start to nnls process!!")
            data_in,step_x = make_dataset_nnls(loss,max_loss)
            step_to_train = predict_step_nnls(data_in,step_x,measure,trains_step,math.ceil(trains_step*0.5))
            # step_to_train = step_predict(data=loss[:], model=model, input_dim=1, predict_step=10, time_step=20,
            #                              div=0.01, top_step=trains_step, low_step=math.ceil(trains_step * 0.5),
            #                              measure=measure)
            res2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
            key2 = list(res2.keys())
            res2_inter = res2[key2[0]]
            res2_items = list(res2_inter)
            retry = int(res2_items[0]['retry'])
            allow_read = load_config(allow_path)
            retry_now = int(allow_read['retry'])
            new_ps = int(allow_read['ps'])
            new_worker = int(allow_read['worker'])
            if retry_now != retry:
                new_ps = int(res2_items[0]['ps'])
                new_worker = int(res2_items[0]['worker'])
                step_to_train = math.ceil(step_to_train * int(allow_read['worker']) / new_worker)
                allow_read['retry'] = retry
                allow_read['worker'] = new_worker
                allow_read['ps'] = new_ps
                save_config2(allow_read, allow_path)

            step_items = [
                {
                    'measurement': measure_t,
                    'tags': {
                        'task': int(pre_list[-1]),
                        'runtimes': int(pre_list[-1]),
                        'retry': int(retry)
                    },
                    'fields': {
                        'training_step': step_to_train,
                        'ps': new_ps,
                        'worker': new_worker
                    }
                }
            ]
            print(step_to_train)
            influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
            print("Writed result in db")
            iftrain = iftrain + 1
            print("Predict " + str(iftrain) + " costs time: " + str(time.time() - time_start))
            time_total = 0
            time_total += 1
            time.sleep(float(time_mean))
        else:
            result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
            key = result.keys()
            result_inter = result[key[0]]
            result_items = list(result_inter)
            trains_step = int(result_items[0]['training_step'])
            if step_now >= trains_step - 3:
                print("This process is ended!!")
                break
            retry_now = int(result_items[0]['retry'])
            allow_read = load_config(allow_path)
            print("Reload success!!")
            allow_read['retry'] = retry_now
            ps_now = int(result_items[0]['ps'])
            worker_now = int(result_items[0]['worker'])
            allow_read['worker'] = worker_now
            allow_read['ps'] = ps_now
            save_config2(allow_read, allow_path)
            print("save success!!")
            result2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
            key2 = result2.keys()
            result_inter2 = result2[key2[0]]
            result_items2 = list(result_inter2)
            retry_top = int(result_items2[0]['retry'])
            if retry_top != retry_now:
                new_ps = int(result_items2[0]['ps'])
                new_worker = int(result_items2[0]['worker'])
                trains_step = math.ceil(trains_step * worker_now / new_worker)
                allow_read = load_config(allow_path)
                allow_read['retry'] = retry_top
                allow_read['ps'] = new_ps
                allow_read['worker'] = new_worker
                save_config2(allow_read, allow_path)
                print("saved successful!!")
                # print(trains_step)
                step_items = [
                    {
                        'measurement': measure_t,
                        'tags': {
                            'task': int(pre_list[-1]),
                            'runtimes': int(pre_list[-1]),
                            'retry': int(retry_top)
                        },
                        'fields': {
                            'training_step': int(trains_step),
                            'ps': int(allow_read['ps']),
                            'worker': int(allow_read['worker'])
                        }
                    }
                ]
                print("saved in db")
                influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
                print("Writed in db")
            time_total += 1
            step_to_train = trains_step
            time.sleep(float(time_mean) * 0.8)

    if modekk == 1:
        while True:
            write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
            key_write = write_ss.keys()
            write_inter = write_ss[key_write[0]]
            write_items = list(write_inter)
            # print(write_items[:])
            write_now = int(write_items[0]['modulate'])
            pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
            if ('Succeeded' in pod_status or 'Failed' in pod_status) and (write_now == 0):
                print("Job is ended")
                break
            write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
            ns_list = get_ns(v1)
            key_write = write_ss.keys()
            write_inter = write_ss[key_write[0]]
            write_items = list(write_inter)
            write_now = int(write_items[0]['modulate'])
            if (aim_ns not in ns_list) and (write_now == 0):
                time.sleep(9)
                ns_list = get_ns(v1)
                write_ss = influx_client.query("select * from " + measure_write + " order by desc limit 1")
                key_write = write_ss.keys()
                # print(key_write[:])
                write_inter = write_ss[key_write[0]]
                write_items = list(write_inter)
                # print(write_items[:])
                write_now = int(write_items[0]['modulate'])
                if (aim_ns not in ns_list) and (write_now == 0):
                    print("namespace is missing")
                    break
            # print(pod_status)
            print("going on")
            res1 = influx_client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 3")
            key1 = res1.keys()
            res1_inter = res1[key1[0]]
            res1_items = list(res1_inter)
            step_now = int(res1_items[0]['step'])
            time_mean_list = [float(i['time_d']) for i in res1_items]
            time_mean = np.mean(time_mean_list)
            result = influx_client.query("select * from " + measure_t + " order by desc limit 1")
            key = result.keys()
            result_inter = result[key[0]]
            result_items = list(result_inter)
            trains_step = int(result_items[0]['training_step'])
            if step_now >= trains_step - 3:
                print("This process is ended!!")
                break
            retry_now = int(result_items[0]['retry'])
            allow_read = load_config(allow_path)
            print("Reload success!!")
            allow_read['retry'] = retry_now
            ps_now = int(result_items[0]['ps'])
            worker_now = int(result_items[0]['worker'])
            allow_read['worker'] = worker_now
            allow_read['ps'] = ps_now
            save_config2(allow_read, allow_path)
            print("save success!!")
            result2 = influx_client.query("select * from " + measure_up + " order by desc limit 1")
            key2 = result2.keys()
            # print(key2)
            result_inter2 = result2[key2[0]]
            result_items2 = list(result_inter2)
            # print(result_items2)
            retry_top = int(result_items2[0]['retry'])
            if retry_top != retry_now:
                new_ps = int(result_items2[0]['ps'])
                new_worker = int(result_items2[0]['worker'])
                trains_step = math.ceil(trains_step * worker_now / new_worker)
                allow_read = load_config(allow_path)
                allow_read['retry'] = retry_top
                allow_read['ps'] = new_ps
                allow_read['worker'] = new_worker
                save_config2(allow_read, allow_path)
                print("saved successful!!")
                # print(trains_step)
                step_items = [
                    {
                        'measurement': measure_t,
                        'tags': {
                            'task': int(pre_list[-1]),
                            'runtimes': int(pre_list[-1]),
                            'retry': int(retry_top)
                        },
                        'fields': {
                            'training_step': int(trains_step),
                            'ps': int(allow_read['ps']),
                            'worker': int(allow_read['worker'])
                        }
                    }
                ]
                print("saved in db")
                influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
                print("Writed in db")
                time.sleep(float(0.3 * time_mean))
            else:
                time.sleep(float(time_mean))

    conn.close()
    lock.acquire()
    # lock.release()
    tmp = dictionary['running_number']
    tmp = tmp - 1
    dictionary['running_number'] = tmp
    lock.release()
    # print(data_x.shape)
    # print(data_y.shape)
    # print(data_twice_x.shape)
    # print(data_twice_y.shape)
    # print(normalization(loss,max_loss))
    # print(data_x)
    # print(data_twice_x)
    time_end = time.time()
    print(time_end - time_start)
    print("This prediction end!")




if __name__ == '__main__':
    HOST = '192.168.128.5'
    PORT = 12527
    ADDR = (HOST,PORT)
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    dictionary['running_number'] = 0
    lock = mgr.Lock()
    pool = multiprocessing.Pool(processes=45)
    pool_size = 45
    connect_try = 5
    predict_fre = 100
    # new_mem = joblib.load('est_mem.pkl')
    # new_cpu = joblib.load('est_cpu.pkl')
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print(dictionary['running_number'])
    print("Waiting for connection...")
    while True:
        conn,addr = server.accept()
        print("Get an request!")
        # step_predict_handle(conn,dictionary,lock,pool_size=5,connect_try=5,predict_fre=150)
        # pool.apply_async(step_predict_handle, (conn, dictionary, lock,pool_size,connect_try,predict_fre))
        pool.apply_async(step_resource_predict_handle,
                         (conn, dictionary, lock, pool_size, connect_try, predict_fre))
        print("Allocate Pool Process Success")
    pool.close()  # 进程池不再接收新任务
    pool.join()  # 进程池内的进程都执行完了
    server.close()













