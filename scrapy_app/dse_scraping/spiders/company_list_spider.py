import sys
import scrapy
from scrapy.loader import ItemLoader
from scrapy_app.dse_scraping.items import CompanyItem

class CompanySpider(scrapy.Spider):
    name = "companies"
    start_urls = ['https://www.dse.com.bd/company_listing.php']


    def parse(self, response):

        requested_page = response.url.split("/")[-2]
        main_div = response.xpath("//div[@class='col-md-12 col-sm-12 col-xs-18']/*")

        print('<------------------------------------------------------------- look here ------------------------------------------------------------->')

        for div in main_div[2].xpath("//div[@class='col-lg-4 col-md-4 col-sm-6 col-xs-12 background-white']"):
            category = div.xpath('./*')[0]
            category = category.xpath('./h2[@class="BodyHead"]/text()').get()

            items = []
            body_content = div.xpath('./*')[1]
            for company in body_content.xpath('./*'):
                item = company.xpath('text()').get()
                items.append(item.encode('ascii','ignore'))


            name_code_pairs = zip(items[0:][::2], items[1:][::2])
            for pair in name_code_pairs:
                item = CompanyItem()

                pair = list(pair)
                print(type(pair))

                if ' ' in pair[0]: pair = self.swap_values(pair)
                item['name'] = pair[1].strip('()')
                item['category'] = category
                item['trading_code'] = pair[0]
                item['sector'] = ''
                yield item

    def swap_values(self, values):
        temp = values[0]
        values[0] = values[1]
        values[1] = temp
        return values
