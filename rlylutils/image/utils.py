# -*- coding:utf-8 -*-
# @Time    : 2022/12/10 15:56
# @Author  : Ray Lam YL

import random

import numpy as np
import cv2


def read_image(filename, resize_height=None, resize_width=None, normalization=False, colorSpace='RGB', alpha2None: bool =False):
    '''
    读取图片数据,默认返回的是uint8,[0,255]
    :param filename:
    :param resize_height:
    :param resize_width:
    :param normalization:是否归一化到[0.,1.0]
    :param colorSpace 输出格式：RGB or BGR
    :param alpha2None 是否去除alpha层
    :return: 返回的图片数据
    '''
    bgr_image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    # bgr_image = cv2.imread(filename,cv2.IMREAD_IGNORE_ORIENTATION|cv2.IMREAD_UNCHANGED)
    if bgr_image is None:
        print("Warning: no image:{}".format(filename))
        return None
    if len(bgr_image.shape) == 2:  # 若是灰度图则转为三通道
        print("Warning:gray image", filename)
        bgr_image = cv2.cvtColor(bgr_image, cv2.COLOR_GRAY2BGR)

    if alpha2None == True:
        bgr_image = bgr_image[:, :, :3]

    if colorSpace == 'RGB':
        image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)  # 将BGR转为RGB
    elif colorSpace == "BGR":
        image = bgr_image
    else:
        exit(0)
    # show_image(filename,image)
    # image=Image.open(filename)
    image = resize_image(image, resize_height, resize_width)
    image = np.asanyarray(image)
    if normalization:
        image = image_normalization(image)
    # show_image("src resize image",image)
    rows = image.shape[0]
    cols = image.shape[1]
    return image, rows, cols


def resize_image(image, resize_height=None, resize_width=None):
    '''
    :param image:
    :param resize_height:
    :param resize_width:
    :return:
    '''
    image_shape = np.shape(image)
    height = image_shape[0]
    width = image_shape[1]
    if (resize_height is None) and (resize_width is None):  # 错误写法：resize_height and resize_width is None
        return image
    if resize_height is None:
        resize_height = int(height * resize_width / width)
    elif resize_width is None:
        resize_width = int(width * resize_height / height)
    image = cv2.resize(image, dsize=(resize_width, resize_height))
    return image


def image_normalization(image, mean=None, std=None):
    '''
    正则化，归一化
    image[channel] = (image[channel] - mean[channel]) / std[channel]
    :param image: numpy image
    :param mean: [0.5,0.5,0.5]
    :param std:  [0.5,0.5,0.5]
    :return:
    '''
    # 不能写成:image=image/255
    if isinstance(mean, list):
        mean = np.asarray(mean, dtype=np.float32)
    if isinstance(std, list):
        std = np.asarray(std, dtype=np.float32)
    image = np.array(image, dtype=np.float32)
    image = image / 255.0
    if mean is not None:
        image = np.subtract(image, mean)
    if std is not None:
        image = np.multiply(image, 1 / std)
    return image


class Cmap:
    """
    # random color map  R
    """

    def __init__(self, cluster, rand_seed):
        self.c = cluster
        self.c_list = self.gen_color_list()
        random.seed(rand_seed)

    def __str__(self):
        return ('color_map_len :{}\ncolor_map :{}'.format(len(self.c_list), self.c_list))

    def gen_color_list(self):
        c_list = set()
        while len(c_list) < self.c:
            c_list.add(self.get_random_color())
        return list(c_list)

    def get_random_color(self):
        r = lambda: random.randint(0, 255)
        return (r(), r(), r())


if __name__ == '__main__':
    c = Cmap(6)
    c.gen_color_list()


