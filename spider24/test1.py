

from fake_useragent import UserAgent
import random

fake_ua=UserAgent() # 构建UserAgent()对象
headers = {'User-Agent':fake_ua.random} #用random来随机取得用户代理。
print(headers)