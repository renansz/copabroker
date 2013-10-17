from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from broker.models import Stock
from compiler.ast import Dict

def home(request):
    g = Stock.objects.order_by('group')
    groups = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[]}
    for stock in g:
        groups[stock.group].append(stock)
    return render_to_response("broker/broker.html",{'groups':groups})


def book(request):
    return render_to_response("broker/book.html",{})