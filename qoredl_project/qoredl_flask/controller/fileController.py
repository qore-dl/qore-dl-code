import os
from pypinyin import lazy_pinyin
from flask import Blueprint, request, send_from_directory
from werkzeug.utils import secure_filename
from util.Result import success
from util.randomFilename import random_filename

file = Blueprint('file', __name__)

@file.route('/uploadDataSet', methods=['POST'])
def uploadDataSet():
    f = request.files['file']
    basepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 当前文件所在路径
    filename = random_filename(secure_filename(''.join(lazy_pinyin(f.filename))))#使用第三方库（pypinyin)，将中文名转换成拼音
    upload_path = os.path.join(basepath, 'dataSet', filename)
    f.save(upload_path)

    data={'path':upload_path
          }

    return success(data)


@file.route('/download', methods=['GET'])
def downloadrequest():
    filePath=request.args.get('filepath')
    name = filePath.split('\\')[-1]  # 切割出文件名称
    filePath = filePath.replace(name, '')
    return send_from_directory(filePath, name)
