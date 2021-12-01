from entity.ConstantMessage import ConstantMessage
from entity.StatusCode import StatusCode

def success(data):
    return {
        'code':StatusCode.SUCCESS,
        'msg':ConstantMessage.REQUEST_SUCCESS,
        'data':data
    }

def error(msg):
    return {
        'code':StatusCode.COMMON_FAIL,
        'msg':msg,
        'data':None
    }
