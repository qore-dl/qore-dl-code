import json
import numpy as np
import os
import time
import paramiko

from entity.nodeMessage import *
from util import influx_client, DBTools


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


gap_time=30
database="project"
def node_gpu_monitor():
    if not os.path.exists("/home/NFSshare/PROGECT"):
        os.makedirs("/home/NFSshare/PROGECT", exist_ok=True)
    if not os.path.exists("/home/NFSshare/PROGECT/global_uuid.json"):
        global_uuid = {}
    else:
        global_uuid = load_config("/home/NFSshare/PROGECT/global_uuid.json")
    connection = {}  # SSH连接，与其他各节点。节点信息在entity.nodeMessage中

    for node in node_name.keys():#建立连接并保存
        coon = paramiko.SSHClient()
        coon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        coon.load_system_host_keys()
        coon.connect(node_ip[node], username=node_username, password=node_password)
        connection[node]=coon

    for node in node_name.keys():
        if node not in global_uuid.keys():
            global_uuid[node] = {}

        stdin, stdout, stderr = connection[node].exec_command(
            "nvidia-smi --query-gpu=uuid,index,utilization.gpu,memory.total --format=csv,noheader,nounits")
        output = stdout.read().decode().strip()
        lines = output.split("\n")
        # print(lines)

        if (not lines[0]) or not lines:
            print("This machince do not have GPU!!!")
            global_uuid.pop(node)
            continue
            # break
        num_of_gpu = len(lines)

        for gp in range(num_of_gpu):
            gpu_static = lines[gp].split(", ")
            if gpu_static[0] not in global_uuid[node].keys():
                global_uuid[node][gpu_static[0]] = {"id":int(gpu_static[1]),"capacity":int(gpu_static[-1])}

    # print(global_uuid)
    save_config(global_uuid,"/home/NFSshare/PROGECT/global_uuid.json")

    while True:


        time0 = time.time()
        time_use = DBTools.match_timestamp(time0,'s')
        for node in global_uuid.keys():
            gpu_msg = {}
            gpu_id_list = list(global_uuid[node].keys())
            stdin, stdout, stderr = connection[node].exec_command(
                "nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader,nounits")
            output = stdout.read().decode().strip()

            lines = output.split("\n")
            stdin2, stdout2, stderr2 = connection[node].exec_command(
                "nvidia-smi --query-gpu=uuid,utilization.gpu --format=csv,noheader,nounits")
            output2 = stdout2.read().decode().strip()

            lines2 = output2.split("\n")
            # print(lines)
            # print(lines2)
            now_gpu_set = list(set([line.split(", ")[0].strip() for line in lines2]))
            global_gpu_set = list(set(global_uuid[node].keys()))
            if not (now_gpu_set == global_gpu_set):
            # for node in node_name.keys():
                if node not in global_uuid.keys():
                    global_uuid[node] = {}
                stdin, stdout, stderr = connection[node].exec_command(
                    "nvidia-smi --query-gpu=uuid,index,utilization.gpu,memory.total --format=csv,noheader,nounits")
                output = stdout.read().decode().strip()
                lines = output.split("\n")
                # print(lines)
                if (not lines[0]) or not lines:
                    print("This machince do not have GPU!!!")
                    global_uuid.pop(node)
                    continue
                    # break
                # lines = lines[0:-1]
                # num_gpu = len(lines)
                num_of_gpu = len(lines)
                for gp in range(num_of_gpu):
                    gpu_static = lines[gp].split(", ")
                    if gpu_static[0] not in global_uuid[node].keys():
                        global_uuid[node][gpu_static[0]] = {"id": int(gpu_static[1]), "capacity": int(gpu_static[-1])}
            # print(global_uuid)
                save_config(global_uuid,"/home/NFSshare/PROGECT/global_uuid.json")
            gen_items = [
                {
                    'measurement': node_name[node],
                    'tags': {
                        'node_name': node_name[node]
                    },
                    'fields': {
                        'total': len(gpu_id_list)
                    },
                    'time': time_use
                }
            ]
            for item in lines2:
                item_split = item.split(", ")
                gen_items[0]['fields'][('gpu%d' % global_uuid[node][item_split[0]]['id']) + '_u'] = float("%.1f" % float(item_split[1]))/100
                gen_items[0]['fields']['gpu%d' % global_uuid[node][item_split[0]]['id']] = "-1"
                gen_items[0]['fields'][('gpu%d' % global_uuid[node][item_split[0]]['id']) + '_m'] = float("%.1f" % (0.0))
                gen_items[0]['fields'][('gpu%d' % global_uuid[node][item_split[0]]['id']) + '_mp'] = float("%.1f" % (0.0))
                #     ['GPU-75b9e402-8887-724e-f48d-78589f5626c8, 44910, python, 1193', 'GPU-75b9e402-8887-724e-f48d-78589f5626c8, 46456, python, 1193', 'GPU-75b9e402-8887-724e-f48d-78589f5626c8, 50391, python, 8167', 'GPU-fe5dad5c-01e2-ba1f-8ffc-01b605814ee4, 44912, python, 1193', 'GPU-48f9c670-995d-0d7d-0386-3d0fa3f20a70, 44911, python, 1193', 'GPU-51b1703f-23c7-12d4-4630-c62ed7da0c4c, 44913, python, 1193', 'GPU-51b1703f-23c7-12d4-4630-c62ed7da0c4c, 50394, python, 11779', 'GPU-46fe70bc-f986-2546-9516-3e93422ba697, 44914, python, 1193', 'GPU-46fe70bc-f986-2546-9516-3e93422ba697, 46459, python, 1193', 'GPU-46fe70bc-f986-2546-9516-3e93422ba697, 50393, python, 8327', 'GPU-e68730e7-3e85-958b-e888-00971ef5e81c, 44915, python, 1193', 'GPU-e68730e7-3e85-958b-e888-00971ef5e81c, 50396, python, 8071']
            # for uuid in gpu_id_list:

            if not lines[0] or not lines:
                avial = len(gpu_id_list)
                uuid_legal_set = []
                gen_items[0]['fields']['avail'] = avial
            else:
                uuid_legal_set = list(set([item.split(", ")[0].strip() for item in lines]))
                avial = len(gpu_id_list) - len(uuid_legal_set)
                gen_items[0]['fields']['avail'] = avial
                # gen_items[0]['fields']

                for uuid in gpu_id_list:
                    gpu_msg[uuid] = {"pid":[],"memory":[]}
                    # gen_items[0]['fields']
                for item in lines:
                    item_split = item.split(", ")
                    gpu_msg[item_split[0].strip()]['pid'].append(int(item_split[1].strip()))
                    gpu_msg[item_split[0].strip()]['memory'].append(int(item_split[-1].strip()))
                for use_id in gpu_msg.keys():
                    pids = ""
                    if len(gpu_msg[use_id]['pid']) <= 0:
                        pids = "-1"
                    else:
                        if len(gpu_msg[use_id]['pid']) > 1:
                            gpu_msg[use_id]['pid'].sort()
                            for k in range(len(gpu_msg[use_id]['pid']) - 1):
                                pids += str(gpu_msg[use_id]['pid'][k]) + ";"
                        pids += str(gpu_msg[use_id]['pid'][-1])
                    gen_items[0]['fields']['gpu%d' % global_uuid[node][use_id]['id']] = pids
                    # gen_items[0]['fields'][('gpu%d' % global_uuid[node][use_id]['id']) + 'u'] = 0
                    gen_items[0]['fields'][('gpu%d' % global_uuid[node][use_id]['id']) + '_m'] = float("%.1f" % float(np.sum(gpu_msg[use_id]['memory'])))
                    gen_items[0]['fields'][('gpu%d' % global_uuid[node][use_id]['id']) + '_mp'] = float("%.1f" % gen_items[0]['fields'][('gpu%d' % global_uuid[node][use_id]['id']) + '_m'])/ float(global_uuid[node][use_id]['capacity'])
                # for item in lines:
            # print(avial)
            # print(gen_items)
            influx_client.write_points(gen_items, time_precision="s", database=database)
        time.sleep(gap_time)  # sampling rate