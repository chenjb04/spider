# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/6 18:44'
import requests
from lxml import etree
import re


def html_decode(data):
    # 抖音编码对应数字
    num_list = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
    ]
    for name in num_list:
        for num in name['name']:
            data = re.sub(num, str(name['value']), data)
    return data


def read_id():
    with open('douyin_hot_id.txt', 'r') as f:
        for hot_id in f.readlines():
            hot_id.replace(" ", '')
            yield hot_id


def handle_share_web():
    """
    抖音分享页面数据
    :return:
    """
    for hot_id in read_id():
            share_web_url = "https://www.douyin.com/share/user/{}".format(hot_id)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
            }
            response = requests.get(share_web_url, headers=header)
            data = html_decode(response.text)
            html = etree.HTML(data)
            item = dict()
            # 抖音昵称
            item['nick_name'] = html.xpath("//p[@class='nickname']/text()")[0]
            # 抖音ID
            douyin_id1 = re.sub(r'抖音ID：', '', html.xpath("//p[@class='shortid']/text()")[0].replace(" ", ''))
            douyin_id2 = "".join(html.xpath("//p[@class='shortid']/i/text()"))
            item['douyin_id'] = douyin_id1 + douyin_id2
            # 工作
            if html.xpath('//span[@class="info"]/text()'):
                item['job'] = html.xpath('//span[@class="info"]/text()')[0].strip()
            else:
                item['job'] = '无'
            # 个人简介
            item['desc'] = html.xpath("//p[@class='signature']/text()")[0].replace("\n", '')
            # 位置
            item['address'] = html.xpath('//span[contains(@class, "location")]/text()')[0]
            # 星座
            item['constellation'] = html.xpath('//span[contains(@class, "constellation")]/text()')[0]
            # 关注
            follow = "".join(html.xpath("//span[@class='focus block']//text()")).replace(' ', '')
            follow = re.sub(r'关注', '', follow)
            item['follow'] = follow
            # 粉丝
            fans = "".join(html.xpath("//span[@class='follower block']//text()")).replace(' ', '')
            fans = re.sub(r'粉丝', '', fans)
            item['fans'] = fans
            # 点赞
            praise = "".join(html.xpath("//span[@class='liked-num block']//text()")).replace(" ", '')
            praise = re.sub(r"赞", '', praise)
            item['praise'] = praise
            print(item)


if __name__ == '__main__':
    handle_share_web()