
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
node_list = ['izbp10smzw7rg0ih27wbl3z','izbp11dpzwhp6pia1tyr3kz','izbp11ycujbqzxrpj66jksz','izbp156pkpio477f5f2tf6z','izbp156pkpio477f5f2tf8z']
node_index = {'Good1':1,'Good2':2,'Good3':3,'Norm1':4,'Norm2':5}
node_measure = {'izbp10smzw7rg0ih27wbl3z':'Good 1','izbp11dpzwhp6pia1tyr3kz':'Good 2','izbp11ycujbqzxrpj66jksz':'Good 3',
                'izbp156pkpio477f5f2tf6z':'Norm 1','izbp156pkpio477f5f2tf8z': 'Norm 2','izbp179ga4nl6y5b59bmphz': 'Master'}
node_name = {'izbp10smzw7rg0ih27wbl3z':'Good1','izbp11dpzwhp6pia1tyr3kz':'Good2','izbp11ycujbqzxrpj66jksz':'Good3',
                'izbp156pkpio477f5f2tf6z':'Norm1','izbp156pkpio477f5f2tf8z': 'Norm2','izbp179ga4nl6y5b59bmphz': 'Master'}
node_ip = {'izbp10smzw7rg0ih27wbl3z': '172.16.190.92','izbp11dpzwhp6pia1tyr3kz': '172.16.190.91','izbp11ycujbqzxrpj66jksz': '172.16.190.90',
           'izbp156pkpio477f5f2tf6z': '172.16.190.93','izbp156pkpio477f5f2tf8z': '172.16.190.96','izbp179ga4nl6y5b59bmphz': '172.16.190.97'}
MON_GPU_PORT = 14527

def control_mon(IP_AIM,measure,dictionary):
    global MON_GPU_PORT
    monitor_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (IP_AIM,MON_GPU_PORT)
    monitor_client.connect(ADDR)
    monitor_client.send(bytes(measure, 'utf-8'))
    connect_try = 5
    try_times = 1
    connected = False
    while True:
        if dictionary['mode'] == 0:
            time.sleep(1)
        elif dictionary['mode'] == 1:
            while True:
                if try_times > connect_try:
                    break
                msg_from_server = monitor_client.recv(4096)
                if not msg_from_server:
                    break
                msg_from_server_str = str(msg_from_server.decode('utf-8'))
                msg_from_server_list = msg_from_server_str.split(" ")
                if msg_from_server_list[0] == '400':
                    connected = True
                    break
                monitor_client.send(bytes(measure, 'utf-8'))
                try_times = try_times + 1
            if connected:
                time.sleep(1)
            else:
                monitor_client.close()
                print('controller break without connection!!!')
                return
        else:
            if connected:
                end_msg = 'end'
                monitor_client.send(bytes(end_msg, 'utf-8'))
                time.sleep(5)
                monitor_client.close()
                print('Quit the process successfully!!!')
                break
            else:
                monitor_client.close()
                break




if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=5)
    pool_size = 5
    connect_try = 5
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    dictionary['mode'] = 0

    while True:
        boots = input("Please Input 'start' to start:\n")
        if boots == 'start':
            dictionary['mode'] = 1
            for k in node_list:
                IP_A = node_ip[k]
                measure0 = node_measure[k]
                pool.apply_async(control_mon,(IP_A,measure0,dictionary))

        if boots == 'end':
            dictionary['mode'] = 2
            pool.close()
            pool.join()
            break

