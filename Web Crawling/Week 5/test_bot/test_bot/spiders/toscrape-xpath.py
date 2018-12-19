# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    topic_keyword = input("Input Topic Keyword : ")  # keyword #
    start_urls = [
        'https://www.brainyquote.com/topics/' + topic_keyword,
    ]
    

    def parse(self, response):
        for quote in response.xpath('//div[@class="m-brick grid-item boxy bqQt"]'):
            yield {
                'text': quote.xpath('.//a[@title="view quote"]/text()').extract_first(),
                'author': quote.xpath('.//a[@title="view author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="kw-box"]/a[@class="oncl_list_kc"]/text()').extract()
            }

        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
