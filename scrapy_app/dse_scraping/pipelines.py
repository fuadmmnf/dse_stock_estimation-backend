import uuid
from main.models import DailyData


class DSEScrapingPipeline(object):
    def process_item(self, item, spider):
        item = {k: v.replace(',', '').replace('--', '0') for k, v in item.items()}
        company_data = DailyData.objects.filter(trading_code__exact=item['trading_code']).order_by('-date')[: 1]

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
                yesterdays_closing_price=float(item['yesterdays_closing_price']),
                change=float(item['change']),
                trade=int(item['trade']),
                value_mn=float(item['value_mn']),
                volume=float(item['volume'])

            )
        return item
