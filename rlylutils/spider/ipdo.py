import random
import requests


from rlylutils.spider.utils import *

url = 'http://icanhazip.com/'

ip = ['58.246.58.150:9002', '117.74.65.215:9080', '88.132.253.187:80']
for i in range(100):
    try:
        real_ip = random.choice(ip)
        proxy = {'http': real_ip}
        res_text = requests.get(url=url, proxies=proxy, timeout=3)
        print("成功")
    except:
        print("{}不可用".format(real_ip))
        ip.remove(real_ip)
