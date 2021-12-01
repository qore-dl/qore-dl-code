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
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingRegressor
import time
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import optimizers
from keras.layers import LSTM,Dense,Activation,Dropout,Input,concatenate
from keras.models import Sequential,Model
from keras.callbacks import EarlyStopping, ModelCheckpoint,LearningRateScheduler,ReduceLROnPlateau
# from keras.utils.vis_utils import plot_model
# import matplotlib.pyplot as plt

import time
import json
import re
from fps import vgg3fpmodel,res3fpmodel
from TimeoutException import Myhandler,TimeoutError

def check_parts(est_gpu,bath_size,flops,params):
    bfp = np.array([bath_size,flops,params]).reshape(1,3)
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
                bfp = np.array([real_batch, flops, params]).reshape(1, 3)
                predict_res = est_gpu.predict(bfp)
                pre_res = int(predict_res[0])
                if pre_res == 1:
                    part = bath_size
                    break
                else:
                    part = -1
                    break

            else:
                bfp = np.array([real_batch, flops, params]).reshape(1, 3)
                predict_res = est_gpu.predict(bfp)
                pre_res = int(predict_res[0])
                if pre_res == 1:
                    part = part
                    break

    return part

def load_task(params_dict,template_id):
    if template_id == 1:
        try:
            batch,flops,params = vgg3fpmodel.vgg3fp(**params_dict)
        except:
            print("报错")
    elif template_id == 2:
        try:
            batch,flops,params = res3fpmodel.res3fp(**params_dict)
        except Exception as e:
            print(e)

    return batch,flops,params
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

def derivation(x1,x2):
    xx = (x1 - x2)**2
    result = float((math.sqrt((xx))) / x1)
    return result

def get_ns(v1):
    ns_list = []
    for i in v1.list_namespace().items:
        ns_list.append(i.metadata.name)
    return ns_list

def step_resource_predict_handle(conn,dictionary,lock,est_gpu,pool_size,connect_try=5,predict_fre=150):
    lock.acquire()
    # lock.release()
    tmp = dictionary['running_number']
    tmp = tmp + 1
    dictionary['running_number'] = tmp
    lock.release()
    influx_client = influxdb.InfluxDBClient(host='172.16.190.17',port=8086,username='admin',password='admin',database="PREDICT")
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
    # measure_s = pre_list[0] + 'S' + pre_list[-1]
    # measure_t = pre_list[0] + 'T' + pre_list[-1]
    lock.acquire()
    # lock.release()
    tmp_running = dictionary['running_number']
    lock.release()
    res_pool = pool_size - tmp_running
    response = "400 "+pre_list[0]+" "+pre_list[-1]+" "+str(res_pool)
    conn.send(bytes(response,'utf-8'))

    msg2 = conn.recv(4096)
    msg2_str = str(msg2.decode('utf-8'))
    print(msg2_str)
    if pre_list[0] == 'VGG':
        template_id = 1
    elif pre_list[0] == 'RES':
        template_id = 2

    time_start = time.time()
    try:
        paramss = json.loads(msg2_str)
        print(paramss)
    except Exception as e:
        print("解析错误")
        print(e)
        ress = '405 ' + 'json error!'
        conn.send(bytes(ress, 'utf-8'))
    try:
        signal.signal(signal.SIGALRM, Myhandler)
        signal.alarm(600)
        try:
            batch,flop, param = load_task(paramss, template_id=template_id)
            if flop == 0 or param == 0:
                ress = '407 ' + 'predict error!'
                # conn.send(bytes(ress, 'utf-8'))
            else:
                data = np.array([batch, flop, param])
                data = np.mat(data)
                data = data.A
                try:
                    part = check_parts(est_gpu,batch,flop,param)
                    # mem_req = est_mem.predict(data)
                    ress = "400 %d %d %d %d" % (batch, flop, param, part)
                except Exception as e5:
                    print(e5)
                    ress = '407 ' + 'predict error!'
                    # conn.send(bytes(ress, 'utf-8'))
        except Exception as e0:
            print(e0)
            ress = '409'+ 'get feature error!'

        signal.alarm(0)
    except TimeoutError as e4:
        print(e4)
        ress = '406 ' + 'get feature data error!'
        print("Send TimeoutError!")
            # conn.send(bytes(ress, 'utf-8'))
    conn.send(bytes(ress, 'utf-8'))
    print("Send message successfully!!")
    re_client = conn.recv(1024)
    re_client_str = str(re_client.decode('utf-8'))
    if re_client_str == '0':
        conn.close()
        lock.acquire()
        # lock.release()
        tmp = dictionary['running_number']
        tmp = tmp - 1
        dictionary['running_number'] = tmp
        lock.release()
        print("YUCEJISHULE")
        return
    print('Get cpu and memory costs: %f' % (time.time() - time_start))

    conn.close()
    lock.acquire()
    # lock.release()
    tmp = dictionary['running_number']
    tmp = tmp - 1
    dictionary['running_number'] = tmp
    lock.release()

    time_end = time.time()
    print(time_end - time_start)

if __name__ == '__main__':
    HOST = '172.16.190.97'
    PORT = 12529
    ADDR = (HOST,PORT)
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    dictionary['running_number'] = 0
    lock = mgr.Lock()
    pool = multiprocessing.Pool(processes=2)
    pool_size = 2
    connect_try = 5
    predict_fre = 150
    est_gpu = joblib.load('est_gpu.pkl')
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
                         (conn, dictionary, lock, est_gpu, pool_size, connect_try, predict_fre))
        print("Allocate Pool Process Success")
    pool.close()  # 进程池不再接收新任务
    pool.join()  # 进程池内的进程都执行完了
    server.close()













