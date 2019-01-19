# -*- coding: utf-8 -*-
import scrapy
from guoke.items import GuokeItem
import urllib.parse


class GkSpider(scrapy.Spider):
    name = 'gk'
    allowed_domains = ['guokr.com']
    start_urls = ['https://www.guokr.com/ask/highlight/']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='ask-list-cp']/li")
        for li in li_list:
            item = GuokeItem()
            item['title'] = li.xpath("./div[@class='ask-list-detials']/h2/a/text()").extract_first()
            item['href'] = li.xpath("./div[@class='ask-list-detials']/h2/a/@href").extract_first()
            item['answer_num'] = li.xpath(".//p[@class='ask-answer-nums']/span/text()").extract_first()
            item['focus_num'] = li.xpath(".//p[@class='ask-focus-nums']/span/text()").extract_first()
            item['tag'] = li.xpath(".//p[@class='tags']/a/text()").extract()
            # print(item)
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta={'item': item}
            )
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        div_list = response.xpath("//div[contains(@class,'answer gclear')]")
        answer_list = list()
        for div in div_list:
            one_answer = dict()
            one_answer['name'] = div.xpath(".//a[@class='answer-usr-name']/text()").extract_first()
            one_answer['like'] = div.xpath(".//a[@class='answer-digg-up']/span[1]/text()").extract_first()
            one_answer['unlike'] = div.xpath(".//a[@class='answer-digg-dw']/span[1]/text()").extract_first()
            one_answer['answer_time'] = div.xpath(".//a[@class='answer-date']/text()").extract_first()
            one_answer['answer_content'] = div.xpath(".//div[@class='answer-txt answerTxt gbbcode-content']//text()").extract()
            one_answer['answer_img'] = div.xpath(".//div[@class='answer-txt answerTxt gbbcode-content']//img/@src").extract()
            if one_answer['answer_img']:
                one_answer['answer_img'] = div.xpath(
                    ".//div[@class='answer-txt answerTxt gbbcode-content']//img/@src").extract()
            else:
                one_answer['answer_img'] = None
            answer_list.append(one_answer)
        item['content'] = answer_list
        print(item)
