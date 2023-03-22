# -*- coding:utf-8 -*-

import sys
import re
import socket
import requests

import yaml
from lxml import etree

from rlylutils.spider.utils import *

__all__ = ['FreeIp']


class FreeIp:
    def __init__(self):
        self.start_url = "https://ip.jiangxianli.com/?page={}"
        self.url_list = [self.start_url.format(i) for i in range(1, 6)]  # 这里可以按实际情况更改
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        self.verify = True

    def parse(self, html):
        tr_list = html.xpath("//table[@class='layui-table']/tbody/tr")
        ip_list = []
        for tr in tr_list:
            # print(tr.xpath("./td/text()"))
            try:
                if tr.xpath("./td/text()")[2] == "高匿" and tr.xpath("./td/text()")[3] == "HTTP":
                    ip = {}
                    ip["ip"] = tr.xpath("./td/text()")[0]
                    ip["port"] = tr.xpath("./td/text()")[1]
                    ip_list.append(ip)
            except:
                pass

        return ip_list

    def check_ip(self, ip_list, stop_ip_num):
        correct_ip = []
        for ip in ip_list:
            ip_port = ip["ip"] + ":" + ip["port"]
            proxies = {'http': ip_port}
            try:
                response = requests.get('http://icanhazip.com/', proxies=proxies, timeout=5).text
                if response.strip() == ip["ip"]:  # 如果请求该网址，返回的IP地址与代理IP一致，则认为代理成功
                    print("可用的IP地址为：{}".format(ip_port))
                    correct_ip.append(ip_port)
            except:
                pass
                # print("不可用的IP地址为：{}".format(ip_port))
            if len(correct_ip) >= stop_ip_num:
                break
        return correct_ip

    def get_ip(self, stop_ip_num=8):
        # 获得URL地址
        correct_all_ip = []
        for idx, url in enumerate(self.url_list):
            # 获得请求
            if idx == 0:
                try:
                    response = requests.get(url, headers=self.headers,
                                            verify=self.verify).content.decode()  # verify=False慎用，网络安全问题
                except:
                    veri = input('ssl verify问题未能获得请求，是否将verify 调为False? (y/n) :')
                    if veri == 'y':
                        self.verify = False
                        response = requests.get(url, headers=self.headers, verify=self.verify).content.decode()
                    else:
                        sys.exit()
            else:
                response = requests.get(url, headers=self.headers, verify=self.verify).content.decode()

            # 解析页面
            html = etree.HTML(response)
            # 得到IP
            ip_list = self.parse(html)
            # 检查IP
            correct_ip = self.check_ip(ip_list, stop_ip_num)
            correct_all_ip.extend(correct_ip)
            if len(correct_all_ip) >= stop_ip_num:
                break

        with open('./ippool.txt', 'w', encoding='utf-8') as f:
            if correct_all_ip:
                for line in correct_all_ip:
                    f.writelines(line + '\n')
        # 返回所有IP
        return correct_all_ip


if __name__ == '__main__':
    print(f'local_ip:{get_host_ip()}')
    try:
        print(f'ip:{get_ip()}')
    except:
        print("无法联网或其他错误，无法获取本机外网ip")

    free_ip = FreeIp()
    ip = free_ip.get_ip(3)
    print(ip)
    print(len(ip))
