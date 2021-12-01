import os

from flask import Blueprint, request
import socket
import json
import ast

from werkzeug.utils import secure_filename

from entity.nodeMessage import task_severIp, task_severPort
from util.Result import success, error
from pypinyin import lazy_pinyin

from util.randomFilename import random_filename

task = Blueprint('task', __name__)

def client_socket_function(message={},aim='start'):
    SERVER_IP = task_severIp
    SERVER_PORT=task_severPort
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_ADDR = (SERVER_IP,SERVER_PORT)
    client.connect(SERVER_ADDR)
    response = {}
    while True:
        client.send(bytes(aim, 'utf-8'))
        msg_from_server = client.recv(4096)
        msg_from_server_str = str(msg_from_server.decode('utf-8'))
        return_code = msg_from_server_str.split("@")[0]
        if int(return_code.strip()) == 200:
            break
        else:
            response['code'] = int(return_code.strip())
            response['reason'] = msg_from_server_str
            return response
    message['aim'] = aim
    out_data = json.dumps(message)
    client.send(bytes(out_data, 'utf-8'))
    succeed = False
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


def list_train_config_dir(base_path='/home/NFSshare/PROGECT/conf'):
    data_list = os.listdir(base_path)
    data_list = list(data_list)
    return data_list

@task.route('upload_train_config', methods=['POST'])
def upload_train_config():#上传yaml文件
    base_path = '/home/NFSshare/PROGECT/conf'
    f = request.files['file']
    if f.filename not  in os.listdir(base_path):
        upload_path = os.path.join(base_path, f.filename)
        f.save(upload_path)
        return success(None)
    else:
        return error("存在相同命名的文件")


@task.route('delete_train_config', methods=['DELETE'])
def delete_train_config():#删除yaml文件
    base_path = '/home/NFSshare/PROGECT/conf'
    config_file_name = request.args.get('config_file_name')
    try :
        c_path = os.path.join(base_path, config_file_name)
        os.remove(c_path)
        return success(None)
    except:
        return error("删除失败")

@task.route('submit', methods=['POST'])
def submit():
    '''
    :return:
    '''
    requestData = json.loads(request.get_data())
    response = client_socket_function(requestData,"submit")
    return success(response)

@task.route('adjust', methods=['POST'])
def adjust():
    '''
    :return:
    '''
    requestData = json.loads(request.get_data())
    response = client_socket_function(requestData, "adjust")
    return success(response)

@task.route('getTaskList', methods=['GET'])
def selectAll():
    '''
    :return:
    '''
    select_config = {"level": 1}
    response = client_socket_function(select_config, "select")
    return success(response)


@task.route('delete', methods=['POST'])
def delete():
    '''
    :return:
    '''
    requestData = json.loads(request.get_data())
    response = client_socket_function(requestData, "delete")
    return success(response)

@task.route('getTrainConfigList', methods=['GET'])
def getTrainConfigList():
    '''
    :return:
    '''
    data=list_train_config_dir()
    return success(data)

@task.route('selectOne', methods=['GET'])
def selectOne():
    '''
    :return:
    '''
    job_name = request.args.get('job_name')
    select_config = {"level": 0,"job_name":job_name}
    response = client_socket_function(select_config, "select")
    return success(response)
