# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/5 17:04'
import requests
import json
import time
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba


class Spider(object):
    """
    电视剧黄金瞳评论爬取
    """
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            "Referer": "http://m.maoyan.com/movie/1209205/comments?_v_=yes",
        }
        self.url = "http://m.maoyan.com/review/v2/comments.json?movieId=1209205&userId=-1&offset={}&limit=15&type=3"
        self.url2 = "http://m.maoyan.com/review/v2/comments.json?movieId=1209205&userId=-1&offset={}&limit=15&level=2&type=3"

    def get_url_list(self):
        return [self.url.format(i) for i in range(0, 320, 15)]

    def get_url2_list(self):
        return [self.url2.format(i) for i in range(0, 320, 15)]

    def get_content(self, url):
        response = requests.get(url=url, headers=self.header)
        json_response = json.loads(response.text)
        for data in json_response['data']['comments']:
            item = dict()
            item['nick'] = data['nick']
            item['score'] = data['score']
            item['userLevel'] = data['userLevel']
            item['content'] = data['content']
            item['time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(data['time']/1000)).strip()
            item['upCount'] = data['upCount']
            yield item

    def save_csv_title(self):
        title = ['nick', 'score', 'userLevel', 'content', 'time', 'upCount']
        with open('hjt.csv', 'a', encoding='utf-8-sig', newline='') as f1:
            write = csv.DictWriter(f1, title)
            write.writeheader()

    def save_csv(self, item):
        with open('hjt.csv', 'a', encoding='utf-8-sig', newline='') as f1:
            write = csv.writer(f1)
            title = ['nick', 'score', 'userLevel', 'content', 'time', 'upCount']
            write.writerow([item[i] for i in title])
        print('保存成功')

    def word(self):
        with open('hjt.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            column = [row['content'] for row in reader]
        text = "".join(column)
        word_list = jieba.cut(text, cut_all=True)
        wl_split = " ".join(word_list)
        word_cloud = WordCloud(font_path="C:\\Windows\\Fonts\\STFANGSO.ttf", width=1000, height=800).generate(wl_split)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()

    def run(self):
        for url in self.get_url_list():
            for item in self.get_content(url):
                self.save_csv(item)

        for url2 in self.get_url2_list():
            for item in self.get_content(url2):
                self.save_csv(item)


if __name__ == '__main__':
    spider = Spider()
    spider.save_csv_title()
    spider.run()
    spider.word()