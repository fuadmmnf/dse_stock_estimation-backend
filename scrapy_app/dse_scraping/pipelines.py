from main.models import DailyData, Company
from main.apps import MainConfig

class DSEScrapingPipeline(object):
    def __process_sharedata(self, item):
        item = {k: v.replace(',', '').replace('--', '0') for k, v in item.items()}
        company_data = DailyData.objects.filter(trading_code__exact=item['trading_code']).order_by('-parsed_date')[: 1]

        if len(company_data) > 0:
            company_data[0].trading_code = item['trading_code']
            company_data[0].last_traded_price = float(item['last_traded_price'])
            company_data[0].high = float(item['high'])
            company_data[0].low = float(item['low'])
            company_data[0].closing_price = float(item['closing_price'])
            company_data[0].yesterdays_closing_price = float(item['yesterdays_closing_price'])
            company_data[0].change = float(item['change'])
            company_data[0].trade = int(item['trade'])
            company_data[0].value_mn = float(item['value_mn'])
            company_data[0].volume = float(item['volume'])
            company_data[0].save(force_update=True)
        else:
            DailyData.objects.create(
                trading_code=item['trading_code'],
                last_traded_price=float(item['last_traded_price']),
                high=float(item['high']),
                low=float(item['low']),
                closing_price=float(item['closing_price']),
                predicted_next_day_closing_price= self.__predict_closing(item),
                yesterdays_closing_price=float(item['yesterdays_closing_price']),
                change=float(item['change']),
                trade=int(item['trade']),
                value_mn=float(item['value_mn']),
                volume=float(item['volume'])

            )

    def __process_companydata(self, item, is_create):
        if is_create:
            Company.objects.create(
                name=item['name'],
                trading_code=item['trading_code'],
                sector=item['sector'],
                category=item['category'],

            )
        else:
            print(item['sector'].decode("utf-8"))
            company = Company.objects.filter(name__exact=item['name'].decode("utf-8"))[0]

            sec = item['sector'].decode("utf-8")
            company.sector = sec
            company.save()

    def process_item(self, item, spider):
        if spider.name == 'latest_share':
            self.__process_sharedata(item)
        elif spider.name == 'display_company' or spider.name == 'companies':
            self.__process_companydata(item, spider.name == 'companies')
        return item

    def __predict_closing(self, item):
        company_model = MainConfig.dse_models[item['trading_code']]
        # return company_model.predict([['macd', 'ema_long', 'sample_moving_average']])[0]
        return 0.0
