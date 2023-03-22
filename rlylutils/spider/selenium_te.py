# http://c.biancheng.net/python_spider  爬虫学习网址

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# options.add_experimental_option("detach", True) #运行完不自动关浏览器
driver = webdriver.Chrome('chromedriver.exe', chrome_options = options) #此exe要加入环境变量


driver = webdriver.Chrome()
# 访问C语言中文网首页
first_url= 'http://c.biancheng.net'
driver.get(first_url)
# 访问c语言教程
second_url='http://c.biancheng.net/c/'
driver.get(second_url)
