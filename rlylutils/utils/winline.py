# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL

import os
import os.path as osp

__all__ = ['Wline']


class Wline:
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
    def pip_src():
        contents = '[global]\ntimeout=300\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple/\n' \
                   '[install]\ntrusted-host=pypi.tuna.tsinghua.edu.cn'
        print(contents)
        home_path = osp.expanduser('~')
        pip_path = osp.join(home_path, 'pip')
        if not osp.exists(pip_path):
            os.mkdir(pip_path)
            with open(osp.join(pip_path, 'pip.ini'), 'w', encoding='utf-8') as f:
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


if __name__ == '__main__':
    Wline.conda_src()

