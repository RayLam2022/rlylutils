# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL

import multiprocessing as mp
import math

import numpy as np

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator

__all__ = ['N3Dop']


@Decorator.cdec(Cfg.default['param'])
class N3Dop:

    default = {'src': 'image,nparray',    # 原始图像
               'center': [0, 0, 0],  # 旋转中心，默认是
               'camera': [1, 1, 1],
               'camera_cali': [],  # 相机标定参数
               'scaler_x': 1,
               'scaler_y': 1,
               'scaler_z': 1,
               'rotate_alpha': math.pi * 0.5,
               'rotate_beta': 0,
               'rotate_gamma': math.pi * 0.5,
               'default_rotate_seq': 'ZYX', #默认旋转顺序，排头优先
               'delta_x': 0,
               'delta_y': 1,
               'delta_z': 0
               }

    def __init__(self):
        self.__dict__.update(self.default)
        self.rot_seq = {'X': self.Rotate_x(),
                        'Y': self.Rotate_y(),
                        'Z': self.Rotate_z()
                        }
        self.transformer = self.R_3d()

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【三维变换处理{}】len:{}'.format(varname, len(iterable))

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

    def Rotate_x(self):
        # 弧度  >0表示逆时针旋转； <0表示顺时针旋转
        theta = self.rotate_alpha
        return np.array([[1, 0, 0, 0],
                         [0, math.cos(theta), -math.sin(theta), 0],
                         [0, math.sin(theta), math.cos(theta), 0],
                         [0, 0, 0, 1]])

    def Rotate_y(self):
        # 弧度>0表示逆时针旋转；<0表示顺时针旋转
        theta = self.rotate_beta
        return np.array([[math.cos(theta), 0, math.sin(theta), 0],
                         [0, 1, 0, 0],
                         [-math.sin(theta), 0, math.cos(theta), 0],
                         [0, 0, 0, 1]])

    def Rotate_z(self):
        # 弧度>0表示逆时针
        theta = self.rotate_gamma
        return np.array([[math.cos(theta), -math.sin(theta), 0, 0],
                         [math.sin(theta), math.cos(theta), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    def Move_3d(self):  # 平移
        # delta>0远离原点
        return np.array([[1, 0, 0, self.delta_x],
                         [0, 1, 0, self.delta_y],
                         [0, 0, 1, self.delta_z],
                         [0, 0, 0, 1]])

    def Zoom_3d(self):  # 缩放
        # factor>1表示放大；factor<1表示缩小
        # np.eye(4) * factor
        return np.array([[self.scaler_x, 0, 0, 0],
                         [0, self.scaler_y, 0, 0],
                         [0, 0, self.scaler_z, 0],
                         [0, 0, 0, 1]])

    def R_3d(self):
        seq = self.default_rotate_seq
        R_r = np.matmul(self.rot_seq[seq[1]], self.rot_seq[seq[0]])
        R_r = np.matmul(self.rot_seq[seq[2]], R_r)

        R_s = self.Zoom_3d()
        R_t = self.Move_3d()

        R = np.matmul(R_r, R_s)  # 先旋转，再绽放，后平移
        R = np.matmul(R_t, R)
        return R

    def transform_3d(self, matrix):
        """
               'scaler_x': 1,
               'scaler_y': 1,
               'scaler_z': 1,
               'rotate_alpha': 0,
               'rotate_beta': 0,
               'rotate_gamma': 0,
               'delta_x': 0,
               'delta_y': 0,
               'delta_z': 0
        """
        b = np.ones((matrix.shape[0], 1))
        matrix = np.concatenate((matrix, b), axis=-1)  # 齐次

        R = self.transformer

        matrix_c = np.matmul(R, matrix.T)

        return matrix_c.T[:, :-1]  # 去掉齐次


if __name__ == '__main__':
    import open3d as o3d

    N3Dop.add_params(center=[0, 0, 0],
                     camera=[1, 1, 1],
                     camera_cali=[],  # 相机标定参数
                     scaler_x=1,
                     scaler_y=1,
                     scaler_z=1,
                     rotate_alpha=math.pi / 2,
                     rotate_beta=0,
                     rotate_gamma=math.pi / 2,
                     default_rotate_seq='ZYX',  # 默认旋转顺序，排头优先
                     delta_x=0,
                     delta_y=1,
                     delta_z=0)

    no = N3Dop()
    np.random.seed(2)
    p = np.random.random(size=(1000, 3))

    # p=np.array([[2,0,0],[3,0,0]])

    p_convert = no.transform_3d(p)


