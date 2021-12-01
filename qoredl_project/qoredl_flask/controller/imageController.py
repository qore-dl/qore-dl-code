import os

import requests
from flask import Blueprint, request, send_from_directory, current_app
import urllib.request
import json

from pypinyin import lazy_pinyin
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE

from entity.ConstantMessage import ConstantMessage
from entity.StatusCode import StatusCode
from util.Result import success, error
from util.randomFilename import random_filename

image = Blueprint('image', __name__)


server_ip = '172.16.20.190'
basepath="/home/NFSshare/docker_registry"
@image.route('getImageList', methods=['GET'])
def getImageList():
    '''
    获取镜像列表
    :return:
    '''
    try:
        cmd = "http://%s:5000/v2/_catalog" % server_ip
        # {"repositories":["cuda11.04-ubuntu18.04-wenet","wenet-k8s-torch","wennet-k8s-torch"]}
        msg = urllib.request.urlopen(cmd).read()
        objs = json.loads(msg)
        # item_global = {"global": []}
        result = {}
        for i in objs["repositories"]:
            # curl -XGET http://172.16.20.190:5000/v2/wenet-k8s-torch/tags/list
            result[i] = []
            #                 {"name":"wenet-k8s-torch","tags":["1.4","1.5","1.7","1.8","1.9","1.10","1.11","1.12","1.14","2.1","2.3"]}
            cmd2 = "http://%s:5000/v2/%s/tags/list" % (server_ip, i)
            msg2 = urllib.request.urlopen(cmd2).read()
            imageobjs = json.loads(msg2)
            if imageobjs['tags'] is not None:
                for version in imageobjs['tags']:
                    result[i].append("%s" % (version))
                    # item_global['global'].append("%s:%s" % (i, version)).
            none_err = []
            for k in result.keys():
                if not result[k]:
                    none_err.append(k)
            if none_err:
                for k in none_err:
                    result.pop(k)
        return success(result)
    except BaseException as e:
        return error(None)

@image.route('getImage', methods=['GET'])
def getImage():
    '''
    查找name的所有版本镜像
    :return:
    '''
    image_name= request.args.get("imageName")
    result = {}
    # item_global = {"global": []}
    cmd = "http://%s:5000/v2/%s/tags/list" % (server_ip, image_name)
    try:
        response = urllib.request.urlopen(cmd)
        result[image_name] = []
        msg = response.read()
        imageobjs = json.loads(msg)
        if imageobjs['tags'] is not None:
            for version in imageobjs['tags']:
                result[image_name].append("%s" % (version))
        if len(result[image_name]) == 0:
            result = None
        return success(result)
    except urllib.error.HTTPError as e:
        return success(None)

@image.route('pushImage', methods=['PUT'])
def pushImage():
    '''
    上传镜像
    :return:
    '''

    #####
    #上传镜像文件到资源管理器中
    f = request.files['file']
    imageName = request.args.get('imageName')
    imageVersion = request.args.get('imageVersion')
    if imageVersion==None:
        imageVersion = 'latest'
    fileName = random_filename(secure_filename(''.join(lazy_pinyin(f.filename))))  # 使用第三方库（pypinyin)，将中文名转换成拼音
    upload_path = os.path.join(basepath, fileName)
    f.save(upload_path)


    p = Popen(["docker", "load", "-i", upload_path], stdout=PIPE)
    stdout, stderror = p.communicate()
    output = stdout.decode('UTF-8')
    lines = output.strip().split(os.linesep)
    results = lines[0]
    if "Loaded image:" not in results:
        return "errors: %s" % output.strip()
    if stderror:
        return "errors: %s" % stderror.decode('UTF-8').strip()
    raw_image_name_full = results.split(" ")[-1].strip()
    raw_image_name = raw_image_name_full.split("/")[-1]

    if imageName:
        image_name = "%s:5000/%s:%s" % (server_ip, imageName, imageVersion)
    else:
        image_name = "%s:5000/%s" % (server_ip,raw_image_name)

    os.system("docker tag %s %s" % (raw_image_name_full, image_name))

    # raw_name =
    p = Popen(["docker", "push", image_name], stdout=PIPE)
    stdout, stderror = p.communicate()
    output = stdout.decode('UTF-8').strip()
    # lines = output.split(os.linesep)
    os.remove(upload_path)
    if stderror:
        return error("%s" % stderror.decode('UTF-8').strip())
    return success(None)


@image.route('pullImage', methods=['GET'])
def pullImage():
    '''
    下载镜像
    :return:
    '''
    imageName =  request.args.get('imageName')
    imageVersion = request.args.get('imageVersion')

    image_path = "%s:5000/%s:%s" % (server_ip, imageName, imageVersion)

    p = Popen(["docker", "pull", image_path],
              stdout=PIPE)
    stdout, stderror = p.communicate()
    if stderror:
        return error(error("errors: %s" % stderror.decode('UTF-8').strip()))
    download_filename = "%s:%s.tar" % (imageName, imageVersion)
    download_filename_full = os.path.join(basepath, download_filename)
    p2 = Popen(["docker", "save", image_path, "-o", download_filename_full], stdout=PIPE)
    stdout2, stderror2 = p2.communicate()
    if stderror2:
        return error("errors: %s" % stderror.decode('UTF-8').strip())
    if os.path.exists(download_filename_full):
        def generate():
            with open(download_filename_full,'rb') as f:
                yield from f
            os.remove(download_filename_full)
        r = current_app.response_class(generate(), mimetype='"application/x-tar"')
        r.headers.set('Content-Disposition', 'attachment', filename=imageName+imageVersion+'.tar')
        return r
    return error(ConstantMessage.DOWNLOAD_ERROR)


@image.route('deleteImage', methods=['DELETE'])
def deleteImage():
    '''
    删除镜像
    :return:
    '''
    imageName = request.args.get('imageName')
    imageVersion = request.args.get('imageVersion')
    repo_port = 5000
    head = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
    url_base = "http://" + server_ip + ":" + str(repo_port) + "/v2/"
    url = url_base + imageName + "/manifests/" + imageVersion
    res_for_manifest = requests.get(url, headers=head, verify=False)
    manifest = res_for_manifest.headers['Docker-Content-Digest']
    delete_operation_url = url_base + imageName + "/manifests/" + manifest
    delete_result = requests.delete(delete_operation_url, verify=False)
    if delete_result.status_code == 202:
        return success(None)
            # "%d: delete %s success......" % (int(delete_result.status_code), image_name + ':' + version)
    else:
        return error(None)
            # "%d: delete %s fail......" % (int(delete_result.status_code), image_name + ':' + version)