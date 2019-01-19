# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/1/17 18:20'
from selenium import webdriver
import time


class DouYu(object):
    def __init__(self):
        self.start_url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def get_content(self):
        li_list = self.driver.find_elements_by_xpath('//ul[@id="live-list-contentbox"]/li')
        content_list = list()
        for li in li_list:
            item = dict()
            item['author'] = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
            item['title'] = li.find_element_by_xpath('.//h3[@class="ellipsis"]').text
            item['watch_num'] = li.find_element_by_xpath('.//span[@class="dy-num fr"]').text
            item['tag'] = li.find_element_by_xpath('.//span[@class="tag ellipsis"]').text
            content_list.append(item)
        # 提取下一页
        next_url = self.driver.find_elements_by_xpath('//a[@class="shark-pager-next"]')
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    @staticmethod
    def save_content(content_list):
        for content in content_list:
            print(content)

    def run(self):
        self.driver.get(self.start_url)
        content_list, next_url = self.get_content()
        self.save_content(content_list)

        # 下一页元素提取
        while next_url is not None:
            next_url.click()
            time.sleep(3)
            content_list, next_url = self.get_content()
            self.save_content(content_list)

        self.driver.quit()


if __name__ == '__main__':
    douyu = DouYu()
    douyu.run()

