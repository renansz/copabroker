# -*- coding: utf-8 -*-
from django.db import models
from BrokerEngine.models import User, Stock, Order, PortfolioItem, Historical

class StockView(models.Model):
    ticker = models.ForeignKey(Stock)
    ticker_name = models.CharField(max_length=10)
    group = models.CharField(max_length=1)
    image = models.CharField(max_length=16)

    def __unicode__(self):
        return "StockView(%s, %s, %c, %s)" %(self.ticker, self.ticker_name, self.group, self.image)
