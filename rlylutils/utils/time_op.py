# -*- coding:utf-8 -*-
# @Time    : 2022/12/10 16:00
# @Author  : Ray Lam YL


import time
from datetime import datetime



class Timop:
    '''

    '''
    default = {
               }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):

        return '【时间操作{}】len:{}'.format(varname, len(iterable))

    def namestr(self, obj, namespace):
        '''
        变量名转字符串
        #例（变量名，globals()）
        '''
        return [name for name in namespace if namespace[name] is obj][0]

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)

    @classmethod
    def current_time(cls):
        return time.time()

    @classmethod
    def stamp2local(cls, timestamp):
        localtime = time.localtime(timestamp)
        return localtime

    @classmethod
    def local2str(cls, localtime, timeformat="%Y-%m-%d %H:%M:%S"):
        strtime = time.strftime(timeformat, localtime)
        return strtime

    @classmethod
    def str2local(cls, strtime, timeformat="%Y-%m-%d %H:%M:%S"):
        localtime = time.strptime(strtime, timeformat)
        return localtime


    @classmethod
    def local2stamp(cls, localtime):
        timestamp = time.mktime(localtime)
        return timestamp


if __name__ == '__main__':
    T = Timop
    t = T.current_time()

    print(t)
    l = T.stamp2local(t)
    print(l)
    l = T.local2str(l, '%Y年')
    print(l)
    l = T.str2local(l, '%Y年')
    print(l)
    l = T.local2stamp(l)
    print(l)


