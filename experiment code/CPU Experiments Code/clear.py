import os
import json
datapath = '/tfdata/tfcnn/expjob/'

datalist = os.listdir(datapath)
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

# aim_ns = ["re-458-458","re-536-536","re1","res-614-614","res-616-616","res-617-617","res-619-619",
#           "res-681-681","res-682-682","res-683-683",
#           "res-684-684","res-688-688","res-691-691","res-707-707","res-716-716","res-717-717","res-718-718","res-721-721",
#           "res-734-734","res-763-763","res-767-767","res-782-782","res1","vgg-635-635","vgg-640-640",
#           "vgg-653-653","vgg-656-656","vgg-678-678","vgg-679-679","vgg-681-681","vgg-734-734",
#           "vgg-735-735","vgg-747-747","vgg-761-761","vgg-796-796","vgg-797-797","vgg-801-801",
#           "vgg-807-807","vgg-809-809","vgg-813-813","vgg-814-814","vgg-825-825","vgg-836-836","vgg-845-845",
#           "vgg-848-848","vgg-856-856","vgg2","vgg5","xce1","xception-739-739","xception-740-740",
#           "xception-762-762","xception-790-790","xception-801-801","xception-804-804","xception-809-809",
#           "xception-814-814","xception-817-817","xception-876-876","xception-880-880","xception-886-886","xception-894-894"]

aim_ns = [
        "vgg-926-926","vgg-941-941","vgg-944-944"
]

def deletehelp2(delete_job_name,v1):
    v1.delete_namespace(delete_job_name)
    command0 = "kubectl get namespace " + delete_job_name + " -o json > /tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
    os.system(command0)
    tmp = load_config("/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
    tmp["spec"]["finalizers"] = []
    save_config(tmp, "/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
    command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
    try:
        command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
        os.system(command1)
    except Exception as helpe:
        print(helpe)
        commandopen = 'kubectl proxy --port=8081'
        os.system(commandopen)
        os.system(command1)
# for wen in datalist:
#     path = os.path.join(datapath,wen)
#     commond = 'kubectl delete -f '+path
#     try:
#         os.system(commond)
#     except Exception as ee:
#         print(ee)
import kubernetes
import time
kubernetes.config.load_kube_config()
v1 = kubernetes.client.CoreV1Api()
last_ns = []
for a in aim_ns:
    try:
        deletehelp2(a,v1)
    except Exception as e:
        print(e)
        time.sleep(3)
        try:
            deletehelp2(a,v1)
        except Exception as eee:
            last_ns.append(a)
            print(eee)

print(last_ns)