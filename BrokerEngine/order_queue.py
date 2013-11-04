"""
    order_queue.py
    
    Controla a fila de ordens"""

import Queue, threading, logging, atexit
import engine

__all__ = ['add_order', 'open_market', 'stop_market']

queue = Queue.Queue()
queue_processor = None
inited = False

logger = logging.getLogger("CopaBroker.BrokerEngine.order_queue")

"""
def add_order(order):
    global queue
    logger.info(u"Ordem adicionada à fila: %s" %order)
    queue.put(order)

def thread_processor(queue):
    while True:
        logger.info(u"Aguardando ordem...")
        order = queue.get()
        if order == None:
            logger.info(u"Mensagem de término recebida. Finalizando thread.")
            break
        logger.info(u"Ordem retirada da fila: %s" %order)
        engine.processa_ordem(order)

def open_market():
    global inited
    if inited:
        logger.warn(u"Tentativa de iniciar um mercado já aberto")
        return
    logger.info(u"Iniciando abertura de mercado")
    global queue_processor
    global queue

    queue_processor = threading.Thread(target=thread_processor, args=(queue,))
    logger.info(u"Iniciando processador de ordens")
    queue_processor.start()
    inited = True
    logger.info(u"Mercado pronto para operar")

def stop_market():
    global inited
    if not inited:
        logger.warn(u"Tentativa de parar um mercado fechado")
    logger.info(u"Iniciando fechamento de mercado")
    global queue_processor
    global queue
    logger.info(u"Enviando ordem de término de processamento")
    queue.put(None)
    logger.info(u"Aguardando término dos processamentos")
    queue_processor.join()
    inited = False

# ============================================================================ #
"""

dispatcher = None
inited = False

class StockProcessor:
    def __init__(self, ticker, autostart=True):
        self.ticker = ticker
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self.thread_processor, args=(self.queue,))
        if autostart:
            self.thread.start()
        logger.info(u"[%s] Criando fila de ordens" %self.ticker)
    def put(self, order):
        self.queue.put(order)
        logger.info(u"[%s] Ordem incluída da fila: %d" %(self.ticker, order.id) )
    def start(self):
        self.thread.start()
    def stop(self):
        self.queue.put(None)
        logger.info("[%s] Mensagem de término enviada. Aguardando término da thread." %self.ticker)
        self.thread.join()
        logger.info("[%s] Thread de processamento finalizada." %self.ticker)
    def thread_processor(self, queue):
        while True:
            logger.info(u"[%s] Aguardando mensagem" %self.ticker)
            order = queue.get()
            if order == None:
                break
            logger.info(u"[%s] Ordem retirada da fila: %d" %(self.ticker, order.id) )
            engine.processa_ordem(order)
    
class QueueDispatcher:
    def __init__(self, ticker_list):
        self.stock_processor = dict()
        logger.info(u"Inicializando threads de processamento")
        for ticker in ticker_list:
            self.stock_processor[ticker] = StockProcessor(ticker)
        logger.info(u"Roteador de ordens inicializado")
    def put(self, order, ticker):
        logger.info(u"Recebendo nova ordem id=%d", order.id)
        self.stock_processor[ticker].put(order)
    def stop(self):
        for ticker, processor in stock_processor.iteritems():
            logger.info(u"Enviando mensagem de término para %s", ticker)
            processor.put(None)
        for ticker, processor in stock_processor.iteritems():
            logger.info(u"Aguardando término de %s", ticker)
            processor.stop()
        logger.info(u"Todas as threads foram finalizadas.")

def add_order(order, ticker):
    global dispatcher
    if dispatcher == None:
        open_market()
    dispatcher.put(order, ticker)

def open_market():
    global inited
    if inited:
        logger.warn(u"Tentativa de iniciar um mercado já aberto")
        return
    logger.info(u"Iniciando abertura de mercado")
    
    global dispatcher
    from models import Stock
    all_tickers = [stock.ticker for stock in Stock.objects.all()]
    dispatcher = QueueDispatcher(all_tickers)

    #load_defunct_orders(order_queue)
    inited = True
    
def stop_market():
    global inited
    if not inited:
        logger.warn(u"Tentativa de parar um mercado fechado")
    logger.info(u"Iniciando fechamento de mercado")

    global dispatcher
    dispatcher.stop()
    inited = False

# DEBUG, em produção é melhor ativar/desativar o mercado parametricamente
def signal_stop():
    global inited
    if inited:
        logger.info("EXIT SIGNAL recebido, tentando parar graciosamente o mercado...")
        stop_market()
        logger.info("Mercado Finalizado")
        
open_market()
atexit.register(signal_stop)