#!/usr/bin/env python3.9
import datetime, os, re
from time import sleep
from distutils.dir_util import copy_tree

#actual_date = datetime.datetime(2021,12,9,0,30)
actual_date = datetime.datetime(2021,12,8,1,0)

while True:
    chrono = datetime.datetime.now()
    #Executer le fichier python
    exec(open("./main3.py").read())
    #Copie le dossier temp dans images
    copy_tree("/home/leo/Working/NoSQL/adsb/station_glissant/temp/","/home/leo/Working/NoSQL/adsb/station_glissant/images/")

    #Réinitialise le dossier images dans var
    varimages = "/var/www/html/stats/images/"
    for filename in os.listdir(varimages) :
        os.remove(varimages + "/" + filename)

    #Copier le dossier images dans /var/www/html/stats/images pour les afficher sur la page Web ensuite
    copy_tree("/home/leo/Working/NoSQL/adsb/station_glissant/images/", "/var/www/html/stats/images/")
    print("Données actualisées")
    #Réinitialise les dossiers images et temp
    images = "/home/leo/Working/NoSQL/adsb/station_glissant/images/"
    for filename in os.listdir(images) :
        os.remove(images + "/" + filename)
    temp = "/home/leo/Working/NoSQL/adsb/station_glissant/temp/"
    for filename in os.listdir(temp) :
        os.remove(temp + "/" + filename)

    #Variable pour voir le temps à attendre avant de relancer le programme
    endchrono = datetime.datetime.now() - chrono
    #15 minutes - le temps que le script a mit
    wait = datetime.timedelta(minutes=15) - endchrono
    #Récupérer les minutes et les secondes
    wait = re.search(r'[0-9]{2}:[0-9]{2}.[0-9]*',str(wait))
    wait = wait.group(0)
    minutes = int(wait[:2])
    secondes = float(wait[3:])
    #Attendre 15 minutes - le temps passé à exécuter le script
    print("Temps avant réexécution du script : %s minutes %s" % (str(minutes),str(secondes)))
    sleep((minutes*60)+secondes)

    #Incrémenter la date de 15 minutes
    actual_date += datetime.timedelta(minutes=15)