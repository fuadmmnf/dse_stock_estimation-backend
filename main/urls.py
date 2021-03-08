from django.urls import path
from .views import *

urlpatterns = [
    # path("test/", test_api, name="test_api"),
    path("companies/", get_companies, name="get_companies"),
    path("companies/<slug:company_code>/data/", get_data_by_company, name="get_data_by_company"),
    path("predictions/", get_predictions_by_date, name="get_predictions_by_date"),
]
