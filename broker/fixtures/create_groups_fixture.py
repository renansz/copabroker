#!/usr/bin/python
# -*- coding: utf-8 -*-

f = open(r'groups_fixture.json','w')

#GRUPO A
teams = [("URU2014",    "Uruguai",      "A"),
         ("MEX2014",    "México",       "A"),
         ("AFR2014",    "África do Sul","A"),
         ("FRA2014",    "França",       "A")]
#GRUPO B
teams.append(("ARG2014",    "Argentina",        "B"))
teams.append(("CRS2014",    "Coréia do Sul",    "B"))
teams.append(("GRE2014",    "Grécia",           "B"))
teams.append(("NIG2014",    "Nigéria",          "B"))
#GRUPO C
teams.append(("EUA2014",    "Estados Unidos",   "C"))
teams.append(("ING2014",    "Inglaterra",       "C"))
teams.append(("ESL2014",    "Eslovênia",        "C"))
teams.append(("AGL2014",    "Argélia",          "C"))
#GRUPO D
teams.append(("GER2014",    "Alemanha",     "D"))
teams.append(("GAN2014",    "Gana",         "D"))
teams.append(("AUS2014",    "Austrália",    "D"))
teams.append(("SRV2014",    "Sérvia",       "D"))
#GRUPO E
teams.append(("HOL2014",    "Holanda",      "E"))
teams.append(("JAP2014",    "Japão",        "E"))
teams.append(("DIN2014",    "Dinamarca",    "E"))
teams.append(("CAM2014",    "Camarões",     "E"))
#GRUPO F
teams.append(("PAR2014",    "Paraguai",         "F"))
teams.append(("ESQ2014",    "Eslováquia",       "F"))
teams.append(("NVZ2014",    "Nova Zelândia",    "F"))
teams.append(("ITA2014",    "Itália",           "F"))
#GRUPO G
teams.append(("BRA2014",    "Brasil",           "G"))
teams.append(("POR2014",    "Portugal",         "G"))
teams.append(("CDM2014",    "Costa do Marfim",  "G"))
teams.append(("CRN2014",    "Coréia do Norte",  "G"))
#GRUPO H
teams.append(("ESP2014",    "Espanha",      "H"))
teams.append(("CHI2014",    "Chile",        "H"))
teams.append(("SUI2014",    "Suiça",        "H"))
teams.append(("HON2014",    "Honduras",     "H"))

id = 1
f.write("[")
for ticker,team,group in teams:
    f.write("""  {
    "model": "broker.stock",
    "pk": %d,
    "fields": {
          "ticker": "%s",
          "country_name": "%s",
          "group": "%s",
          "fair_value": %5.2f
    }
  },
  """ % (id,ticker,team,group,3.13))
    id += 1

f.seek(-4,1)

f.write("]")
f.close()
print "Groups Fixture created successfully"