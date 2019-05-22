# -*- coding: utf-8 -*-
import os
# from scrapy import Request
# import requests
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookspiderPipeline(object):

    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        file_name = base_dir + '/yiyantongtian.txt'
        print(file_name)
        with open(file_name, mode='a') as fp:
            fp.write(''.join(item['title']) + '\n')
            fp.write(''.join(item['content']) + '\n\n\n')
        return item
