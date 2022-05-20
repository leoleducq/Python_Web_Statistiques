#!/usr/bin/env python3.9
import pymongo
from Modules.connect import NoSQLConnect
import datetime

startChrono = datetime.datetime.now()
db = NoSQLConnect()

#---------------Création des collections-----------------
#Collection dict_15min
try:
    db.create_collection("dict_15min")
    db.dict_15min.create_index("stdate")
except:
    raise
#Collection dict_1h
try:
    db.create_collection("dict_1h")
    db.dict_1h.create_index("stdate")
except:
    raise
#Instanciation des dictionnaires
dict_15min = {}
dict_1h = {}
#Dictionnaire temporaire
temp_dict_15min = {}
temp_dict_1h ={}
#---------------Lecture collection adsb------------------
#Lit le document en entier
for doc in db.adsb.find({}).sort("tm",pymongo.ASCENDING).limit(1000000):
    #Liste des stations ayant reçu le message
    sts = str(doc["st"]).split(",")
    #Icao
    icao = str(doc["icao"])
    #--------Date---------
    tm = str(doc["tm"])
    #Année
    year = int(tm[:4])
    #Mois
    month = int(tm[5:7])
    #Jour
    day = int(tm[8:10])
    #Heure
    hour= int(tm[11:13])
    #Minutes
    minute = int(tm[14:16])
#--------------------Gestion des variables--------------------
    #----------------------dict_15min------------------------
    #Gestion des minutes
    if minute < 15:
        minute = 0
    elif minute < 30:
        minute = 15
    elif minute < 45:
        minute = 30
    elif minute <= 59:
        minute = 45
    #Date mini dict_15min
    date_15min_min = datetime.datetime(year,month,day,hour,minute)
    #---------------------------dict_1h-----------------------
    #Date mini dict_1h
    date_1h_min = datetime.datetime(year,month,day,hour)
    for st in sts:
        #Nom du dictionnaire dict_15min
        name_dict_15min = str(st)+" "+str(date_15min_min).replace("datetime.datetime(","").replace(")","")
        #Nom du dictionnaire dict_1h
        name_dict_1h = str(st)+" "+str(date_1h_min).replace("datetime.datetime(","").replace(")","")
#----------------------------Dictionnaires---------------------------
    #----------------------dict_15min----------------------------
        #Si la station et la date sont dans le dictionnaire dict_15min et que l'ICAO n'y est pas
        if (name_dict_15min in dict_15min) and (icao not in dict_15min[name_dict_15min][st][date_15min_min]):
            dict_15min[name_dict_15min][st][date_15min_min].append(icao)
        #Si name_dict_15min n'est pas dans le dictionnaire
        if name_dict_15min not in dict_15min:
            temp_dict_15min = {name_dict_15min:{st:{
                    date_15min_min:
                        [icao]
                }
            }}
            dict_15min.update(temp_dict_15min)
        
    #----------------------dict_1h-----------------------------
            #Si la station et la date sont dans le dictionnaire 
        if name_dict_1h in dict_1h and (icao not in dict_1h[name_dict_1h][st][date_1h_min]):
            dict_1h[name_dict_1h][st][date_1h_min].append(icao)
            #Si la station et la date ne sont pas dans le dictionnaire
        if name_dict_1h not in dict_1h:
            temp_dict_1h={name_dict_1h:{st:{
                date_1h_min:
                [icao]
                }
            }}
            dict_1h.update(temp_dict_1h)
        
#dict_15min        
txt = open("Log/dict_15min.txt",encoding="utf-8",mode ="a")
txt.write(str(dict_15min))
txt.close

#dict_1h
txt = open("Log/dict_1h.txt",encoding="utf-8",mode ="a")
txt.write(str(dict_1h))
txt.close


#-------------------------Insertion------------------------
#-----------dict_15min-----------------
for row in dict_15min.values():
    row = str(row)
    row = row.split(":")
    st = row[0].replace("{'","").replace("'","")
    #----------------------------DATE-----------------------------------------------------
    date_15min_min = row[1].replace("{datetime.datetime(","").replace(")","").strip().split(",")
    #Annee
    year = int(date_15min_min[0])
    #Mois
    month = int(date_15min_min[1])
    #Jour
    day = int(date_15min_min[2])
    #Heure
    hour= int(date_15min_min[3])
    #Minutes
    minute = int(date_15min_min[4])
    #Intervalle de 15 minutes
    date_min = datetime.datetime(year,month,day,hour,minute)
    date_max = date_min+datetime.timedelta(minutes=15)
    #Liste ICAO
    icao = row[2].replace("}}","").replace("'","").replace("[","").replace("]","").replace(" ","").split(",")
    #Nombre d'icao
    nbicao = len(icao)
    try:
        insert_historique = db.dict_15min.insert_one({"stdate":{"st":st,"date":{"min":date_min,"max":date_max}},"icao":icao,"nbicao":nbicao})
    except:
        txt = open('Log/error_histo.txt',encoding='utf-8',mode ='a')
        text = st+":"+str(dict_15min[name_dict_15min])
        txt.write(text+"\n")
        txt.close
        continue

#------------dict_1h------------------
for row in dict_1h.values():
    row = str(row)
    row = row.split(":")
    #Station
    st = row[0].replace("{'","").replace("'","")
    #----------------------------DATE-----------------------------------------------------
    date_1h_min = row[1].replace("{datetime.datetime(","").replace(")","").strip().split(",")
    year = int(date_1h_min[0])
    #Mois
    month = int(date_1h_min[1])
    #Jour
    day = int(date_1h_min[2])
    #Heure
    hour= int(date_1h_min[3])
    #Intervalle d'1 heure
    date_min = datetime.datetime(year,month,day,hour)
    date_max = date_min+datetime.timedelta(hours=1)
    #nbicao
    icao = row[2].replace("}}","").replace("'","").replace("[","").replace("]","").replace(" ","").split(",")
    #Nombre d'icao
    nbicao = len(icao)
    try:
        insert_nbicaohour = db.dict_1h.insert_one({"stdate":{"st":st, "date":{"min":date_min,"max":date_max}},"icao":icao,"nbicao": nbicao})
    except:
        txt = open('Log/error_nbicao.txt',encoding='utf-8',mode ='a')
        text = st+":"+str(dict_1h[name_dict_1h])
        txt.write(text+"\n")
        txt.close
        continue
print(datetime.datetime.now()-startChrono)