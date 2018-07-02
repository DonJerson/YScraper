# -*- coding: utf-8 -*-
import scrapy


class YelpspiderSpider(scrapy.Spider):
    name = 'YelpSpider'
    allowed_domains = ['yelp.com']
    start_urls = ['http://yelp.com/']
    b_type_list = ['barbershop']
    zipcode_list = ['36467']
    def start_requests(self):
     	for b_type,zipcode in zip(b_type_list,zipcode_list):
        	urls = [
            	'https://www.yelp.com/search?find_desc=%s&find_loc=%s'%(b_type, zipcode)
            	]
        	yield scrapy.Request(url=url, callback=self.parse)
        pass
    def parse(self, response):
    	page = response.url.split("/")[-2]
        filename = 'leads-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        pass
