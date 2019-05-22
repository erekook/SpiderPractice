import scrapy
from bookspider.items import BookspiderItem


class BookSpider(scrapy.Spider):
    name = "book"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.allowed_domains = ['www.bequge.com']
        self.start_urls = ['https://www.bequge.com/11_11400/3054982.html']

    # 从该方法发送请求
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        book = BookspiderItem()
        content_arr = response.xpath('//div[@id="content"]/text()').extract()

        # 去除文章内容的空格
        for item in content_arr:
            content_arr[content_arr.index(item)] = item.strip()

        content = ''.join(content_arr)
        book['title'] = response.css('div.bookname h1::text').extract()
        book['content'] = content
        yield book
        next_page = response.css('div.bottem1 a::attr(href)').extract()[3]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
