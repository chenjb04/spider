# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['http://book.jd.com/booksort.html']

    def parse(self, response):
        # 获取大分类分组
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = dict()
            item['big_cate'] = dt.xpath("./a/text()").extract_first()
            # 获取小分类分组
            em_list = dt.xpath("./following-sibling::*[1]/em")
            for em in em_list:
                item['small_cate'] = em.xpath("./a/text()").extract_first()
                item['small_href'] = "https:" + em.xpath("./a/@href").extract_first()
                # 小分类href进入列表页
                yield scrapy.Request(
                    item['small_href'],
                    callback=self.parse_book_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item['book_author'] = li.xpath(".//span[@class='p-bi-name']/span/a/text()").extract()
            item['book_press'] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            item['book_date'] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()
            item['book_href'] = "https:" + li.xpath(".//div[@class='p-name']/a/@href").extract_first()
            # item['book_evaluation_num'] = li.xpath(".//div[@class='p-commit']/strong/a/text()").extract_first()
            item['book_img'] = li.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            item['book_brand'] = li.xpath(".//div[@class='p-shopnum']/span/text()").extract_first()
            # 请求价格
            price_url = 'http://p.3.cn/prices/mgets?ext=11101000&pin=&type=1&area=1_72_2799_0&skuIds=J_{}'.format(li.xpath("./div/@data-sku").extract_first())
            yield scrapy.Request(
                price_url,
                callback=self.parse_book_price,
                meta={'item': deepcopy(item)}
            )
            # 翻页
            next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
            if next_url is not None:
                yield response.follow(
                    next_url,
                    callback=self.parse_book_list,
                    meta={'item': item}
                )

    def parse_book_price(self, response):
        item = response.meta['item']
        item['book_price'] = re.findall(r'"p"\:"(.*?)"', response.body.decode())[0]
        print(item)