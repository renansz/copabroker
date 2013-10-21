# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from broker.models import StockView
from compiler.ast import Dict
import json

def home(request):
    g = StockView.objects.order_by('group')
    groups = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[]}
    for stock in g:
        groups[stock.group].append(stock)
    return render_to_response("broker/broker.html",{'groups':groups})


def book(request,ticker):
    #precisa pegar o book do ativo em questão
    #na teoria seria a chamada /api/get_book/ticker
    #carregar a imagem (ou as dimensoes de corte, pegar o ultimo preço e exibir o book
    stock = StockView.objects.filter(ticker = ticker)[0]
    return render_to_response("broker/book.html",{'stock': stock})

def profile(request):
    #precisa pegar o portfolio do usuario em questao
    #na teoria seria a chamada /api/get_user_portfolio/ID
    #acredito que seria util já termos o preço do ativo na resposta da api ou devemos fazer uma segunda query mesmo?

    return render_to_response("broker/profile.html",{'user':'Joao da Silva','stocks':[{'name':'BRA2014','qty':150,'price':49.87},{'name':'NIG2014','qty':350,'price':3.13},{'name':'JAP2014','qty':500,'price':2.13},{'name':'EUA2014','qty':1000,'price':9.02},{'name':'GER2014','qty':10,'price':41.05},{'name':'ALG2014','qty':3500,'price':5.13},{'name':'HOL2014','qty':150,'price':31.57},{'name':'FRA2014','qty':800,'price':13.13}]})
                                                     