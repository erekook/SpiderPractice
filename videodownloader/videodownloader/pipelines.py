# -*- coding: utf-8 -*-
from urllib import request
from videodownloader import settings
import random
import time
import os
import queue
import threading


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class VideodownloaderPipeline(object):

    def __init__(self) -> None:
        super().__init__()
        self.error_urls = []
        self.video_queue = queue.Queue()
        self.threads = []
        self.num_worker_threads = 10
        self.video_path = settings.VIDEO_STORE
        self.len = 0
        self.time_start = time.time()
        self.time_end = 0.0

    def process_item(self, item, spider):
        # 视频存储路径
        video_urls = item['video_urls']
        # 把要下载的视频url放入队列
        self.len = len(video_urls)
        for i in range(len(video_urls)):
            self.video_queue.put(video_urls[i])

        for i in range(self.num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)

        # block until all tasks are done
        self.video_queue.join()

        # stop workers
        for i in range(self.num_worker_threads):
            self.video_queue.put(None)
        for t in self.threads:
            t.join()

        print(self.error_urls)
        for err_url in self.error_urls:
            with open('error.txt', 'wb') as f:
                f.write(err_url + '\n')

        print('----------------------------------------')
        self.time_end = time.time()
        print('finished! used %f s' % (self.time_end - self.time_start))

    def worker(self):
        while True:
            _url = self.video_queue.get()
            if _url is None:
                break
            filename = self.video_path + _url.split('/')[-1].strip()
            if os.path.exists(filename):
                print('%s already done' % filename.split('/')[-1])
            else:
                print('process>>>>>>>>left %d' % self.video_queue.qsize())
                self.download_video(_url, filename)
            self.video_queue.task_done()

    def download_video(self, url, filename):
        print('>>>Downloading++++++')
        user_agent = random.choice(settings.USER_AGENTS)
        print('choose UserAgent>>>>>>>>>\n', user_agent)
        headers = {
            'User_Agent': user_agent,
            'Connection': 'close'
        }
        try:
            req = request.Request(url=url, headers=headers)
            res = request.urlopen(req)
            if res.status == 200:
                with open(filename, 'wb') as f:
                    f.write(res.read())
                print('%s download successfully' % filename.split('/')[-1])
            else:
                self.error_urls.append(url)
                print('%s download failed' % url)
        except Exception as e:
            print(e)
            print('download failed')
