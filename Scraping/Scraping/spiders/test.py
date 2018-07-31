from scrapy import Selector
from scrapy.http import HtmlResponse

url = 'https://www.yelp.com/search?find_desc=restaurant&find_loc=90001&start=30'

body = '<html><body><div class="secondary-attributes">\n                            <div class="secondary-attributes-ad-icon">\n                                    <span aria-hidden="true" data-hovercard-id="1" style="width: 18px; height: 18px;" class="icon icon--18-info icon--size-18 icon--currentColor yloca-info yloca-hover-info">\n    <svg role="img" class="icon_svg">\n        <use xlink:href="#18x18_info"></use>\n    </svg>\n</span>\n\n                            </div>\n                                    <span class="offscreen">Phone number</span>\n        <span class="biz-phon">\n            (323) 587-0100\n        </span>\n\n                                                <address>\n            3053 E Florence Ave\n        </address>\n\n                            <span class="biz-city">Huntington Park, CA</span>\n\n\n\n                        </div></body></html>'

response = Selector(text=body)
container = response.xpath('//div[@class="secondary-attributes"]').extract()

filtered_container = []


for element in container:
	element = Selector(text=element)

	if element.xpath('//span[@class="biz-phone"]') != []:
		filtered_container.append(element)

print(filtered_container)
