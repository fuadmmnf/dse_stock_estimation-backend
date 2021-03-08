from django.http import JsonResponse
import json
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from .models import Company, DailyData


def test_api(request):
    return JsonResponse({'res': ''})




@csrf_exempt
def get_companies(request):
    if request.method == 'POST':
        return JsonResponse({'res': 'must be get request with category_name'})

    companies = Company.objects.get()
    return JsonResponse({'data': companies}, safe=False)


@csrf_exempt
def get_predictions_by_date(request):
    if request.method == 'POST':
        return JsonResponse({'res': 'must be get request'})


    daily_data = DailyData.objects.filter(date__exact=date.today()).get()
    return JsonResponse({'data': daily_data}, safe=False)


@csrf_exempt
def get_data_by_company(request, company_code):
    if request.method == 'POST':
        return JsonResponse({'res': 'must be get request'})


    company_predictions = DailyData.objects\
        .filter(company_code__exact= company_code)\
        .order_by('-date')[:30]

    return JsonResponse({'data': company_predictions}, safe=False)