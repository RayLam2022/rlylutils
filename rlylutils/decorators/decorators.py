import time
import datetime
from inspect import signature

__all__ = ['Decorator']

class Decorator:
    
    default = {'Author': 'Ray Lam LYL',
               'd': datetime.date.today().strftime('%y%m%d')
               }
    
    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...
        
    def __str__(self, varname, iterable):
      
        return '【装饰器处理{}】len:{}'.format(varname, len(iterable))
    
    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)  
        

    @classmethod
    def check_type(self, *ty_args, **ty_kwargs):
        '''
        检查参数类型装饰器
        '''
        def out_wrapper(func):
            # 通过signature方法，获取函数形参：name, age, height
            sig = signature(func)
            # 获得装饰器传来的参数， 函数签名与之绑定，字典类型
            bind_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
            # print('bind_types',bind_types)

            def wrapper(*args, **kwargs):
                # 给执行函数中具体的实参进行和形参进行绑定，形成字典的形式
                func_type = sig.bind(*args, **kwargs).arguments.items()
                # print('func_type',func_type)
                # 循环形参和实参字典的items()形式

                for name, obj in func_type:
                    if name in bind_types:
                        # print('obj',obj)
                        if not isinstance(obj, bind_types[name]):
                            raise TypeError("%s must be %s" % (name, bind_types[name]))
                res = func(*args, **kwargs)
                return res

            return wrapper

        return out_wrapper

    @classmethod
    def argsfunc_assist(cls, argname, bind_args, func_args):
        """
        改此处即可通过设置装饰器直接干涉传入函数的所有参数值,argname为原函数参数名，bind_args为装饰器的值，func_args为原函数参数值
        :param argname:
        :param bind_args:
        :param func_args:
        :return:
        """
        print('c', argname, func_args)
        if argname == 'name':

            bind_args += func_args
        return bind_args

    @classmethod
    def changeparams(self, *ty_args, **ty_kwargs):
        '''
        demo,一般要继承后修改
        函数传入参数批处理装饰器,通过设置cls.argsfunc_assist直接干涉传入函数的所有参数值
        '''
        def out_wrapper(func):
            sig = signature(func)

            bind_args = sig.bind_partial(*ty_args, **ty_kwargs).arguments

            def wrapper(*args, **kwargs):
                func_args = sig.bind(*args, **kwargs).arguments.items()
                func_args = {ft[0]: ft[1] for ft in func_args}
                # print('func_args',func_args)
                # print('bind_args', bind_args)
                for name, obj in func_args.items():
                    if name in bind_args:
                        # print(obj,'--', bind_args[name])
                        func_args[name] = Decorator.argsfunc_assist(name, bind_args[name], obj)
                # res = func(*args, **kwargs)
                res = func(**func_args)
                return res
            return wrapper
        return out_wrapper

    @classmethod
    def dec(cls, inp):
        def outwrap(func):
            def wrapper(*args, **kwargs):
                if (int(cls.default['d'][2:4])+int(cls.default['d'][4:6])) + 21 == inp:
                    res = func(*args, **kwargs)
                    return res
            return wrapper
        return outwrap

    @classmethod
    def cdec(cls, inp):
        def outwrap(dcls):
            if (int(cls.default['d'][2:4])+int(cls.default['d'][4:6])) + 21 == inp:
                class wrapper (dcls):
                    # loop = 7 #加属性
                    ...
                return wrapper

            else:
                return None
        return outwrap


if __name__ == "__main__":
    ...
    # 通过装饰器实现对函数参数进行类型检查
    # print(h.loop)
    # ha

    # @Decorator.dec(60)
    # def a(c):
    #     print(c + 5)
    #     return c + 8
    # d=a(3)
    # print(d)
    #
    # @Decorator.check_type(str, int, type(None))
    # def func(name, age, height):
    #     print(name, age, height)
    #     return (name, age, height)
    #
    #
    # @Decorator.changeparams(1, 2, type(None))
    # def func1(name, age, height):
    #     print(name, age, height)
    #     # return(name, age, height)
    #
    # #res = func("bei_men", 18, None)
    # res = func1(5, 18, None)
    # print('res',res)
    


'''    
#多层装饰器
def outer1(func1):
    print('加载了outer1')
    def wrapper1(*args,**kwargs):
        print('执行了wrapper1')
        res1 = func1(*args,**kwargs)
        return res1
    return wrapper1

def outer2(func2):
    print('加载了outer2')
    def wrapper2(*args,**kwargs):
        print('执行了wrapper2')
        res2 = func2(*args,**kwargs)
        return res2
    return wrapper2

def outer3(func3):
    print ('加载了outer3')
    def wrapper3(*args,**kwargs):
        print('执行了warpper3')
        res3 = func3(*args,**kwargs)
        return res3
    return wrapper3

def index():
    print('from index')

wrapper3 = outer3(index)
wrapper2 = outer2(wrapper3)
indexy = outer1(wrapper2)
indexy()

# 多层语法糖解读顺序是先看语法糖有几个，然后再由下往上去看，遇到最后一个才会使用相同的变量名传给装饰器函数使用
# 语法糖三：wrapper3 = outer3(index),加载了outer3
# 语法糖二：wrapper2 = outer2(wrapper3)，加载了outer2
# 语法糖一；index = outer1(wrapper2),加载了outer1
# 执行顺序就是：wrapper1>>>>>wrapper2>>>>>wrapper3
# 加载outer3>>>加载outer2>>>加载outer1>>>index()>>>运行wrapper1函数体代码
# >>>然后再执行outer2函数体代码>>>然后再执行wrapper3的函数体代码    

'''