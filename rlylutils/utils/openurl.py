# -*- coding:utf-8 -*-
# @Time    : 2022/12/2 20:48
# @Author  : Ray Lam YL

import os
import sys
import platform
plat = platform.system().lower()

from importlib import import_module
import webbrowser

if plat == 'windows':
    try:
        winreg = import_module('winreg')
    except:
        os.system(f'{sys.executable} -m pip install winreg')
        winreg = import_module('winreg')
    __all__ = ['win_url', 'default_url']
else:
    __all__ = ['lnx_url', 'default_url']

# 浏览器注册表信息


browser_regs = {
    '360': r"SOFTWARE\Clients\StartMenuInternet\360Chrome\DefaultIcon",
    'IE': r"SOFTWARE\Clients\StartMenuInternet\IEXPLORE.EXE\DefaultIcon",
    'chrome': r"SOFTWARE\Clients\StartMenuInternet\Google Chrome\DefaultIcon",
    'edge': r"SOFTWARE\Clients\StartMenuInternet\Microsoft Edge\DefaultIcon",
    'firefox': r"SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon",
}



default_url = {'cuda': 'https://developer.nvidia.com/cuda-toolkit-archive',
               'cudnn': 'https://developer.nvidia.com/rdp/cudnn-download',
               'paddle': 'https://paddlepaddle.org.cn/whl/stable.html',
               'torch': 'https://download.pytorch.org/whl/torch_stable.html'
               }

def lnx_url(url):
    print(url)
    os.system(f'firefox {url}')

def win_url(url, browsers=['edge','chrome','firefox','360','IE']):
    print(url)
    for browser in browsers:
        path = get_browser_path(browser)
        if path:
            print('open with browser: {}, path: {}'.format(browser, path))
            webbrowser.register(browser, None, webbrowser.BackgroundBrowser(path))
            webbrowser.get(browser).open(url)
            break




def get_browser_path(browser):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, browser_regs[browser])
    except FileNotFoundError:
        return None
    value, _type = winreg.QueryValueEx(key, "")
    return value.split(',')[0]


if __name__ == '__main__':
    print("360: ", get_browser_path('360'))
    print("IE:", get_browser_path('IE'))
    print("谷歌:", get_browser_path('chrome'))
    print("edge: ", get_browser_path('edge'))
    print("火狐:", get_browser_path('firefox'))
    browsers = ['360', 'edge']
    if win_url('www.xx.com', browsers=browsers):
        print('打开成功')
    else:
        print('打开失败，请安装{}浏览器后重试'.format('或'.join(browsers)))

