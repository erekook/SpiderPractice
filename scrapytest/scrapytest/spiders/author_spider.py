import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        # 每一页作者的链接
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'author_name': extract_with_css('h3.author-title::text'),
            'birthday': extract_with_css('span.author-born-date::text'),
            'desc': extract_with_css('div.author-description::text'),
        }
