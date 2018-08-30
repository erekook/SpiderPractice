# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    content = scrapy.Field()


class ComicItem(scrapy.Item):
    # 章节名
    dir_name = scrapy.Field()
    # 每个章节的链接
    link_url = scrapy.Field()
    # 图片地址
    img_url = scrapy.Field()
    # 图片保存路径
    image_paths = scrapy.Field()


class ProxyItem(scrapy.Item):
    ips = scrapy.Field()
    protocols = scrapy.Field()