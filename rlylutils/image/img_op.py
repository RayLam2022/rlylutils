# -*- coding:utf-8 -*-
# @Time    : 2022/12/4 14:59
# @Author  : Ray Lam YL

import os
import os.path as osp
import sys
import platform

import multiprocessing as mp

from importlib import import_module

import numpy as np

try:
    cv2 = import_module('cv2')
    PIL_Image = import_module('PIL.Image')
except:
    os.system(f'{sys.executable} -m pip install opencv-python')
    cv2 = import_module('cv2')
    os.system(f'{sys.executable} -m pip install pillow')
    PIL_Image = import_module('PIL.Image')


from rlylutils.image.utils import *
from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.files_op import Filesop

__all__ = ['Imgop']


@Decorator.cdec(Cfg.default['param'])
class Imgop(Filesop):
    """
    未做透视，视频保存
    """
    default = {'src': 'image,ndarray',    # 原始图像
               'center': 'center',  # 旋转中心，默认是[0,0]
               'scaler': 1,
               'rotate': 0,
               'delta_x': 0,
               'delta_y': 0
               }

    def __init__(self):
        super().__init__()
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【图片通用处理{}】len:{}'.format(varname, len(iterable))

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
    def read(f, resize_height=None, resize_width=None, normalization=False, colorSpace='BGR', alpha2None: bool =False):
        """
        cv2读取的图片三通道为BGR 不是RGB，ndarray形式要注意
        :param f:
        :return: img, rows, cols
        """
        img, rows, cols = read_image(f,
                                               resize_height=resize_height,
                                               resize_width=resize_width,
                                               normalization=normalization,
                                               colorSpace=colorSpace,
                                                alpha2None=alpha2None)

        return img, rows, cols

    @staticmethod
    def read_decode(f):
        """
        imread不支持中文路径，中文路径时用 R
        :param f: path
        :return: img ndarray
        """
        img = cv2.imdecode(np.fromfile(f, dtype=np.uint8), -1)
        rows = img.shape[0]
        cols = img.shape[1]
        return img, rows, cols

    @staticmethod
    def read_gray(f):
        """
        读灰度图 R
        :param f:
        :return:
        """
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        rows = img.shape[0]
        cols = img.shape[1]
        return img, rows, cols

    @staticmethod
    def read_video(f: str or int, is_show=False):
        """
        读视频 生成器 for 循环
        :param f: 视频地址，如整数则为摄像头索引
        :param is_show: 是否显示
        :return: frame
        """
        plat = platform.system().lower()
        if plat == 'windows' and isinstance(f, int):
            cap = cv2.VideoCapture(f, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(f)

        if is_show:
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('frame', frame)
                    yield frame
                    if cv2.waitKey(1) & 0xFF == ord('q'):  # cv2.waitKey(0) 堵塞
                        cap.release()
                        break
                else:
                    cap.release()
        else:
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    yield frame
                else:
                    cap.release()

        cv2.destroyAllWindows()

    @staticmethod
    def show(img):
        """
        R
        :param img:
        :return:
        """
        cv2.imshow('img', img)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()

    @staticmethod
    def write(outpath, img):
        cv2.imwrite(outpath, img)

    @staticmethod
    def gen_color_list(cluster, rand_seed):
        """

        :param cluster: 要生成几种颜色
        :param rand_seed: 随机种子
        :return:  [[xxx,xxx,xxx],[xxx,xxx,xxx]]
        """
        c = Cmap(cluster, rand_seed)
        return c.gen_color_list()

    @staticmethod
    def color_bgr2gray(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def color_bgr2rgb(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def color_rgb2bgr(img):
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    @staticmethod
    def color_channels_split(bgr_img):
        """
        分离三通道
        :param bgr_img:
        :return: b_img, g_img, r_img
        """
        b, g, r = np.dsplit(bgr_img, 3)
        return b, g, r

    @staticmethod
    def color_channels_merge(b_img, g_img, r_img):
        """
        通道合并
        :param b_img:
        :param g_img:
        :param r_img:
        :return:
        """
        return np.dstack((b_img, g_img, r_img))

    @staticmethod
    def color_channels_add_alpha(img):
        """
        增加第四通道,透明层alpha通道
        """
        width = img.shape[0]
        height = img.shape[1]
        alpha_value = np.ones((width, height, 1)) * 255
        return np.dstack((img, alpha_value))

    @staticmethod
    def background_create(width, height, is_gray: bool = False):
        """
        创建单通或三通黑色背景
        """
        channels = 3
        if is_gray:
            channels=1
        background = np.zeros((width, height, channels))
        return background

    @staticmethod
    def letterbox_image(image, resize_width, resize_height):
        """
        图片统一尺寸，补灰条操作
        :param: image
        :return: new_image
        """
        ih = image.shape[0]
        iw = image.shape[1]

        w = resize_width
        h = resize_height

        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = cv2.resize(image, (nw, nh))
        new_image = np.full((h, w, 3), 128, dtype=image.dtype)  # channels为3，仅jpg和三通道图

        new_image[(h - nh) // 2: (h - nh) // 2 + nh, (w - nw) // 2:(w - nw) // 2 + nw, :] = image
        # print(new_image.shape)
        return new_image

    @staticmethod
    def mirror_horizon(img):
        """
        水平翻转
        :param img:
        :return:
        """
        return cv2.flip(img, 1)

    @staticmethod
    def mirror_vertical(img):
        """
        垂直翻转
        :param img:
        :return:
        """
        return cv2.flip(img, 0)

    @staticmethod
    def image_rotation(image, rotation, scale: float = 1.0):
        """

        :param image:
        :param rotation: 顺时针，单位：角度
        :param scale: 缩放比例
        :return:
        """
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        # 得到旋转矩阵，第一个参数为旋转中心
        M = cv2.getRotationMatrix2D(center, -rotation, scale)
        # 仿射变换，第三个参数是变换之后的图像大小
        image_rotation = cv2.warpAffine(image, M, (width, height))
        return image_rotation

    @staticmethod
    def image_affine(img,
                     matrix_three_point_1: '3 points ndarray or list' =[[0,0],[0,0],[0,0]],
                     matrix_three_point_2: '3 points ndarray or list' =[[0,0],[0,0],[0,0]]):
        """
        仿射变换
        :param img:
        :param matrix_three_point_1:
        :param matrix_three_point_2:
        :return:
        """

        height, width = img.shape[:2]
        if isinstance(matrix_three_point_1, list):
            matrix_three_point_1 = np.array(matrix_three_point_1).astype(np.float32)
        elif isinstance(matrix_three_point_1, np.ndarray):
            matrix_three_point_1 = matrix_three_point_1.astype(np.float32)  # 要np.float32，否则会报错

        if isinstance(matrix_three_point_2, list):
            matrix_three_point_2 = np.array(matrix_three_point_2).astype(np.float32)
        elif isinstance(matrix_three_point_2, np.ndarray):
            matrix_three_point_2 = matrix_three_point_2.astype(np.float32)
        # matSrc = np.float32([[0, 0], [0, height - 1], [width - 1, 0]])
        # matDst = np.float32([[0, 0], [30, height - 30], [width - 30, 30]])
        M = cv2.getAffineTransform(matrix_three_point_1, matrix_three_point_2)
        img_affine = cv2.warpAffine(img, M, (width, height))
        return img_affine

    @staticmethod
    def corp_margin(img):
        """
        图片去灰色边框操作  灰条都是[128,128,128]
        :param img:
        :return:
        """
        img2 = img.sum(axis=2)
        (row, col) = img2.shape
        row_top = 0
        raw_down = 0
        col_top = 0
        col_down = 0
        for r in range(0, row):
            if img2.sum(axis=1)[r] != (128*3)*col:
                # 对channel维求和，灰条都是[128,128,128],如整列刚好相等则为灰条，不等则为正常区域，停止求边距
                row_top = r
                break
        for r in range(row-1, 0, -1):
            if img2.sum(axis=1)[r] != (128*3)*col:
                raw_down = r
                break
        for c in range(0, col):
            if img2.sum(axis=0)[c] != (128*3)*row:
                col_top = c
                break
        for c in range(col-1, 0, -1):
            if img2.sum(axis=0)[c] != (128*3)*row:
                col_down = c
                break
        new_img = img[row_top:raw_down+1, col_top:col_down+1, 0:3]
        return new_img

    @staticmethod
    def points_from_image(img_bgr):
        """
        鼠标从图片获取指定点坐标
        :param img_bgr:
        :return:
        """
        npimg = np.array(img_bgr.shape)
        print(npimg)

        def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                xy = "%d,%d" % (x, y)
                print('loc:', (x, y))
                print('RGB:', img_bgr[y, x])
                cv2.circle(img_bgr, (x, y), 1, (255, 0, 0), thickness=-1)

                cv2.putText(img_bgr, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (0, 0, 0), thickness=1)

                cv2.imshow("image", img_bgr)

        cv2.namedWindow("image")
        cv2.moveWindow("image", 100, 100)
        cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
        while (1):
            cv2.imshow("image", img_bgr)
            if cv2.waitKey(0) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

    @staticmethod
    def color_from_image(img_bgr, colortype: 'HSV or RGB or BGR' = 'RGB'):
        """
        鼠标从图片提取指定像素的颜色值
        :param img_bgr:
        :param colortype: 'HSV or RGB or BGR'
        :return:
        """
        if colortype == 'HSV':  # 是否提取hsv颜色
            img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        elif colortype == 'RGB':
            img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        def mouseColor(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(r'{colortype}:', img[y, x])  # 输出图像坐标(x,y)处的HSV的值
        cv2.namedWindow("Color Picker")
        cv2.setMouseCallback("Color Picker", mouseColor)
        cv2.imshow("Color Picker", img_bgr)
        if cv2.waitKey(0):
            cv2.destroyAllWindows()

    @staticmethod
    def image_shape_filename_paring(img_dir1, img_dir2, exten1=['.jpg', '.png'], exten2=['.jpg', '.png']):
        fop = Filesop()
        paired_list, notpaired_list = fop.pairing_check(img_dir1, img_dir2, exten1, exten2)
        for imp1, imp2 in paired_list:
            img1_basename = osp.basename(imp1)
            img2_basename = osp.basename(imp2)
            img1 = cv2.imread(imp1, cv2.IMREAD_UNCHANGED)
            img2 = cv2.imread(imp2, cv2.IMREAD_UNCHANGED)
            shp1 = img1.shape
            shp2 = img2.shape

            if not np.array_equal(shp1,shp2):
                print(f'{img1_basename}:{shp1}    {img2_basename}:{shp2}')

        print(f'notpaired_files:{notpaired_list}')





