import scrapy
from scrapy_djangoitem import DjangoItem
from main.models import DailyData, Company

class DailyShareData(DjangoItem):
    django_model = DailyData



class CompanyItem(DjangoItem):
    django_model = Company


class DisplayCompanyItem(scrapy.Item):
    name = scrapy.Field()
    sector = scrapy.Field()
    total_no_of_outstanding_securities = scrapy.Field()
