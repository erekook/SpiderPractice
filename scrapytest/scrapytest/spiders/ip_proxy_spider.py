import scrapy
from scrapy import Selector
import requests
from scrapytest.items import ProxyItem


class IpSpider(scrapy.Spider):
    name = "ip"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.allowed_domain = ['www.xicidaili.com']
        self.start_urls = ['http://www.xicidaili.com/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        item = ProxyItem()
        ips = []
        protocols = []
        sel = Selector(response)
        host_tds = sel.xpath('//tr/td[2]').extract()
        port_tds = sel.xpath('//tr/td[3]').extract()
        protocol_tds = sel.xpath('//tr/td[6]').extract()

        # 去除td标签
        for i in range(len(host_tds)):
            host = host_tds[i].replace('<td>', '').replace('</td>', '')
            port = port_tds[i].replace('<td>', '').replace('</td>', '')
            protocol = protocol_tds[i].replace('<td>', '').replace('</td>', '').lower()
            ip = protocol + '://' + host + ':' + port
            ips.append(ip)
            protocols.append(protocol)

        item['ips'] = ips
        item['protocols'] = protocols
        yield item
