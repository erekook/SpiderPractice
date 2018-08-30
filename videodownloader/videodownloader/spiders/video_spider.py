import scrapy
import requests
import os
from videodownloader.items import VideodownloaderItem
from videodownloader import settings


class VideoSpider(scrapy.Spider):
    name = "video"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = ['http://yun.kubo-zy-youku.com/ppvod/D2D567798AAD2050BA65661F634849C0.m3u8']
        # 切片视频url
        self.video_urls = []
        self.video_path = settings.VIDEO_STORE

    def parse(self, response):
        item = VideodownloaderItem()
        # 获取m3u8文件,写入文件
        m3u8_file = self.video_path + self.start_urls[0].split('/')[-1][-10:]
        m3u8_res = requests.get(self.start_urls[0])
        with open(m3u8_file, 'wb') as f:
            f.write(m3u8_res.content)

        fo = open(m3u8_file, 'rb')
        for line in fo.readlines():
            decode_line = line.decode('utf-8')
            if '.ts' in decode_line:
                ts_url = 'http://yun.kubo-zy-youku.com' + decode_line
                self.video_urls.append(ts_url)
            else:
                continue

        fo.close()

        item['video_urls'] = self.video_urls
        yield item

