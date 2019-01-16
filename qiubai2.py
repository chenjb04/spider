# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/1/13 18:45'
import requests
from lxml import etree
from functools import reduce
import re
from multiprocessing import Process
from multiprocessing import JoinableQueue as Queue


class QiuBai(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/hot/page/{}/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/71.0.3578.98 Safari/537.36'}
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_url_list(self):
        # return [self.url.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            self.url_queue.put(self.url.format(i))

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            print(response)
            if response.status_code != 200:
                self.url_queue.put(url)
            else:
                self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            html_str = self.html_queue.get()
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
            self.content_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self):
        while True:
            content_list = self.content_queue.get()
            for content in content_list:
                # print(content)
                pass
            self.content_queue.task_done()

    def run(self):
        thread_list = list()
        t_url = Process(target=self.get_url_list)
        thread_list.append(t_url)
        for i in range(3):
            t_parse = Process(target=self.parse_url)
            thread_list.append(t_parse)
        t_get = Process(target=self.get_content_list)
        thread_list.append(t_get)
        t_save = Process(target=self.save_content_list)
        thread_list.append(t_save)

        for process in thread_list:
            process.daemon(True)
            process.start()

        for q in [self.url_queue, self.content_queue, self.html_queue]:
            q.join()
        # for url in self.get_url_list():
        #     html_str = self.parse_url(url)
        #     content_list = self.get_content_list(html_str)
        #     self.save_content_list(content_list)


if __name__ == '__main__':
    qiubai = QiuBai()
    qiubai.run()
