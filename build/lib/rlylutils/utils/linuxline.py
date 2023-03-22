# -*- coding:utf-8 -*-
# @Time    : 2022/12/10 16:00
# @Author  : Ray Lam YL

import os
import os.path as osp

__all__ = ['Lline']


class Lline:
    default = {
    }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self):

        return '【命令行】'

    def __call__(self):
        ...

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)


    @staticmethod
    def cuda_bashrc():
        contents = 'export CUDA_HOME=/usr/local/cuda\n' \
                   'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}\n' \
                   'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}'
        print(contents)

    @staticmethod
    def pip_src():
        contents = '[global]\ntimeout=300\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple/\n' \
                   '[install]\ntrusted-host=pypi.tuna.tsinghua.edu.cn'
        print(contents)
        home_path = osp.expanduser('~')
        pip_path = osp.join(home_path, '.pip')
        if not osp.exists(pip_path):
            os.mkdir(pip_path)
            with open(osp.join(pip_path, 'pip.conf'), 'w', encoding='utf-8') as f:
                f.writelines(contents)
            print('已完成pip换源')

    @staticmethod
    def conda_src():
        contents = ['ssl_verify: true\n', 'channels:\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/\n',
                    '  - http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/\n',
                    '  - defaults\n', 'show_channel_urls: true\n']
        print(contents)
        home_path = osp.expanduser('~')
        conda_path = osp.join(home_path, '.condarc')
        if not osp.exists(conda_path):
            with open(conda_path, 'w', encoding='utf-8') as f:
                f.writelines(contents)
            print('已完成conda换源')

    @staticmethod
    def apt_src():
        with open('/etc/apt/sources.list', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open('/etc/apt/sources.list.bak', 'w', encoding='utf-8') as f:
            f.writelines(lines)

        contents = ['deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal universe\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates universe\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal multiverse\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates multiverse\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security universe\n',
                    'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security multiverse']
        print(contents)
        with open('/etc/apt/sources.list', 'w', encoding='utf-8') as f:
            f.writelines(contents)


if __name__ == '__main__':
    Lline.cuda_bashrc()
