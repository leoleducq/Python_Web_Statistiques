#!/usr/bin/env python3.9
import datetime
from dateutil import relativedelta
#-----------------Général----------------
    #Variables pour le diagramme
def var(first_date,last_date,list_icao,in_date_dic,incr_date):
    date = first_date
    #Instanciation des Listes
    in_date,nb_icao,list_cpt = [],[],[]
    cpt_icao,cpt_len = 0,0
    #Tant que la date n'est pas supérieur à la date maximum
    while date <= last_date:
        #Append la liste in_date
        in_date += [str(date)]
        #Liste du nb d'icao
        list_cpt += [cpt_icao]
        cpt_icao +=1
        #Si la date est dans le dictionnaire des dates, mettre le nb d'icao dans la liste nb_icao
        if str(date) in in_date_dic:
            #Obtiens le nombre d'icao dans la liste de liste d'icao
            nb_icao += [len(str(list_icao[cpt_len]).split(","))]
            #Incrémente l'indice de la liste de liste d'icao
            cpt_len +=1
        #Sinon ajouter 0
        else:
            nb_icao += [0]
        #Incrémentation de la date
        date += incr_date
    #Valeurs max dans nb_icao
    max_icao = max(nb_icao)

    return in_date,nb_icao, max_icao, list_cpt

def barname(in_date):
    barname = []
    for date in in_date:
        barname += [datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")]
    return barname
#-----------------Hour-------------------
def intervalle_hour(year,month,day,hour):
    first_date = datetime.datetime(year,month,day,hour)
    last_date = first_date + datetime.timedelta(hours=1)
    #Incrémentation de la date pour les intervalles dans var
    incr_date = datetime.timedelta(minutes=15)

    return first_date, last_date, incr_date

#-----------------Day-------------------
def intervalle_day(year,month,day):
    first_date = datetime.datetime(year,month,day)
    last_date = first_date + datetime.timedelta(days=1)
    #Incrémentation de la date pour les intervalles dans var
    incr_date = datetime.timedelta(hours=1)

    return first_date, last_date, incr_date
#-----------------Week-------------------
def intervalle_week(year,month,day):
    first_date = datetime.datetime(year,month,day)
    last_date =  first_date + datetime.timedelta(days=7)
    #Incrémentation de la date pour les intervalles dans var
    incr_date = datetime.timedelta(days=1)

    return first_date, last_date, incr_date