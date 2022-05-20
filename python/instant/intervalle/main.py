#!/usr/bin/env python3.9
import re, pymongo, pylab, os
import matplotlib.pyplot as plt
from Modules.connect import NoSQLConnect
import datetime
from Modules.dictionnary import *
from Modules.intervalle import *
from Modules.pics import *

startChrono = datetime.datetime.now()
db = NoSQLConnect()

#Instanciation des dictionnaires vides
dict_hour, dict_day, dict_week, dict_month, dict_year = {},{},{},{},{}
#---------------Lecture collection adsb------------------
#Lit le document en entier
for doc in db.historique.find({}).sort("stdate.date",pymongo.ASCENDING).limit(10000):
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
    #year = int(tm[:4])
    year = re.search(r'^[0-9]{4}',tm)
    year = year.group(0)
    #Mois
    month = tm[5:7]
    #month = re.findall(r'[0-9]{2}',tm)
    #Jour
    day = tm[8:10]
    #Heure
    hour= tm[11:13]
    #hour = re.search(r' [0-9]*',tm)
    if len(str(hour)) != 2:
        hour = "0"+str(hour)
    #Minutes
    minute = tm[14:16]
    #minute = re.search(r'[0-9]{2}$',tm)
    #minute = minute.group(0)
    if len(str(minute)) != 2:
        minute = "0"+str(minute)
#--------------------Gestion des variables--------------------
    #Date mini
    date_mini_quart = "%s-%s-%s %s:%s:00" %(year,month,day,hour,minute)
    #Date mini dict_hour
    date_mini_hour = "%s-%s-%s %s:00:00" %(year,month,day,hour)
    #Date mini dict_day
    date_mini_day = "%s-%s-%s 00:00:00" % (year,month,day)
    #Récupère le numéro de semaine
    #number_week = str(datetime.datetime(year,month,day).isocalendar()[1])
    #---------Date mini dict_week---------
    #date_mini_week = str(year)+", week : "+str(number_week)
    #-----Date Month-----
    date_mini_month = "%s-%s-01 00:00:00" % (year,month)
    day_month = "%s-%s-%s 00:00:00" % (year,month,day)
    #Date mini dict_year
    date_mini_year = "%s-01-01 00:00:00" %(year)
    for icao in list_icao:
    #----------------------------Dictionnaires---------------------------
        #----------------------------Hour-------------------------------
        dict_hour = dictionnary(st,dict_hour,date_mini_hour,date_mini_quart,icao)
        #----------------------------Day---------------------------------
        dict_day = dictionnary(st,dict_day,date_mini_day,date_mini_hour,icao)
        #---------------------------Week-------------------------------
        dict_week = dictionnary(st,dict_week,date_mini_day,date_mini_day,icao)
        #--------------------------Month-------------------------------
        dict_month = dictionnary(st,dict_month,date_mini_month,day_month,icao)
        #----------------------------year----------------------------
        dict_year = dictionnary(st,dict_year,date_mini_year,date_mini_month,icao)

#----------------------------------Stats---------------------------------
dict = [dict_hour, dict_day, dict_week, dict_month, dict_year]
#Compteur pour parcourir tous les dictionnaires et toutes les fonctions
cpt_dic = 0
cpt_function_pic = 0
cpt_function_intervalle = 0

while cpt_dic < 2:
    for keys, values in dict[cpt_dic].items():
    #--------Récupérer la 1ère intervalle---------
        #Récupère la liste des 1ère dates de chaque station
        list_key = re.findall(r'key [0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*', str(values))
        #Récupère la 1ère intervalle de date
        for first_key in list_key:
            first_intervalle = dict[cpt_dic][keys][first_key]
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
                fonction_intervalle = [intervalle_hour(year,month,day,hour), intervalle_day(year,month,day), intervalle_year(year,month)]
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

            #plt.savefig('%s : %s au %s.png'%(keys,first_date,last_date))
            #plt.show()

        #-------------Création des dossiers-----------------
            #Liste des fonctions pic à parcourir
            fonction_pic = [pic_hour(keys,first_date,first_key), pic_day(keys,first_date,first_key),pic_year(keys,first_key)]
            type_tri, name_pic, list_dir, pic = fonction_pic[cpt_function_pic]
            #Création des dossiers
            for dir in list_dir:
                try:
                    os.makedirs(dir,exist_ok=True)
                except OSError:
                    if not os.path.isdir(dir):
                        raise
            #Enregistre la photo
            plt.savefig(pic, bbox_inches='tight')
            plt.close()

    #Incrémentation des compteurs
    cpt_dic += 1 
    cpt_function_pic +=1
    cpt_function_intervalle +=1
"""#Création du dossier avec le nom de la station
try:
    os.makedirs('../Station/'+keys, exist_ok = True)
except OSError:
    #Vérifie si le chemin existe et qu'il s'agit d'un dossier, s'il existe -> exception non envoyée
    if not os.path.isdir('../Station/'+keys):
        raise
#Création du dossier avec le type de tri
try:
    os.makedirs('../Station/'+keys+'/'+type_tri,exist_ok=True)
except OSError:
    #Vérifie si le chemin existe et qu'il s'agit d'un dossier, s'il existe -> exception non envoyée
    if not os.path.isdir('../Station/'+keys+'/'+type_tri):
        raise
#Création du dossier qui regroupe les stats
try:
    os.makedirs('../Station/'+keys+'/'+type_tri+'/'+intervalle, exist_ok=True)
except OSError:
    #Vérifie si le chemin existe et qu'il s'agit d'un dossier, s'il existe -> exception non envoyée
    if not os.path.isdir('../Station/'+keys+'/'+type_tri+'/'+intervalle):
        raise

#Enregistrement du graphique dans le dossier
try:
    plt.savefig('../Station/'+keys+'/'+type_tri+'/'+intervalle+'/'+name_pic)
except:
    raise"""

print(datetime.datetime.now()-startChrono)
