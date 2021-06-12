import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import time


class AIASpider(scrapy.Spider):
    name = "aia"
    all_archs = {}

    def start_requests(self):
        base_url = 'https://www.aiany.org/resources/firm-directory/?api_page='
        urls = [base_url + str(i) for i in range(1,28)]
        # urls = [base_url + str(i) for i in range(1,4)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hxs = Selector(response)
        items = hxs.xpath('//div[@class="textReg title"]/a')
        for arch in items:
            arch_link = arch.xpath('@href').extract()
            sub_url = arch_link[0]
            print(sub_url)
            # time.sleep(5)
            yield scrapy.Request(sub_url, callback=self.parse_arch_page)

    def parse_arch_page(self, response):
        hxs = Selector(response)
        item = {}
        item['Title'] = hxs.xpath('//div[@id="content"]/header/div/div/h1/text()').extract()[0]
        firm_info = hxs.xpath('//div[@id="content"]/section[@class="page-content"]/'
                                     'div[@class="layout-left-sidebar block"]/div[@class="sidebar"]'
                                     '/div[@class="module module-sidebar module-sidebar-facts block"]').extract()
        tsoup = BeautifulSoup(firm_info[0], "lxml")
        spans = tsoup.findAll('span')
        span_length = len(spans)
        for i in range(span_length)[::2]:
            try:
                item[spans[i].text] = spans[i+1].text
            except:
                pass

        item['Url'] = response.url

        self.all_archs[item['Url']] = item
