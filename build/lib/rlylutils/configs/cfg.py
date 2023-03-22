import os


__all__=['Cfg']

class Cfg:
    default = { 'Author': 'Ray Lam LYL',
                'param': int(os.getenv('Cparam')),
                'path':__file__
               }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【配置{}】len:{}'.format(varname, len(iterable))

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)




if __name__ == '__main__':
    print(Cfg.default['path'])