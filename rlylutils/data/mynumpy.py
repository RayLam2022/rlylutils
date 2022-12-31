# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL

import multiprocessing as mp
import math

import numpy as np

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator

__all__ = ['N2Dop']


@Decorator.cdec(Cfg.default['param'])
class N2Dop:

    default = {'src': 'image,nparray',    # 原始图像
               'center': 'center',  # 旋转中心，默认是[0,0]
               'scaler':1,
               'rotate':0,
               'delta_x':0,
               'delta_y':0
               }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【二维变换处理{}】len:{}'.format(varname, len(iterable))

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
        #多进程
        :return:
        """
        ...

    def read(self, f):
        """
        :param f:
        :return:
        """
        ...

    def last_dimen_stack(self, maxtrix_a, maxtrix_b):
        """
        末维堆叠 ，二维时是纵列堆叠
        :param maxtrix_a:
        :param maxtrix_b:
        :return: maxtrix_c
        """
        maxtrix_c = np.concatenate((maxtrix_a, maxtrix_b), axis=-1)
        return maxtrix_c

    def gen_R_2d(self):
        self.transformer = self.R_2d(self.scaler, self.rotate, self.delta_x, self.delta_y)

    def Rotate_2d(self, theta):               # 旋转
        # 弧度theta>0表示逆时针旋转；theta<0表示顺时针旋转
        return np.array([[math.cos(theta), -math.sin(theta), 0],
                        [math.sin(theta), math.cos(theta), 0],
                        [0, 0, 1]])

    def Move_2d(self, delta_x=0, delta_y=0):      # 平移
        # delta_x>0右移，delta_x<0左移
        # delta_y>0上移，delta_y<0下移
        return np.array([[1, 0, delta_x], [0, 1, delta_y], [0, 0, 1]])

    def Zoom_2d(self, scaler):               # 缩放
        # factor>1表示放大；factor<1表示缩小
        # np.eye(3) * factor
        return np.array([[scaler, 0, 0], [0, scaler, 0], [0, 0, 1]])

    def R_2d(self, scaler=1, rotate=0, delta_x=0, delta_y=0):
        R_x = self.Rotate_2d(rotate)
        R_s = self.Zoom_2d(scaler)
        R_m = self.Move_2d(delta_x, delta_y)

        R = np.matmul(R_x, R_s) #先旋转，再缩放，后平移
        R = np.matmul(R_m, R)
        return R

    def transform_2d(self, matrix):
        """
        :param matrix: 被变换向量 要先齐次再转置
        :param scaler: 绽放比例
        :param rotate: 旋转弧度，正数逆时针
        :param delta_x: 横向平移
        :param delta_y: 纵向平移
        :return: matrix_c 变换后向量
        """
        b = np.ones((matrix.shape[0], 1))
        matrix = np.concatenate((matrix,b),axis=-1)  #齐次

        R = self.transformer

        matrix_c = np.matmul(R, matrix.T)

        return matrix_c.T[:, :-1]  # 去掉齐次

    def Horizontal(self):                # 水平镜像
        self.transform = np.array([[1, 0, 0], [0, -1, self.cols-1], [0, 0, 1]])

    def Vertically(self):                # 垂直镜像
        self.transform = np.array([[-1, 0, self.rows-1], [0, 1, 0], [0, 0, 1]])

    def fangshe(self):
        return

    def toushi(self):
        return



if __name__ == '__main__':
    x = np.arange(4).reshape((2, 2))

    N2Dop.add_params(src=x, scaler=2, rotate=math.pi, delta_x=0, delta_y=2)
    n = N2Dop()
    n.gen_R_2d()
    print(x)
    m = n.transform_2d(x)

    print(m)


