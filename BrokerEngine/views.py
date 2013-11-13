# Create your views here.

from django.http import HttpResponse

from models import User, Stock, Order, PortfolioItem, Historical
import order_queue

from decimal import Decimal

import traceback
import json
import datetime

class JsonResponse(HttpResponse):
    def __init__(self, content={}, status=None):
        super(JsonResponse, self).__init__(json.dumps(content), mimetype='application/json', status=status)

def get_all_tickers(request):
    """ Obtém a lista de todos os ativos cadastrados """
    
    # @todo: Colocar status nos ativos: (ativos/inativos, negociavel/inegociavel, etc)
    response = [ (t.ticker, t.name) for t in Stock.objects.all()]
    return JsonResponse(response)

def get_book(request, ticker):
    
    # @todo checar a questão da data de inclusão de ordens para o caso de modificações.
    size = request.GET.get('size', 10)
    stock = Stock.objects.get(ticker=ticker)

    compras = Order.objects.filter(
        status__in=(Order.STATUS_OPEN, Order.STATUS_PARTIAL), 
        tipo=Order.ORDER_BUY, 
        stock=stock
        ).order_by('-value','included')[:size]
    vendas  = Order.objects.filter(
        status__in=(Order.STATUS_OPEN, Order.STATUS_PARTIAL), 
        tipo=Order.ORDER_SELL, 
        stock=stock
        ).order_by( 'value','included')[:size]
    
    #clist = [ ("R$ %s" %unicode(c.value).replace('.',','), c.qty) for c in compras]
    #vlist = [ ("R$ %s" %unicode(v.value).replace('.',','), v.qty) for v in vendas ]
    
    clist = [ (unicode(c.value), c.qty) for c in compras]
    vlist = [ (unicode(v.value), v.qty) for v in vendas ]
    
    response = {'ticker': stock.ticker, 'buy':clist, 'sell':vlist, 'last': 99.99}
    return JsonResponse(response)

def get_user_portfolio(request):
    #alterei aqui... ,esmo caso ali abaixo
    #(ORIGINAL) user  = User.objects.get( id=request.POST['user_id'  ])
    user = User.objects.get(pk=request.session.get(u'_auth_user_id'))

    portfolio = PortfolioItem.objects.filter(user=user).order_by('stock')
    response = [(p.stock.ticker, p.qty) for p in portfolio if p.qty != 0]
    return JsonResponse(response)

# Ver se dá para usar aquele pacote 
def get_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    response = {
        'ticker' : order.stock.ticker,
        'tipo' : order.tipo,
        'status' : order.status,
        'original_qty' : order.original_qty,
        'qty' : order.qty,
        'value' : unicode(order.value),
        'included' : unicode(order.included),
        'cancel_reason': order.cancel_reason
    }
    return JsonResponse(response)
    
#@atomic
def new_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'only POST method allowed'}, 405)
    try:
        #alterei aqui... nao sei o que seria mais correto fazer, mas dessa foram , garantimos que o user da session é quem faz o request e nao precisamos de mais uma consulta ao banco pra pegar o ticker
        #(ORIGINAL) user  = User.objects.get( id=request.POST['user_id'  ])
        #(ORIGINAL) user  = User.objects.get( id=request.POST['user_id'  ])
        user  = User.objects.get(pk=request.session.get(u'_auth_user_id'))
        stock = Stock.objects.get(ticker=request.POST['ticker'])
        
        tipo = request.POST['order_type']
        qty = int(request.POST['order_qty'])
        value = Decimal(request.POST['order_value'])
        
        ordem = Order(user=user, stock=stock, tipo=tipo, original_qty=qty, qty=qty, value=value)

        ordem.save() 
        order_queue.add_order(ordem, stock.ticker)

        return JsonResponse({'status':'ok', 'order_id':ordem.id}, 201)
    except Exception as e:
        return JsonResponse({'error': unicode(e), 'traceback': traceback.format_exc()}, 500)
    
def update_order(request):
    if request.method not in ('PATCH', 'PUT'):
        return JsonResponse({'error': 'only PATCH and PUT methods are allowed'}, 405)
        
    try:
        order = Order.objecs.get( id=request.POST['order_id'] )
        new_qty = int(request.POST['new_qty'])
        new_value = int(request.POST['new_value'])
        
        if new_qty < order.qty:
            return JsonResponse({'error': 'new_qty smaller than current qty' }, 400)
        order.qty = new_qty
        order.value = new_value
        order.included = datetime.datetime.now()
        order.save()
    except Exception as e:
        return JsonResponse({'error': unicode(e), 'traceback': traceback.format_exc()}, 500)
        
        
    # Nao esquecer de atualizar o timestamp
    
