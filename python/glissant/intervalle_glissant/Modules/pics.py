#!/usr/bin/env python3.9
#Permet d'obtenir les mois en français
import locale, calendar
#locale.setlocale('fr_FR')

#-----------------Hour------------------
def pic_hour(keys):
    name_pic = keys+"_heure"
    pic = str('../station_glissant/temp/'+name_pic)

    return name_pic, pic

#-----------------Day------------------
def pic_day(keys):
    name_pic = keys+"_jour"
    pic = str('../station_glissant/temp/'+name_pic)

    return name_pic, pic

#-----------------Year------------------
def pic_week(keys):
    name_pic = keys+"_semaine"
    pic = str('../station_glissant/temp/'+name_pic)

    return name_pic, pic