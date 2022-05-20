#!/usr/bin/env python3.9
#Bibliothèques nécessaires
import re, pylab
import matplotlib.pyplot as plt
#Module pour insérer des metadata
from PIL import Image, ExifTags
import piexif
from Modules.connect import NoSQLConnect
import datetime
from Modules.dictionnary import *
from Modules.intervalle2 import *
from Modules.pics import *

#Importer la variable d'un autre fichier
import sys
sys.path.append("/downloads/exec")
from exec import actual_date
end = actual_date

#------Lancement du chrono---------
startChrono = datetime.datetime.now()
#Date de départ Tri par heures
start_hour = end - datetime.timedelta(hours=1)
#Date de départ Tri par jours
start_day = end - datetime.timedelta(days=1)
#Date de départ Tri par semaines
start_week = end - datetime.timedelta(days=7)
#Liste des dates de départ
list_date = [start_hour,start_day,start_week]

#--------Compteur-----------
cpt_dic = 0
cpt_function_pic = 0
cpt_function_intervalle = 0
cpt_date = 0

#Connection à la BDD
db = NoSQLConnect()

while cpt_dic < 3:
    #Instanciation des dictionnaires vides
    dict_hour, dict_day, dict_week = {},{},{}
    start = list_date[cpt_dic]
    print(start,end)

    #Variables pour garder la même date de départ à chaque itération
    hour_start = str(start)[11:13]
    minute_start = str(start)[14:16]
#---------------Lecture collection adsb------------------
#Lit le document selon la plage horaires des variables start et end
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
        #Date pour le dictionnaire Hour
        date_quart = "%s-%s-%s %s:%s:00" %(year,month,day,hour,minute)
        #Date pour le dictionnaire Day
        date_hour = "%s-%s-%s %s:%s:00" %(year,month,day,hour,minute_start)
        #Date pour le dictionnaire Week
        date_day = "%s-%s-%s %s:%s:00" % (year,month,day,hour_start,minute_start)
        for icao in list_icao:
            list_dict = [dictionnary(st,dict_hour,str(start),date_quart,icao), dictionnary(st,dict_day,str(start),date_hour,icao), dictionnary(st,dict_week,str(start),date_day,icao)]
        #----------------------------Dictionnaire---------------------------
            dict = list_dict[cpt_dic]
    #----------------------------------Stats---------------------------------
        #pprint.pprint(dict)
    #Test si le dictionnaire est vide
    try:
        dict.items()
    except:
        cpt_dic += 1
        cpt_function_pic +=1
        cpt_function_intervalle +=1
        continue
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
                fonction_intervalle = [intervalle_hour(year,month,day,hour,minute), intervalle_day(year,month,day,hour,minute), intervalle_week(year,month,day,hour,minute)]
                #Intervalle
                first_date,last_date, incr_date, colors, crop1, crop2 = fonction_intervalle[cpt_function_intervalle]
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
            #Instanciation de la figure
            fig = plt.figure(keys)
            #Axe x = Liste des nombres d'icao
            x = listcpt
            #Axe y  du graphe = Nombre d'icao
            y = nb_icao
            #Nom des barres sur l'axe x, crop1 et crop 2 : variables pour découper la date
            BarName = barname(in_date,crop1, crop2)
            #Génère les barres du diagramme
            plt.bar(x,y,color=colors)
            plt.xlim()
            plt.ylim()
            #Met des grilles
            plt.grid()
            #Liste des xlabel
            list_xlabel = ["Découpés en quart d'heure", "Découpés en heures","Découpés en jours"]
            plt.ylabel("Nombre d'avions captés")
            plt.xlabel(list_xlabel[cpt_dic])
            plt.title("Période du %s au %s" % (first_date,last_date))
            pylab.xticks(x, BarName, rotation=0)

        #-------------Création des dossiers-----------------
            #Liste des fonctions pic à parcourir
            fonction_pic = [pic_hour(keys), pic_day(keys),pic_week(keys)]
            name_pic, pic = fonction_pic[cpt_function_pic]
            #Enregistre la photo
            plt.savefig(pic+".jpg", bbox_inches='tight',format="jpg")
            plt.close()
            #Insére les metadata
            
            zeroth_ifd = {
                        piexif.ImageIFD.Make: str(max_icao),
                        }

            exif_dict = {"0th":zeroth_ifd}
            exif_bytes = piexif.dump(exif_dict)
            image = Image.open(pic+".jpg")
            image.save(pic+".jpg", exif=exif_bytes)



#Incrémentation des compteurs
    cpt_dic += 1
    cpt_function_pic +=1
    cpt_function_intervalle +=1
endChrono = datetime.datetime.now()-startChrono
print(endChrono)