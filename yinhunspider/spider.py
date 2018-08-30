from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
from lxml import etree
import time
from random import randint
import re
import os
from urllib import request
import queue
import threading


url = 'http://ac.qq.com/ComicView/index/id/505435/cid/1'
image_store_path = '/home/erek/images/yinhu/'
server = 'http:ac.qq.com'
res = requests.get(url)
html = etree.HTML(res.text)
# 章节url地址
chapter_urls = []
chapter_url_list = html.xpath('//ul[@id="catalogueList"]/li/a/@href')
for chapter_url in chapter_url_list:
	chapter_urls.append(server+chapter_url)
# 章节名称地址
titles = []
title_list = html.xpath('//span[@class="tool_chapters_list_title"]/text()')
# strip
for title in title_list:
	titles.append(re.sub(r' ','_',title))
chapter_queue = []
# 循环每一章
for i in range(0, len(titles)):
	chapter_queue.append(titles[i]+'|'+chapter_urls[i])

# 获取图片url
def get_images_url(title,chapter_url):
	print('get image urls',title)
	image_urls = []
	option = webdriver.ChromeOptions()
	option.add_argument('--headless')
	option.add_argument('--disable-gpu')
	# option.add_argument('''user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"''')
	browser = webdriver.Chrome(chrome_options=option)
	# browser = webdriver.Chrome()
	browser.get(chapter_url)
	imgs = browser.find_elements_by_xpath('//ul[@id="comicContain"]/li/img')

	# 页面长度 len(imgs) * 960 + 2000
	# js滚动页面
	for i in range(0, int((len(imgs) + 1)/4+1)):
		js = 'window.scrollTo( 800 ,' + str((i + 1) * 3800) + ')'
		browser.execute_script(js)
		time.sleep(randint(2, 4))

	for i in range(0, len(imgs)):
		image_urls.append(imgs[i].get_attribute("src"))

	browser.close()
	save_images(title,image_urls)


def save_images(title,image_urls):
	#章节目录
	dir_path = image_store_path + title
	# 文件夹不存在则创建文件夹
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	for image in image_urls:
		image_file_name = image.split('/')[-2][-7:]
		image_file_path = '%s/%s' % (dir_path, image_file_name)

		if os.path.exists(image_file_path):
			continue
		# 保存图片
		try:
			with open(image_file_path, 'wb') as handle:
				res = request.urlopen(image).read()
				handle.write(res)
		except Exception as e:
			print('save image failed',e)
		
if __name__ == '__main__':
	print(chapter_queue)
	for chapter_title_url in chapter_queue:
		print(chapter_title_url)
		if chapter_title_url is None:
			break
		title = chapter_title_url.split('|')[0]
		url = chapter_title_url.split('|')[1]
		dir_path = image_store_path + title
		# 检查是否下载本章节
		if os.path.exists(dir_path):
			print(title,'-此章节已下载')
			continue
		get_images_url(title,url)

