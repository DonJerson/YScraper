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

    def start_requests(self):
        b_type_list = ['restaurant','barbershop','church','liquor store','law','upholstery','auto','game','tattoo','flower','pharmacy','postal','printing services','real estate','grocery store','dentist','weed','construction','breakfast','gas station','hair salon','hotel','tobbaco']
        zipcode_list = ['36467']
        
        for zipcode in zipcode_list:
                        for b_type in b_type_list:
                                urls = [
                                'https://www.yelp.com/search?find_desc=%s&find_loc=%s'%(b_type, zipcode)
                                ]
                                self.zipcode = zipcode
                                yield scrapy.Request(url=urls[0], callback=self.parse)
        pass

    def parse(self, response):
        container = response.xpath('//div[@class="biz-attributes"]').extract()
        if container == []:
                container = response.xpath('//div[@class="biz-listing-large services-layout-result u-space-t1 u-space-b1"]').extract()
                if container == []:
                        container = response.xpath('//div[@class="biz-listing-large"]').extract()
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
        if response.xpath('//span[@class="pagination-label responsive-hidden-small pagination-links_anchor"]')==[]:
                pass
        else: 
                urlx = 'https://www.yelp.com' + response.xpath('//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract()[0]
                print(urlx)
                yield scrapy.Request(url=urlx, callback=self.parse)
                