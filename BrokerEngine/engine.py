
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from models import User, Stock, Order, PortfolioItem, Historical
import logging 
import traceback

# Logger basicão, só para DEV. Em produção vamos afinar isso.
logging.basicConfig(
    filename="BrokerEngine.engine.log", 
    level=logging.INFO, 
    format="%(asctime)s %(levelname)8s %(name)s %(module)s.%(funcName)s - %(message)s")

logger = logging.getLogger("CopaBroker.BrokerEngine.engine")

def modifica_portfolio_usuario(user, stock, qty):
    """ Adiciona ou remove ações de um dado ticker ao portfólio do usuário dado """
    logger.info(u" *** Atualizando portfolio de %s: %d %s" %(user.name, qty, stock.ticker))
    item, created = PortfolioItem.objects.get_or_create(user=user,stock=stock,defaults={'qty': 0})
    item.qty += qty
    item.save()

def efetua_negociacao(user_buy_side, user_sell_side, stock, qty, valor_transacao):
    """ Efetua uma negociação de um ativo entre dois usuários. A atomicidade da 
    operação deve ser garantida externamente """
    logger.info(u" *** Efetuando Negociação de %d %s vendidas de %s para %s a %f" \
        %(qty, stock.ticker, user_sell_side.name, user_buy_side.name, valor_transacao))

    if user_buy_side.saldo < valor_transacao: #@todo usar saldo bloqueado
        # Verifica se o usuario que vai comprar tem saldo suficiente
        logger.info(u" *** Usuario %s nao tem fundos para negociação" %user_buy_side)
        raise ValueError("User is broken!")
        
    user_buy_side.saldo -= valor_transacao
    modifica_portfolio_usuario(user_buy_side, stock, qty)
    
    user_sell_side.saldo += valor_transacao
    modifica_portfolio_usuario(user_sell_side, stock, -qty)
    
    logger.info(u" *** Negociação OK")
    
def get_book_top(stock, order_type):
    """ Obtém a ordem mais antiga com o valor mais negociável em um book """
    value = '-value' if order_type == Order.ORDER_BUY else 'value'
    try:
        return Order.objects.filter(
            status__in=[Order.STATUS_OPEN, Order.STATUS_PARTIAL], 
            tipo=order_type, 
            stock=stock
            ).order_by(value,'included')[0]
    except ObjectDoesNotExist:
        return None
    except IndexError:
        return None

def finaliza_ordem(ordem):
    """ Finaliza a ordem dada """
    ordem.status = Order.STATUS_FINALIZED
    ordem.save()
    logger.info("Ordem Finalizada: %s" %ordem)
    
def cancela_ordem(ordem, reason=None):
    """ Cancela a ordem dada. Opcionalmente informa uma razão para tal. """
    ordem.status = Order.STATUS_CANCELLED
    if reason: ordem.cancel_reason = reason
    ordem.save()
    logger.info("Ordem Cancelada: %s" %ordem)

def adiciona_ordem(ordem):
    """ Adiciona uma ordem a um book de um ativo. """
    if ordem.qty == ordem.original_qty: 
        # Qdo uma ordem cai no topo do book depois de ter agredido a outra ponta, ela cai nesse caso.
        ordem.status = Order.STATUS_OPEN
    ordem.save()
    logger.info("Ordem Adicionada: %s" %ordem)
    
def pos_processa_ordem(ordem):
    """ Verificações feitas após uma ordem ter sido executada """
    logger.info(u"Ordem Pós-Processada: %s" %ordem)
    if ordem.qty == 0:
        finaliza_ordem(ordem)
        return
    if ordem.qty != ordem.original_qty:
        ordem.status = Order.STATUS_PARTIAL
    ordem.save()

def processa_ordem(ordem):
    """ Processa uma ordem dada. Essa função é o ponto de entrada de uma ordem nova. """
    logger.info("Processando ordem: %s" %ordem)
    stock = ordem.stock
    if ordem.status not in (Order.STATUS_OPEN, Order.STATUS_PARTIAL, Order.STATUS_NEW): # Nunca deveria acontecer, mas é bom checar
        cancela_ordem(ordem, u"Status inválido durante o processamento. A ordem foi abortada.")
        logger.warn(u"Ordem inválida para processamento: %s. Status deveria ser 'Order.STATUS_OPEN', 'Order.STATUS_PARTIAL' ou 'Order.STATUS_NEW'" %ordem)
        return
    
    if ordem.tipo == Order.ORDER_BUY:
        book_top = get_book_top(stock, Order.ORDER_SELL)
        logger.info("Book top is: %s" %book_top)
        if book_top is not None and ordem.value >= book_top.value:
            executa_ordem(ordem, book_top)
        else:
            adiciona_ordem(ordem)
            
    if ordem.tipo == Order.ORDER_SELL:
        book_top = get_book_top(stock, Order.ORDER_BUY)
        logger.info("Book top is: %s" %book_top)
        if book_top is not None and ordem.value <= book_top.value: # -> ISSO AQUI ESTÁ FALHANDO BIZARRAMENTE!
            executa_ordem(ordem, book_top)
        else:
            adiciona_ordem(ordem)

def executa_ordem(ordem, book_top):
    """ Executa uma ordem dada contra outra que veio do topo do book de um ativo """
    logger.info(" (!) Executando ordens: %s contra %s" %(ordem, book_top))
    
    # Identifica quem é quem (compra e venda x topo do book e ordem agressora)
    if ordem.tipo == Order.ORDER_BUY:
        ordem_compra = ordem
        ordem_venda  = book_top
    elif ordem.tipo == Order.ORDER_SELL:
        ordem_compra = book_top
        ordem_venda  = ordem

    # Identifica os valores da negociação
    value = min(ordem_compra.value, ordem_venda.value)  # Valor que será efetivamente negociado
    qty   = min(ordem_compra.qty  , ordem_venda.qty)    # Quantidade que será de fato executada
    
    # Checa se a execução será parcial ou não
    continua_ordem = qty != ordem.qty                   # Checa se a ordem recebida será finalizada
    
    # Inicia o processo de negociação entre as duas ordens - bloco deve ser atômico.
    try:
        rb = transaction.savepoint() # Savepoint
        efetua_negociacao(ordem_compra.user, ordem_venda.user, ordem_compra.stock, qty, value*qty) # Sessao critica #1
        
        ordem_compra.qty -= qty # Sessao critica 2
        ordem_venda.qty -= qty
        
        ordem_compra.user.save()
        ordem_venda.user.save()  # Salva no banco a transacao. Atualiza os saldos e itens em carteira dos usuarios.
        
        pos_processa_ordem(ordem_compra) # Direciona as ordens restantes
        pos_processa_ordem(ordem_venda)
        
        transaction.savepoint_commit(rb) # Comita as mudancas em caso de sucesso.
        publica_negociacao(ordem.stock, qty, value, ordem_compra.user, ordem_venda.user)
    except Exception as e: #TIPAR AQUI - CADA EXCEPTION VAI TER UM TRATAMENTO DIFERENTE!!!!!!
        logger.error("executa_ordem FALHOU:", exc_info=True) # Debug only
        transaction.savepoint_rollback(rb) # Desfaz as alteracoes
        cancela_ordem(ordem_compra, traceback.format_exc()) # Cancela a ordem de compra
        return

    if continua_ordem:
        processa_ordem(ordem)
    else:
        finaliza_ordem(ordem)

def publica_negociacao(stock, qty, value, user_buy, user_sell):
    """ Registra a negociação efetuada entre duas partes. """
    hist = Historical(stock=stock,qty=qty,value=value,user_buy=user_buy,user_sell=user_sell)
    hist.save()

def load_defunct_orders():
    """ Verifica se ficou lixo no banco e executa """
    logger.info("Procurando ordens defuntas")
    import order_queue
    orders = Order.objects.filter(status=Order.STATUS_NEW).order_by('included')
    for order in orders:
        logger.warn("Adicionando ordem defunta: %s", order)
        order_queue.add_order(order)

#load_defunct_orders()