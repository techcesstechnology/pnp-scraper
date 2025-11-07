import scrapy


class PnpScraperItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
