# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Field

class BillionsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class YiCheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CarBrandName = Field()
    price = Field()
    CarBrandImgHttpUrl = Field()
    CarDetailUrl = Field()
    vendorName = Field()
    vendorImg = Field()
    CarBrandList = Field()

class D1evItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    newsUrl = Field()
    homeTuUrl = Field()
    image_urls = Field()
    images = Field()
    image_path= Field(default='D1ev')
    wjj = Field()
    html_content = Field()


