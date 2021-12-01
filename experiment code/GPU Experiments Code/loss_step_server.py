import influxdb
import pandas as pd
import numpy as np
import kubernetes
import os
import math
import socket
import multiprocessing
import datetime as dt
from utils import Timer
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
    return config_content

def load_data(min_steps,length,measure,db="PREDICT",host='192.168.128.10',first=True):
    print("Start for db load data")
    client = influxdb.InfluxDBClient(host=host,port=8086,username='admin',password='admin',database=db)
    pre_list = measure.split(" ")
    measure_s = pre_list[0]+'S'+pre_list[-1]
    measure_t = pre_list[0]+'T'+pre_list[-1]
    print(measure_s)
    if first:
        while True:
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

            if step_now >= min_steps:
                break
            else:
                div_num = min_steps - step_now + 1
                sleep_last = interval_step * div_num
                print(sleep_last)
                print(div_num)
                print(interval_step)
                time.sleep(sleep_last)
        result = client.query("select * from " + measure_s + " where nodes='worker0' order by desc")
    else:
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

    return loss,max_loss
    # tmp_step.reverse()
    # tmp_loss.reverse()
    # msg['step'] = tmp_step
    # msg['loss'] = tmp_loss
    # step_set = set(tmp_step)

def normalization(loss,max_loss):
    loss_array = []
    for i in loss:
        tmp = i / max_loss
        loss_array.append(tmp)
    loss_array = np.asarray(loss_array)

    return loss_array

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
        pone = predict_once(data1[i],data2[i],model,input_dim,time_step,predict_step)
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

def step_predict_handle(conn,dictionary,lock,pool_size,connect_try=5,predict_fre=150):
    #measure,db="PREDICT",host='192.168.128.10'
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
        return
    print("connect success!")
    measure = matched.group()
    pre_list = measure.split(" ")
    measure_s = pre_list[0] + 'S' + pre_list[-1]
    measure_t = pre_list[0] + 'T' + pre_list[-1]
    lock.acquire()
    # lock.release()
    tmp_running = dictionary['running_number']
    lock.release()
    res_pool = pool_size - tmp_running
    response = "400 "+pre_list[0]+" "+pre_list[-1]+" "+str(res_pool)
    conn.send(bytes(response,'utf-8'))

    result = influx_client.query("select training_step from " + measure_t + " order by desc limit 1")
    key = result.keys()
    result_inter = result[key[0]]
    result_items = list(result_inter)
    trains_step = result_items[0]['training_step']
    print(trains_step)
    min_steps = math.ceil(trains_step*0.2)
    length = math.ceil(min_steps*0.4)
    print("Initial Config Success!"+"min_steps:"+str(min_steps))
    time_start = time.time()
    print("start to load data")
    loss,max_loss = load_data(min_steps=min_steps,length=length,measure=measure,first=True)
    # loss_array = normalization(loss,max_loss)
    print("Get data first time")
    data_x,data_y,data_twice_x,data_twice_y = make_dataset(loss[:],max_loss,20,10,1)
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
        model = build_lstm_model(time_step=20,predict_step=10,input_dim=1)
    print("Start to train")
    history, model = train(x=data_x_lstm,y=data_y,epochs=100,batch_size=64,save_dir='save_model',model=model,measure=measure)

    step_to_train = step_predict(data=loss[:],model=model,input_dim=1,predict_step=10,time_step=20,div=0.01,top_step=trains_step,low_step=math.ceil(trains_step*0.5),measure=measure)
    res1 = influx_client.query("select * from "+measure_s+" order by desc limit 1")
    key1 = res1.keys()
    res1_inter = res1[key1[0]]
    res1_items = list(res1_inter)
    retry = res1_items[0]['retry']


    step_items = [
        {
            'measurement': measure_t,
            'tags': {
                'task': int(pre_list[-1]),
                'runtimes': int(pre_list[-1]),
                'retry': int(retry)
            },
            'fields': {
                'training_step': step_to_train
            }
        }
    ]
    print("saved in db")
    print(step_to_train)
    influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
    print("Writed in db")
    print("First prdict cost time: "+str(time.time() - time_start))
    iftrain = 0
    while True:
        res1 = influx_client.query("select * from " + measure_s + " where nodes='worker0' order by desc limit 10")
        key1 = res1.keys()
        print(key1[:])
        res1_inter = res1[key1[0]]
        res1_items = list(res1_inter)
        print(res1_items[:])
        step_now = res1_items[0]['step']
        time_mean_list = [float(i['time_d']) for i in res1_items]
        time_mean = np.mean(time_mean_list)
        print(time_mean)
        print(step_now)
        catched_job = pre_list[0]
        catched_job = catched_job.lower()
        if catched_job=='xce':
            aim_ns = 'xception-'+pre_list[-1]+'-'+pre_list[-1]
        else:
            aim_ns = catched_job+"-"+pre_list[-1]+"-"+pre_list[-1]
        ns_list = get_ns(v1)
        print(ns_list)
        print(aim_ns)
        print(aim_ns in ns_list)
        if aim_ns not in ns_list:
            time.sleep(15)
            ns_list = get_ns(v1)
            if aim_ns not in ns_list:
                print("namespace is missing")
                break
        pod_status = [i.status.phase for i in v1.list_namespaced_pod(aim_ns).items]
        print(pod_status)
        print("going on")
        print(measure)
        print(math.ceil(step_to_train*0.75))
        print(step_now)
        if 'Succeeded' in pod_status or 'Failed' in pod_status:
            print("Job is ended")
            break
        else:
            time.sleep(3)
            print("Job is going")
        print(math.ceil(step_to_train*0.75))
        print(step_now)
        panduan_going = math.ceil(step_to_train*0.75)
        print(type(step_now))
        step_now = int(step_now)
        print(type(step_now))
        print(step_now)
        if step_now >= panduan_going:
            print("It need not to predict")
            break
        else:
            time.sleep(3)
            print("Job is going to load")
        time.sleep(5)
        print(measure)
        print(length)
        print(type(length))
        print("load data again")
        loss,max_loss = load_data(min_steps=min_steps,length=length,measure=measure,first=False)
        print("Start to load model!")
        model = load_model('save_model/%s.h5' % measure_s)
        if iftrain > 0 and iftrain % 10 == 9:
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
        step_to_train = step_predict(data=loss[:],model=model,input_dim=1,predict_step=10,time_step=20,div=0.01,top_step=trains_step,low_step=math.ceil(trains_step*0.5),measure=measure)
        res2 = influx_client.query("select * from " + measure_s + " order by desc limit 1")
        key2 = res2.keys()
        res2_inter = res2[key2[0]]
        res2_items = list(res2_inter)
        retry = res2_items[0]['retry']

        step_items = [
            {
                'measurement': measure_t,
                'tags': {
                    'task': int(pre_list[-1]),
                    'runtimes': int(pre_list[-1]),
                    'retry': int(retry)
                },
                'fields': {
                    'training_step': step_to_train
                }
            }
        ]
        print(step_to_train)
        influx_client.write_points(step_items, time_precision="ms", database="PREDICT")
        print("Writed result in db")
        iftrain = iftrain+1
        print("Predict " + str(iftrain)+" costs time: "+str(time.time() - time_start))
        time_sleep = predict_fre*time_mean
        print(iftrain)
        print(time_mean)
        print(time_sleep)
        time.sleep(time_sleep)

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
    # from_client_msg_str = str(from_client_msg.decode('utf-8'))


if __name__ == '__main__':
    HOST = '192.168.128.21'
    PORT = 12527
    ADDR = (HOST,PORT)
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    dictionary['running_number'] = 0
    lock = mgr.Lock()
    pool = multiprocessing.Pool(processes=5)
    pool_size = 5
    connect_try = 5
    predict_fre = 150
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print(dictionary['running_number'])
    print("Waiting for connection...")
    while True:
        conn,addr = server.accept()
        print("Get an request!")
        # step_predict_handle(conn,dictionary,lock,pool_size=5,connect_try=5,predict_fre=150)
        pool.apply_async(step_predict_handle, (conn, dictionary, lock,pool_size,connect_try,predict_fre))
        print("Allocate Pool Process Success")
    pool.close()  # 进程池不再接收新任务
    pool.join()  # 进程池内的进程都执行完了
    server.close()

    # time_start = time.time()
    # measure = "VGG 1"
    #
    # loss,max_loss = load_data(min_steps=200,length=800,measure="VGG 1")
    # # loss_array = normalization(loss,max_loss)
    # data_x,data_y,data_twice_x,data_twice_y = make_dataset(loss,max_loss,20,10,1)
    # data_x_lstm = reshape_for_lstm(data_x[:])
    # data_y_lstm = reshape_for_lstm(data_y[:])
    # data_twice_x_1 = data_twice_x[:,1,:]
    # data_twice_x_2 = data_twice_x[:,0,:]
    # data_twice_y = reshape_for_lstm(data_twice_y[:])
    # data_twice_x_1_lstm = reshape_for_lstm(data_twice_x_1[:])
    # data_twice_x_2_lstm = reshape_for_lstm(data_twice_x_2[:])
    #
    #
    #
    # # model = load_model('save_model/31122019-031018-e10.h5')
    # if os.path.exists("save_model/%s.h5" % measure):
    #     model = load_model('save_model/%s.h5' % measure)
    # else:
    #     model = build_lstm_model(time_step=20,predict_step=10,input_dim=1)
    #
    # history, model = train(x=data_x_lstm,y=data_y,epochs=100,batch_size=32,save_dir='save_model',model=model,measure=measure)
    #
    # step_to_train = step_predict(data=loss[:],model=model,input_dim=1,predict_step=10,time_step=20,div=0.01,top_step=2000,measure=measure)
    # print(step_to_train)
    # # print(data_x.shape)
    # # print(data_y.shape)
    # # print(data_twice_x.shape)
    # # print(data_twice_y.shape)
    # # print(normalization(loss,max_loss))
    # # print(data_x)
    # # print(data_twice_x)
    # time_end = time.time()
    # print(time_end - time_start)













