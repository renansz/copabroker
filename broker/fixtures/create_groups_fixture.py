#!/usr/bin/python
# -*- coding: utf-8 -*-

f = open(r'stockview_fixture.json','w')
g = open(r'stock_fixture.json','w')

#GRUPO A
teams = [("BRA",    "Brazil","A"),
         ("CRO",    "Croatia", "A"),
         ("MEX",    "Mexico", "A"),
         ("CMR",    "Cameroon",       "A")]
#GRUPO B
teams.append(("ESP",    "Spain",        "B"))
teams.append(("NED",    "Netherlands",    "B"))
teams.append(("CHI",    "Chile",           "B"))
teams.append(("AUS",    "Australia",          "B"))
#GRUPO C
teams.append(("COL",    "Colombia",   "C"))
teams.append(("GRE",    "Greece",       "C"))
teams.append(("CIV",    "Côte d'Ivoire",        "C"))
teams.append(("JPN",    "Japan",          "C"))
#GRUPO D
teams.append(("URU",    "Uruguay",     "D"))
teams.append(("CRC",    "Costa Rica",         "D"))
teams.append(("ENG",    "England",    "D"))
teams.append(("ITA",    "Italy",       "D"))
#GRUPO E
teams.append(("SUI",    "Switzerland",      "E"))
teams.append(("ECU",    "Ecuador",        "E"))
teams.append(("FRA",    "France",    "E"))
teams.append(("HON",    "Honduras",     "E"))
#GRUPO F
teams.append(("ARG",    "Argentina",         "F"))
teams.append(("BIH",    "Bosnia-Herzegovina",       "F"))
teams.append(("IRN",    "Iran",    "F"))
teams.append(("NGA",    "Nigeria",           "F"))
#GRUPO G
teams.append(("GER",    "Germany",           "G"))
teams.append(("POR",    "Portugal",         "G"))
teams.append(("GHA",    "Ghana",  "G"))
teams.append(("USA",    "United States of America",  "G"))
#GRUPO H
teams.append(("BEL",    "Belgium",      "H"))
teams.append(("ALG",    "Algeria",        "H"))
teams.append(("RUS",    "Russia",        "H"))
teams.append(("KOR",    "Korea Republic",     "H"))

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
