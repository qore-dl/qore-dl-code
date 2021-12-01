import os
import json
base_file = "/tfdata/tfcnn/Dynamicmodulation3/system_info.json"

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

if __name__ == '__main__':
    tasks = load_config(base_file)
    aim_job = tasks['finish'][:]
    job_aims  = {}
    for job in aim_job:
        # job0 = reload_jobs(job, -1)
        aim_dir = '/tfdata/k8snfs/%s/' % job
        # handle_for_remove(aim_dir)
        # file_list = os.listdir(aim_dir)
        # for i in file_list:
        #     if 'model.ckpt' in i or 'checkpoint' in i or 'events' in i or 'graph' in i:
        #         aim_file = aim_dir+'/%s' % i
        #         os.remove(aim_file)
        res_file = '/tfdata/k8snfs/%s/%s_res.json' % (job, job)
        res_i = load_config(res_file)
        job_aims[res_i['start_time']] = job

    job_aim_key = list(job_aims.keys())
    job_aim_key2 = [float(i) for i in job_aim_key]

    list.sort(job_aim_key2)
    aim_job0 = []
    for i in job_aim_key2:
        aim_job0.append(job_aims[i])
    tasks['aim'] = aim_job0[:]
    save_config(tasks,base_file)

    # for i in aim_job0:
    #     command = 'cp /tfdata/k8snfs/%s/%s_res.json /tfdata/expn2' % (i,i)
    #     os.system(command)
    #
    # command = 'cp /tfdata/tfcnn/Dynamicmodulation/system_info.json /tfdata/expn2/Dynamic.json'
    # os.system(command)
    #
    # command = 'cp /tfdata/tfcnn/Optimus/system_info.json /tfdata/expn2/Optimus.json'
    # os.system(command)
    #
    # command = 'cp /tfdata/tfcnn/Raw/system_info.json /tfdata/expn2/Raw.json'
    # os.system(command)
    #
    # command = 'cp /tfdata/tfcnn/SLAQ/system_info.json /tfdata/expn2/SLAQ.json'
    # os.system(command)

