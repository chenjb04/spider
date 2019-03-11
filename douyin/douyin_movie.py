# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/11 19:51'
import requests
import re
import json
from selenium import webdriver
import os
import time


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
share_id = '87701259337'
share_url = "https://www.douyin.com/share/user/{}".format(share_id)
response = requests.get(share_url, headers=header)

dytk = re.findall(r"dytk: '(.*?)'", response.text)[0]
tac = "var tac='" + re.findall(r"<script>tac='(.*?)'</script>", response.text)[0] + "';"

with open('html_head.txt', 'r') as f1:
    f1_read = f1.read()

with open('html_foot.txt', 'r') as f2:
    f2_read = f2.read().replace("&&&", share_id)

with open('html.html', 'w') as f:
    f.write(f1_read + "\n" + tac + "\n" + f2_read)

# 无界浏览获取秘钥
driver = webdriver.PhantomJS()
base_dir = os.path.dirname(__file__)
path = os.path.join("file://", base_dir, 'html.html')
driver.get(path)
signature = driver.title
time.sleep(0.1)
driver.close()

# count最多请求35个
movie_url = 'https://www.douyin.com/aweme/v1/aweme/post/?user_id={}&count=35&max_cursor=0&aid=1128&_signature={}&dytk={}'.format(share_id, signature, dytk)

while True:
    movie_response = requests.get(movie_url, headers=header)
    if json.loads(movie_response.text)['aweme_list']:
        for item in json.loads(movie_response.text)['aweme_list']:
            print(item['video']['play_addr']['url_list'][0])
        break
    else:
        continue