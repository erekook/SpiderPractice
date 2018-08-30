import scrapy

class TestSpider(scrapy.Spider):
    name = "test"

    start_urls = ['http://www.gufengmh.com/manhua/woweicangsheng/']

    # 解析章节名和链接
    def parse(self, response):
        # 章节链接地址
        urls = response.xpath('//ul[@id="chapter-list-1"]/li/a/@href').extract()
        # 章节名
        dir_names = response.xpath('//ul[@id="chapter-list-1"]/li/a/span/text()').extract()
        # 保存章节名和和链接
        print(len(dir_names))

