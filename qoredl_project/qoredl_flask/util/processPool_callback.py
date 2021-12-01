from controller import logger


def processPool_callback(worker):
    '''
    线程池出现异常回调函数，输出异常信息
    :param worker:
    :return:
    '''
    worker_exception = worker.exception()
    if worker_exception:
        logger.exception("Worker return exception: {}".format(worker_exception))
