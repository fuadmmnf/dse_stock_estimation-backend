from main.models import DailyData, Company
from main.apps import MainConfig
import numpy as np

class DSEScrapingPipeline(object):
    def __process_sharedata(self, item):
        item = {k: v.replace(',', '').replace('--', '0') for k, v in item.items()}
        company_data = DailyData.objects.filter(trading_code__exact=item['trading_code']).order_by('-parsed_date')[: 1]

        if item['trading_code'] in MainConfig.dse_models:
            if len(company_data) > 0:
                company_data[0].trading_code = item['trading_code']
                company_data[0].last_traded_price = round(float(item['last_traded_price']), 3)
                company_data[0].high = round(float(item['high']), 3)
                company_data[0].low = round(float(item['low']), 3)
                company_data[0].closing_price = round(float(item['closing_price']), 3)
                company_data[0].predicted_next_day_closing_price = round(self.__predict_closing(item), 3)
                company_data[0].yesterdays_closing_price = round(float(item['yesterdays_closing_price']), 3)
                company_data[0].change = round(float(item['change']), 3)
                company_data[0].trade = int(item['trade'])
                company_data[0].value_mn = round(float(item['value_mn']), 3)
                company_data[0].volume = round(float(item['volume']), 3)
                company_data[0].save(force_update=True)
            else:
                DailyData.objects.create(
                    trading_code=item['trading_code'],
                    last_traded_price=round(float(item['last_traded_price']), 3),
                    high=round(float(item['high']), 3),
                    low=round(float(item['low']), 3),
                    closing_price=round(float(item['closing_price']), 3),
                    predicted_next_day_closing_price=round(self.__predict_closing(item), 3),
                    yesterdays_closing_price=round(float(item['yesterdays_closing_price']), 3),
                    change=round(float(item['change']), 3),
                    trade=int(item['trade']),
                    value_mn=round(float(item['value_mn']), 3),
                    volume=round(float(item['volume']), 3)

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
        ohlc = (float(item['yesterdays_closing_price']) + float(item['high']) + float(item['low']) + float(
            item['closing_price'])) / 4

        scaled_ohlc = MainConfig.minmax_scalers[item['trading_code']].transform([ohlc])
        predicted_ohlc = MainConfig.dse_models[item['trading_code']].predict(np.reshape(scaled_ohlc, (1, 1, 1))) if item['trading_code'] in MainConfig.dse_models else 0.0
        predicted_ohlc = MainConfig.minmax_scalers[item['trading_code']].inverse_transform(predicted_ohlc)
        print('predicted eije')
        print(item['trading_code'] + ': ' + str(predicted_ohlc))
        return predicted_ohlc
