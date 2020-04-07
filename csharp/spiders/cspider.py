# -*- coding: utf-8 -*-
from urllib import response

import scrapy
from scrapy import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from csharp.items import CsharpItem, FileItem


class CspiderSpider(CrawlSpider):
    name = 'cspider'
    allowed_domains = ['47.95.144.194']
    start_urls = ['http://47.95.144.194/mod/workshop/view.php?id=144']
    job_url = []
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

    rules = [
        # http://47.95.144.194/mod/workshop/submission.php?cmid=137&id=328
        Rule(LinkExtractor(allow=r'http://47.95.144.194/mod/workshop/submission.php?cmid=137&id=\d+'),
             callback='parse_item', follow=True, ),
        # http://47.95.144.194/pluginfile.php/1606/mod_workshop/submission_attachment/328/55170537%E5%AD%99%E4%B8%80%E5%9D%A4.rar?forcedownload=1
        Rule(LinkExtractor(allow=r'http://47.95.144.194/pluginfile.php/1606/mod_workshop/submission_attachment/.*'),
             callback='', follow=True, )
    ]

    # def ammend_req_header(self, request):
    #     request.cookies = self.cookies
    #     return request

    def start_requests(self):
        # myurl = r'http://47.95.144.194/mod/workshop/submission.php?cmid=137&id='
        # for i in range(100,400):
        #     yield scrapy.Request(url=myurl+str(i),
        #                          headers=self.headers,
        #                          cookies=self.cookies,
        #                          callback=self.parse_item)
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 callback=self.parse_url)

    def _build_request(self, rule, link):
        r = Request(url=link.url, headers=self.headers, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def parse_url(self, response):
        urls = response.xpath(
            '//tr/td[@class = "submission cell c1"]/a[@class = "title"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 callback=self.parse_item)

    def parse_item(self, response):
        item = CsharpItem()

        sno = response.xpath(
            '//div[@class = "submission-full"]/div[@class = "header"]/h3[@class = "title"]/text()').extract()
        name = response.xpath(
            '//div[@class = "author"]/div[@class = "fullname"]/a/text()').extract()
        info = response.xpath(
            '//div[@class = "attachments"]/ul/li/a/@href').extract()

        item['name'] = name[0].replace(' ', '')
        item['sno'] = sno[0]
        item['info'] = info[0]

        yield item

        zipper = FileItem()
        # url = response.urljoin(info[0].replace('?forcedownload=1', ''))
        url = response.urljoin(info[0])
        zipper = FileItem()
        zipper['file_urls'] = [url]
        zipper['name'] = name[0].replace(' ', '')
        zipper['sno'] = sno[0]
        zipper['info'] = info[0]

        yield zipper
