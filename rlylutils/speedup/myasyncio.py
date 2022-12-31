# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL



import time
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor

import psutil

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator


__all__=['Masyncio','thread_worker']


class ThreadPool():

    def __init__(self, max_workers):

        self._thread_pool = ThreadPoolExecutor(max_workers)

    async def run(self, _callable, *args, **kwargs):

        future = self._thread_pool.submit(_callable, *args, **kwargs)

        return await asyncio.wrap_future(future)


class ThreadWorker:

    def __init__(self, max_workers):

        self._thread_pool = ThreadPool(max_workers)

    def __call__(self, func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            return self._thread_pool.run(func, *args, **kwargs)

        return _wrapper

@Decorator.cdec(Cfg.default['param'])
class Masyncio:

    default = {'Author': 'Ray Lam LYL',
               'cpuphy_count': psutil.cpu_count(logical=False),
               'cpulog_count': psutil.cpu_count(logical=True)
               }

    def __init__(self):
        self.__dict__.update(self.default)


    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【异步{}】len:{}'.format(varname, len(iterable))


    def namestr(self, obj, namespace):
        '''
        变量名转字符串
        #例（变量名，globals()）
        '''
        return [name for name in namespace if namespace[name] is obj][0]

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)

    async def hello(self):
        await asyncio.sleep(1)
        print('Hello World:%s' % time.time())



thread_worker = ThreadWorker(Masyncio.default['cpuphy_count'])




if __name__ =='__main__':
    start=time.time()
    @thread_worker
    def hel():
        time.sleep(1)
        print('dd\n')

    # asyncio.run(some_io_block())

    loop = asyncio.get_event_loop()
    h=Masyncio()
    tasks = [hel() for i in range(5)]
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time()-start)
