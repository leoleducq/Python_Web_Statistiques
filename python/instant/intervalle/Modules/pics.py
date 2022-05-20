#!/usr/bin/env python3.9
#Permet d'obtenir les mois en français
import locale, calendar
#locale.setlocale('fr_FR')

#-----------------Hour------------------
def pic_hour(keys,first_date,first_key):
    #Type de tri des icao
    type_tri = "Heure"
    #Récupère l'année
    annee = str(first_date)[:4]
    #Traduction du numéro du mois en lettres
    mois = int(str(first_date)[5:7])
    mois = calendar.month_name[mois]
    mois = str(mois).title()
    #Récupère le jour
    jour = str(first_date)[8:10]
    #Nom de la photo = Heures
    name_pic = str(first_key)[11:]

    list_dir = [str('../Station/'+keys),str('../Station/'+keys+'/'+type_tri),str('../Station/'+keys+'/'+type_tri+'/'+annee),str('../Station/'+keys+'/'+type_tri+'/'+annee+'/'+mois),str('../Station/'+keys+'/'+type_tri+'/'+annee+'/'+mois+'/'+jour)]
    pic = str('../Station/'+keys+'/'+type_tri+'/'+annee+'/'+mois+'/'+jour+'/'+name_pic)

    return type_tri, name_pic, list_dir, pic

#-----------------Day------------------
def pic_day(keys,first_date,first_key):
    #Type de tri des icao
    type_tri = "Jour"
    #Récupère l'année
    annee = str(first_date)[:4]
    #Traduction du numéro du mois en lettres
    mois = int(str(first_date)[5:7])
    mois = calendar.month_name[mois]
    mois = str(mois).title()
    #Nom de la photo = Jours
    name_pic = str(first_key)[8:10]

    list_dir = [str('../Station/'+keys),str('../Station/'+keys+'/'+type_tri),str('../Station/'+keys+'/'+type_tri+'/'+annee),str('../Station/'+keys+'/'+type_tri+'/'+annee+'/'+mois)]
    pic = str('../Station/'+keys+'/'+type_tri+'/'+annee+'/'+mois+'/'+name_pic)

    return type_tri, name_pic, list_dir, pic

#-----------------Year------------------
def pic_year(keys,first_key):
    #Type de tri des icao
    type_tri = "Annee"
    #Nom de la photo = Annee
    name_pic = str(first_key[:4])

    list_dir = [str('../Station/'+keys),str('../Station/'+keys+'/'+type_tri)]
    pic = str('../Station/'+keys+'/'+type_tri+'/'+name_pic)

    return type_tri, name_pic, list_dir, pic