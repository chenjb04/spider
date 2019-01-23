# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class BookPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'dangdang':
            item['big_cate'] = "".join([i.strip() for i in item['big_cate']])
            item['middle_cate'] = "".join([i.strip() for i in item['middle_cate']])
        print(item)
        return item
