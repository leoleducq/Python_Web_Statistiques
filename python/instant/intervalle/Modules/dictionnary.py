#!/usr/bin/env python3.9
#-----------main 5 et ultérieur-------------
def dictionnary(st,dict,date_mini,date,icao):
    date_mini = "key "+date_mini
    #Si la station n'est pas dans le dictionnaire
    if st not in dict:
        dict[st] = {date_mini:{date:[icao]}}
    #Si la station et la date sont dans le dictionnaire et que l'ICAO n'y est pas
    elif (st in dict) and (date_mini in dict[st]) and (date in dict[st][date_mini]) and (icao not in dict[st][date_mini][date]):
        dict[st][date_mini][date].append(icao)
    #Si la station est dans le dictionnaire mais pas l'intervalle
    elif (st in dict) and (date_mini not in dict[st]):
        dict[st][date_mini] = {date:[icao]}
    #Si la station et l'intervalle sont dans le dictionnaire mais pas l'intervalle au sein de cette même intervalle
    elif (st in dict) and (date not in dict[st][date_mini]):
        dict[st][date_mini][date] = [icao]
    
    return dict