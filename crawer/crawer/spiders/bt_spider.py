# -*- coding: utf-8 -*-
import scrapy
import scrapy.log
import sys

# from Model.BtModel import BtItem
from crawer.items import BtItem

reload(sys)
sys.setdefaultencoding('utf-8')


class BtIndexSpider(scrapy.Spider):
    name = '404Index'
    allowed_domains = []

    def start_requests(self):
        self.url_index = 'https://bt.orzx.im'
        start_urls = [
            'https://bt.orzx.im/list.php?BoardID=2&ItemID=17'
        ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        login_page = response.xpath('//div/div/div/div/div/div[contains(@class,"left size-auto")]')
        question = login_page.xpath('text()').extract()[0].strip()
        print(question)
        if u'表番' in question:
            answer = '里番'
        elif u'Hentai' in question:
            answer = '绅士'
        elif u'School' in question:
            answer = '人渣诚'
        else:
            answer = 'failed'
            print('failed')
        print(answer.decode('utf-8'))
        return scrapy.FormRequest.from_response(
            response,
            formdata={'a': answer},
            callback=self.content_parse
        )

    def content_parse(self, response):
        if "authentication failed" in response.body:
            self.log("Login failed", level=scrapy.log.ERROR)
            return

        token = response.xpath('//table[contains(@id,"viewarticle")]/tr/td/span/@id').extract()
        token = token[0].encode('utf-8')

        table = \
            response.xpath('//table[contains(@id,"viewarticle")]/tr/td/table[contains(@id,"' + token + '")]/tbody/tr')[
                0]
        href = table.xpath('//td/p/a/@href').extract()
        info = table.xpath('//td[contains(@id,"'+token+'")]/text()').extract()

        for i in range(len(href)):
            items = BtItem()
            sub_url = self.url_index + '/' + href[i]
            items['file_size'] = info[i * 3 + 1]
            items['pub_time'] = info[i * 3 + 2]
            yield scrapy.Request(sub_url, meta={'items': items}, callback=self.get_bt_detail, dont_filter=True)

        next = table.xpath('//a[contains(@class,"p_redirect")]/@href').extract()
        if next[2]!=next[3]:
            next = self.url_index+'/'+next[2]
            print(next)
            yield scrapy.Request(next, callback=self.content_parse, dont_filter=True)

    def get_bt_detail(self, response):
        items = response.meta['items']
        table = response.xpath('//table[contains(@class,"MainTable")]')[2]
        table = table.xpath('//tr/td/table/tr/td/table')[0]
        token = table.xpath('@id').get()

        name = table.xpath('//h3[contains(@id,"' + token + '")]/text()').get()
        items['name'] = name

        href = table.xpath('//p/a[contains(@id,"' + token + '")]/@href').re(r'id=(\d*)')[0]
        items['href'] = 'bt.orzx.im/display.php?id=' + href

        yield items
