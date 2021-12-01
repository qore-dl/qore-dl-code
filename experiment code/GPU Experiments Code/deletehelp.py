import os
import json
import kubernetes
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

def deletehelp(delete_job_name,v1):
    try:
        v1.delete_namespace(delete_job_name)
    except Exception as eeeeee:
        print(eeeeee)
        command0 = "kubectl get namespace " + delete_job_name + " -o json > /tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
        os.system(command0)
        tmp = load_config("/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        tmp["spec"]["finalizers"] = []
        save_config(tmp, "/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
        try:
            command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/'+delete_job_name+'/finalize'
            os.system(command1)
        except Exception as helpe:
            print(helpe)
            commandopen = 'kubectl proxy --port=8081'
            os.system(commandopen)
            os.system(command1)

def deletehelp2(delete_job_name,v1):
    v1.delete_namespace(delete_job_name)
    command0 = "kubectl get namespace " + delete_job_name + " -o json > /tfdata/tfcnn/deletebuf/" + delete_job_name + ".json"
    os.system(command0)
    tmp = load_config("/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
    tmp["spec"]["finalizers"] = []
    save_config(tmp, "/tfdata/tfcnn/deletebuf/" + delete_job_name + ".json")
    try:
        command1 = 'curl -k -H "Content-Type: application/json" -X PUT --data-binary @/tfdata/tfcnn/deletebuf/' + delete_job_name + '.json http://127.0.0.1:8081/api/v1/namespaces/' + delete_job_name + '/finalize'
        os.system(command1)
    except Exception as helpe:
        print(helpe)
        commandopen = 'kubectl proxy --port=8081'
        os.system(commandopen)
        os.system(command1)

if __name__ == '__main__':
    kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    # workname = ['re-406-406','re-409-409','re-414-414','re-445-445','re-469-469','res-478-478','res-514-514','res-609-609','res-627-627','res-667-667','res-670-670','res-671-671','res-677-677','res-678-678',
    #             'vgg-160-160',
    #             'vgg-363-363',
    #             'vgg-416-416',
    #             'vgg-425-425',
    #             'vgg-480-480',
    #             'vgg-555-555',
    #             'vgg-556-556','xception-431-431','xception-521-521','xception-530-530','xception-685-685','xception-705-705']
    # # delete_job_name = 'res-613-613'
    workname=[
       "vgg-631-631",
        "vgg-634-634",
        "vgg-633-633",
        "vgg-632-632",
        "vgg-637-637",
        "res-681-681",
        "vgg-636-636",
        "res-686-686",
        "res-683-683",
        "res-689-689",
        "res-685-685",
        "vgg-644-644",
        "vgg-639-639",
        "res-690-690",
        "vgg-646-646",
        "vgg-647-647",
        "vgg-648-648",
        "vgg-642-642",
        "vgg-649-649",
        "vgg-641-641",
        "vgg-650-650",
        "res-693-693",
        "vgg-652-652",
        "res-695-695",
         "vgg-643-643",
        "vgg-640-640",
        "res-697-697",
        "vgg-655-655",
        "vgg-645-645",
        "res-700-700",
        "res-696-696",
        "vgg-651-651",
        "res-699-699",
        "vgg-654-654",
        "vgg-657-657",
        "res-701-701",
        "vgg-659-659",
        "res-698-698",
        "vgg-660-660",
        "res-709-709",
        "res-682-682",
        "res-710-710",
        "vgg-664-664",
        "res-711-711",
        "vgg-653-653",
        "res-692-692",
        "vgg-665-665",
        "vgg-656-656",
        "res-712-712",
        "res-713-713",
        "vgg-667-667",
        "res-714-714",
        "vgg-658-658",
        "res-715-715",
        "vgg-669-669",
        "res-705-705",
        "vgg-661-661",
        "res-719-719",
        "vgg-668-668",
        "res-706-706",
        "res-702-702",
        "vgg-663-663",
        "vgg-666-666",
        "vgg-670-670",
        "vgg-671-671",
        "vgg-662-662",
        "res-687-687",
        "res-703-703",
        "res-717-717",
        "res-720-720",
         "res-687-687",
        "res-703-703",
        "res-717-717",
        "res-720-720"                		
]
    worker2 = [
        "xception-739-739",
        "res-733-733",
        "vgg-680-680",
        "res-735-735",
        "res-732-732",
        "res-736-736",
        "xception-741-741"]
    import time
    start = time.time()
    for i in worker2:
    # for i in workname:
   	 deletehelp(i,v1)
    endtime = time.time() - start
    print(endtime)

    '''
re-406-406         Active   27d
re-409-409         Active   27d
re-414-414         Active   40d
re-445-445         Active   30d
re-469-469         Active   25d
re1                Active   88d
res-478-478        Active   49d
res-514-514        Active   48d
res-609-609        Active   2d1h
res-627-627        Active   25d
res-667-667        Active   22d
res-670-670        Active   22d
res-671-671        Active   22d
res-677-677        Active   22d
res-678-678        Active   22d
res1               Active   88d
vgg-160-160        Active   2d2h
vgg-363-363        Active   52d
vgg-416-416        Active   49d
vgg-425-425        Active   49d
vgg-480-480        Active   48d
vgg-555-555        Active   2d
vgg-556-556        Active   2d
vgg2               Active   101d
vgg5               Active   87d
xce1               Active   88d
xception-431-431   Active   50d
xception-521-521   Active   48d
xception-530-530   Active   48d
xception-685-685   Active   24d
xception-705-705   Active   24d
    '''

