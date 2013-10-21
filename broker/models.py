# -*- coding: utf-8 -*-
from django.db import models

class StockView(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    group = models.CharField(max_length=1)
    last_price = models.DecimalField(max_digits=10,decimal_places=2,default=3.13)
    flag_position = models.CharField(max_length=16)
