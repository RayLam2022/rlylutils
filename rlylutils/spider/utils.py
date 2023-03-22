# -*- coding:utf-8 -*-
# @Time    : 2023/2/2 17:07
# @Author  : Ray Lam YL

import sys
import re
import socket
import requests

from lxml import etree


def get_host_ip():
    """
    查询本机ip地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_ip():
    return (requests.get('http://ifconfig.me/ip', timeout=1).text.strip())


if __name__ == '__main__':
    print(f'local_ip:{get_host_ip()}')
    try:
        print(f'ip:{get_ip()}')
    except:
        print("无法联网或其他错误，无法获取本机外网ip")
