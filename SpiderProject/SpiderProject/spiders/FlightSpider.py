import scrapy
from selenium import webdriver
import os
import time
from datetime import datetime
from SpiderProject.SpiderProject.items import FlightSpiderItem
from SpiderProject.SpiderProject.settings import CUSTOM_CONFIG


class FlightSpider(scrapy.Spider):
    name = "flight"
    start_urls = ['https://www.flightradar24.com/data/statistics']

    def __init__(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('prefs', {'download.default_directory' : CUSTOM_CONFIG['DOWNLOAD_PATH']})
        self.driver = webdriver.Chrome(executable_path=CUSTOM_CONFIG['CHROME_PATH'], chrome_options=chromeOptions)

    def parse(self, response):
        self.driver.get('https://www.flightradar24.com/data/statistics')
        time.sleep(6)
        self.driver.find_element_by_xpath('//div[@data-highcharts-chart="1"]//*[@class="highcharts-exporting-group"]').click() # load the menu js
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element_by_xpath('//div[@data-highcharts-chart="1"]//*[contains(text(), "Download CSV")]'))
        time.sleep(6)
        os.rename(CUSTOM_CONFIG['DOWNLOAD_PATH'] + '\\number-of-commercial-fli.csv',
                  CUSTOM_CONFIG['DOWNLOAD_PATH'] + '\\number-of-commercial-fli-' + str(datetime.today().date()) + '.csv')

        flightSpiderItem = FlightSpiderItem()
        flightSpiderItem['file_path'] = CUSTOM_CONFIG['DOWNLOAD_PATH'] + '\\number-of-commercial-fli-' + str(datetime.today().date()) + '.csv'
        yield flightSpiderItem