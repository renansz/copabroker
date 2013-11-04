# -*- coding: utf-8 -*-
from django.db import models
from BrokerEngine.models import User, Stock, Order, PortfolioItem, Historical

class StockView(models.Model):
    ticker = models.ForeignKey(Stock)
    group = models.CharField(max_length=1)
    flag_position = models.CharField(max_length=16)

    def __unicode__(self):
        return "StockView(%s, %c, %s)" %(self.ticker, self.group, self.flag_position)
