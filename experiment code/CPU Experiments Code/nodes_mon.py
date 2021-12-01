import kubernetes
import requests
from multiprocessing import Process
import multiprocessing
import urllib
import urllib3
import time
import os
import pandas as pd
import argparse
aToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLTJ3dGRuIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI5YWE4ZTc4OS0zODM1LTExZWEtYWZlMi1mYTE2M2UzMzBlYWEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.qzHVo1KysWhnSAMwKAcaKLWkqOxBlSBr7qR4LtldusdM0Z9dDQVH2TMmtvmkBDyfqVKQttMmTGXDHhW-dOD9uJVn8w84zitd7eAgVCrHm2nhTMbsf2ZKH0DuU6t_SGYkyBWVIedMpZis-K2mzCjmSq5TAd67cMSCqGHQVMtjEsqpPyBeY_nrqgzWWwX3X3E0hHGk7CvICndFiqUeI9xKVluA-TdR6HzPXbaCIGAcvSHeIlc4GdhmDTJ47U4rQON3IL0dhC6Adom7c65I5pwBdYpfqkDhKld1o7ErhXS8Qhcv0BHhfuj-Bdn6MMsH7PXpH-7I5dxoKDVlTC-q7KV9EQ'
#verify=False

def parse():
    parser = argparse.ArgumentParser(description="Node Monitor")
    parser.add_argument('--save_path', default='/tfdata/nodedata', help='save path')
    # parser.add_argument('--train_pg', action='store_true', help='whether train policy gradient')
    # parser.add_argument('--train_dqn', action='store_true', help='whether train DQN')
    # parser.add_argument('--test_pg', action='store_true', help='whether test policy gradient')
    # parser.add_argument('--test_dqn', action='store_true', help='whether test DQN')

    args = parser.parse_args()
    return args

def update_token():
    cacheData = os.popen("echo $(kubectl describe secret $(kubectl get secret -n kube-system | grep ^admin-user | awk '{print $1}') -n kube-system | grep -E '^token'| awk '{print $2}')").read()
    cacheToken = cacheData[:-1]
    newToken = str(cacheToken)

    return newToken

def make_headers(Token):
    text = 'Bearer '+Token
    headers = {'Authorization': text}
    return headers

def catch_message(url):
    global aToken

    aToken = update_token()
    headers = make_headers(aToken)

    response = requests.get(url,headers=headers,verify=False)
    res_json = response.json()

    return res_json

# def create_database()

class Node_mess(multiprocessing.Process):
    def __init__(self,url,derivation,args):
        multiprocessing.Process.__init__(self)
        self.url = url
        self.time_mess = {}
        self.derivation = derivation
        self.arg = args
        self.save_path = args.save_path
        if not os.path.exists(self.arg.save_path):
            os.makedirs(self.arg.save_path)
    def run(self):
        print(multiprocessing.current_process().pid)
        print(os.getpid())
        response = catch_message(self.url)
        self.time_mess['creation'] = [response['items'][0]['metadata']['creationTimestamp']]
        for item in response['items']:
            self.time_mess[item['metadata']['name']] = [item['timestamp']]

        time.sleep(self.derivation)
        while True:
            response = catch_message(self.url)
            self.time_mess['creation'].append(response['items'][0]['metadata']['creationTimestamp'])
            for item in response['items']:
                self.time_mess[item['metadata']['name']].append(item['timestamp'])
            if len(self.time_mess['creation'])%100==0 and len(self.time_mess['creation']) > 0:
                data_frame = pd.DataFrame(self.time_mess)
                data_frame.to_csv(self.save_path + '/' + 'struct.csv', mode='a+', index=False, sep=',')
                for key in self.time_mess:
                    self.time_mess[key] = []
            time.sleep(self.derivation)





# def node_message(url):
#     response = catch_message(url)

if __name__ == '__main__':
    '''
    json结构数据如下：
    {'kind': 'NodeMetricsList', 'apiVersion': 'metrics.k8s.io/v1beta1',
     'metadata': {'selfLink': '/apis/metrics.k8s.io/v1beta1/nodes'}, 
     'items': [
        {'metadata': {'name': 'k8s-master', 'selfLink': '/apis/metrics.k8s.io/v1beta1/nodes/k8s-master', 
            'creationTimestamp': '2020-01-19T07:53:49Z'}, 
        'timestamp': '2020-01-19T07:53:46Z', 'window': '30s', 
        'usage': {'cpu': '550839278n', 'memory': '5235160Ki'}
        }, 
        {'metadata': {'name': 'k8s-worker0', 'selfLink': '/apis/metrics.k8s.io/v1beta1/nodes/k8s-worker0', 
        'creationTimestamp': '2020-01-19T07:53:49Z'}, 
        'timestamp': '2020-01-19T07:53:38Z', 'window': '30s', 
        'usage': {'cpu': '313078381n', 'memory': '5200776Ki'}}, 
    '''
    url = 'https://192.168.128.10:6443/apis/metrics.k8s.io/v1beta1/nodes'
    args = parse()
    node_p = Node_mess(url=url,derivation=4,args=args)
    node_p.daemon = True
    k1 = os.getpid()
    k2 = multiprocessing.current_process().pid
    print(k1,k2)
    while True:
        ans = input("Please input to start")

        if ans == 'start':
            node_p.start()
        if ans == 'end':
            break

    # a = {}
    # a['master'] = list()
    # a['master'].append(1)
    # print(type(a))
    # print(type(a['master']))
    # print(a)
    # a['worker'] = list()
    # a['worker'].append(2)
    # for key in a:
    #     print(key)



    #查看类型：type(r.json())

    # creation = []
    # master = []
    # worker0 = []
    # worker1 = []
    # worker2 = []

    # while(True)

