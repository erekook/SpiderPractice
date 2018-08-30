# -*- coding: utf-8 -*-
import time
import os
from scrapy import Request
from scrapytest import settings
import requests


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        file_name = base_dir + '/note.txt'
        with open(file_name, mode='a') as fp:
            fp.write(''.join(item['title']) + '\n')
            fp.write(''.join(item['content']) + '\n\n\n')
            # time.sleep(1)
        return item


class ComicImgDownloadPipeline(object):
    def process_item(self, item, spider):
        # 如果获取了图片链接，进行如下操作
        if 'img_url' in item:
            images = []
            # 文件夹名字
            dir_path = '%s/%s' % (settings.IMAGES_STORE, item['dir_name'])
            # 文件夹不存在则创建文件夹
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            # 获取每一个图片链接
            for image_url in item['img_url']:
                # 解析链接，根据链接为图片命名
                houzhui = item['img_url'].index(image_url)
                qianzhui = item['link_url'].split('/')[-1].split('.')[0]
                # 图片名
                image_file_name = '第' + qianzhui + '页.' + str(houzhui)
                # 图片保存路径
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue
                # 保存图片
                with open(file_path, 'wb') as handle:
                    response = requests.get(url=image_url)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            # 返回图片保存路径
            item['image_paths'] = images
        return item


class IpProxyPipeline(object):
    def process_item(self, item, spider):
        ok_ips = []
        if 'ips' in item:
            for i in range(len(item['ips'])):
                proxies = {
                    item['protocols'][i]: item['ips'][i]
                }
                headers = {
                    "User_Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                }
                try:
                    res = requests.get(url='http://www.baidu.com', proxies=proxies, headers=headers, timeout=2)
                    if res.status_code == 200:
                        ok_ips.append(item['ips'][i])
                        print("%s successful" % item['ips'][i])
                except:
                    print("%s failed" % item['ips'][i])

        with open('proxies.txt', 'a') as f:
            for proxy in ok_ips:
                f.write(proxy + '\n')
