﻿# Bootstrap.py
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
    (1,u"BR",u"A",u"http://placehold.it/150x85"),
    (2,u"SP",u"A",u"http://placehold.it/150x85"),
    (3,u"IT",u"A",u"http://placehold.it/150x85"),
    (4,u"PT",u"A",u"http://placehold.it/150x85"),
    (5,u"NZ",u"B",u"http://placehold.it/150x85"),
    (6,u"NL",u"B",u"http://placehold.it/150x85"),
    (7,u"IQ",u"B",u"http://placehold.it/150x85"),
    (8,u"AT",u"B",u"http://placehold.it/150x85")
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
    s = StockView(ticker_id=stockview[0], ticker_name=stockview[1], group=stockview[2], image=stockview[3])
    try:
        s.save()
        log.info(u"Adicionada 'View' da Stock : '%s'", s)
    except:
        log.error(u"Não pude adicionar 'View' da açao '%s'", s, exc_info=True)

log.info("Bootstrap finalizado")
import sys
sys.exit(0)
