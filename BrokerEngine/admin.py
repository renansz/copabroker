from models import User, Stock, Order, PortfolioItem, Historical
from django.contrib import admin

admin.site.register(User)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(PortfolioItem)
admin.site.register(Historical)