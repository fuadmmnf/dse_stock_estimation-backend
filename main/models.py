import json
import uuid

from django.db import models
from django.utils import timezone


class Company(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data = models.TextField()  # this stands for our crawled data
    date = models.DateTimeField(default=timezone.now)

    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id

class DailyData(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    trading_code = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(default=timezone.now)
    last_traded_price = models.DecimalField()
    high = models.DecimalField()
    low = models.DecimalField()
    closing_price = models.DecimalField()
    yesterdays_closing_price = models.DecimalField()
    change = models.DecimalField()
    trade = models.IntegerField()
    value_mn = models.DecimalField()
    volume = models.DecimalField()