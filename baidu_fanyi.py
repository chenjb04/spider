# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/1/11 19:19'
import requests
import json


class Translate(object):
    def __init__(self, query_string):
        self.url = 'https://fanyi.baidu.com/basetrans'
        self.query_string = query_string
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like\
         Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

    def language_testing(self):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {
            'query': self.query_string
        }
        response = requests.post(url, data=data, headers=self.headers)
        ret = response.content.decode()
        json_str = json.loads(ret)
        language = json_str['lan']
        return language

    def get_post_data(self):
        post_data = {
            "query": self.query_string,
            'from': 'zh' if self.language_testing() == 'zh' else 'en',
            'to': 'en' if self.language_testing() == 'zh' else 'zh'
        }

        return post_data

    def parse_url(self, url, data):
        response = requests.post(url, data=data, headers=self.headers)
        return response.content.decode()

    def get_ret(self, json_str):
        temp_dict = json.loads(json_str)
        ret = temp_dict['trans'][0]['dst']
        print('{} : {}'.format(self.query_string, ret))

    def run(self):
        post_data = self.get_post_data()
        json_str = self.parse_url(self.url, post_data)
        self.get_ret(json_str)


if __name__ == '__main__':
    fanyi = Translate('today is a nice day')
    fanyi.run()