from main.models import DailyData


class DSEScrapingPipeline(object):
    def process_item(self, item, spider):

        item ={k: v.replace(',', '').replace('--', '0') for k, v in item.items()}
        DailyData.objects.update_or_create(
            trading_code=item['trading_code'],
            last_traded_price=float(item['last_traded_price']),
            high=float(item['high']),
            low=float(item['low']),
            closing_price=float(item['closing_price']),
            yesterdays_closing_price=float(item['yesterdays_closing_price']),
            change=float(item['change']),
            trade=int(item['trade']),
            value_mn=float(item['value_mn']),
            volume=float(item['volume']),
        )
        return item
