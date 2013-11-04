# Bootstrap.py
# Cria alguns usuários e ações para popular o banco de dados para testes

import random

# Lista de ativos negociáveis: pares de ticker e nome completo
STOCKS = [
    ("BR", "Brazil"),
    ("SP", "Spain"),
    ("IT", "Italy"),
    ("PT", "Portugal"),
    ("NZ", "New Zeland"),
    ("NL", "Nowhere Land"),
    ("IQ", "Iraq"),
    ("AT", "Antartida")
]

STOCKSVIEWS = [
    (1,"A","-894px -336px"),
    (2,"A","-149px -420px"),
    (3,"A","-894x -336px"),
    (4,"A","-298px -588px"),
    (5,"B","-1043px -420px"),
    (6,"B","-149px -336px"),
    (7,"B","-894px -252px"),
    (8,"B","-1043px -336px")
]

# Lista de usuários: Pares de Nomes e saldos iniciais
USER_LIST = [
    (u"Usuário_01", 10000),
    (u"Pafúncio", 23456),
    (u"Joselito", 100000000),
    (u"Zé Pobreta", 12),
    (u"Aleatório_01", random.randint(1,10000)),
    (u"Aleatório_02", random.randint(1,10000)),
    (u"Aleatório_03", random.randint(1,10000))
]


#import CopaBroker.settings
from BrokerEngine.models import User, Stock
from broker.models import StockView
import logging
logging.basicConfig(level=logging.INFO)

log = logging.getLogger("bootstrap")

for user in USER_LIST:
    u = User(name=user[0], saldo=user[1])
    try:
        u.save()
        log.info(u"Adicionado Usuario: '%s'", u)
    except:
        log.error(u"Não pude adicionar usuário '%s'", u, exc_info=True)

for stock in STOCKS:
    s = Stock(ticker=stock[0], name=stock[1])
    try:
        s.save()
        log.info(u"Adicionada Ação: '%s'", s)
    except:
        log.error(u"Não pude adicionar Ação '%s'", s, exc_info=True)

for stockview in STOCKSVIEWS:
    s = StockView(ticker_id=stockview[0], group=stockview[1], flag_position=stockview[2])
    try:
        s.save()
        log.info(u"Adicionada 'View' da Stock : '%s'", s)
    except:
        log.error(u"Não pude adicionar 'View' da açao '%s'", s, exc_info=True)

log.info("Bootstrap finalizado")
import sys
sys.exit(0)
