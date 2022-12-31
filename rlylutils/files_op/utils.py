# -*- coding:utf-8 -*-
# @Time    : 2022/12/10 15:55
# @Author  : Ray Lam YL

import os
import os.path as osp
from glob import glob
from pathlib import Path


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
                yield file_name


def iter_dirs(rootDir, keyword_a='', keyword_b=''):
    """
    按关键词遍历多层文件夹
    :param rootDir:
    :param keyword_a:
    :param keyword_b:
    :return:
    """
    for root, dirs, files in os.walk(rootDir):
        for di in dirs:
            di_name = os.path.join(root, di)
            if keyword_a in di_name and keyword_b in di_name:
                yield di_name


def iter_child_dirs(rootDir, resDir, layers=0, file_exten_name='.png'):
    """
    可指定源根目录下第几层下的子文件夹，glob搜索指定扩展名的文件，
    拼接目标根目录，无子文件夹层次则自动创建，

    :param rootDir: 源根目录
    :param resDir: 目标根目录
    :param layers: 范围仅根目录下第n层单层文件
    :param file_exten_name: 扩展名
    :return: 列表 [(srcfile1,tgtfile1),(srcfile2,tgtfile2)...]
    """
    lis = []
    dir_set = set()

    if not osp.isabs(rootDir):
        rootDir = osp.abspath(rootDir)
    root_len = len(rootDir)
    # print(rootDir[:root_len])
    if not osp.isabs(resDir):
        resDir = osp.abspath(resDir)

    src = rootDir
    if layers > 0:
        for layer in range(layers):
            src = osp.join(src, '*')

    srcfiles = glob(osp.join(src, '*' + file_exten_name))
    for f_src in srcfiles:
        f_tgt = resDir + f_src[root_len:]
        lis.append((f_src, f_tgt))
        dir_set.add(osp.dirname(f_tgt))
    for d in dir_set:
        if not osp.exists(d):
            os.makedirs(d)
    return lis


def pairing_check(dir1, dir2, exten1=['.jpg', '.png'], exten2=['.json']):
    """
    不同文件夹同名成对文件检测与输出,扩展名仅作分别文件筛选，配对上只配对名称，不配对扩展名
    :param dir1:
    :param dir2:
    :param exten1:
    :param exten2:
    :return: paired_list [(paired dir1file1, paired dir2file1),(paired dir1file2, paired dir2file2)...]  ,notpaired_dir1filelist [...]
    """
    paired_list = []
    notpaired_dir1_files = set()

    temp_list = []
    for ext in exten1:
        temp_list.extend(glob(osp.join(dir1, '*' + ext)))
    for f in temp_list:
        name = osp.splitext(osp.basename(f))[0]
        for ex in exten2:
            dir2file = osp.join(dir2, name + ex)
            if osp.exists(dir2file):
                paired_list.append((f, dir2file))
            else:
                notpaired_dir1_files.add(f)
    return paired_list, list(notpaired_dir1_files)


class DirectionTree:
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """

    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            # self.tree += '    |' * n + '-' * 4 + self.pathname.name + '\n'
            ...
        elif self.pathname.is_dir():
            self.tree += '    |' * n + '-' * 4 + \
                str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)


if __name__ == '__main__':
    rootDir = r'D:\work\py\my yolo-EM\my yolo-EM\img\val'
    resDir = r'D:\work\py\my yolo-EM\my yolo-EM\ei\val'
    #x,y = pairing_check(rootDir, resDir, exten1=['.png'], exten2=['.json'])
    #print(x)
    #print(y)

    dirtree = DirectionTree()
    dirtree.set_path(resDir)
    dirtree.generate_tree()
    print(dirtree.tree)
