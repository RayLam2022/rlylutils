# -*- coding:utf-8 -*-
# @Time    : 2022/12/18 1:56
# @Author  : Ray Lam YL


import multiprocessing as mp
import math

import numpy as np

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator

__all__ = ['Dataop']


@Decorator.cdec(Cfg.default['param'])
class Dataop:
    default = {
    }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【数据处理{}】len:{}'.format(varname, len(iterable))

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)

    def process(self):
        ...

    def namestr(self, obj, namespace):
        """
        变量名转字符串
        #例（变量名，globals()）
        :param obj:
        :param namespace:
        :return:
        """

        return [name for name in namespace if namespace[name] is obj][0]

    def multiprocess(self):
        """
        多进程
        :return:
        """
        ...

    def clamp(self, n, smallest, largest):
        """
        数据截取
        :param n:
        :param smallest:
        :param largest:
        :return:
        """
        return max(smallest, min(n, largest))
