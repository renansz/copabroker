# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from broker.models import StockView,BrokerNew
from BrokerEngine.models import Historical,Stock
from BrokerEngine.models import User as brokerUser
from django.contrib.auth.models import User

from decimal import Decimal

import json
import traceback
import datetime

class JsonResponse(HttpResponse):
    def __init__(self, content={}, status=None):
        super(JsonResponse, self).__init__(json.dumps(content), mimetype='application/json', status=status)

@login_required
def grupos(request):
    """exibe todos os times divididos em grupo ou rankeados (selecao do usuario) """
    g = [g for g in StockView.objects.prefetch_related()]
    groups = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[]}
    for stock in g:
        _dict = {'name':stock.ticker.name, 'ticker':stock.ticker.ticker, 'image':stock.image}
        try:
            h = Historical.objects.filter(stock = stock.ticker).order_by('-timestamp').values('value')[0]
            _dict['value'] = h['value']
        except:
            _dict['value'] = 0.00
        groups[stock.group].append(_dict)
    return render_to_response("broker/grupos.html",{'groups': sorted(groups.iteritems())})

@login_required
def news(request):
    """exibe as notícias mais recentes na página de notícias"""
    news = BrokerNew.objects.order_by('date')
    return render_to_response("broker/news.html",{'news': news})

@login_required
def book(request,ticker):
    """View que renderiza o book de ofertas de um determinado ativo"""
    #TODO Repliquei o ticker na tabela stockview para nao ter q consultar o banco novamente, se precisar do nome tem que gravar em algum lugar, ou fazer a referencia cruzada mesmo.
    #TODO testar a logica ticker_id ticker_name .. etc
    try:
        s = StockView.objects.get(ticker_name = ticker)
    except:
        #TODO criar uma página de erro com o objeto abaixo
        s = StockView(ticker_id= 0, ticker_name= None, group= '#', image= 'http://placehold.it/150x85')
    stock = {'name': s.country_name, 'ticker': s.ticker_name, 'image': s.image}
    return render_to_response("broker/book.html",{'stock': stock})

@login_required
def painel(request,ticker):
    """View que renderiza o book de ofertas de um determinado ativo"""
    #TODO Repliquei o ticker na tabela stockview para nao ter q consultar o banco novamente, se precisar do nome tem que gravar em algum lugar, ou fazer a referencia cruzada mesmo.
    #TODO testar a logica ticker_id ticker_name .. etc
    try:
        s = StockView.objects.get(ticker_name = ticker)
    except:
        #TODO criar uma página de erro com o objeto abaixo
        s = StockView(ticker_id= 0, ticker_name= None, group= '#', image= 'http://placehold.it/150x85')
    stock = {'name': s.country_name, 'ticker': s.ticker_name, 'image': s.image}
    return render_to_response("broker/painel.html",{'stock': stock})


@login_required
def minha_carteira(request):
    #precisa pegar o portfolio do usuario em questao
    #na teoria seria a chamada /api/get_user_portfolio/ID e já calcular o total 
    #acredito que seria util já termos o preço do ativo na resposta da api ou devemos fazer uma segunda query mesmo?
    #TODO associar à conta django.auth e verificar cookies
    try:
        u = brokerUser.objects.get(pk=request.session.get(u'_auth_user_id'))
    except:
        #TODO criar uma página de erro com o objeto abaixo
        u = brokerUser(id= 0, name= u"Joe Doe", saldo= 0)
    return render_to_response("broker/minha_carteira.html",{'user': u})

def login_user(request):
  logout(request)
  username = password = ''
  if request.POST:
    #se o usuario estiver logado no FB, tratar separadamentes
    if request.POST.has_key('fb'):
        pass
        #redirect nao está funcionando direito, tem q fazer o esquema certo.
        #return JsonResponse({'status':'ok', 'url':'/broker/grupos'})
        #falta definir o que fazer se ele estiver no primeiro acesso via facebook.
    else:
      user = authenticate(username=request.POST['username'], password=request.POST['password'])
      if user and user.is_active:
        login(request, user)
        return HttpResponseRedirect('/broker/grupos')
      else:
        return render_to_response('login.html',{'error':'Usuario ou senha inválidos'}, context_instance=RequestContext(request))
  return render_to_response('login.html',context_instance=RequestContext(request))

#TODO implementar logout!
@login_required
def logout_user(request):
  print 'none'
  logout(request)
  return render_to_response('login.html',context_instance=RequestContext(request))

#TODO views que ainda faltam
def noticias(request):
  pass

def minhas_ordens(request):
  pass

def fundamentos(request):
  pass

def tutorial(request):
  pass

def cadastro(request):
  pass

#TODO escrever a funcao de logout
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

