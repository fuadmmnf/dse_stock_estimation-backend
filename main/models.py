import json
import uuid

from django.db import models
from datetime import datetime


class Company(models.Model):
    unique_id = models.UUIDField(primary_key=True, blank=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False)
    trading_code = models.CharField(max_length=100, null=False)
    sector = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False)
    # total_no_of_outstanding_securities = models.IntegerField()
    # This is for basic and custom serialisation to return it to client as a JSON.


class DailyData(models.Model):
    unique_id = models.UUIDField(primary_key=True, blank=True, default=uuid.uuid4)
    trading_code = models.CharField(max_length=100, null=False)
    parsed_date = models.DateTimeField(default=datetime.now())
    last_traded_price = models.DecimalField(max_digits=13, decimal_places=3)
    high = models.DecimalField(max_digits=13, decimal_places=3)
    low = models.DecimalField(max_digits=13, decimal_places=3)
    closing_price = models.DecimalField(max_digits=13, decimal_places=3)
    predicted_next_day_ohlc_price = models.DecimalField(max_digits=13, decimal_places=3)
    yesterdays_closing_price = models.DecimalField(max_digits=13, decimal_places=3)
    change = models.DecimalField(max_digits=13, decimal_places=3)
    trade = models.IntegerField()
    value_mn = models.DecimalField(max_digits=13, decimal_places=3)
    volume = models.DecimalField(max_digits=13, decimal_places=3)
