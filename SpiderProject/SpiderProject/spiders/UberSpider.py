import scrapy
from selenium import webdriver
import time
import pickle
from SpiderProject.SpiderProject.items import UberSpiderItem
from SpiderProject.SpiderProject.settings import CUSTOM_CONFIG
from datetime import datetime
from utils.utils import send_email
import traceback


class UberSpider(scrapy.Spider):
    name = "uber"
    start_urls = ['https://www.uber.com/us/en/price-estimate/']

    def __init__(self):
        self.driver = webdriver.Chrome(CUSTOM_CONFIG['CHROME_PATH'])
        self.driver.implicitly_wait(10)
        self.paths = {
            ('Grand central station, 89 E 42nd St, New York, NY', 'World Trade Center, New York, NY'),
            ('Grand central station, 89 E 42nd St, New York, NY', 'John F. Kennedy International Airport, Queens, NY'),
            ('Grand central station, 89 E 42nd St, New York, NY', 'Citi Field, 41 Seaver Way, Queens, NY')
        }

    def parse(self, response):
        self.driver.get('https://www.uber.com/us/en/price-estimate/')
        for cookie in pickle.load(open(CUSTOM_CONFIG['COOKIES_PATH'] + '\\cookies_uber.pkl', "rb")): # change cookie fie
            self.driver.add_cookie(cookie)

        now = datetime.now()
        price_records = []
        for origin, destination in self.paths:
            self.driver.get('https://www.uber.com/us/en/price-estimate/')
            time.sleep(6) # wait for the webpage to get fully loaded
            self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[2]/div[1]/input').send_keys(origin)
            time.sleep(6) # wait for dropdown to get fully loaded
            self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[2]/ul/li[1]').click()
            time.sleep(6)
            self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/input').send_keys(destination)
            time.sleep(6)
            self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[2]/ul/li[1]').click()
            time.sleep(6)
            try:
                price_records.append({
                    'time': now,
                    'origin': origin,
                    'destination': destination,
                    'Pool': float(self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/span').text[1:]),
                    'UberX': float(self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[3]/div[2]/div[2]/div[1]/div/span').text[1:]),
                    'WAV': float(self.driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div/div/div[1]/div[3]/div[2]/div[3]/div[1]/div/span').text[1:])
                })
            except Exception as e:
                print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
                send_email('uber')

        uberSpiderItem = UberSpiderItem()
        uberSpiderItem['price_records'] = price_records
        yield uberSpiderItem