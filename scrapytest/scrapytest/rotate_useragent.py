import random
import base64
import os
# from scrapytest.settings import PROXIES
# from settings import PROXIES


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        print("**************************" + random.choice(self.agents))
        request.headers.setdefault('User-Agent', random.choice(self.agents))


# class ProxyMiddleWare(object):
#     """docstring for ProxyMiddleWare"""
#
#     def process_request(self, request, spider):
#         '''对request对象加上proxy'''
#         proxy = self.get_random_proxy()
#         print("this is request ip:" + proxy)
#         request.meta['proxy'] = proxy
#
#     def process_response(self, request, response, spider):
#         '''对返回的response处理'''
#         # 如果返回的response状态不是200，重新生成当前request对象
#         if response.status != 200:
#             proxy = self.get_random_proxy()
#             print("this is response ip:" + proxy)
#             # 对当前reque加上代理
#             request.meta['proxy'] = proxy
#             return request
#         return response
#
#     def get_random_proxy(self):
#         '''随机从文件中读取proxy'''
#         base_dir = os.getcwd()
#         file_name = base_dir + '/scrapytest/proxies.txt'
#         while 1:
#             with open(file_name, 'r') as f:
#                 proxies = f.readlines()
#             if proxies:
#                 break
#             else:
#                 time.sleep(1)
#         proxy = random.choice(proxies).strip()
#         return proxy
