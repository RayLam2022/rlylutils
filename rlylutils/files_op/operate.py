# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL

import os
import os.path as osp
import re
import sys
from glob import glob
import shutil
import multiprocessing as mp
import json
from importlib import import_module


try:
    ijson = import_module('ijson')
    scio = import_module('scipy.io')
except Exception as e:
    os.system(f'{sys.executable} -m pip install ijson')
    ijson = import_module('ijson')
    os.system(f'{sys.executable} -m pip install scipy')
    scio = import_module('scipy.io')


from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.files_op.utils import *

__all__ = ['Findop', 'Filesop', 'Jsonop', 'Txtop', 'Matop']


@Decorator.cdec(Cfg.default['param'])
class Findop:
    default = {
              }
    
    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...
        
    def __str__(self, varname, iterable):
      
        return '【文件及内容查找通用处理{}】len:{}'.format(varname, len(iterable))
    
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
        
    def multulayer_find_content(self, path, findpartcontent, exten=['.txt', '.xml', '.json'], coding='utf-8'):
        """
        多层级文件夹所有文件搜查指定内容
        :param path:
        :param findpartcontent:
        :param exten:
        :param coding:
        :return:
        """
        result = os.listdir(path)

        for res in result:         # for 循环判断递归查到的内容是文件夹还是文件
            p = osp.join(path, res)
            if osp.isdir(p):    # 若是文件夹，继续将该文件夹的路径传给 search() 函数继续递归查找
                yield from self.multulayer_find_content(p, findpartcontent, exten, coding)
            elif osp.splitext(res)[-1] in exten:  
                f = open(p, 'r', encoding=coding)         # 利用 open() 函数读取文件，并通过 try...except... 捕获不可读的文件格式（.zip 格式）
                # print(f.read())
                try:
                    content = f.read()
                    if findpartcontent in content:
                        yield p
                except:
                    print('这是不可读文件格式的文件的所在路径：{} '.format(p))
                    continue
                finally:
                    f.close()

    def singlayer_find_files(self, path, findpartname, exten=['.jpg', '.png']):
        """
        单一层文件夹内查找指定名文件
        :param path:
        :param findpartname:
        :param exten:
        :return:
        """
        # files = list(filter(lambda f: re.search('[xls|txt]$', f),files))
        result = os.listdir(path)
        for res in result:
            if findpartname in res and osp.splitext(path)[-1] in exten:
                yield res
            
    def multilayer_find_files(self, path, findpartname, exten=['.jpg', '.png']):
        """
        【生成器：任意格式文件名查找】
        使用：要先创建
        定义 search() 函数，传入 "path" 文件路径， "findpartname" 要查找的目标文件部分连续字符

        获取当前路径下所有内容
        判断每个内容的类型（文件夹还是文件）
        若是文件夹则继续递归查找
        :param path:
        :param findpartname:
        :param exten:
        :return:
        """

        result = os.listdir(path)

        for res in result:         # for 循环判断递归查到的内容是文件夹还是文件
            p = osp.join(path, res)
            if osp.isdir(p):    # 若是文件夹，继续将该文件夹的路径传给 search() 函数继续递归查找
                yield from self.multilayer_find_files(p, findpartname, exten)
            elif findpartname in res and osp.splitext(res)[-1] in exten:        # 若是文件，则将该查询到的文件所在路径插入 final_result 空列表
                yield p


@Decorator.cdec(Cfg.default['param'])
class Filesop:
    default = {
              }
    
    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...
        
    def __str__(self, varname, iterable):
      
        return '【文件通用处理{}】len:{}'.format(varname, len(iterable))

    def __call__(self):
        ...
    
    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)
    
    def process(self):
        ...
    
    def namestr(self, obj, namespace):
        # 例（变量名，globals()）
        """
        变量名转字符串
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

    def abspath(self, path):
        return osp.abspath(path)
    
    def getcwd(self):
        """
        R
        :return:
        """
        return os.getcwd()
        
    def copy_file(self, source, target):
        print(source)
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("File{} Unable to copy.{}".format(source, e))
        else:
            print("File {} Unexpected error:{}".format(source, sys.exc_info()))

    def rename(self, source, target):
        """
        重命名目录或文件
        :param source:
        :param target:
        :return:
        """
        try:
            os.rename(source, target)
        except Exception as e:
            print('{}未成功重命名,错误信息：{}'.format(source, repr(e)))
        
    def getsize(self, f):
        """
        获取文件大小
        :param f:
        :return: MB
        """
        size = osp.getsize(f)
        size = size / (1024 * 1024)
        return round(size, 2)
        
    def remove(self, f):
        """
        删除文件
        :param f:
        :return:
        """
        try:
            os.remove(f)
        except Exception as e:
            print('{}未成功删除,错误信息：{}'.format(f,repr(e)))
            
    def makedirs(dir_path):
        """
        创建目录路径
        :return:
        """

        if not osp.exist(dir_path):
            os.makedirs(dir_path)
            print(''.format('创建了文件目录路径：{}'.format(dir_path)))
            
    def copytree(self, source, target, symlinks=False):
        """
        把olddir拷贝一份newdir，
        如果 symlinks 为真值，源目录树中的符号链接会在新目录树中表示为符号链接，并且原链接的元数据在平台允许的情况下也会被拷贝；如果为假值或省略，则会将被链接文件的内容和元数据拷贝到新目录树。
        R
        :param source:
        :param target:
        :param symlinks:
        :return:
        """
        print('正复制目录路径{}内所有内容至{}:'.format(source, target))
        shutil.copytree(source, target, symlinks)
    
    def rmtree(self, path):
        """
        递归删除一个目录以及目录内的所有内容
        R
        :param path:
        :return:
        """
        if osp.exists(path):
            shutil.rmtree(path)
            print('已删除目录路径:{}'.format(path))
        else:
            print('不存在目录路径：{}'.format(path))

    def singlelayer_dirs(self, rootDir):
        path = os.listdir(rootDir)
        dp_list = []
        for p in path:
            if osp.isdir(osp.join(rootDir,p)):
                dp_list.append(p)
        return dp_list

    def singlelayer_files(self, rootDir):
        path = os.listdir(rootDir)
        fp_list = []
        for p in path:
            if not osp.isdir(osp.join(rootDir, p)):
                fp_list.append(p)
        return fp_list

    def iter_child_dirs(self, rootDir, resDir, layers=0, file_exten_name='.png'):
        """
        可指定源根目录下第几层下的子文件夹，glob搜索指定扩展名的文件，
        拼接目标根目录，无子文件夹层次则自动创建，

        :param rootDir: 源根目录
        :param resDir: 目标根目录
        :param layers: 范围仅根目录下第n层单层文件
        :param file_exten_name: 扩展名
        :return: 列表 [(srcfile1,tgtfile1),(srcfile2,tgtfile2)...]
        """
        return iter_child_dirs(rootDir, resDir, layers, file_exten_name)

    def iter_files(self, rootDir, keyword_a='', keyword_b=''):
         return iter_files(rootDir, keyword_a, keyword_b)

    def pairing_check(self, dir1, dir2, exten1=['.jpg', '.png'], exten2=['.json']):
        paired_list, notpaired_list = pairing_check(dir1, dir2, exten1, exten2)
        return paired_list, notpaired_list

    def directionTree(self, rootDir):
        """
        生成目录文件夹树
        :param rootDir:
        :return: str
        """
        dirtree = DirectionTree()
        dirtree.set_path(rootDir)
        dirtree.generate_tree()
        return dirtree.tree

    def generate_root(self, rootDir=r'D:\work\py\2022061220\ori', find_file_exten=['.xml']):
        """
        对根目录，按目录结构生成另一根目录及有指定扩展名文件和其所在文件夹
        :param rootDir:
        :param find_file_exten:
        :return:
        """
        outputpath = osp.join(osp.dirname(rootDir), 'new0_'+osp.basename(rootDir))
        for root, dirs, files in os.walk(rootDir):
            for file in files:
                # print('ori',root)
                # print('new',root.replace(rootDir,outputpath))
                if osp.splitext(file)[-1] in find_file_exten:
                    new_root = root.replace(rootDir, outputpath)  # 要小心这句斜杠问题

                    if osp.exists(new_root) == False:
                        os.makedirs(new_root)
                    source = osp.join(root, file)
                    target = osp.join(new_root, file)
                    try:
                        shutil.copy(source, target)
                    except:
                        print("File{} Unable to copy.".format(file))


@Decorator.cdec(Cfg.default['param'])
class Txtop(Filesop):
    
    def __new__(cls, *args, **kw):
        """
        共享父类default属性
        :param args:
        :param kw:
        """
        ob = super().__new__(cls, *args, **kw)
        ob.default = cls.default
        return ob
    
    def __iter__(self):
        ...

    def readline(self, f, coding='utf-8'):
        """
        文件逐行读取R
        :param f: 
        :param coding: 
        :return: 
        """
        with open(f, 'r', encoding=coding) as f:
            line = f.readline()
            while line:
                yield line
                line = f.readline()
                
    def big_file(self, filepath, readlenth=20000, coding='utf-8'):
        """
        未test:读取大文件,现仅读取了部分,待完善
        """

        with open(filepath, 'r', encoding=coding) as f:
            data = f.read(readlenth)
        return data
    
    def add_contents(self, filepath, contents, conding='utf-8'):
        """
        追加内容
        :param filepath:
        :param contents:
        :param conding:
        :return:
        """

        with open(filepath, mode='a', encoding=conding) as txt_file:
            txt_file.writelines(contents)
    
    def write(self, filepath, contents, conding='utf-8'):
        """
        覆写文件
        :param filepath:
        :param contents:
        :param conding:
        :return:
        """
        with open(filepath, mode='w', encoding=conding) as txt_file:
            txt_file.writelines(contents)


@Decorator.cdec(Cfg.default['param'])
class Jsonop(Filesop):
    
    def __new__(cls, *args, **kw):
        """
        共享父类default属性
        :param args:
        :param kw:
        """
        ob = super().__new__(cls, *args, **kw)
        ob.default = super().default
        # ob.add_params = super().add_params
        return ob

    def __init__(self):
        super().__init__()

    def __iter__(self):
        ...
                   
    def read_big_json(self, filepath, find='item.america.item', coding='utf-8'):
        """
        读取大文件json，find中item代表列，格式为按迭代列表item和字典的key顺序找到要迭代的列表item
        :param filepath:
        :param find:
        :param coding:
        :return:
        """
        with open(filepath, 'r', encoding=coding) as f:
            obj = ijson.items(f, find) 
            for ob in obj:
                yield ob
                
    def read(self, filepath, coding='utf-8'):
        """
        读取json
        :param filepath:
        :param coding:
        :return:
        """
        with open(filepath, "r", encoding=coding) as jsonFile:
            data = json.load(jsonFile)  
        return data
        
    def write(self, filepath, json_content, coding='utf-8', indent=None):
        """
        写入json R
        :param filepath:
        :param json_content:
        :param coding:
        :param indent:
        :return:
        """
        with open(filepath, "w", encoding=coding) as jsonFile:
            json.dump(json_content, jsonFile, ensure_ascii=False, indent=indent)
            
        
@Decorator.cdec(Cfg.default['param'])
class Matop(Filesop):
    """

    """
    def __new__(cls, *args, **kw):
        ob = super().__new__(cls, *args, **kw)
        ob.default = cls.default
        return ob

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return
                   
    def read(self, path):
        data = scio.loadmat(path)
        print('mat_keys:', data.keys())
        return data
    
    def write(self, path, data):
        scio.savemat(path, data)






