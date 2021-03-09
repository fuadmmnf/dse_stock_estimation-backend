from django.core import serializers
from django.http import JsonResponse
from django.utils.timezone import datetime #important if using timezones
from django.views.decorators.csrf import csrf_exempt
from .models import Company, DailyData


def test_api(request):
    return JsonResponse({'res': ''})


@csrf_exempt
def get_companies(request):
    if request.method == 'POST':
        return JsonResponse({'res': 'must be get request with category_name'})

    companies = Company.objects.all()
    return JsonResponse({'data': serializers.serialize('json', companies)}, safe=False)


@csrf_exempt
def get_predictions_by_date(request):
    if request.method == 'POST':
        return JsonResponse({'res': 'must be get request'})


    daily_data = DailyData.objects.filter(date__day=datetime.now()).get()
    return JsonResponse({'data': serializers.serialize('json', daily_data)})


@csrf_exempt
def get_data_by_company(request, company_code):
    if request.method == 'POST':
        return JsonResponse({'res': 'must be get request'})

    company_predictions = DailyData.objects \
                              .filter(trading_code__exact=company_code) \
                              .order_by('-date')[:30]

    return JsonResponse({'data': serializers.serialize('json', company_predictions)}, safe=False)
