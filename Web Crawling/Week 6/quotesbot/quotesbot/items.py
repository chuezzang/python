# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()  # 사이트
    category = scrapy.Field()  # 카테고리
    text = scrapy.Field()  # 텍스트
    author = scrapy.Field()  # 저자
    author_description = scrapy.Field()  #저자에 대한 설명
    tag = scrapy.Field()  # 태그

    pass
