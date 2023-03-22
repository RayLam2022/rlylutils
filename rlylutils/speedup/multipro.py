# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL


import multiprocessing as mp
import time
import psutil
from tqdm import tqdm

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator

__all__ = ['Multipro']

@Decorator.cdec(Cfg.default['param'])
class Multipro:
    '''
    多进程在jupyter会报错或无返回数据，要生成py再运行，且win多进程要有if __name__=='__main__':
    '''
    default = {'Author': 'Ray Lam LYL',
             'cpuphy_count':psutil.cpu_count(logical=False),
             'cpulog_count':psutil.cpu_count(logical=True)
                }
    
    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self,f):
        ...
        
    def __str__(self, varname, iterable):
      
        return '【多进程{}】len:{}'.format(varname, len(iterable))
    
    def namestr(self, obj, namespace):
        '''
        变量名转字符串
        #例（变量名，globals()）
        '''
        return [name for name in namespace if namespace[name] is obj][0]
    
    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)
    
    def multiprolist_assitant(self, mgrd, func, tasklist, task_in, idx, iter_funparams_name, **kwargs):
        '''
        多进程：辅助加入mgr.list()数据传递接口
        '''
        kwargs.update({iter_funparams_name: task_in})
        res = func(**kwargs) #单元被多进程的函数，输入列表单元，要放第一参数
        mgrd[idx] = res
        return mgrd

    def multipro_list(self, func, iter_funparams_name, tasklist, workers_num=4, **kwargs):
        '''
        传入列表，返回列表[func(listitem1),func(listitem2)....]
        多进程：字典变量传递  (多进程mgr.list()参数传递顺序经测试不准确，只采用字典方式代替)
        第二参数是被多进程的func函数要迭代的参数名，此处示例以func的第三参数"c"为迭代对象
        要求使用此多进程的函数，要将函数没有默认值的参数全部按如下填在mul.multipro_list的参数workers_num后
        
        def func(a,b,c,d=3):
            pass
        
        if __name__=='__main__':
            mul=Multi()
            tlist=[2,5,8,0,10,3,1,98,3]
            y=mul.multipro_list(task,'c',tlist,workers_num=6,a=2,b=2,c=3)    
        func()
        '''
        mgr = mp.Manager()
        mgrd = mgr.dict()
        jobs = [mp.Process(target=self.multiprolist_assitant, 
                           # args=(mgrd,func,tasklist,*args),
                           kwargs={'mgrd': mgrd,
                                   'func': func,
                                   'tasklist': tasklist,
                                   'task_in': task_in,
                                   'idx': str(idx),
                                   'iter_funparams_name': iter_funparams_name,
                                   **kwargs}) 
                for idx, task_in in enumerate(tasklist)]
        
        for i in tqdm(range(0, len(jobs), workers_num)):
            job = jobs[i:i+workers_num]
            print(job)
            for j in job:
                j.start()
            for j in job:
                j.join()
        mgrd = dict(mgrd)
        flatdic = sorted(mgrd.items(), key=lambda d: int(d[0]), reverse=False)
        flatlis = [i[1] for i in flatdic]
        print('multiprolist Done')
        return flatlis
        
    def multiprolist_assitant_noreturn(self, func, tasklist, task_in, idx, iter_funparams_name, **kwargs):
        '''
        多进程：辅助加入mgr.list()数据传递接口
        '''
        kwargs.update({iter_funparams_name: task_in})
        func(**kwargs) #单元被多进程的函数，输入列表单元，要放第一参数

    def multipro_list_noreturn(self, func, iter_funparams_name, tasklist, workers_num=4, **kwargs):
        '''
        多进程：无变量传递
        '''

        jobs = [mp.Process(target=self.multiprolist_assitant_noreturn, 
                           # args=(mgrd,func,tasklist,*args),
                           kwargs={
                                   'func': func,
                                   'tasklist': tasklist,
                                   'task_in': task_in,
                                    'idx': str(idx),
                                   'iter_funparams_name': iter_funparams_name,
                                   **kwargs}) 
                for idx, task_in in enumerate(tasklist)]
        
        for i in tqdm(range(0, len(jobs), workers_num)):
            job = jobs[i:i+workers_num]
            print(job)
            for j in job:
                j.start()
            for j in job:
                j.join()
        print('multiprolist_noreturn Done')

    def multiprodict_key_assitant(self, mgrd, func, tasklist, task_in, iter_funparams_name, **kwargs):
        '''
        多进程：辅助加入mgr.list()数据传递接口
        '''
        kwargs.update({iter_funparams_name: tasklist[task_in]})
        res = func(**kwargs) #单元被多进程的函数，输入列表单元，要放第一参数
        mgrd[task_in] = res
        return mgrd

    def multipro_dic_key(self, func, iter_funparams_name, tasklist, workers_num=4, **kwargs):
        '''
        循环字典传入字典值，被多进程函数参数传入有字典val一个参数进行处理，而函数会返回{key1:fun(val1),key2:fun(val2)....}
        多进程：字典变量传递  (多进程mgr.list()参数传递顺序经测试不准确，只采用字典方式代替)
        第二参数是被多进程的func函数要迭代的参数名，此处示例以func的第三参数"c"为迭代对象
        要求使用此多进程的函数，要将函数没有默认值的参数全部按如下填在mul.multipro_dic的参数workers_num后
        
        def func(a,b,c,d=3):
            pass
        
        if __name__=='__main__':
            mul=Multi()
            tlist=[2,5,8,0,10,3,1,98,3]
            y=mul.multipro_dic(task,'c',tlist,workers_num=6,a=2,b=2,c=3)    
        func()
        '''
        mgr = mp.Manager()
        mgrd = mgr.dict()
        jobs = [mp.Process(target=self.multiprodict_key_assitant, 
                           # args=(mgrd,func,tasklist,*args),
                           kwargs={'mgrd': mgrd,
                                   'func': func,
                                   'tasklist': tasklist,
                                   'task_in': task_in,
                                   'iter_funparams_name': iter_funparams_name,
                                   **kwargs}) 
                for task_in in tasklist.keys()]
        
        for i in tqdm(range(0, len(jobs), workers_num)):
            job = jobs[i:i+workers_num]
            print(job)
            for j in job:
                j.start()
            for j in job:
                j.join()
        mgrd = dict(mgrd)

        print('multiprodickey Done')
        return mgrd   
    
    def multiprodict_item_assitant(self, mgrd, func, tasklist, task_in_key, task_in_val, iter_funparams_name_key, iter_funparams_name_val, **kwargs):
        '''
        多进程：辅助加入mgr.list()数据传递接口
        '''
        kwargs.update({iter_funparams_name_key: task_in_key, iter_funparams_name_val: task_in_val})
        res = func(**kwargs) #单元被多进程的函数，输入列表单元，要放第一参数
        mgrd[task_in_key] = res
        return mgrd

    def multipro_dic_item(self, func, iter_funparams_name_key, iter_funparams_name_val, tasklist, workers_num=4, **kwargs):
        '''
        循环字典，被多进程函数参数传入有字典key,val两个参数，返回{key1:func(key1,val1),key2:func(key2,val2)...}
        多进程：字典变量传递  (多进程mgr.list()参数传递顺序经测试不准确，只采用字典方式代替)
        第二参数是被多进程的func函数要迭代的参数名，此处示例以func的第三参数"c"为迭代对象
        要求使用此多进程的函数，要将函数没有默认值的参数全部按如下填在mul.multipro_dic的参数workers_num后
        
        def func(a,b,key,val=3):
            pass
        
        if __name__=='__main__':
            mul=Multi()
            tlist={'m':2,'n':5,'k':8}
            y=mul.multipro_dic_item(task,'key','val',tlist,workers_num=6,a=2,b=2,c=3)    
        func()
        '''
        mgr = mp.Manager()
        mgrd = mgr.dict()
        jobs = [mp.Process(target=self.multiprodict_item_assitant, 
                           # args=(mgrd,func,tasklist,*args),
                           kwargs={'mgrd': mgrd,
                                   'func': func,
                                   'tasklist': tasklist,
                                   'task_in_key': task_in_key,
                                   'task_in_val': task_in_val,
                                   'iter_funparams_name_key': iter_funparams_name_key,
                                   'iter_funparams_name_val': iter_funparams_name_val,
                                   **kwargs}) 
                for task_in_key, task_in_val in tasklist.items()]
        print(jobs)
        for i in tqdm(range(0, len(jobs), workers_num)):
            job = jobs[i:i+workers_num]
            print(job)
            # for j in job:
            #     j.daemon = True
            for j in job:
                j.start()
            for j in job:
                j.join()
            
        mgrd = dict(mgrd)

        print('multiprodickey Done')
        return mgrd   
    

def task(x, a):
    time.sleep(3)
    print(x)
    print(a)
    return a*3


if __name__ == '__main__':
    t = time.time()
    mul = Multipro()

    tlist = [2,5,8,0,10,3,1,98,3]
    
    y = mul.multipro_list(task, 'x', tlist, workers_num=6, a=12)
    # for i in range(len(tlist)):
    #     y.append(task(tlist[i]))
    print(y)
    print(time.time()-t)
    