import os
import uuid


def random_filename(filename):
    '''
    不带路径的文件名转换为不会重复的字符串
    :param filename:
    :return:
    '''
    ext = os.path.splitext(filename)[1]#后缀
    new_filename = uuid.uuid1().hex + ext
    return new_filename
