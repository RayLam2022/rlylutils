# -*- coding:utf-8 -*-
# @Time    : 2022/12/11 23:04
# @Author  : Ray Lam YL

import os
import os.path as osp
import sys
import time
import platform
from importlib import import_module

try:
    pynvml = import_module('pynvml')
except:
    os.system(f'{sys.executable} -m pip install nvidia-ml-py3')
    print('Installing nvidia-ml-py3,if failed,pip install nvidia-ml-py')
    pynvml = import_module('pynvml')


__all__ = ['general_info', 'gpu_info']


def general_info():
    print(f'platform:{platform.uname()}')
    print(f'cwd:{os.getcwd()}')
    print(f"(.):{osp.abspath('.')}")
    print(f"user:{osp.expanduser('~')}")

    try:
        s = "".join(os.popen('python -V').readlines())
    except:
        s = 'no python'
    finally:
        print(f"{s}")

    s = "".join(os.popen(f'{sys.executable} -V').readlines())
    print(f"{s}")
    print(f"ppath:{sys.executable}")
    print('-'*50)
    try:
        s = "".join(os.popen('nvcc -V').readlines())
    except:
        s = 'no cuda'
    finally:
        print(f"cuda:\n{s}")

def get_gpu_device():
    deviceCount = pynvml.nvmlDeviceGetCount()
    gpu_list = []
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        print("GPU", i, ":", pynvml.nvmlDeviceGetName(handle))
        gpu_list.append(i)
    return gpu_list


def get_gpu_info(gpu_id):
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    M = 1024**2
    gpu_info = "id:{}  total:{}M free:{}M  used:{}M free_rate:{}%".format(gpu_id, info.total/M, info.free/M, info.used/M, get_free_rate(gpu_id))
    return gpu_info


def release():
        #最后要关闭管理工具
    pynvml.nvmlShutdown()


def get_free_rate(gpu_id):
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    free_rate = int((info.free / info.total) * 100)
    return free_rate


def gpu_info(keeptime=3):
    """
    :param keeptime: minutes
    :return:
    """
    start = time.time()

    while True:
        pynvml.nvmlInit()
        gpu_devices = get_gpu_device()
        for gpuid in gpu_devices:
            print(get_gpu_info(gpuid))
        release()
        time.sleep(3)
        if time.time()-start > 60 * keeptime:
            break

if __name__ == '__main__':
    general_info()
    gpu_info()


