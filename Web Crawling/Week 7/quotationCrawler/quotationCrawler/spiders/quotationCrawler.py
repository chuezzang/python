# -*- coding: utf-8 -*-
import scrapy
import time
import csv
from quotationCrawler.items import QuotationcrawlerItem


class quotationUrlSpider(scrapy.Spider):
    name = 'quotationUrlCrawler'
   
    def start_request(self):
        #단지번호, 평형수 
        pageCode = ['C059689']  # C059689
        flagCode = ['KBM035167']  # KBM035167, KBM019730, KBM019729
 
        for page in pageCode:
            for flag in flagCode:
                yield scrapy.Request("https://onland.kbstar.com/quics?page={0}&%EB%AC%BC%EA%B1%B4%EC%8B%9D%EB%B3%84%EC%9E%90={1}&%ED%83%AD%EA%B5%AC%EB%B6%84=1&%EB%A7%A4%EB%AC%BC%EA%B1%B0%EB%9E%98%EA%B5%AC%EB%B6%84=1&QSL=F#CP".format(page, flag), 
                                    self.parse_quotation)

# 과거시세조회 버턴 클릭 후 표시되는 페이지 정보 (javascript) : xpath('//*[@id="hscmFlxbBtnArea"]/a[1]').extract

# 레이어 팝업 정보 (별도 페이지 링크 없슴)
# 조희 버턴 클릭 : xpath('//*[@id="layer4"]/div[2]/div[2]/button')
# 테이블 정보 가져오기 (또는 시세다운로드 버턴 클릭 -> csv 파일 저장) : xpath('//*[@id="siseTableTbody"]')
# xpath('//*[@id="siseTableTbody"]/tr[1]') [0]~[6]
# 매매가, 전세가 정보만 가져오기 / 월세가는 제외
# 레이어 팝업 닫기 : xpath('//*[@id="layer4"]/button')
# 
def parse_quotation(self, response):
    for quotation in response.xpath(''):
        item = QuotationcrawlerItem()

        item['date'] = quotation.xpath('').extract()[0][:8]
        item['sales_high'] = quotation.xpath('').extract()[0]
        item['sales_mean'] = quotation.xpath('').extract()[0]
        item['sales_low'] = quotation.xpath('').extract()[0]
        item['rent_high'] = quotation.xpath('').extract()[0]
        item['rent_mean'] = quotation.xpath('').extract()[0]
        item['rent_low'] = quotation.xpath('').extract()[0]

        # print('-' * 100)
        # print(item['date'])

        time.sleep(5)
        yield item

    # next_page_url = response.xpath(
    #     '//li[@class="next"]/a/@href').extract_first()

    # if next_page_url is not None:
    #     yield scrapy.Request(response.urljoin(next_page_url))


class quotationSpider(scrapy.Spider):
    name = "quotationCrawler"
 
    def start_requests(self):
        with open('quotationUrlCrawl.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield scrapy.Request(row['url'], self.parse_news)
 
    def parse_quotation(self, response):
        item = NewscrawlingItem()
 
        tem['date'] = quotation.xpath('').extract()[0[:8]]
        item['sales_high'] = quotation.xpath('').extract()[0]
        item['sales_mean'] = quotation.xpath('').extract()[0]
        item['sales_low'] = quotation.xpath('').extract()[0]
        item['rent_high'] = quotation.xpath('').extract()[0]
        item['rent_mean'] = quotation.xpath('').extract()[0]
        item['rent_low'] = quotation.xpath('').extract()[0]

        # print('-' * 100)
        # print(item['date'])
 
        time.sleep(5)
        yield item
