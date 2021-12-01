import socket
import json
import ast
import time
# 本层为将flask的消息通过socket发送后接收解析并进一步发送至后端的函数
# aim
# - "start": 启动后端
        # message = {}即可，后续可以添加权限校验
# - "end": 结束后端
        # message = {}即可，后续可以添加权限校验
# - "submit": 发布,即job_config的相关参数: generate_job_config
# - "adjust": 调整:
# - "select": 查询
# - "delete": 删除任务
import os
def list_train_config_dir(base_path='/home/NFSshare/PROGECT/conf'):
    data_list = os.listdir(base_path)
    data_list = list(data_list)
    return data_list

def generate_job_config(image,training_config_file,priority=0,master_replicas=1,worker_replicas=1, cpu_allocate=-1,
                  mem_allocate=-1,backend="nccl",num_workers=1,
                  gpu_monitor_interval=15.0,
                  gpu_monitor_failure=15,
                  pin_memory=1): # 1 or 0,需要映射，输入bool值报错
    job_config = {"priority":priority,
                  "image_name":image,
                  "training_config_file":training_config_file,
                  "master_replicas":master_replicas,
                  "worker_replicas":worker_replicas,
                  "cpu_allocate":cpu_allocate,#core*1000
                  "mem_allocate":mem_allocate,#MB
                  "backend":backend,#nccl,gloo
                  "num_workers":num_workers,#2
                  "gpu_monitor_interval":gpu_monitor_interval,
                  "gpu_monitor_failure":gpu_monitor_failure,
                  "pin_memory":pin_memory
                  }
    return job_config
# # adjust_config: {"cpu_allocate":-1,"mem_allocate":-1,"master_relicas":1,"worker_replicas":1}
def generate_adjust_config(job_name,cpu_allocate=-1,mem_allocate=-1,master_relicas=1,worker_replicas=1):
    adjust_config = {
        "job_name":job_name,
        "cpu_allocate": cpu_allocate,
        "mem_allocate": mem_allocate,
        "master_replicas": master_relicas,
        "worker_replicas": worker_replicas
    }
    return adjust_config

def generate_select_config(level=0,job_name="null"):
    select_config = {"level":level,"job_name":job_name}
    # level 0 -> 某个任务的配置信息
    # level 1 -> 集群当前状态信息
    return select_config

def generate_delete_config(job_name):
    delete_config = {"job_name":job_name}
    return delete_config

def client_socket_function(SERVER_IP='172.16.20.190',SERVER_PORT=14527,message={},aim='start'):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_ADDR = (SERVER_IP,SERVER_PORT)
    client.connect(SERVER_ADDR)
    while True:
        client.send(bytes(aim, 'utf-8'))
        msg_from_server = client.recv(4096)
        msg_from_server_str = str(msg_from_server.decode('utf-8'))
        return_code = msg_from_server_str.split("@")[0]
        if int(return_code.strip()) == 200:
            break
        else:
            response = {}
            response['code'] = int(return_code.strip())
            response['reason'] = msg_from_server_str
            return response
    message['aim'] = aim
    out_data = json.dumps(message)
    client.send(bytes(out_data, 'utf-8'))
    succeed = False
    response = {}
    msg_from_server = client.recv(4096)
    msg_from_server_str = str(msg_from_server.decode('utf-8'))
    response = ast.literal_eval(msg_from_server_str)
    if int(response['code']) == 202:
        succeed = True
    response['success'] = succeed
    if "pin_memory" in response.keys():
        if response['pin_memory']:
            response['pin_memory'] = True
        else:
            response['pin_memory'] = False
    return response
if __name__ == '__main__':
    # message = generate_job_config(image="172.16.20.190:5000/wenet-k8s-torch:8.2",training_config_file="train_conformer.yaml")
    #response = client_socket_function(message={"image_name":"172.16.20.190:5000/wenet-k8s-torch:8.2",
    #               "training_config_file":"train_conformer.yaml"}, aim="submit")
    #print(response)
    #message = generate_adjust_config("exp-36",-1,-1,1,2)
    #response = client_socket_function(message=message,aim="adjust")
    #print(response)
    # time.sleep(30)
    # message = generate_select_config(level=0,job_name="exp-6")
    # response = client_socket_function(message=message,aim="select")
    # print(response)
    # time.sleep(30)
    message = generate_delete_config(job_name="exp-35")
    response = client_socket_function(message=message, aim="delete")
    print(message)
# if __name__ == '__main__':
#     k = generate_adjust_config("kk")
#     print(k.keys())
#     k = generate_job_config("kk","kk2")
#     print(k.keys())
#     k = generate_delete_config("kk")
#     print(k.keys())
#     k = generate_select_config(0,"kk")
#     print(k.keys())
#     print((json.dumps(k)))
#     # ['cpu_allocate']
#     print(ast.literal_eval(json.dumps(k)))
