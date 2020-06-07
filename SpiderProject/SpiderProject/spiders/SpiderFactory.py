from scrapy.crawler import CrawlerProcess
from SpiderProject.SpiderProject.spiders.FlightSpider import FlightSpider
from SpiderProject.SpiderProject.spiders.MaskSpider import MaskSpider
from SpiderProject.SpiderProject.spiders.UberSpider import UberSpider
from SpiderProject.SpiderProject.settings import CUSTOM_CONFIG

SPIDER_FACTORY = {'flight': FlightSpider, 'mask': MaskSpider, 'uber': UberSpider}

def order_factory(Spiderclass):
    if Spiderclass == FlightSpider:
        return run_flight_spider
    elif Spiderclass == MaskSpider:
        return run_mask_spider
    elif Spiderclass == UberSpider:
        return run_uber_spider
    else:
        raise ValueError('Invalid spider class.')

def run_flight_spider(FlightSpider):
    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {'SpiderProject.SpiderProject.pipelines.FlightSpiderPipline': 100,
                           'SpiderProject.SpiderProject.pipelines.UberSpiderPipline': 200,
                           'SpiderProject.SpiderProject.pipelines.MaskSpiderPipline': 300}
    })
    process.crawl(FlightSpider)
    process.start()

def run_mask_spider(MaskSpider):
    process = CrawlerProcess(settings={
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': CUSTOM_CONFIG['CHROME_PATH'],
        'SELENIUM_DRIVER_ARGUMENTS': ['--headless'],
        'DOWNLOADER_MIDDLEWARES': {'scrapy_selenium.SeleniumMiddleware': 800},
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2,
        'AUTOTHROTTLE_DEBUG': True,
        'ITEM_PIPELINES': {'SpiderProject.SpiderProject.pipelines.MaskSpiderPipline': 100,
                           'SpiderProject.SpiderProject.pipelines.FlightSpiderPipline': 200,
                           'SpiderProject.SpiderProject.pipelines.UberSpiderPipline': 300}
    })
    process.crawl(MaskSpider)
    process.start()

def run_uber_spider(UberSpider):
    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {'SpiderProject.SpiderProject.pipelines.UberSpiderPipline': 100,
                           'SpiderProject.SpiderProject.pipelines.MaskSpiderPipline': 200,
                           'SpiderProject.SpiderProject.pipelines.FlightSpiderPipline': 300}
    })
    process.crawl(UberSpider)
    process.start()