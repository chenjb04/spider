# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy


class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = 'dangdang'

    def parse(self, response):
        # 获取大分类分组
        div_list = response.xpath("//div[@class='con flq_body']/div")[1:-1]
        for div in div_list:
            item = dict()
            item['big_cate'] = div.xpath(".//dl[contains(@class,'primary_dl')]/dt//text()").extract()
            # 获取中间分类分组
            dl_list = div.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:
                item['middle_cate'] = dl.xpath("./dt//text()").extract()
                # 获取小分类分组
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    item['small_cate'] = a.xpath("./text()").extract_first()
                    item['small_href'] = a.xpath("./@href").extract_first()
                    # print(item)

                    # 列表页请求
                    yield scrapy.Request(
                        item['small_href'],
                        callback=self.parse_book_list,
                        meta={'item': deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath("//ul[@id='component_59']/li")
        for li in li_list:
            item['book_name'] = li.xpath("./a/@title").extract_first()
            item['book_href'] = li.xpath("./a/@href").extract_first()
            item['book_author'] = li.xpath(".//p[@class='search_book_author']/span[1]/a[1]/@title").extract_first()
            item['book_press'] = li.xpath(".//p[@class='search_book_author']/span[3]/a/text()").extract_first()
            item['book_date'] = li.xpath(".//p[@class='search_book_author']/span[2]/text()").extract_first().replace("/", '').strip()
            item['book_desc'] = li.xpath(".//p[@class='detail']/text()").extract_first()
            item['book_price'] = li.xpath(".//span[@class='search_now_price']/text()").extract_first()
            item['book_commit_num'] = li.xpath(".//p[@class='search_star_line']/a/text()").extract_first()
            item['book_store'] = li.xpath("./p[@class='search_shangjia']/a[1]/text()").extract_first()
            if item['book_store'] is None:
                item['book_store'] = '当当自营'
            yield item

            # 实现翻页
            next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
            if next_url is not None:
                yield response.follow(
                    next_url,
                    callback=self.parse_book_list,
                    meta={'item': item}
                )
