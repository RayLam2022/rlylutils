# -*- coding:utf-8 -*-
# @Time    : 2022/12/9 15:17
# @Author  : Ray Lam YL

import os

import shutil

__all__ = ['ipyclear', 'print_code']


def iter_files(rootDir, keyword_a='', keyword_b=''):
    """
    按关键词遍历多层文件夹文件
    :param rootDir:
    :param keyword_a:
    :param keyword_b:
    :return:
    """
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root, file)
            if keyword_a in file_name and keyword_b in file_name:
                os.remove(file_name)

        for di in dirs:
            di_name = os.path.join(root, di)
            if keyword_a in di_name and keyword_b in di_name:
                shutil.rmtree(di_name)


def ipyclear(rootDir=r'C:\jupyter_temp_files', keyword='.ipynb_checkpoints'):
    iter_files(rootDir, keyword)

code_str= \
"""
import os

import shutil

def iter_files(rootDir, keyword_a='', keyword_b=''):
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root, file)
            if keyword_a in file_name and keyword_b in file_name:
                os.remove(file_name)

        for di in dirs:
            di_name = os.path.join(root, di)
            if keyword_a in di_name and keyword_b in di_name:
                shutil.rmtree(di_name)


def ipyclear(rootDir=r'C:\jupyter_temp_files', keyword='.ipynb_checkpoints'):
    iter_files(rootDir, keyword)


if __name__ == '__main__':
    rootDir = r'C:\jupyter_temp_files', keyword='.ipynb_checkpoints'
    ipyclear(rootDir, '.ipynb_checkpoints')
     
"""


def print_code():
    print(code_str)


if __name__ == '__main__':
    rootDir = r'C:\Users\RayLam\Desktop\新建文件夹'
    ipyclear(rootDir, '.ipynb_checkpoints')

