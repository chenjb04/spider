# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/1/13 18:45'
import requests
from lxml import etree
from functools import reduce
import re
from queue import Queue
from multiprocessing.dummy import Pool
import time


class QiuBai(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/hot/page/{}/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/71.0.3578.98 Safari/537.36'}
        self.queue = Queue()
        self.pool = Pool(5)
        self.is_running = True
        self.total_request_num = 0
        self.total_response_num = 0

    def get_url_list(self):
        # return [self.url.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            self.queue.put(self.url.format(i))
            self.total_request_num += 1

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        print(response)
        return response.content.decode()

    @staticmethod
    def get_content_list(html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@id='content-left']/div")
        content_list = []
        for div in div_list:
            item = dict()
            item['user_name'] = div.xpath('.//h2/text()')[0].strip()
            item['content'] = [re.sub(r'\n+', '', i) for i in div.xpath('.//div[@class="content"]/span/text()')]
            t = reduce(lambda x, y: str(x)+str(y), item['content'])
            item['content'] = t
            content_list.append(item)
        return content_list

    @staticmethod
    def save_content_list(content_list):
        for content in content_list:
            # print(content)
            pass

    def _execute_request_content_save(self):
        url = self.queue.get()
        html_str = self.parse_url(url)
        content_list = self.get_content_list(html_str)
        self.save_content_list(content_list)
        self.total_response_num += 1

    def _callback(self, temp):
        if self.is_running:
            self.pool.apply_async(self._execute_request_content_save, callback=self._callback)

    def run(self):
        self.get_url_list()
        # 设置并发数
        for i in range(6):
            self.pool.apply_async(self._execute_request_content_save, callback=self._callback)

        while True:
            time.sleep(0.0001)
            if self.total_response_num >= self.total_request_num:
                self.is_running = False
                break


if __name__ == '__main__':
    t1 = time.time()
    qiubai = QiuBai()
    qiubai.run()
    print(time.time() - t1)
