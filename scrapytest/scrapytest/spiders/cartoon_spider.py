import scrapy
import re
from scrapy import Selector
from scrapytest.items import ComicItem


class CartonnSpider(scrapy.Spider):
    name = "comic"

    # 首页
    # http: // www.gufengmh.com / manhua / woweicangsheng /  # chapters

    # 标题

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        # 图片链接服务器
        self.server_img = 'http://res.mhkan.com/'
        # 章节链接服务器
        self.server_link = 'http://www.gufengmh.com'
        self.allowed_domains = ['www.gufengmh.com']
        self.start_urls = ['http://www.gufengmh.com/manhua/woweicangsheng/']
        # 匹配图片地址数组正则
        self.pattern_imgs = re.compile(r'\[\".*g\"\]')

    # 从该方法发送请求
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse1)

    # 解析章节名和链接
    def parse1(self, response):
        hxs = Selector(response)
        items = []
        # 章节链接地址
        urls = hxs.xpath('//ul[@id="chapter-list-1"]/li/a/@href').extract()
        # 章节名
        dir_names = hxs.xpath('//ul[@id="chapter-list-1"]/li/a/span/text()').extract()
        # 保存章节名和和链接
        for index in range(len(urls)):
            item = ComicItem()
            item['link_url'] = self.server_link + urls[index]
            item['dir_name'] = dir_names[index]
            items.append(item)

        # 根据每个章节的链接，发送Request请求， 并传递item参数
        for item in items:
            yield scrapy.Request(url = item['link_url'], meta = {'item':item}, callback = self.parse2)


    # 解析获得章节
    def parse2(self, response):
        # 接收传递的item
        item = response.meta['item']
        # 获取该页面的链接
        item['link_url'] = response.url
        hxs = Selector(response)
        script_text = hxs.xpath('//script/text()').re('chapterImages.*chapterPath')[0]
        img_url_suffix1 = 'images/comic' + response.xpath('//script/text()').re('images\/comic(.*?)\"')[0]
        img_urls = []
        img_urls_suffix_list_str = re.findall(self.pattern_imgs, script_text)[0].replace('[', '').replace(']', '')
        img_url_suffix_list = img_urls_suffix_list_str.split(',')
        for img_url_suffix in img_url_suffix_list:
            # 把图片链接的引号去掉
            result = re.sub(r'\"', '', img_url_suffix)
            img_urls.append(self.server_img + img_url_suffix1 + result)

        item['img_url'] = img_urls
        yield item


