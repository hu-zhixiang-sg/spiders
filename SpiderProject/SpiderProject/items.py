import scrapy


class FlightSpiderItem(scrapy.Item):
    file_path = scrapy.Field()

class MaskSpiderItem(scrapy.Item):
    mask_count = scrapy.Field()

class UberSpiderItem(scrapy.Item):
    price_records = scrapy.Field()