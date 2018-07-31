# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from ..items import ScrapingItem
from scrapy.loader import ItemLoader

class YelpspiderSpider(scrapy.Spider):
    name = 'YelpSpider'
    allowed_domains = ['yelp.com']
    start_urls = ['http://yelp.com/']
    zipcode = ''
    filename = 'leads-1.xlsx'
    def start_requests(self):
        b_type_list = ['restaurant']
        zipcode_list = ['90001']
        
        for b_type,zipcode in zip(b_type_list,zipcode_list):
            urls = [
            'https://www.yelp.com/search?find_desc=%s&find_loc=%s'%(b_type, zipcode)
            ]
            self.zipcode = zipcode
            yield scrapy.Request(url=urls[0], callback=self.parse)
        pass

    def parse(self, response):
        container = response.xpath('//div[@class="biz-attributes"]').extract()
        filtered_container = []
        for element in container:
                element = Selector(text=element)
                if element.xpath('//span[@class="biz-phone"]') != []:
                        filtered_container.append(element)

        for element in filtered_container:
                b_name = element.xpath('//a[@class="biz-name js-analytics-click"]/span/text()').extract()[0]
                phone = element.xpath('//span[@class="biz-phone"]/text()').extract()[0].strip()
                address = element.css("div.secondary-attributes address::text").extract()
                if address == []:
                        address = 'No address'
                else: 
                        address = address[0].strip()
                item = ItemLoader(item=ScrapingItem(), response=response)
                item.add_value('BusinessName',b_name)
                item.add_value('BusinessAddress',address)
                item.add_value('BusinessPhone',phone)
                item.add_value('BusinessZipcode',self.zipcode)
                yield item.load_item()