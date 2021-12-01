import multiprocessing
import time
import os

def ceshi_pool(dictionary,lock,limit):
    while True:
        if dictionary['state'] == False:
            time.sleep(2)
            if dictionary['state'] == False:
                break
        lock.acquire()
        tmp = dictionary['number']
        print("生产者%s:当前池中数量： %d" % (os.getpid(),tmp))
        if tmp < limit:
            tmp = tmp + 1
            print("进行生产，生产后池中数量： %d" % tmp)
        dictionary['number'] = tmp
        lock.release()
        time.sleep(1)

def ceshi1(dictionary,lock,limit):
    time.sleep(2)
    pool = multiprocessing.Pool(processes=1)
    try:
        pool.apply_async(ceshi_pool,args=(dictionary,lock,limit))
    except Exception as e:
        print(e)
    while True:
        if dictionary['state'] == False:
            time.sleep(10)
            break



def ceshi2(dictionary,lock):
    time.sleep(2)
    while True:
        if dictionary['state'] == False:
            time.sleep(2)
            if dictionary['state'] == False:
                break
        lock.acquire()
        tmp = dictionary['number']
        print("消费者%s：当前池中数量： %d" % (os.getpid(), tmp))
        if tmp > 0:
            tmp = tmp - 2
            print("进行消费，消费后池中数量： %d" % tmp)
        dictionary['number'] = tmp
        lock.release()
        time.sleep(2)



# def system_start_end(dictionary,process_list):
#     while True:
#         time.sleep(1)
#         state = input(">")
#         if state == 'start':
#             dictionary['state'] = True
#         if state == 'end':
#             dictionary['state'] = False
#             for i in process_list:
#                 i.join()




if __name__ == '__main__':
    mgr = multiprocessing.Manager()

    dictionary = mgr.dict()
    dictionary['state'] = False
    dictionary['number'] = 0
    lock = mgr.Lock()
    p1 = multiprocessing.Process(target=ceshi1,args=(dictionary,lock,6))
    p2 = multiprocessing.Process(target=ceshi2,args=(dictionary,lock))
    process_list = []
    process_list.append(p1)
    process_list.append(p2)
    # system_p = multiprocessing.Process(target=system_start_end,args=(dictionary,process_list))

    boot = input("system start:")
    if boot == 'start':
        dictionary['state'] = True
        time.sleep(1)
        p1.start()
        p2.start()
        # system_p.start()

    while True:
        boot = input("system start:")
        if boot == 'end':
            dictionary['state'] = False
            time.sleep(1)
        if dictionary['state'] == False:
            for i in process_list:
                i.join()
            break

    # system_p.join()





