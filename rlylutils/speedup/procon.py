# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL


import multiprocessing as mp
from multiprocessing import Queue, Process
import time
import psutil
from tqdm import tqdm

__all__=['Producer','Consumer','ProCon']


class Producer(Process):

    default = {'Author': 'Ray Lam LYL',
               'cpuphy_count': psutil.cpu_count(logical=False),
               'cpulog_count': psutil.cpu_count(logical=True)
               }

    def __init__(self, name, my_q):
        super().__init__()
        self.__dict__.update(self.default)
        self.name = name
        self.q = my_q

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【多进程producer{}】len:{}'.format(varname, len(iterable))


    def namestr(self, obj, namespace):
        '''
        变量名转字符串
        #例（变量名，globals()）
        '''
        return [name for name in namespace if namespace[name] is obj][0]

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)


    def run(self):
        for i in range(100):
            info = self.name + "的%s" % str(i)
            # 数据放入队列
            self.q.put(info)
        self.q.put(None)


class Consumer(Process):

    default = {'Author': 'Ray Lam LYL',
               'cpuphy_count': psutil.cpu_count(logical=False),
               'cpulog_count': psutil.cpu_count(logical=True)
               }

    def __init__(self, name, my_q):
        super().__init__()
        self.__dict__.update(self.default)
        self.name = name
        self.q = my_q

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【多进程consumer{}】len:{}'.format(varname, len(iterable))


    def namestr(self, obj, namespace):
        '''
        变量名转字符串
        #例（变量名，globals()）
        '''
        return [name for name in namespace if namespace[name] is obj][0]

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)


    def run(self):
        while True:
            info = self.q.get()
            if info:
                print("%s拿走了%s" % (self.name, info))
            else:
                break

class ProCon:

    default = {'Author': 'Ray Lam LYL',
               'cpuphy_count': psutil.cpu_count(logical=False),
               'cpulog_count': psutil.cpu_count(logical=True)
               }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【多进程consumer{}】len:{}'.format(varname, len(iterable))


    def namestr(self, obj, namespace):
        '''
        变量名转字符串
        #例（变量名，globals()）
        '''
        return [name for name in namespace if namespace[name] is obj][0]

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)

    def run(self):
        my_q = Queue(3)   # 建立一个长度为3的队列
        mgr = mp.Manager()
        mgrd = mgr.dict()

        p_pro = Producer('生产者', my_q)
        p_con = Consumer('消费者', my_q)
        p_pro.start()
        p_con.start()
        p_pro.join()

if __name__ == '__main__':
    start = time.time()
    pc=ProCon()
    pc.run()
    print(time.time()-start)
