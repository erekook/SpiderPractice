import scrapy
from scrapytest.items import BookItem


class BookSpider(scrapy.Spider):
    name = "book1"

    start_urls = [
        'http://www.biqugex.com/book_43727/29207423.html'
    ]

    def parse(self, response):
        book = BookItem()
        content_arr = response.xpath('//div[@id="content"]/text()').extract()
        for item in content_arr:
            content_arr[content_arr.index(item)] = item.strip()

        content = ''.join(content_arr)
        book['title'] = response.css('div.content h1::text').extract()
        book['content'] = content
        yield book
        next_page = response.css('div.page_chapter a::attr(href)').extract()[2]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

