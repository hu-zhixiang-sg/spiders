import scrapy
from scrapy_selenium import SeleniumRequest
import re
from SpiderProject.SpiderProject.items import MaskSpiderItem


class MaskSpider(scrapy.Spider):
    name = "mask"

    def start_requests(self):
        urls = [
            'https://www.etsy.com/search?q=mask',
        ]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//div[@data-search-results]//ul//li//a[1]/@href').getall():
            yield SeleniumRequest(url=link, callback=self.parse_store)

        next_page = response.xpath('//div[@data-appears-component-name="search_pagination"]//ul[1]//li[2]//a/@href').get()
        if next_page:
             yield SeleniumRequest(url=next_page, callback=self.parse)

    def parse_store(self, response):
        maskSpiderItem = MaskSpiderItem()
        maskSpiderItem['mask_count'] = int(''.join(re.findall('\d+', response.xpath('//div[@data-buy-box]//div//div//div//a//span/text()').get())))
        yield maskSpiderItem