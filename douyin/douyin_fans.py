# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/9 20:06'
import json


def response(flow):
    if 'aweme/v1/user/follower/list' in flow.request.url:
        for user in json.loads(flow.response.text)['followers']:
            item = dict()
            item['share_id'] = user['uid']
            item['douyin_id'] = user['short_id']
            item['nick_name'] = user['nickname']
            print(item)