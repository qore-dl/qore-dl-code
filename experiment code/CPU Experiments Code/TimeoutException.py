import time
import signal
import multiprocessing
import os

# 自定义超时异常
class TimeoutError(Exception):
    def __init__(self, msg):
        super(TimeoutError, self).__init__()
        self.msg = msg

def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("run func timeout")

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)       # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)              # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except TimeoutError as e:
                callback(e)
        return wrapper
    return decorator


def timeout_callback(e):
    print(e.msg)


def Myhandler(signum, frame):
    raise TimeoutError("run func timeout")

# @time_out(2, timeout_callback)
def task1():
    print("task1 start")
    time.sleep(3)
    print("task1 end")

def ceshi():
    ids = os.getpid()
    try:
        signal.signal(signal.SIGALRM, Myhandler)
        signal.alarm(2)  # interval秒后向进程发送SIGALRM信号
        # result = func(*args, **kwargs)
        task1()
        signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
        # return result
    except TimeoutError as e:
        print("%d进程： %s"  % (ids,e.msg))
# @time_out(2, timeout_callback)
# def task2():
#     print("task2 start")
#     time.sleep(1)
#     print("task2 end")

if __name__ == '__main__':
    task1()
    # print(a)


    pool = multiprocessing.Pool(processes=5)
    pool_size = 5
    while True:
        pool.apply_async(ceshi)
