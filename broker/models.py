from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    country_name = models.CharField(max_length=30)
    group = models.CharField(max_length=1)
    fair_value = models.DecimalField(max_digits=10,decimal_places=2,default=3.13)

class Order(models.Model):
    ORDER_TYPES = (
        (u'A',u'Ask'),
        (u'B',u'Bid'),
    )
    type = models.CharField(max_length=1, choices = ORDER_TYPES)
    stock = models.ForeignKey(Stock)
    price = models.DecimalField(max_digits=4,decimal_places=2,default=0)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    @classmethod
    def create(cls,type,stock,price,quantity):
        order = cls(type=type,stock=stock,price=price,quantity=quantity)
        order.total = price * quantity
        return order
        