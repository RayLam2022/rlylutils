# -*- coding:utf-8 -*-
# @Time    : 2022/12/24 18:41
# @Author  : Ray Lam YL


from inspect import isfunction

__all__ = ['Sugar']


class Meta(type):
    def __new__(cls, name, base, attrs):
        # print(newcls.__dict__)
        attrs['te'] = d
        print(base)
        base = (int,)
        newcls = type.__new__(cls, name, base, attrs)
        return newcls

    def __init__(self, name, base, attrs):
        return type.__init__(self, name, base, attrs)

    def __call__(cls, *args, **kws):
        return type.__call__(cls, *args, **kws)


class Sugar(type):
    namespace = dict()

    def __new__(cls, name, base, attrs):
        for var in list(Sugar.namespace.keys()):
            print(var)
            if isfunction(Sugar.namespace[var]):
                attrs[var] = staticmethod(Sugar.namespace[var])
        newcls = type.__new__(cls, name, base, attrs)
        return newcls

    def __init__(self, name, base, attrs):
        return type.__init__(self, name, base, attrs)

    def __call__(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)
