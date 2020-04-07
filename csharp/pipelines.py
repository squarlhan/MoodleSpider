# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import csv
import os
from os.path import join, basename, dirname
from urllib.parse import urlparse

from pandas import DataFrame
from scrapy import item, Request
from scrapy.pipelines.files import FilesPipeline


class CsharpPipeline(object):

    def __init__(self):
        # csv文件的位置,无需事先创建
        # store_file = os.path.dirname(__file__) + '/result5.csv'
        store_file = r'F:/2020/result5.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'w', newline='')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if item['name']:
            self.writer.writerow([item['sno'], item['name'], item['info']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


class CsharpFilePlipeline(FilesPipeline):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': '47.95.144.194',
        'Referer': 'http://47.95.144.194/mod/workshop/view.php?id=144',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    cookies = {
        'Hm_lvt_b393d153aeb26b46e9431fabaf0f6190': '1584790973,1585047181,1585297448,1585970119',
        'Hm_lpvt_b393d153aeb26b46e9431fabaf0f6190': '1586010377',
        'MOODLEID1_': '%2501%25C4%258Egt%2507%2514%25FD%2529',
        'MoodleSession': '77itrqf2m8d39fikr8en8j8ldd'
    }

    def get_media_requests(self, item, info):
        for image_url in item['file_urls']:
            yield Request(url=image_url, headers=self.headers, cookies=self.cookies, meta={'name': item['name']})

    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        name1 = basename(dirname(path))
        name2 = basename(path)
        extended_name = os.path.splitext(path)[1]
        name = request.meta['name']
        temp = join('', name + extended_name)
        return temp
