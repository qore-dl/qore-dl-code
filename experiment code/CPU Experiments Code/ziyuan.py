import json
import numpy as np
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


from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor
rfr = joblib.load('rfr_batch.pkl')

def predict_min_first(rfr,cpu_alpha,mem_alpha,batch,flops,params):
    data = np.array([batch, flops, params, cpu_alpha, mem_alpha])
    data = np.mat(data)
    data = data.A
    iteration = rfr.predict(data)
    iteration = float(iteration)
    return iteration

tasks = load_config("system_info.json")
aa1 = tasks['finish'][:]
aa2 = tasks['fail'][:]
aa3 = []

pio = {}

for k in aa1:
    if k not in aa2:
        aa3.append(k)
print(len(aa3))
for k in aa3:
    res_path = '/tfdata/k8snfs/setad2/%s/%s_res.json' % (k,k)
    step_path = '/tfdata/k8snfs/setad2/%s/%s_pw.json' % (k,k)

    # step_config = load_config(step_path)

    config = load_config(res_path)
    batch_res = config['batch_res']
    flops_res = config['flops_res']
    params_res = config['params_res']

    mini_batch = predict_min_first(rfr=rfr, cpu_alpha=1, mem_alpha=1, batch=batch_res,
                                                       flops=flops_res, params=params_res)

    aim_job_step_base = load_config(step_path)
    his_step_key = list(aim_job_step_base["changen"].keys())
    his_step = []
    for hsk in his_step_key:
        his_step.append(float(hsk))

    # list.sort(his_step)
    aim_job_step_base_pre = aim_job_step_base["changen"][str(min(his_step))]

    # tmp_step0 = aim_job_step_base_pre["stepbefore"]*aim_job_step_base_pre["wbefore"]
    # tmp_step0 = math.ceil(tmp_step0/2)
    # ps_r = 1
    # worker_r = 2
    tmp_step0 = aim_job_step_base_pre["stepbefore"]
    deadline0 = mini_batch * tmp_step0

    perce = deadline0/config['deadline']
    item_pio = {'cpu':config['cpu_high'],'mem':config['memory_base'],'percent':perce}

    pio[k] = item_pio

save_config(pio,"resource_his.json")

    # ps_base =