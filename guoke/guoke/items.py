# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuokeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    focus_num = scrapy.Field()
    answer_num = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()
    img = scrapy.Field()

