# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotationcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()  # 날짜
    sales_high = scrapy.Field()  # 매매 사한가
    sales_mean = scrapy.Field()  # 매매 평균가
    sales_low = scrapy.Field()  # 매매 하한가
    rent_high = scrapy.Field()  # 전세 상한가
    rent_mean = scrapy.Field()  # 전세 평균가
    rent_low = scrapy.Field()  # 전세 하한가
    
    pass
