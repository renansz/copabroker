# -*- coding: utf-8 -*-
from django.db import models
from BrokerEngine.models import User, Stock, Order, PortfolioItem, Historical

class StockView(models.Model):
  ticker = models.ForeignKey(Stock)
  ticker_name = models.CharField(max_length=3)
  country_name = models.CharField(max_length=30)
  group = models.CharField(max_length=1)
  image = models.CharField(max_length=16)
  
  def __unicode__(self):
    return "StockView(%s, %s, %c, %s)" %(self.ticker, self.ticker_name, self.group, self.image)
        
class BrokerNew(models.Model):
  title = models.CharField(max_length=60)
  short_text = models.CharField(max_length=180)
  full_text = models.TextField()
  date = models.TimeField()
  category = models.CharField(max_length=10)
  image_path = models.CharField(max_length=16)
  
  def __unicode__(self):
    return "BrokerNew(%s, %s, %s, %s,%s,%s)" %(self.title, self.short_text, self.full_text, self.date, self.category, self.image_path)
