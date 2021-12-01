from multiprocessing import Process
from flask import Blueprint, request

from controller import node_monitor
from util.Result import success
from util.MysqldbClass import *
from util.node_cpu_mem_monitor import node_cpu_mem_monitor
from util.node_gpu_monitor import node_gpu_monitor

monitor = Blueprint('monitor', __name__)


# @code.route('trainANDtestModel1', methods=['POST'])
# def trainANDtestModel1():
#     '''
#     :return:
#     '''
#     requestData = json.loads(request.get_data())
#     task=processPool.submit(trainANDtestModelthread1, requestData)
#     task.add_done_callback(processPool_callback)
#     return success(None)
#
# def trainANDtestModelthread1(requestData):
#     '''
#     :param requestData:
#     :return:
#     '''

@monitor.route('startMonitorNode', methods=['GET'])
def startMonitorNode():
    '''
    开启监控
    :return:
    '''
    if node_monitor['node_cpu_monitor_process'] == None and node_monitor['node_gpu_monitor_process'] == None:
        node_monitor['node_gpu_monitor_process'] = Process(target=node_cpu_mem_monitor)
        node_monitor['node_cpu_monitor_process'] = Process(target=node_gpu_monitor)
        # node_monitor['node_cpu_monitor_process'].daemon = True
        # node_monitor['node_gpu_monitor_process'].daemon = True
        node_monitor['node_cpu_monitor_process'].start()
        node_monitor['node_gpu_monitor_process'].start()
        return success(None)
    return success("监控已经运行")

@monitor.route('endMonitorNode', methods=['GET'])
def endMonitorNode():
    '''
    结束监控
    :return:
    '''
    if node_monitor['node_cpu_monitor_process'] != None and node_monitor['node_gpu_monitor_process'] != None:
        node_monitor['node_gpu_monitor_process'].terminate()
        node_monitor['node_cpu_monitor_process'].terminate()
        node_monitor['node_cpu_monitor_process'] = None
        node_monitor['node_gpu_monitor_process'] = None
        return success(None)
    return success("监控未在运行")


@monitor.route('ifMonitorNode', methods=['GET'])
def ifMonitorNode():
    '''
    结束监控
    :return:
    '''
    if node_monitor['node_cpu_monitor_process'] == None and node_monitor['node_gpu_monitor_process'] == None:
        return success("False")
    return success("True")

