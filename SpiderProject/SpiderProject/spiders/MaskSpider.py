import scrapy
from scrapy_selenium import SeleniumRequest
import re
import time
import traceback
from SpiderProject.SpiderProject.items import MaskSpiderItem


class MaskSpider(scrapy.Spider):
    name = "mask"

    def start_requests(self):
        urls = [
            'https://www.etsy.com/search?q=mask&explicit=1&order=highest_reviews',
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
        try:
            maskSpiderItem['mask_count'] = int(''.join(re.findall('\d+', response.xpath('//*[@id="listing-page-cart"]/div/div[1]/div/div/a[1]/span[1]/text()').get())))
        except Exception as e:
            print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
            time.sleep(3)
            try:
                maskSpiderItem['mask_count'] = int(''.join(re.findall('\d+', response.xpath('//*[@id="listing-page-cart"]/div/div[1]/div/div/a[1]/span[1]/text()').get())))
            except Exception as e:
                print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
                try:
                    maskSpiderItem['mask_count'] = int(''.join(re.findall('\d+', response.xpath('//*[@id="shop_overview"]/div/div[1]/div[2]/div[1]/p[2]/text()').get())))
                except Exception as e:
                    print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
                    maskSpiderItem['mask_count'] = 0
        yield maskSpiderItem