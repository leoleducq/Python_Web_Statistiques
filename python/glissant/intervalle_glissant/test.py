#!/usr/bin/env python3.9
from Modules.connect import*
import datetime
import sys
sys.path.append("/downloads/exec")
from exec import actual_date

end = actual_date
start_hour = end - datetime.timedelta(minutes=15)
start_day = end - datetime.timedelta(days=1, minutes=15)
start_week = end - datetime.timedelta(days=7, minutes=15)

list_date = [start_hour,start_day,start_week]

cpt = 0
db = NoSQLConnect()
"""for doc in db.historique.find({"$and":[{"stdate.date.min":{"$gte":start_hour}},{"stdate.date.max":{"$lte":end}}]}).sort("stdate.st"):
    continue"""

while cpt < 3:
    #for doc in db.historique.find({"$and":[{"stdate.date.min":{"$gte":list_date[cpt]}},{"stdate.date.max":{"$lte":end}}]}).sort("stdate.st"):
    print(list_date[cpt])
    cpt +=1
    date = ["oui","non"]