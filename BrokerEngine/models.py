from django.db import models

#Precisa existir uma conversao ticker -> ticker_id mais facil, ou definir como trabalhar com o ticker.name,
#na maioria dos casos só tenho o nome do ticker, nao o id.

class User(models.Model):
    """ Usuario que pode operar ativos """
    name = models.CharField(max_length=200)
    saldo = models.DecimalField(max_digits=12, decimal_places=3)
    
    def __unicode__(self):
        return "User(%s, %.3f)" %(self.name, self.saldo)

class Stock(models.Model):
    """ Representa um ativo """
    ticker = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "Stock(%s, %s)" %(self.ticker, self.name)

class Order(models.Model):
    """ Ordem criada por um usuario, que vai para o book de um dado ativo """
    ORDER_BUY = 'C'
    ORDER_SELL = 'V'
    
    STATUS_NEW = 'N'
    STATUS_OPEN = 'A'
    STATUS_PARTIAL = 'P'
    STATUS_FINALIZED = 'F'
    STATUS_CANCELLED = 'C'
    
    ORDER_TYPES = [ 
        (ORDER_BUY, "Compra"),
        (ORDER_SELL, "Venda") ]
    ORDER_STATUS = [
        (STATUS_NEW, "Nova"),
        (STATUS_OPEN, "Aberta"),
        (STATUS_PARTIAL, "Parcialmente Executada"),
        (STATUS_FINALIZED, "Finalizada"),
        (STATUS_CANCELLED, "Cancelada") ]
        
    user = models.ForeignKey(User)
    stock = models.ForeignKey(Stock)
    
    tipo = models.CharField(max_length=1, choices=ORDER_TYPES) 
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=STATUS_NEW) 
    original_qty = models.IntegerField()
    qty = models.IntegerField()
    value = models.DecimalField(max_digits=6, decimal_places=3)
    included = models.DateTimeField(auto_now_add = True)
    
    cancel_reason = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "Order(%c, %d, %s, %s, %s | %s)" %(self.tipo, self.qty, self.stock.ticker, self.value, self.user.name, self.status)

class PortfolioItem(models.Model):
    """ Representa um ativo em uma custódia """
    user  = models.ForeignKey(User)
    stock = models.ForeignKey(Stock)
    qty   = models.IntegerField()
    
    def __unicode__(self):
        return "PortfolioItem(%s, %s, %d)" %(self.user.name, self.stock.ticker, self.qty)
        
class Historical(models.Model):
    """ Registra uma negociacao efetuada """
    stock = models.ForeignKey(Stock)
    qty = models.IntegerField()
    value = models.DecimalField(max_digits=6, decimal_places=3)
    user_buy = models.ForeignKey(User, related_name='buy_historical')
    user_sell = models.ForeignKey(User, related_name='sell_historical')
    timestamp = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return "Historical(%s, %d, %s, %s, %s)" %\
            (self.stock.ticker, self.qty, self.value, self.user_buy.name, self.user_sell.name)
