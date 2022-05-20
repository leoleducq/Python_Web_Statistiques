#!/usr/bin/env python3.9
import re, pymongo, pylab
import matplotlib.pyplot as plt
from Modules.connect import NoSQLConnect
import datetime
from Modules.dictionnary import *
from Modules.intervalle import *
from Modules.pics import *
#Importer la variable d'un autre fichier
import sys
sys.path.append("/downloads/exec")
from exec import date

end = date

start_hour = end - datetime.timedelta(hours=1)
start_day = end - datetime.timedelta(days=1)
start_week = end - datetime.timedelta(days=7)
#-----Compteur-------
cpt_dic = 0
cpt_function_pic = 0
cpt_function_intervalle = 0
cpt_date = 0

startChrono = datetime.datetime.now()
db = NoSQLConnect()

list_date = [start_hour,start_day,start_week]

while cpt_dic < 3:
    #Instanciation des dictionnaires vides
    dict_hour, dict_day, dict_week = {},{},{}
    start = list_date[cpt_dic]
    print(start, end)
#---------------Lecture collection adsb------------------
#Lit le document en entier
    for doc in db.historique.find({"$and":[{"stdate.date.min":{"$gte":start}},{"stdate.date.max":{"$lte":end}}]}).sort("stdate.st"):
        #Nom de la station
        st = str(doc["stdate"]["st"])
        #Enlève les stations de plus de 5 caractères
        if len(st) > 5:
            continue
        #Icao
        list_icao = str(doc["icao"]).replace("}}","").replace("'","").replace("[","").replace("]","").replace(" ","").split(",")
        #--------Date---------
        tm = str(doc["stdate"]["date"]["min"])
        #Année
        year = re.search(r'^[0-9]{4}',tm)
        year = year.group(0)
        #Mois
        month = tm[5:7]
        #Jour
        day = tm[8:10]
        #Heure
        hour= tm[11:13]
        if len(str(hour)) != 2:
            hour = "0"+str(hour)
        #Minutes
        minute = tm[14:16]
        if len(str(minute)) != 2:
            minute = "0"+str(minute)
    #--------------------Gestion des variables--------------------
        #Date mini
        date_mini_quart = "%s-%s-%s %s:%s:00" %(year,month,day,hour,minute)
        #date_mini_quart = "%s-%s-%s %s:%s:00" %(year,month,day,hour,minute)
        #Date mini dict_hour
        date_mini_hour = "%s-%s-%s %s:00:00" %(year,month,day,hour)
        #date_mini_hour = "%s-%s-%s %s:%s:00" %(year,month,day,hour,minute)
        #Date mini dict_day
        date_mini_day = "%s-%s-%s 00:00:00" % (year,month,day)
        for icao in list_icao:
            list_dict = [dictionnary(st,dict_hour,date_mini_hour,date_mini_quart,icao), dictionnary(st,dict_day,date_mini_day,date_mini_hour,icao), dictionnary(st,dict_week,date_mini_day,date_mini_day,icao)]
        #----------------------------Dictionnaire---------------------------
            dict = list_dict[cpt_dic]
    #----------------------------------Stats---------------------------------
    for keys, values in dict.items():
    #--------Récupérer la 1ère intervalle---------
        #Récupère la liste des 1ère dates de chaque station
        list_key = re.findall(r'key [0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*', str(values))
        #Récupère la 1ère intervalle de date
        for first_key in list_key:
            first_intervalle = dict[keys][first_key]
        #-------------------Date---------------------
            #Regex pour récupérer la date
            date = re.findall(r'[0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*',str(first_intervalle))
            try:
                #Enlève le mot key
                first_key = str(first_key).replace("key ","")
                #Année
                year = int(first_key[:4])
                #Mois
                month = int(first_key[5:7])
                #Jour
                day = int(first_key[8:10])
                #Heure
                hour= int(first_key[11:13])
                #Minutes
                minute = int(first_key[14:16])
        #--------Liste des fonctions intervalle à parcourir-----
                fonction_intervalle = [intervalle_hour(year,month,day,hour), intervalle_day(year,month,day), intervalle_week(year,month,day)]
                #Intervalle
                first_date,last_date, incr_date = fonction_intervalle[cpt_function_intervalle]
            except:
                raise
            #Date à l'intérieur de l'intervalle
            in_date_dic = date[0:]
        #-------------------ICAO--------------------
            #Regex permettant de prendre la liste d'icao
            list_icao = re.findall(r'\[(.*?)\]',str(first_intervalle).replace("'",""))
            #Déclaration des variables dans la fonction var
            in_date, nb_icao, max_icao,listcpt = var(first_date,last_date,list_icao,in_date_dic,incr_date)
        #-------------Génération du graphe-----------
            fig = plt.figure(keys)

            x = listcpt
            height = nb_icao
            width = 0.04
            BarName = barname(in_date)
            plt.bar(x, height, width, color="b" )
            plt.bar(x,height,color="b")
            plt.scatter([i+width/2.0 for i in x],height,color='k',s=20)
            #plt.xlim()
            #plt.xlim(0,max(listcpt))
            plt.ylim(0,max_icao+1)
            plt.grid()

            plt.ylabel("Nombre d'avions captés")
            plt.xlabel("Date de réception")
            plt.title("Nombre d'avions capté par la station '%s' du %s au %s" % (keys,first_date,last_date))

            pylab.xticks(x, BarName, rotation=90)

        #-------------Création des dossiers-----------------
            #Liste des fonctions pic à parcourir
            fonction_pic = [pic_hour(keys), pic_day(keys),pic_week(keys)]
            name_pic, pic = fonction_pic[cpt_function_pic]
            #Enregistre la photo
            plt.savefig(pic, bbox_inches='tight')
            plt.close()

#Incrémentation des compteurs
    cpt_dic += 1
    cpt_function_pic +=1
    cpt_function_intervalle +=1

print(datetime.datetime.now()-startChrono)
