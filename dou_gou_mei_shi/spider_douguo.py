# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/4 19:16'
import requests
import json
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
import pymongo
from pymongo.collection import Collection

queue = Queue()


def handle_request(url, data):
    """
    请求函数
    :param url:
    :param data: 请求数据
    :return:
    """
    header = {
            "client": "4",
            "version": "6933.4",
            "device": "HUAWEI MLA-AL10",
            "sdk": "22, 5.1.1",
            "imei": "863064010164764",
            "channel": "baidu",
            "resolution": "720*1280",
            "dpi": "1.5",
            "brand": "HUAWEI",
            "scale": "1.5",
            "timezone": "28800",
            "language": "zh",
            "cns": "3",
            "carrier": "CHINA+MOBILE",
            "user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
            "reach": "1",
            "newbie": "0",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
            "Host": "api.douguo.net"
        }
    response = requests.post(url, headers=header, data=data)
    return response


def handle_category():
    """
    获取食材类别
    :return:
    """
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
        "client": "4",
        "_vs": "2305"
    }
    response = handle_request(url, data)
    response_dict = json.loads(response.text)
    for big_cate in response_dict["result"]["cs"]:
        for second_cate in big_cate['cs']:
            for food_material in second_cate['cs']:
                data_2 = {
                    "client": "4",
                    "keyword": food_material['name'],
                    "order": "3",
                    "_vs": "400",
                }
                queue.put(data_2)


def handle_menu_list(data):
    """
    获取菜谱
    :param data:
    :return:
    """
    menu_list_url = "http://api.douguo.net/recipe/v2/search/0/20"
    menu_list_response = handle_request(url=menu_list_url, data=data)
    menu_list_response_dict = json.loads(menu_list_response.text)
    for item in menu_list_response_dict['result']['list']:
        menu_info = dict()
        menu_info['food_material'] = data['keyword']
        if item['type'] == 13:
            menu_info['user_name'] = item['r']['an']
            menu_info['food_material_id'] = item['r']['id']
            menu_info['desc'] = item['r']['cookstory'].replace("\n", '').replace(' ', '')
            menu_info['menu_name'] = item['r']['n']
            menu_info['condiments'] = item['r']['major']
            detail_url = "http://api.douguo.net/recipe/detail/{}".format(menu_info['food_material_id'])
            detail_data = {
                "client": "4",
                "author_id": "0",
                "_vs": "2803",
                "_ext": '{"query": {"kw": '+data['keyword']+', "src": "2803", "idx": "1", "type": "13", "id": '+str(menu_info['food_material_id'])+'}',
            }
            detail_response = handle_request(detail_url, detail_data)
            detail_response_dict = json.loads(detail_response.text)
            menu_info['tips'] = detail_response_dict['result']['recipe']['tips']
            menu_info['cook_step'] = detail_response_dict['result']['recipe']['cookstep']
            print('当前入库的菜谱是: ', menu_info['menu_name'])
            save_mongodb(menu_info)
        else:
            continue


def save_mongodb(item):
    """
    保存到MongoDB数据库
    :return:
    """
    client = pymongo.MongoClient("localhost", 27017)
    db_data = client['dou_guo_mei_shi']
    db_collection = Collection(db_data, 'dou_guo_mei_shi_item')
    db_collection.insert(item)


if __name__ == '__main__':
    handle_category()
    pool = ThreadPoolExecutor(max_workers=20)
    while queue.qsize() > 0:
        pool.submit(handle_menu_list, queue.get())