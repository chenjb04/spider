# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 大分类分组
        div_list = response.xpath("//div[@class='menu-list']/div[@class='menu-item']")
        div_sub_list = response.xpath("//div[@class='menu-list']/div[@class='menu-sub']")
        for div in div_list:
            item = dict()
            item['big_cast'] = div.xpath(".//h3/a/text()").extract_first()
            # 获取中间分类
            current_sub_div = div_sub_list[div_list.index(div)]
            p_list = current_sub_div.xpath(".//div[@class='submenu-left']/p[@class='submenu-item']")
            for p in p_list:
                item['middle_cast'] = p.xpath("./a/text()").extract_first()
                # 获取小分类
                li_list = p.xpath("./following-sibling::ul[1]/li")
                for li in li_list:
                    item['small_cast'] = li.xpath("./a/text()").extract_first()
                    item['small_href'] = li.xpath("./a/@href").extract_first()
                    # 请求图书列表页
                    yield scrapy.Request(
                        item['small_href'],
                        callback=self.parse_book_list,
                        meta={'item': deepcopy(item)}
                    )
                    # 请求另一部分内容
                    next_part_url_temp = """https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp=0&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=010&paging=1&sub=0"""
                    ci = item['small_href'].split('/')
                    if ci[2] == 'list.suning.com':
                        ci = item['small_href'].split('-')[1]
                        next_part_url = next_part_url_temp.format(ci)
                        yield scrapy.Request(
                            next_part_url,
                            callback=self.parse_book_list,
                            meta={'item': deepcopy(item)}
                        )

    def parse_book_list(self, response):
        item = response.meta['item']
        # li_list = response.xpath("//div[@id='filter-results']/ul/li")
        li_list = response.xpath("//li[contains(@class,'product      book')]")
        for li in li_list:
            item['book_name'] = li.xpath(".//p[@class='sell-point']/a/text()").extract_first().strip()
            item['book_href'] = li.xpath(".//p[@class='sell-point']/a/@href").extract_first()
            item['book_img'] = li.xpath(".//div[@class='img-block']/a/img/@src2").extract_first()
            item['book_store'] = li.xpath(".//p[contains(@class,'seller oh no-more')]/a/text()").extract_first()
            item['book_evaluation_num'] = li.xpath(".//p[@class='com-cnt']/a/text()").extract_first()

            # 请求详情页
            yield response.follow(
                item['book_href'],
                callback=self.parse_book_detail,
                meta={'item': deepcopy(item)}
            )

            # 翻页
            next_url_1 = """https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=010"""
            next_url_2 = """https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=010&paging=1&sub=0"""
            ci = item['small_href'].split('/')
            if ci[2] == 'list.suning.com':
                ci = item['small_href'].split('-')[1]
                current_page = re.findall(r'param.currentPage = "(.*?)";', response.body.decode())[0]
                total_page = re.findall(r'param.pageNumbers = "(.*?)";', response.body.decode())[0]
                if int(current_page) < int(total_page):
                    next_page_num = int(current_page) + 1
                    next_url_1.format(ci, next_page_num)
                    yield scrapy.Request(
                        next_url_1,
                        callback=self.parse_book_list,
                        meta={'item': item}
                    )
                    next_url_2.format(ci, next_page_num)
                    yield scrapy.Request(
                        next_url_2,
                        callback=self.parse_book_list,
                        meta={'item': item}
                    )

    def parse_book_detail(self, response):  # 处理图书详情页内容
        item = response.meta["item"]
        price_temp_url = "https://pas.suning.com/nspcsale_0_{}_{}_{}_10_010_0100101_226503_1000000_9017_10106____{}_{}.html"
        p1 = re.findall(r'"passPartNumber":"(.*?)",', response.body.decode())[0]
        p3 = response.url.split("/")[-2]
        p4 = re.findall('"catenIds":"(.*?)",', response.body.decode())
        if len(p4) > 0:
            p4 = p4[0]
            p5 = re.findall('"weight":"(.*?)",', response.body.decode())[0]
            price_url = price_temp_url.format(p1, p1, p3, p4, p5)
            item['price_url'] = price_url
            yield scrapy.Request(
                price_url,
                callback=self.parse_book_price,
                meta={"item": item}
            )

    def parse_book_price(self, response):
        item = response.meta['item']
        item['book_price'] = re.findall('"netPrice":"(.*?)","', response.body.decode())
        if len(item['book_price']) > 0:
            item['book_price'] = re.findall('"netPrice":"(.*?)","', response.body.decode())[0]
        else:
            item['book_price'] = None
        print(item)

