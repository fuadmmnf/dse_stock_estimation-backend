import sys
import scrapy
from scrapy.loader import ItemLoader
from scrapy_app.dse_scraping.items import DisplayCompanyItem

class DisplayCompanySpider(scrapy.Spider):
    name = "display_company"
    start_urls = ['https://www.dse.com.bd/displayCompany.php?name=ACFL']

    def parse(self, response):

        requested_page = response.url.split("/")[-2]

        company_name = response.xpath("//div[@id = 'section-to-print']/h2/i")
        company_name = company_name.xpath('text()').get()
        company_name = company_name.encode('ascii','ignore').strip()

        tables = response.xpath('//table[@id="company"]')
        table_items = tables[2].xpath('./tr/*')

        sector = table_items[-2].xpath('text()').get().encode('ascii','ignore').strip()
        total_no_of_outstanding_securities = table_items[-4].xpath('text()').get().encode('ascii','ignore').strip()

        try:
            item = DisplayCompanyItem()

            item['sector'] = sector
            item['name'] = company_name
            item['total_no_of_outstanding_securities'] = total_no_of_outstanding_securities

            yield item

        except:
            raise Exception("exception occurred")
            print("Oops!", sys.exc_info()[0], "occurred.")
