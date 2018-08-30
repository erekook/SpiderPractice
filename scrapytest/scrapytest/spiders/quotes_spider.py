import scrapy


class QuotesSpider(scrapy.Spider):
    # name是区分不同spider的属性
    name = "quotes"

    # scrapy会自动请求
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        # 'http://quotes.toscrape.com/page/2/',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'title': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            # 等价于上面
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)


        # 将爬取的整个网页html写入文件
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
