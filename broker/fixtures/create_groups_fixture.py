#!/usr/bin/python
# -*- coding: utf-8 -*-

f = open(r'stockview_fixture.json','w')
g = open(r'stock_fixture.json','w')

#GRUPO A
teams = [("BRA",    "Brazil","A"),
         ("JAP",    "Japan", "A"),
         ("CHI",    "Chile", "A"),
         ("HOL",    "Netherlands",       "A")]
#GRUPO B
teams.append(("ARG",    "Argentina",        "B"))
teams.append(("IRA",    "Iran",    "B"))
teams.append(("ECU",    "Ecuador",           "B"))
teams.append(("ITA",    "Italy",          "B"))
#GRUPO C
teams.append(("COL",    "Colombia",   "C"))
teams.append(("KOR",    "Korea Republic",       "C"))
teams.append(("CIV",    "Côte d'Ivoire",        "C"))
teams.append(("ENG",    "England",          "C"))
#GRUPO D
teams.append(("URU",    "Uruguay",     "D"))
teams.append(("AUS",    "Australia",         "D"))
teams.append(("GHA",    "Ghana",    "D"))
teams.append(("POR",    "Portugal",       "D"))
#GRUPO E
teams.append(("SPA",    "Spain",      "E"))
teams.append(("USA",    "United States of America",        "E"))
teams.append(("ALG",    "Algeria",    "E"))
teams.append(("GRE",    "Greece",     "E"))
#GRUPO F
teams.append(("GER",    "Germany",         "F"))
teams.append(("MEX",    "Mexico",       "F"))
teams.append(("NIG",    "Nigeria",    "F"))
teams.append(("BOS",    "Bosnia-Herzegovina",           "F"))
#GRUPO G
teams.append(("BEL",    "Belgium",           "G"))
teams.append(("COS",    "Costa Rica",         "G"))
teams.append(("CAM",    "Cameroon",  "G"))
teams.append(("CRO",    "Croatia",  "G"))
#GRUPO H
teams.append(("SWI",    "Switzerland",      "H"))
teams.append(("HON",    "Honduras",        "H"))
teams.append(("FRA",    "France",        "H"))
teams.append(("RUS",    "Russia",     "H"))

id = 1
f.write("[")
g.write('[')
for ticker,team,group in teams:
    f.write("""  {
    "model": "broker.stockview",
    "pk": %d,
    "fields": {
          "ticker": "%d",
          "ticker_name": "%s",
          "country_name": "%s",
          "group": "%s"
    }
  },
  """ % (id,id,ticker,team,group))
    g.write("""  {
    "model": "BrokerEngine.stock",
    "pk": %d,
    "fields": {
          "ticker": "%s",
          "name": "%s"
    }
  },
  """ % (id,ticker,team))  
    id += 1
f.seek(-4,1)
f.write("]")
f.close()

g.seek(-4,1)
g.write("]")
g.close()

print "Groups Fixture created successfully"
