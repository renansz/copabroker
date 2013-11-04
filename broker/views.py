# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from broker.models import StockView
from BrokerEngine.models import Historical,Stock

from decimal import Decimal

import traceback
import datetime

def home(request):
    g = [g for g in StockView.objects.prefetch_related()]
    groups = {'A':[],'B':[]}
    for stock in g:
        _dict = {'name':stock.ticker.name, 'ticker':stock.ticker.ticker, 'group':stock.group, 'flag_position':stock.flag_position}
        try:
            h = Historical.objects.filter(stock = stock.ticker).order_by('-timestamp').values('value')[0]
            _dict['value'] = h['value']
        except:
            _dict['value'] = 0.00
        groups[stock.group].append(_dict)
    return render_to_response("broker/broker.html",{'groups': groups})

def book(request,ticker):
    """View que renderiza o book de ofertas de um determinado ativo"""
    #Dá pra passar direto e pegar o nome usando a referencia do ticker? ou teria que replicar o campo name no stockview?
    _ticker_id = Stock.objects.get(ticker=ticker)
    try:
        s = StockView.objects.get(ticker_id = _ticker_id.id)
    except:
        _ticker_id = {'id':0, 'name': None}
        s = {'flag_position':''}
    stock = {'name': _ticker_id.name, 'ticker':  ticker, 'flag_position': s.flag_position}
    return render_to_response("broker/book.html",{'stock': stock})

def profile(request,user_id):
    #precisa pegar o portfolio do usuario em questao
    #na teoria seria a chamada /api/get_user_portfolio/ID
    #acredito que seria util já termos o preço do ativo na resposta da api ou devemos fazer uma segunda query mesmo?

    return render_to_response("broker/profile.html",{'user':'Joao da Silva','stocks':[{'name':'BRA2014','qty':150,'price':49.87},{'name':'NIG2014','qty':350,'price':3.13},{'name':'JAP2014','qty':500,'price':2.13},{'name':'EUA2014','qty':1000,'price':9.02},{'name':'GER2014','qty':10,'price':41.05},{'name':'ALG2014','qty':3500,'price':5.13},{'name':'HOL2014','qty':150,'price':31.57},{'name':'FRA2014','qty':800,'price':13.13}]})
                                                     
