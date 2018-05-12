# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuhuSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BrandItem(scrapy.Item):
    name = scrapy.Field()
    remote_logo = scrapy.Field()


class CarItem(scrapy.Item):
    name = scrapy.Field()
    product_id = scrapy.Field()
    remote_logo = scrapy.Field()
    brand_name = scrapy.Field()
    factory_name = scrapy.Field()
    is_baoyang = scrapy.Field()


class CarVersionItem(scrapy.Item):
    name = scrapy.Field()
    t_id = scrapy.Field()
    product_id = scrapy.Field()
    displacement = scrapy.Field()
    year = scrapy.Field()


class CarDisplacementItem(scrapy.Item):
    product_id = scrapy.Field()
    displacement = scrapy.Field()


class CarDisplacement2YearItem(scrapy.Item):
    product_id = scrapy.Field()
    displacement = scrapy.Field()
    year = scrapy.Field()
