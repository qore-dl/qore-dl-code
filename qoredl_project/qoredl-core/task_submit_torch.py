#https://blog.csdn.net/orangefly0214/article/details/81387077

from wenet_template import TorchTemplate
import numpy as np
# https://blog.csdn.net/u013812710/article/details/72886491
# https://blog.csdn.net/ismr_m/article/details/53100896
#https://blog.csdn.net/bcfdsagbfcisbg/article/details/78134172
import kubernetes
import os
import json
import influxdb
import time
import re

import yaml

def load_config(config_file):
    f = open(config_file,encoding='utf-8')
    res = f.read()
    config_content = json.loads(res)
    f.close()
    return config_content

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

def deletehelp(delete_job_name,v1):
    try:
        v1.delete_namespace(delete_job_name)
    except Exception as eeeeee:
        print(eeeeee)
        if not os.path.exists("/home/NFSshare/PROGECT/deletebuf"):
            os.makedirs("/home/NFSshare/PROGECT/deletebuf",exist_ok=True)
        command0 = "kubectl get namespace " + delete_job_name + " -o json > /home/NFSshare/PROGECT/deletebuf/" + delete_job_name + ".json"
        os.system(command0)
        tmp = load_config("/home/NFSshare/PROGECT/deletebuf" + delete_job_name + ".json")
        tmp["spec"]["finalizers"] = []
        save_config(tmp, "/home/NFSshare/PROGECT/deletebuf" + delete_job_name + ".json")
        try:
            command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/home/NFSshare/PROGECT/deletebuf' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/'+delete_job_name+'/finalize'
            os.system(command1)
        except Exception as helpe:
            print(helpe)
            commandopen = 'kubectl proxy --port=8081'
            os.system(commandopen)
            os.system(command1)

def deletehelp2(delete_job_name,v1):
    v1.delete_namespace(delete_job_name)
    time.sleep(5.5)
    command0 = "kubectl get namespace " + delete_job_name + " -o json > /home/NFSshare/PROGECT/deletebuf/" + delete_job_name + ".json"
    # response = os.system('kubectl apply -f ' + job_file)
    response = os.system(command0)
    if response == 0 and os.path.exists("/home/NFSshare/PROGECT/deletebuf/" + delete_job_name + ".json"):
        tmp = load_config("/home/NFSshare/PROGECT/deletebuf/" + delete_job_name + ".json")
        tmp["spec"]["finalizers"] = []
        save_config(tmp, "/home/NFSshare/PROGECT/deletebuf/" + delete_job_name + ".json")
        response2 = 0
        command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/home/NFSshare/PROGECT/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
        try:
            response2 = os.system(command1)
            if response2 != 0:
                commandopen = 'kubectl proxy --port=8081'
                os.system(commandopen)
        except Exception as helpe:
            print(helpe)
            # os.system(command1)
            response2 = os.system(command1)
            if response2 != 0:
                commandopen = 'kubectl proxy --port=8081'
                os.system(commandopen)

def check_path(name):
    train_dir = os.path.join('/home/NFSshare/wenetdata', name)
    print(train_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir,exist_ok=True)
        # os.system("chomod -R 777 %s" % train_dir)
    return train_dir

def save_job_change_layout(job_name,master_n,worker_n):
    # train_dir = os.path.join('/home/NFSshare/expjob/config', job_name)
    save_dir = '/home/NFSshare/expjob/config'
    save_job_path = '%s/%s.json' % (save_dir, job_name)
    job_config = load_config(save_job_path)
    # 'ps_replicas': job.ps_replicas,'worker_replicas': job.worker_replicas
    job_config['master_replicas'] = master_n
    job_config['worker_replicas'] = worker_n
    save_config(job_config, save_job_path)

# % (job_name, job_name)
#     history_filename = "%s/logs/%s-%d.json" % (save_path, job_config["template_name"], task_id)

def save_job_change_resource(job_name,cpu_allocate,mem_allocate):
    # save_dir = os.path.join('/home/NFSshare/expjob/config', job_name)
    save_dir = '/home/NFSshare/expjob/config'
    save_res_path = "%s/%s.json" % (save_dir,job_name)
    job_res_config = load_config(save_res_path)
    # cpu_allocate=-1,mem_allocate=-1,
    job_res_config['cpu_allocate'] = cpu_allocate
    job_res_config['cpu_allocate'] = mem_allocate
    # job_res_config['gpu'] = gpu_limit
    save_config(job_res_config, save_res_path)

def save_job_change_status(job_name,status):
    # save_dir = os.path.join('/home/NFSshare/expjob/config', job_name)
    save_dir = '/home/NFSshare/expjob/config'
    save_res_path = "%s/%s.json" % (save_dir, job_name)
    job_res_config = load_config(save_res_path)
    # cpu_allocate=-1,mem_allocate=-1,
    job_res_config['status'] = status
    # job_res_config['gpu'] = gpu_limit
    save_config(job_res_config, save_res_path)

def save_job_change_replicas(job_name,master_replicas,worker_replicas):
    # "master_replicas":1,
    # "worker_replicas":1,
    # save_dir = os.path.join('/home/NFSshare/expjob/config', job_name)
    save_dir = '/home/NFSshare/expjob/config'
    save_res_path = "%s/%s.json" % (save_dir, job_name)
    job_res_config = load_config(save_res_path)
    # cpu_allocate=-1,mem_allocate=-1,
    job_res_config['master_replicas'] = master_replicas
    job_res_config['worker_replicas'] = worker_replicas
    # job_res_config['gpu'] = gpu_limit
    save_config(job_res_config, save_res_path)



def check_ns(name):
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # v1.create_namespace()
    exist_ns = v1.list_namespace()
    exist_ns_name = []
    for i in exist_ns.items:
        exist_ns_name.append(i.metadata.name)
    if name in exist_ns_name:
        return True
    else:
        return False

# class clusternode():
#     def __init__(self,name,total_cpu,total_memory,compute_label,disk_label):
#         self.total_cpu = total_cpu
#         self.total_memory = total_memory
#         self.compute_label = compute_label
#         self.disk_label = disk_label
#         self.name = name

class ClusterAgent():
    def __init__(self,node_message_path,gpu_message_path):
        # self.time_base
        self.total_cpu = 0
        self.total_gpu = 0
        self.total_memory = 0
        self.total_used_cpu = 0
        self.total_used_memory = 0
        self.total_used_gpu = 0
        self.node_mess = load_config(node_message_path)
        self.node_mess_path = node_message_path
        self.node_resource = {}
        self.gpu_message = load_config(gpu_message_path)
        kubernetes.config.load_kube_config()
        self.v1 = kubernetes.client.CoreV1Api()
        self.nodes = list(self.node_mess['node'].keys())
        self.node_to_id = {}
        self.id_to_node = {}

        for n in self.nodes:
            self.node_to_id[n] = "NODE%d" % self.node_mess['node'][n]
            self.id_to_node["NODE%d" % self.node_mess['node'][n]] = n
        self.gpu_clinet = influxdb.InfluxDBClient(host='172.16.20.190',port=8086,username='voicecomm',password='voicecomm',database="project")
        self.cpu_client = influxdb.InfluxDBClient(host='172.16.20.190',port=8086,username='voicecomm',password='voicecomm',database="project")

    def get_ns(self):
        ns_list = [i.metadata.name for i in self.v1.list_namespace().items]
        return ns_list

    def update_node(self,mode=0,node_update=False,window_size=1):
        if node_update:
            self.node_mess = load_config(self.node_mess_path)
            self.nodes = list(self.node_mess['node'].keys())
            self.node_to_id = {}
            self.id_to_node = {}
            for n in self.nodes:
                self.node_to_id[n] = "NODE%d" % self.node_mess['node'][n]
                self.id_to_node["NODE%d" % self.node_mess['node'][n]] = n
        cpu_total = {}
        items = self.v1.list_node().items
        for node_item in items:
            if node_item.metadata.name not in self.nodes:
                continue
            cpu_total[self.node_to_id[node_item.metadata.name]] = {}
            cpu_total[self.node_to_id[node_item.metadata.name]]['cpu_capacity'] = float(int(node_item.status.allocatable['cpu']) * 1e3)
            cpu_total[self.node_to_id[node_item.metadata.name]]['memory_capacity'] = float(node_item.status.allocatable['memory'][:-2]) / 1024

        if mode == 0:
            # 扩展动态发现节点功能，下一阶段实现
            cpu_node_result = self.cpu_client.query(
                "select * from " + "CPUANDMEM" + " group by node_name order by desc limit %d" % window_size)
            cpu_node_result_keys = list(cpu_node_result.keys())
            cpu_results = {}
            for key in cpu_node_result_keys:
                cpu_result_point = list(cpu_node_result[key])
                cpu_results[key[1]['node_name']] = {'cpu':cpu_result_point[0]['cpu'],'memory':cpu_result_point[0]['memory'],"cpu_percent":cpu_result_point[0]['cpu_percent'],"memory_percent":cpu_result_point[0]["memory_percent"]}
                cpu_results[key[1]['node_name']]['cpu_capacity'] = cpu_total[key[1]['node_name']]['cpu_capacity']
                cpu_results[key[1]['node_name']]['memory_capacity'] = cpu_total[key[1]['node_name']]['memory_capacity']
                tmp_cpu_window = [cpu_result_j['cpu'] for cpu_result_j in cpu_result_point]
                tmp_memory_window = [cpu_result_j['memory'] for cpu_result_j in cpu_result_point]
                tmp_cpu_uti_window = [cpu_result_j['cpu_percent'] for cpu_result_j in cpu_result_point]
                tmp_memory_uti_window = [cpu_result_j['memory_percent'] for cpu_result_j in cpu_result_point]
                cpu_results[key[1]['node_name']]['avg_cpu'] = np.mean(tmp_cpu_window)
                cpu_results[key[1]['node_name']]['avg_memory'] = np.mean(tmp_memory_window)
                cpu_results[key[1]['node_name']]['avg_cpu_percent'] = np.mean(tmp_cpu_uti_window)
                cpu_results[key[1]['node_name']]['avg_memory_percent'] = np.mean(tmp_memory_uti_window)

            for node in self.nodes:
                # "NODE%d" % self.node_mess['node'][node]
                try:
                    node_measure = self.node_to_id[node]
                except Exception as e:
                    print("not found %s as %s" % (node,self.node_to_id[node]))
                    continue
                if self.node_to_id[node] not in self.node_resource.keys():
                    self.node_resource[self.node_to_id[node]] = {}
                node_gpu = self.gpu_clinet.query("select total,avail from " + node_measure + " group by node_name order by desc limit 1")
                node_gpu_res_keys = list(node_gpu.keys())
                node_gpu_mg = list(node_gpu[node_gpu_res_keys[-1]])
                self.node_resource[self.node_to_id[node]]['total'] = int(node_gpu_mg[0]['total'])
                self.node_resource[self.node_to_id[node]]['avail'] = int(node_gpu_mg[0]['avail'])
                self.total_gpu += self.node_resource[self.node_to_id[node]]['total']
                self.total_used_gpu = (self.node_resource[self.node_to_id[node]]['total'] - self.node_resource[self.node_to_id[node]]['avail'])
                for cpu_feature in cpu_results[self.node_to_id[node]].keys():
                    self.node_resource[self.node_to_id[node]][cpu_feature] = float(cpu_results[self.node_to_id[node]][cpu_feature])
                self.total_cpu += (self.node_resource[self.node_to_id[node]]['cpu_capacity'])
                self.total_memory += self.node_resource[self.node_to_id[node]]['memory_capacity']
                self.total_used_cpu += (self.node_resource[self.node_to_id[node]]['cpu'])
                self.total_used_memory += self.node_resource[self.node_to_id[node]]['memory']
                # if node not in self.node_mess.keys()
            # self.nodes = list(self.node_resource.keys())

        # for node_item in items:
        #     se[node_item.metadata.name] = float(int(node_item.status.allocatable['cpu']) * 1e3)
        #     tmp_node_mem[node_item.metadata.name] = float(node_item.status.allocatable['memory'][:-2]) / 1024
# 任务状态 status：发布时为iniital; 调度时为scheduling; 已完成调度为scheduled;调整时为adjusting;运行时根据情况获取；结束时为finished
#               command: ["python","train.py","--config","/home/NFSshare/PROGECT/conf/train_conformer.yaml","--train_data","raw_wav/train/format.data","--cv_data","raw_wav/dev/format.data","--model_dir","exp/conformer","--gpu","0","--ddp.dist_backend","nccl","--num_workers","2","--cmvn","exp/conformer/global_cmvn","--interval","30.0","--failure","15","--database","MONITOR","--dbhost","172.16.20.190","--task_id","1","--template","EXP","--pin_memory"]
class SubTask():
    def __init__(self,priority=0,retry=0,image_name='172.16.20.190:5000/wenet-k8s-torch:8.2',template_name="EXP",training_config_file="train_conformer.yaml",model_dir="exp/model",task_id=1,master_replicas=1,
                 worker_replicas=1,cpu_allocate=-1,mem_allocate=-1,deadline=-1,starttime=-1,train_data_file="raw_wav/train/format.data",cv_data_file="raw_wav/dev/format.data",
                 gpu=0,backend="nccl",num_workers=2,cmvn="global_cmvn",gpu_monitor_interval=30.0,gpu_monitor_failure=15,gpu_monitor_database="podGpu",gpu_monitor_database_server="172.16.20.190",pin_memory=True,node_message_path="/home/NFSshare/PROGECT/global_node.json",gpu_message_path="/home/NFSshare/PROGECT/global_uuid.json",
                 raw_data_path="asr-data",project_config_path="PROGECT",container_work_dir="/var/wenet/examples/aishell/s0",status="initial",run_dir="/var/wenet/examples/aishell/s0/exp/model"):
        self.raw_data_path = raw_data_path
        self.project_config_path = project_config_path
        self.container_work_dir = container_work_dir
        self.template_name = template_name
        self.image = image_name
        self.master_replicas = master_replicas
        self.worker_replicas = worker_replicas
        self.gpu_monitor_interval = gpu_monitor_interval
        self.priority = priority
        self.task_id = task_id
        self.model_dir = model_dir
        self.train_data_file = train_data_file
        self.cv_data_file = cv_data_file
        self.gpu_monitor_failure = gpu_monitor_failure
        self.gpu_monitor_database = gpu_monitor_database
        self.gpuid = gpu
        self.status = status
        self.name = "%s-%d" % (self.template_name,self.task_id)
        # "exp/conformer/global_cmvn"
        self.cmvn = "exp/conformer/%s" % cmvn
        self.template = TorchTemplate.TASK
        self.backend = backend
        self.command = ['python', 'train.py']
        self.pin_memory = pin_memory
        self.num_workers = num_workers
        self.training_config = training_config_file
        self.cluster_agent = ClusterAgent(node_message_path,gpu_message_path)
        self.dbhost = gpu_monitor_database_server
        self.retry = retry
        self.node_affinity = {}
        self.cluster_agent.v1.list_namespace()
        self.influx_client = influxdb.InfluxDBClient(host='192.168.128.10',port=8086,username='admin',password='admin',database="NODEMESSAGE")
        self.node_list = ['k8s-master','k8s-worker0','k8s-worker2','k8sworker1','k8s-worker3','k8s-worker4','k8s-worker5']

        self.cluster_agent.update_node(mode=0,node_update=True)
        self.sa_dir = '/home/NFSshare/expjob/sa/'
        self.bind_dir = '/home/NFSshare/expjob/bind/'
        self.job_dir = '/home/NFSshare/expjob/job/'

        self.cpu_allocate = cpu_allocate
        self.memory_allocate = mem_allocate
        self.deadline = deadline
        self.starttime = starttime
        self.run_dir = run_dir
        # '--retry=' + str(self.retry),
        # ['python', 'train.py', '--config', '/home/NFSshare/PROGECT/conf/train_conformer.yaml', '--train_data', 'raw_wav/train/format.data', '--cv_data', 'raw_wav/dev/format.data', '--model_dir', 'exp/conformer', '--gpu', '0', '--ddp.dist_backend', 'nccl', '--num_workers', '2', '--cmvn', 'exp/conformer/global_cmvn', '--interval', '30.0', '--failure', '15',
        # '--database', 'MONITOR', '--dbhost', '172.16.20.190', '--task_id', '1', '--template', 'EXP', '--pin_memory']
        nowtemplate = self.template_name.upper()
        self.args = ['--config','/home/NFSshare/PROGECT/conf/%s' % self.training_config,
                     '--train_data',self.train_data_file,'--cv_data',self.cv_data_file,
                     '--model_dir',self.model_dir,'--gpu',self.gpuid,'--ddp.dist_backend',self.backend,
                     '--num_workers',self.num_workers,'--cmvn',self.cmvn,'--interval',self.gpu_monitor_interval,
                     '--failure',self.gpu_monitor_failure,'--database',self.gpu_monitor_database,
                     '--dbhost=' + self.dbhost,'--task_id',self.task_id,
                     '--template',nowtemplate
                     ]
    #     '--update_delay=' + str(self.update_delay)
        if self.pin_memory:
            self.args.append("--pin_memory")

    def save_job_logs(self,action, save_path="/home/NFSshare/expjob"):
        log_file = "%s/logs/%s.json" % (save_path, self.name)
        job_log = load_config(log_file)
        now_time = time.time()
        job_log[now_time] = {}
        job_log[now_time]['status'] = self.status
        job_log[now_time]['action'] = action

    def set_deadline(self,start_time,deadline=-1):
        self.deadline = deadline
        self.starttime = start_time

    def set_resource(self,cpu_source=-1,mem_source=-1):
        self.cpu_allocate = cpu_source
        self.memory_allocate = mem_source
    # ['python', 'train.py', '--config', '/home/NFSshare/PROGECT/conf/train_conformer.yaml', '--train_data', 'raw_wav/train/format.data', '--cv_data', 'raw_wav/dev/format.data', '--model_dir', 'exp/conformer', '--gpu', '0', '--ddp.dist_backend', 'nccl', '--num_workers', '2', '--cmvn', 'exp/conformer/global_cmvn', '--interval', '30.0', '--failure', '15', '--database', 'MONITOR', '--dbhost', '172.16.20.190', '--task_id', '1', '--template', 'EXP', '--pin_memory']
    def make_args(self,checkpoint=False):
        self.command = ['python', 'train.py']
        for arg in self.args:
            self.command.append('%s' % (str(arg)))
        if checkpoint:
            train_dir = check_path(self.name)
            files = os.listdir(train_dir)
            model_file = []
            for j in files:
                if ".pt" in j:
                    model_file.append(j)
            start_epoch = []
            for j in model_file:
                matchobj = re.match(r'\d+', j)
                if matchobj:
                    start_epoch.append(int(matchobj.group()))
            checkpoint_file = ""
            if 'init.pt' in model_file:
                checkpoint_file = 'init.pt'
            if start_epoch:
                start_epoch.sort()
                checkpoint_file = "%d.pt" % start_epoch[-1]
            if checkpoint_file:
                checkpoint_file = os.path.join(self.run_dir,checkpoint_file)
                if '--checkpoint' in self.command:
                    aim_index = self.command.index('--checkpoint')
                    self.command.remove('--checkpoint')
                    pt_value = self.command[aim_index]
                    self.command.remove(pt_value)
                if self.pin_memory:
                    self.command.insert(-1, '--checkpoint')
                    self.command.insert(-1, '%s' % checkpoint_file)
                else:
                    self.command.append('--checkpoint')
                    self.command.append('%s' % checkpoint_file)
            else:
                if '--checkpoint' in self.command:
                    aim_index = self.command.index('--checkpoint')
                    self.command.remove('--checkpoint')
                    pt_value = self.command[aim_index]
                    self.command.remove(pt_value)
        else:
            if '--checkpoint' in self.command:
                aim_index = self.command.index('--checkpoint')
                self.command.remove('--checkpoint')
                pt_value = self.command[aim_index]
                self.command.remove(pt_value)

    def set_master_replicas(self,master_replicas):
        self.master_replicas = master_replicas

    def set_worker_replicas(self,worker_replicas):
        self.worker_replicas = worker_replicas

    def set_status(self,status):
        self.status = status
        save_job_change_status(self.name,status)

    def schedule_base(self,mode=0,cpu_weight=0.7):
        self.cluster_agent.update_node(mode=0,node_update=False)
        need_gpu = self.master_replicas + self.worker_replicas
        now_avail_gpu = self.cluster_agent.total_gpu - self.cluster_agent.total_used_gpu
        # mode = 0: 给出调度决策
        if mode == 0:
            if now_avail_gpu < 2:
                print("do not have enough gpu resource to submit a job now.")
                self.node_affinity = {}
                return -1, -1, {}
            else:
                actual_master = self.master_replicas
                actual_worker = self.worker_replicas
                if need_gpu > now_avail_gpu:
                    if self.master_replicas > 1:
                        actual_master = 1
                    if actual_master + actual_worker > now_avail_gpu:
                        actual_worker = now_avail_gpu - actual_master
                    print("gpu resource are not enough, system will reduce the number of workers")
                gpu_avail = {}
                for node_id in list(self.cluster_agent.node_resource.keys()):
                    if int(self.cluster_agent.node_resource[node_id]['avail']) not in gpu_avail.keys():
                        gpu_avail[int(self.cluster_agent.node_resource[node_id]['avail'])] = []
                    gpu_avail[int(self.cluster_agent.node_resource[node_id]['avail'])].append(node_id)
                gpu_avail_value = list(gpu_avail.keys())
                gpu_avail_value.sort()
                gpu_avail_value_sum = 0
                prior_node = {}
                level = 0
                for j in range(len(gpu_avail_value) - 1, -1, -1):
                    prior_node[level] = []
                    for jn in gpu_avail[gpu_avail_value[j]]:
                        prior_node[level].append(jn)
                    gpu_avail_value_sum += (gpu_avail_value[j]) * len(prior_node[level])
                    if gpu_avail_value_sum >= (actual_master + actual_worker):
                        break
                    level = level + 1
                # We use three levels as the selected node in this situation:
                # 1. 按照顺序：GPU可用数量最多的优先，相同多时CPU和内存利用率平均最低的优先
                total_node_to_schedule = []
                levels = list(prior_node.keys())
                for l in range(len(levels)):
                    cpu_base = {}
                    for ln in prior_node[l]:
                        work_value = self.cluster_agent.node_resource[ln]['avg_cpu_percent'] * cpu_weight + (
                                    1 - cpu_weight) * self.cluster_agent.node_resource[ln]['avg_memory_percent']
                        if work_value not in cpu_base.keys():
                            cpu_base[work_value] = []
                        cpu_base[work_value].append(ln)
                    work_value_total = list(cpu_base.keys())
                    work_value_total.sort()
                    for wv in work_value_total:
                        for actual_node in cpu_base[wv]:
                            total_node_to_schedule.append(actual_node)

                labels = {}
                labels[0] = []
                all_actual_gpu = 0
                now_index = 0
                for selected_n in total_node_to_schedule:
                    labels[0].append(selected_n)
                    all_actual_gpu += self.cluster_agent.node_resource[selected_n]['avail']
                    now_index += 1
                    if all_actual_gpu >= actual_worker + actual_master:
                        break
                if now_index <= len(total_node_to_schedule) - 1:
                    labels[1] = total_node_to_schedule[now_index:]
                    self.node_affinity = {0: [int(selected_n[4:]) for selected_n in labels[0]],
                                          1: [int(selected_n[4:]) for selected_n in labels[1]]}
                    return actual_master, actual_worker, {0: [int(selected_n[4:]) for selected_n in labels[0]],
                                                          1: [int(selected_n[4:]) for selected_n in labels[1]]}
                else:
                    labels[1] = []
                    self.node_affinity = {0: [int(selected_n[4:]) for selected_n in labels[0]], 1: []}
                    return actual_master, actual_worker, {0: [int(selected_n[4:]) for selected_n in labels[0]], 1: []} #
        # mode = 1: 给出当前可用资源量
        else:
            now_avail_gpu = self.cluster_agent.total_gpu - self.cluster_agent.total_used_gpu
            return now_avail_gpu

    def assignment_resource(self, cpu_source, memory_source):
        old_cpu = self.cpu_allocate
        old_mem = self.memory_allocate
        self.cpu_allocate = cpu_source
        self.memory_allocate = memory_source
        # if self.cpu_allocate <
        if self.cpu_allocate > 0:
            cpu_usage = str(cpu_source) + 'm'
        if self.memory_allocate > 0:
            mem_usage = str(memory_source) + 'Mi'

        job_file = '%s/%s.yaml' % (self.job_dir,self.name)

        with open(job_file, 'r') as job_yaml:
            job_yaml_obj = yaml.load(job_yaml.read())
        job_yaml.close()
        if self.cpu_allocate < 0:
            if "cpu" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources'][
            'limits'].keys():
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits'].pop("cpu")
            if "cpu" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources'][
                'limits'].keys():
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0][
                    'resources']['limits'].pop("cpu")
        if self.memory_allocate < 0:
            if "memory" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits'].keys():
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits'].pop("memory")
            if "memory" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'].keys():
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'].pop("memory")
        if self.cpu_allocate > 0:
            job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
            job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources'][
                'limits']['cpu'] = cpu_usage
        if self.memory_allocate > 0:
            job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']["memory"] = mem_usage
            job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources'][
                'limits']["memory"] = mem_usage
        f = open(job_file, "w")
        yaml.dump(job_yaml_obj, f)
        f.close()

        response = os.system('kubectl apply -f ' + job_file)
        if response == 0:
            print('assign task resource sucess')
            save_job_change_resource(self.name, cpu_source, memory_source)
            self.save_job_logs(action="modulte cpu resource from %s to %s; modulate memory resource from %s to %s" % (str(old_cpu),str(self.cpu_allocate),str(old_mem),str(self.memory_allocate)))
            message = {"message":"assign task resource sucess"}
            return True,message
        else:
            self.cpu_allocate = old_cpu
            self.memory_allocate = old_mem
            with open(job_file, 'r') as job_yaml:
                job_yaml_obj = yaml.load(job_yaml.read())
            job_yaml.close()
            if self.cpu_allocate < 0:
                if "cpu" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits'].keys():
                    job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0][
                        'resources']['limits'].pop("cpu")
                if "cpu" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'].keys():
                    job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0][
                        'resources']['limits'].pop("cpu")
            if self.memory_allocate < 0:
                if "memory" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits'].keys():
                    job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits'].pop("memory")
                if "memory" in job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'].keys():
                    job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits'].pop("memory")
            if self.cpu_allocate > 0:
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
            if self.memory_allocate > 0:
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']["memory"] = mem_usage
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']["memory"] = mem_usage
            f = open(job_file, "w")
            yaml.dump(job_yaml_obj, f)
            f.close()
            print("Error code:" + str(response))
            self.save_job_logs(action="module resource fail")
            message = {"message":"module resource fail"}
            return False,message

    def assign_replicas(self,master_n,worker_n,mode=0):
        old_master = self.master_replicas
        old_worker = self.worker_replicas
        self.master_replicas = master_n
        self.worker_replicas = worker_n
        if mode == 1:
            save_job_change_replicas(self.name,master_n,worker_n)
            self.save_job_logs("sync the num of replicas: master: %d, worker: %d" % (master_n,worker_n))
            message = {"message":"sync the num of replicas: master: %d, worker: %d" % (master_n,worker_n)}
            return True,master_n,worker_n,message
        self.retry = self.retry + 1
        self.template['spec']['pytorchReplicaSpecs']['Master']['replicas'] = self.master_replicas
        self.template['spec']['pytorchReplicaSpecs']['Worker']['replicas'] = self.worker_replicas
        name = self.name
        # log_dir = '/tfdata/tfcnn/expjob/'

        now_avail_gpu = self.schedule_base(mode=1)
        if old_worker + old_master + now_avail_gpu < self.master_replicas + self.worker_replicas:
            print("do not have enough resources")
            self.save_job_logs("do not have enough resources, cancel adjusting: want: %d, can support: %d" % (self.master_replicas + self.worker_replicas,old_worker + old_master + now_avail_gpu))
            self.master_replicas = old_master
            self.worker_replicas = old_worker
            message = {"message":"do not have enough resources, cancel adjusting: want: %d, can support: %d" % (self.master_replicas + self.worker_replicas,old_worker + old_master + now_avail_gpu)}
            return False,old_master,old_worker,message
        pod_items = self.cluster_agent.v1.list_namespaced_pod(self.name).items
        if pod_items:
            response = os.system('kubectl delete -f ' + self.job_dir + str(name) + '.yaml')
        else:
            response = 0
        if response == 0:
            print('delete task sucess')
        else:
            print("Error code:" + str(response))
            os.system('kubectl apply -f ' + self.job_dir + str(name) + '.yaml')
        if response == 0:
            if self.master_replicas + self.worker_replicas > old_worker + old_master:
                time.sleep(18.5)
            OK,acutal_master,acutal_worker = self.create_tf(checkpoint=True,mode=1)
            message = {"message":""}
            if OK:
                self.save_job_logs("adjust workers successfully!")
                message = {"message":"adjust workers successfully!"}
                save_job_change_replicas(job_name=self.name,master_replicas=acutal_master,worker_replicas=acutal_worker)
            if not OK:
                self.master_replicas = old_master
                self.worker_replicas = old_worker
                job_file = '%s/%s.yaml' % (self.job_dir, self.name)
                with open(job_file, 'r') as job_yaml:
                    job_yaml_obj = yaml.load(job_yaml.read())
                job_yaml.close()
                self.create_tf(checkpoint=True, mode=1)
                acutal_worker = old_worker
                acutal_master = old_master
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Master']['replicas'] = acutal_worker
                job_yaml_obj['spec']['pytorchReplicaSpecs']['Worker']['replicas'] = acutal_master
                f = open(job_file, "w")
                yaml.dump(job_yaml_obj, f)
                f.close()
                os.system('kubectl apply -f ' + self.job_dir + str(name) + '.yaml')
                message = {"message": "adjust workers do not success!"}
            return OK,acutal_worker,acutal_master,message
        else:
            message = {"message":"Error Code: %d" % response}
            return False,old_master,old_worker,message,

        # self.v1.delete_namespace(name=name)

    def create_tf(self,checkpoint=False,mode=0):
        name = '%s-%d' % (self.template_name,self.task_id)
        cpu_source = self.cpu_allocate
        mem_source = self.memory_allocate
        if cpu_source > 0:
            cpu_usage = str(cpu_source)+'m'
        if mem_source > 0:
            mem_usage = str(mem_source)+'Mi'

        ns_body = TorchTemplate.NS
        ns_body['metadata']['name'] = name
        sa_dir = self.sa_dir
        bind_dir = self.bind_dir
        job_dir = self.job_dir
        serviceaccount_body = TorchTemplate.SA
        rolebind_body = TorchTemplate.BIND
        rolename = '%s-%d-reader' % (self.template_name,self.task_id)
        bindname = '%s-%d-bind' % (self.template_name,self.task_id)

        if not check_ns(name):
            self.cluster_agent.v1.create_namespace(ns_body)
            serviceaccount_body['metadata']['name'] = rolename
            serviceaccount_body['metadata']['namespace'] = name

            # f = open(log_dir+str(name)+'.yaml', "w")
            f = open(sa_dir + str(name) + '-sa.yaml', "w")
            yaml.dump(serviceaccount_body, f)
            f.close()
            response = os.system('kubectl apply -f ' + sa_dir + str(name) + '-sa.yaml')
            if response == 0:
                print('create serviceaccount sucess')
            else:
                print("Error code:" + str(response))
            time.sleep(4.5)
            rolebind_body['metadata']['name'] = bindname
            rolebind_body['metadata']['namespace'] = name
            rolebind_body['subjects'][0]['name'] = rolename
            rolebind_body['subjects'][0]['namespace'] = name

            f = open(bind_dir + str(name) + '-bind.yaml', "w")
            yaml.dump(rolebind_body, f)
            f.close()
            response = os.system('kubectl apply -f ' + bind_dir + str(name) + '-bind.yaml')
            if response == 0:
                print('create rolebind sucess')
            else:
                print("Error code:" + str(response))
        train_dir = check_path(name)
        time.sleep(5.0)

        # self.schedule_label()
        acutal_master, acutal_worker, node_affinity = self.schedule_label()
        if acutal_master < 0 or acutal_worker < 0:
            return False,acutal_master, acutal_worker
        #     print(TorchTemplate.TASK['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity']['preferredDuringSchedulingIgnoredDuringExecution'][1])
        self.template = TorchTemplate.TASK
        if not node_affinity:
            self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec'].pop('nodeAffinity')
            self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec'].pop('nodeAffinity')
        else:
            if 'nodeAffinity' not in self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec'].keys():
                self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'] = {}
                self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'] = {}
            self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'][
                'preferredDuringSchedulingIgnoredDuringExecution'] = []
            self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'][
                'preferredDuringSchedulingIgnoredDuringExecution'] = []
            # {'preference': {'matchExpressions': [{'key': 'node', 'operator': 'In', 'values': []}]},
            #             #                      'weight': 5})
            for k in node_affinity:
                # tmps = {'preference':{'matchExpressions'}}
                self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'][
                    'preferredDuringSchedulingIgnoredDuringExecution'].append({'preference': {}})
                self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'][
                    'preferredDuringSchedulingIgnoredDuringExecution'][-1]['preference']['matchExpressions'] = []
                self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'][
                    'preferredDuringSchedulingIgnoredDuringExecution'][-1]['weight'] = k['weight']
                for key in k['preference']['matchExpressions']:
                    self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'][
                        'preferredDuringSchedulingIgnoredDuringExecution'][-1]['preference']['matchExpressions'].append(
                        {"key": "node", "operator": 'In', 'values': []})
                    for value in key['values']:
                        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['nodeAffinity'][
                            'preferredDuringSchedulingIgnoredDuringExecution'][-1]['preference']['matchExpressions'][0]['values'].append(value)
                self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'][
                    'preferredDuringSchedulingIgnoredDuringExecution'].append({'preference': {}})
                self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'][
                    'preferredDuringSchedulingIgnoredDuringExecution'][-1]['preference']['matchExpressions'] = []
                self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'][
                    'preferredDuringSchedulingIgnoredDuringExecution'][-1]['weight'] = k['weight']
                for key in k['preference']['matchExpressions']:
                    self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'][
                        'preferredDuringSchedulingIgnoredDuringExecution'][-1]['preference']['matchExpressions'].append(
                        {"key": "node", "operator": 'In', 'values': []})
                    for value in key['values']:
                        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['nodeAffinity'][
                            'preferredDuringSchedulingIgnoredDuringExecution'][-1]['preference']['matchExpressions'][0]['values'].append(value)
        # {'preference': {'matchExpressions': [{'key': 'cpusch', 'operator': 'In', 'values': ['true']}]}, 'weight': 10}
        # self.node_affinity
        self.template['metadata']['name'] = name
        self.template['metadata']['namespace'] = name
        self.template['spec']['pytorchReplicaSpecs']['Master']['replicas'] = self.master_replicas
        self.template['spec']['pytorchReplicaSpecs']['Worker']['replicas'] = self.worker_replicas

        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['image'] = self.image
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['image'] = self.image

        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0][
            'name'] = 'pytorch'
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0][
            'name'] = 'pytorch'

        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['name'] = name
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['volumes'][0]['hostPath']['path'] = train_dir

        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][1]['name'] = "%s-data" % name
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['volumes'][1]['name'] = "%s-data" % name
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][1]['hostPath']['path'] = "/home/NFSshare/%s" % self.raw_data_path
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['volumes'][1]['hostPath'][ 'path'] = "/home/NFSshare/%s" % self.raw_data_path

        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][2]['name'] = "%s-config" % name
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['volumes'][2]['name'] = "%s-config" % name
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['volumes'][2]['hostPath']['path'] = "/home/NFSshare/%s" % self.project_config_path
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['volumes'][2]['hostPath']['path'] = "/home/NFSshare/%s" % self.project_config_path
        # self.raw_data_path = raw_data_path
        #         self.project_config_path = project_config_path
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['name'] = name
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = "%s/%s" % (self.container_work_dir,self.model_dir)
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][0]['mountPath'] = "%s/%s" % (self.container_work_dir,self.model_dir)

        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][1]['name'] = "%s-data" % name
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][1]['name'] = "%s-data" % name
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][1]['mountPath'] = "/home/NFSshare/%s" % self.raw_data_path
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][1]['mountPath'] = "/home/NFSshare/%s" % self.raw_data_path

        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][2]['name'] = "%s-config" % name
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][2]['name'] = "%s-config" % name
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['volumeMounts'][2]['mountPath'] = "/home/NFSshare/%s" % self.project_config_path
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['volumeMounts'][2]['mountPath'] = "/home/NFSshare/%s" % self.project_config_path
        self.make_args(checkpoint)
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['command'] = self.command[:]
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['command'] = self.command[:]
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['serviceAccount'] = rolename
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['serviceAccount'] = rolename

        if self.cpu_allocate > 0:
            self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
            self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = cpu_usage
        if self.memory_allocate > 0:
            self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
            self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['memory'] = mem_usage
        self.template['spec']['pytorchReplicaSpecs']['Master']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = 1
        self.template['spec']['pytorchReplicaSpecs']['Worker']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = 1

        # log_dir = '/tfdata/tfcnn/expjob/'
        # f = open(log_dir+str(name)+'.yaml', "w")
        f = open(job_dir + str(name) + '.yaml', "w")
        yaml.dump(self.template, f)
        f.close()
        response = os.system('kubectl apply -f '+job_dir+str(name)+'.yaml')
        if response == 0:
            print('create task sucess')
            return True,acutal_master,acutal_worker
        else:
            print("Error code:"+str(response))
            return False,acutal_master,acutal_worker
    def schedule_label(self):
        self.node_affinity = {}
        acutal_master,acutal_worker,affinity = self.schedule_base()
        node_affinity = []
        if not affinity:
            return acutal_master,acutal_worker,node_affinity
        else:
            node_affinity.append({'preference': {'matchExpressions': [{'key': 'node', 'operator': 'In', 'values': []}]}, 'weight': 10})
            for i in affinity[0]:
                node_affinity[0]['preference']['matchExpressions'][0]['values'].append('"%d"' % i)
            if affinity[1]:
                node_affinity.append(
                    {'preference': {'matchExpressions': [{'key': 'node', 'operator': 'In', 'values': []}]},
                     'weight': 5})
                for i in affinity[0]:
                    node_affinity[0]['preference']['matchExpressions'][0]['values'].append('"%d"' % i)
            return acutal_master,acutal_worker,node_affinity

    def delete_tf(self,mode=0):
        log_dir = self.job_dir
        if self.status not in ['Finished','Deleted']:
            response = os.system('kubectl delete -f ' + log_dir + str(self.name) + '.yaml')
            if response == 0:
                print('delete task sucess')
                self.save_job_logs("this job cancelled")
            else:
                print("Error code:" + str(response))
                self.save_job_logs("cancel the job but: %d" % response)
        if mode == 0:
            # deletehelp2(name, self.v1)
            sa_dir = self.sa_dir
            bind_dir = self.bind_dir
            response = os.system('kubectl delete -f ' + bind_dir + str(self.name) + '-bind.yaml')
            response2 = os.system('kubectl delete -f ' + sa_dir + str(self.name) + '-sa.yaml')
            self.save_job_logs("delete this job")
            self.set_status("Deleted")
            self.cluster_agent.v1.delete_namespace(name=self.name)
#
if __name__ == '__main__':
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # v1.create_namespace()
    v1.list_namespace()
    check_path('ceshi')
    ceshi = SubTask(gpu_monitor_database="MONITOR")
    print(ceshi.schedule_base())
    print(ceshi.cluster_agent.node_resource)
    print(ceshi.node_affinity)
    ceshi.create_tf()

    # vgg = VGGTask(1,2,4,80,1.0,2,1,"ms",32,64,128,256,512,2,3,3,4,4)
    # vgg.create_tf()
