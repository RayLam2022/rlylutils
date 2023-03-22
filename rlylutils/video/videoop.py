# -*- coding:utf-8 -*-
# @Time    : 2022/12/7 17:08
# @Author  : Ray Lam YL



from moviepy.editor import *

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.video.utils import *
from rlylutils.metaclass.mcls import *

__all__ = ['Vieop']

Sugar.namespace = globals()


@Decorator.cdec(Cfg.default['param'])
class Vieop(metaclass=Sugar):

    default = {
               }

    def __init__(self):
        self.__dict__.update(self.default)
        self.temp_vi_path = './__temp__.mp4'  # 临时mp4
        self.temp_au_path = './temp-audio.mp3'  # 临时mp3

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【视频通用处理{}】len:{}'.format(varname, len(iterable))

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

    @staticmethod
    def v_read(path, audio=True):
        return v_read(path, audio=audio)

    @staticmethod
    def v_clip(clip, start, end):
        """
        截片段
        :param clip:
        :param start: 截取-开始时间
        :param end: 截取-结束时间
        :return:
        """
        return clip.subclip(start, end)

    @staticmethod
    def v_resize(clip, whnum_or_whrate):
        """
        调视频尺寸(片段,等比例缩放比率或宽高元组)
        :param clip:
        :param whnum_or_whrate:
        :return:
        """
        return clip.resize(whnum_or_whrate)

    @staticmethod
    def save_mp4(clip, savepath, audio=False, threads=3):
        clip.write_videofile(savepath, audio=audio, codec='libx264', threads=threads)

