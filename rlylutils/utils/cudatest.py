# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL


import timeit
from importlib import import_module

__all__ = ['cudatest']


def torchtest(tor):
    print(tor.__version__)
    x = tor.Tensor([1.0])
    xx = x.cuda()
    print(xx)
    print(tor.backends.cudnn.is_acceptable(xx))

def tftest(tf):

    print(tf.test.is_gpu_available())
    print(tf.test.is_built_with_cuda())

    with tf.device("/cpu:0"):
        cpu_a = tf.random.normal([10000, 1000])
        cpu_b = tf.random.normal([1000, 2000])
        print(cpu_a.device, cpu_b.device)

    with tf.device("/gpu:0"):
        gpu_a = tf.random.normal([10000, 1000])
        gpu_b = tf.random.normal([1000, 2000])
        print(gpu_a.device, gpu_b.device)

    def cpu_run():
        with tf.device("/cpu:0"):
            c = tf.matmul(cpu_a, cpu_b)
        return c

    def gpu_run():
        with tf.device("/gpu:0"):
            c = tf.matmul(gpu_a, gpu_b)
        return c

    # warm up
    cpu_time = timeit.timeit(cpu_run, number=10)
    gpu_time = timeit.timeit(gpu_run, number=10)
    print("warmup:", cpu_time, gpu_time)

    cpu_time = timeit.timeit(cpu_run, number=10)
    gpu_time = timeit.timeit(gpu_run, number=10)
    print("run time:", cpu_time, gpu_time)


try:
    tor = import_module('torch')
    torv = import_module('torchvision')
    print('torchvision version', torv.__version__)
    torchtest(tor)
except:
    print('torch或torchvision异常，或是未安装')

try:
    ten = import_module('tensorflow')
    tftest(ten)
except:
    print('tensorflow异常，或是未安装')

