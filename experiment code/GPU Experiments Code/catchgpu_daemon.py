import json
import multiprocessing
import influxdb
from subprocess import Popen, PIPE
import pandas as pd
import numpy as np
import kubernetes
import os
import math
import  sys
import time
import re
import socket
import DBTools
node_index = {'Good1':1,'Good2':2,'Good3':3,'Norm1':4,'Norm2':5}
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

def monitor_caiji(dictionary,conn):
    response = "400 " + "Start to Monitor!"

    conn.send(bytes(response, 'utf-8'))
    tmp_run = dictionary['running']
    tmp_run = 1
    dictionary['running'] = tmp_run
    while True:
        waiting = conn.recv(4096)
        waiting_str = str(waiting.decode('utf-8')).strip()
        if 'end' in waiting_str:
            tmp_run = -1
            dictionary['running'] = tmp_run
            break
    return


if __name__ == '__main__':
    HOST = '172.16.190.93'
    PORT = 14527
    ADDR = (HOST, PORT)
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    dictionary['running_number'] = 0
    dictionary['running'] = 0
    print(dictionary['running_number'])
    print("Waiting for connection...")
    lock = mgr.Lock()
    pool = multiprocessing.Pool(processes=5)
    pool_size = 5
    connect_try = 5
    predict_fre = 150
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    conn, addr = server.accept()
    print("Get an request!")
    msg_from_client = conn.recv(4096)
    legal_pattern = '\w+ \d+'
    try_times = 0
    # msg_from_client = conn.recv(4096)
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

    if matched is None:
        conn.close()
        sys.exit(1)
    mp = multiprocessing.Process(target=monitor_caiji, args=(dictionary,conn))
    mp.daemon = True
    mp.start()
    print("connect success!")
    measure = matched.group()
    pre_list = measure.split(" ")
    measure = pre_list[0]+str(int(pre_list[-1]))

    influx_client = influxdb.InfluxDBClient(host='172.16.190.97', port=8086, username='admin', password='admin',
                                            database="NODEGPU")

    gpu_type = 1
    if 'Good' in pre_list[0].strip():
        gpu_type = 1
    else:
        gpu_type = 2

    total = []
    gavail = []
    gpu0 = []
    gpu0u = []
    gpu0m = []
    gpu1 = []
    gpu1u = []
    gpu1m = []
    gpu2 = []
    gpu2u = []
    gpu2m = []
    gpu3 = []
    gpu3u = []
    gpu3m = []
    times = []

    while True:
        gpu_ava = {}
        gpu_mem = {}
        gpu_use = {}
        gpu_msg = {}

        uuid_legal = []
        uuid_legal_set = []
        uuid_total = []
        uuid_to_index = {}
        index_to_uuid = {}
        time.sleep(0.3)
        if dictionary['running'] < 0:
            break
        time0 = time.time()
        time_use = DBTools.match_timestamp(time0,'ms')
        nvidia_smi = 'nvidia-smi'
        p = Popen([nvidia_smi, "--query-gpu=uuid,index,utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
                  stdout=PIPE)
        stdout, stderror = p.communicate()
        output = stdout.decode('UTF-8')
        lines = output.split(os.linesep)
        if (not lines[0]) or not lines:
            print("This machince do not have GPU!!!")
            break
        lines = lines[0:-1]
        num_gpu = len(lines)
        pp = Popen(["nvidia-smi", '--query-compute-apps=gpu_uuid,pid,process_name,used_memory',
                    '--format=csv,noheader,nounits'], stdout=PIPE)
        # print(lines)
        stdout2, stderror2 = pp.communicate()
        output2 = stdout2.decode('UTF-8')
        lines2 = output2.split(os.linesep)

        avail = num_gpu
        for i in range(num_gpu):
            raw_msg = lines[i]
            gpu_vals = raw_msg.split(', ')
            uuid_total.append(gpu_vals[0])
            uuid_to_index[gpu_vals[0]] = int(gpu_vals[1])
            index_to_uuid[int(gpu_vals[1])] = gpu_vals[0]
            gpu_msg[gpu_vals[0]] = {'id': int(gpu_vals[1]), 'gpuuti': float(gpu_vals[2]), 'gpumem': int(gpu_vals[3]),'pid':-1}
        if not lines2[0]:
            avail = num_gpu
        else:
            lines22 = lines2[0:-1]
            lk = len(lines22)
            for j in range(lk):
                proc_msg = lines22[j]
                proc_vals = proc_msg.split(', ')
                uuid_legal.append(proc_vals[0])
                gpu_msg[proc_vals[0]]['pid'] = int(proc_vals[1])

            uuid_legal_tmp = set(uuid_legal)
            uuid_legal_set = list(uuid_legal_tmp)
            using_gpu = len(uuid_legal_set)
            avail = num_gpu - using_gpu

        if gpu_type == 1:
            total.append(num_gpu)
            gavail.append(avail)
            gpu0.append(gpu_msg[index_to_uuid[0]]['pid'])
            gpu0u.append(gpu_msg[index_to_uuid[0]]['gpuuti'])
            gpu0m.append(gpu_msg[index_to_uuid[0]]['gpumem'])
            times.append(time_use)
            gpu1.append(gpu_msg[index_to_uuid[1]]['pid'])
            gpu1u.append(gpu_msg[index_to_uuid[1]]['gpuuti'])
            gpu1m.append(gpu_msg[index_to_uuid[1]]['gpumem'])
            gpu2.append(gpu_msg[index_to_uuid[2]]['pid'])
            gpu2u.append(gpu_msg[index_to_uuid[2]]['gpuuti'])
            gpu2m.append(gpu_msg[index_to_uuid[2]]['gpumem'])
            gpu3.append(gpu_msg[index_to_uuid[3]]['pid'])
            gpu3u.append(gpu_msg[index_to_uuid[3]]['gpuuti'])
            gpu3m.append(gpu_msg[index_to_uuid[3]]['gpumem'])
            gen_items = [
                {
                    'measurement': measure,
                    'tags':{
                        'node': int(node_index[measure])
                    },
                    'fields':{
                        'total':num_gpu,
                        'avail':avail,
                        'gpu0': gpu_msg[index_to_uuid[0]]['pid'],
                        'gpu0u': gpu_msg[index_to_uuid[0]]['gpuuti'],
                        'gpu0m': gpu_msg[index_to_uuid[0]]['gpumem'],
                        'gpu1': gpu_msg[index_to_uuid[1]]['pid'],
                        'gpu1u': gpu_msg[index_to_uuid[1]]['gpuuti'],
                        'gpu1m': gpu_msg[index_to_uuid[1]]['gpumem'],
                        'gpu2': gpu_msg[index_to_uuid[2]]['pid'],
                        'gpu2u': gpu_msg[index_to_uuid[2]]['gpuuti'],
                        'gpu2m': gpu_msg[index_to_uuid[2]]['gpumem'],
                        'gpu3': gpu_msg[index_to_uuid[3]]['pid'],
                        'gpu3u': gpu_msg[index_to_uuid[3]]['gpuuti'],
                        'gpu3m': gpu_msg[index_to_uuid[3]]['gpumem']
                    },
                    'time': time_use
                }
            ]
            if len(times)>=100:
                datas = {'time':times,'total':total,'avail':gavail,'gpu0':gpu0,'gpu0u':gpu0u,'gpu0m':gpu0m,'gpu1':gpu1,'gpu1u':gpu1u,'gpu1m':gpu1m,'gpu2':gpu2,'gpu2u':gpu2u,'gpu2m':gpu2m,'gpu3':gpu3,'gpu3u':gpu3u,'gpu3m':gpu3m}
                dataframe = pd.DataFrame(datas)
                dataframe.to_csv('/data/tfdata/nodedata/good1.csv', mode='a+', index=False, sep=',')
                total = []
                gavail = []
                gpu0 = []
                gpu0u = []
                gpu0m = []
                gpu1 = []
                gpu1u = []
                gpu1m = []
                gpu2 = []
                gpu2u = []
                gpu2m = []
                gpu3 = []
                gpu3u = []
                gpu3m = []
                times = []
        else:
            total.append(num_gpu)
            gavail.append(avail)
            gpu0.append(gpu_msg[index_to_uuid[0]]['pid'])
            gpu0u.append(gpu_msg[index_to_uuid[0]]['gpuuti'])
            gpu0m.append(gpu_msg[index_to_uuid[0]]['gpumem'])
            times.append(time_use)

            gen_items = [
                {
                    'measurement': measure,
                    'tags': {
                        'node': int(node_index[measure])
                    },
                    'fields': {
                        'total': num_gpu,
                        'avail': avail,
                        'gpu0': gpu_msg[index_to_uuid[0]]['pid'],
                        'gpu0u': gpu_msg[index_to_uuid[0]]['gpuuti'],
                        'gpu0m': gpu_msg[index_to_uuid[0]]['gpumem']
                    },
                    'time': time_use
                }
            ]
            if len(times) >= 100:
                datas = {'time': times, 'total': total, 'avail': gavail, 'gpu0': gpu0, 'gpu0u': gpu0u, 'gpu0m': gpu0m}
                dataframe = pd.DataFrame(datas)
                dataframe.to_csv('/data/tfdata/nodedata/normal1.csv', mode='a+', index=False, sep=',')
                total = []
                gavail = []
                gpu0 = []
                gpu0u = []
                gpu0m = []
                times = []
        influx_client.write_points(gen_items, time_precision="ms", database='NODEGPU')


    # measure_t = pre_list[0] + 'T' + pre_list[-1]

'''
 eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJteWFkbWluLXRva2VuLTdqcDl3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im15YWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI3MjhhMzdiOC1jNDA4LTExZWEtODc4My0wMDE2M2UwOWUzODMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06bXlhZG1pbiJ9.ftVVRAsCk7Od45U_C6yfTutRDPsese-JvSGWNgIYcMlxaPfSxKnr7MO1QIug1RG55ZjLhiMcwQPMV74Bw2at2AqKn_mbk_enkwIPm7bZzkL6KG5p_9EnkZRLrsOx0I3jEsGu9cqPRgsR3XIf7njFyGvUSnX6gp7PaGfkT52qnFQD6TRy3ugxvvBqlG0RIMqMuNy2E9GsT8PwuiPPL_oVe4TaQqX6GoyNgdjby8XiSwdpiBUotJlOa_xH_css5Rd3sANzi3-Vei1_qWBeWetrtEzjMkwQzjWEg9MVxh66gQiZySKtfx0hPnRDq9fwQ08MWP2A8vx_UQnJji6wnnSC6Q
'''
