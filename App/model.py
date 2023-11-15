"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import datetime
assert cf
import tabulate 
import math
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos

datesFormat = "%Y-%m-%dT%H:%M:%S.%fZ"
def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos

    analyzer = {"terremotos" : lt.newList(),
                "fechaIndex" : om.newMap("BST",MENOR_MAYOR),
                "magIndex" : om.newMap("BST", MENOR_MAYOR)
                }         
    analyzer["earthquakes_by_time_magnitude"] = om.newMap(omaptype="RBT", cmpfunction=compare_desc)
    analyzer["earthquakes_by_zone_year"] = mp.newMap(numelements=500, maptype="PROBING", loadfactor=0.75)

    return analyzer


# Funciones para agregar informacion al modelo

def add_data(analyzer, terremoto):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    terremoto["time"]= datetime.datetime.strptime(terremoto["time"][:16], "%Y-%m-%dT%H:%M")
    #ANADIR LISTA NORMAL
    lt.addLast(analyzer["terremotos"], terremoto)

    #ANADIR POR FECHA
    fecha = terremoto['time']
 
    if om.contains(analyzer["fechaIndex"], fecha):
        lt.addLast(om.get(analyzer["fechaIndex"],fecha)["value"], terremoto)
        
    else:
        lista_terremotos= lt.newList("SINGLE_LINKED", MENOR_MAYOR)
        om.put(analyzer["fechaIndex"],fecha, lista_terremotos)
        lt.addLast(om.get(analyzer["fechaIndex"],fecha)["value"], terremoto)
    #ANADIR POR MAG

    magnitud= float(terremoto["mag"])

    if om.contains(analyzer["magIndex"], magnitud):
        lt.addLast(om.get(analyzer["magIndex"], magnitud)["value"], terremoto)
    else:
        lista_terremotos= lt.newList("SINGLE_LINKED",MENOR_MAYOR)
        om.put(analyzer["magIndex"], magnitud, lista_terremotos)
        lt.addLast(om.get(analyzer["magIndex"],magnitud)["value"], terremoto )






    earthquakes_by_time_magnitude = analyzer["earthquakes_by_time_magnitude"]
    earthquakes_by_zone_year = analyzer["earthquakes_by_zone_year"]

    entry = om.get(earthquakes_by_time_magnitude, terremoto["time"])

    if entry is None:
        magnitudes = om.newMap(omaptype="BST", cmpfunction=compare_desc)
        om.put(magnitudes, terremoto["mag"], terremoto)
        om.put(earthquakes_by_time_magnitude, data["time"], magnitudes)
    else:
        entry = om.put(me.getValue(entry), terremoto["mag"], terremoto)

    place_info = terremoto["place"].split(",")
    zone = place_info[len(place_info) - 1].strip()

    entry = mp.get(earthquakes_by_zone_year, zone)

    if entry is None:
        years = mp.newMap(numelements=500, maptype="PROBING", loadfactor=0.75)
        lst = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(lst, terremoto)
        mp.put(years, terremoto["time"].year.real, lst)
        mp.put(earthquakes_by_zone_year, zone, years)
    else:
        years = me.getValue(entry)
        lst = mp.get(years, terremoto["time"].year.real)
        if lst is None:
            lst = lt.newList(datastructure="SINGLE_LINKED")
        else:
            lst = me.getValue(lst)
        lt.addLast(lst, terremoto)
        mp.put(years, terremoto["time"].year.real, lst)

    return analyzer

def add_earthquake(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """

    """earthquakes_by_time_magnitude = data_structs["earthquakes_by_time_magnitude"]
    earthquakes_by_zone_year = data_structs["earthquakes_by_zone_year"]

    entry = om.get(earthquakes_by_time_magnitude, data["time"])

    if entry is None:
        magnitudes = om.newMap(omaptype="BST", cmpfunction=compare_desc)
        om.put(magnitudes, data["mag"], data)
        om.put(earthquakes_by_time_magnitude, data["time"], magnitudes)
    else:
        entry = om.put(me.getValue(entry), data["mag"], data)

    place_info = data["place"].split(",")
    zone = place_info[len(place_info) - 1].strip()

    entry = mp.get(earthquakes_by_zone_year, zone)

    if entry is None:
        years = mp.newMap(numelements=500, maptype="PROBING", loadfactor=0.75)
        lst = lt.newList(datastructure="SINGLE_LINKED")
        lt.addLast(lst, data)
        mp.put(years, data["time"].year.real, lst)
        mp.put(earthquakes_by_zone_year, zone, years)
    else:
        years = me.getValue(entry)
        lst = mp.get(years, data["time"].year.real)
        if lst is None:
            lst = lt.newList(datastructure="SINGLE_LINKED")
        else:
            lst = me.getValue(lst)
        lt.addLast(lst, data)
        mp.put(years, data["time"].year.real, lst)"""


# Funciones para creacion de datos

def create_earthquake(earthquake):
    earthquake["mag"] = float(earthquake["mag"])
    earthquake["time"] = datetime.strptime(earthquake["time"], datesFormat).replace(second=0)
    earthquake["updated"] = datetime.strptime(earthquake["updated"], datesFormat).replace(second=0)
    earthquake["sig"] = int(earthquake["sig"])
    earthquake["tsunami"] = bool(int(earthquake["tsunami"]))
    earthquake["sources"] = earthquake["sources"][1:-1].split("-")
    earthquake["types"] = earthquake["types"][1:-1].split("-")
    earthquake["ids"] = earthquake["ids"][1:-1].split("-")
    if earthquake["gap"] == "":
        earthquake["gap"] = "Unknown"
    else:
        earthquake["gap"] = int(float(earthquake["gap"]))
    if earthquake["nst"] == "":
        earthquake["nst"] = 1
    else:
        earthquake["nst"] = int(float(earthquake["nst"]))
    earthquake["long"] = round(float(earthquake["long"]), 3)
    earthquake["lat"] = round(float(earthquake["lat"]), 3)
    earthquake["depth"] = float(earthquake["depth"])
    return earthquake
















# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass












# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(analyzer, ini, fini):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    ini= datetime.datetime.strptime(ini, "%Y-%m-%dT%H:%M")
    fini= datetime.datetime.strptime(fini, "%Y-%m-%dT%H:%M")
    
    list= om.values(analyzer["fechaIndex"],ini, fini)
    list_ind= lt.newList()
    for x in lt.iterator(list):
        for y in lt.iterator(x):
            lt.addFirst(list_ind,y)

    tamaño_lista= lt.size(list)

    Primeros_3= lt.subList(list_ind,1,3)
    ultimos_3= lt.subList(list_ind,tamaño_lista-2,3)
    
    resu=[tamaño_lista,Primeros_3,ultimos_3]

    return resu


def req_2(analyzer, ini, fin):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    lista= om.values(analyzer["magIndex"],ini,fin)
    
    lista_ind= lt.newList()
    
    for x in lt.iterator(lista):
            
            for y in lt.iterator(x):
                lt.addFirst(lista_ind,y)
            
            
    Primeros_3= lt.subList(lista,1,3)
    for x in lt.iterator(Primeros_3):
        merg.sort(x,sort_por_fecha_des)
        if lt.size(x)>6:
            primeros= lt.subList(x,1,3)
            ultimos= lt.subList(x,lt.size(x)-2,3)
            
        



    tamaño_lista= lt.size(lista_ind)
    Consulta_tiene= lt.size(lista)
    
    ultimos_3= lt.subList(lista,Consulta_tiene-2,3)
    resu=[Consulta_tiene,tamaño_lista, Primeros_3, ultimos_3]
    


    return resu


def req_3(analyzer, mag_min, prof_max):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    mapa_fechas= om.newMap("RBT",MENOR_MAYOR)

    for magnitud in lt.iterator(om.values(analyzer["magIndex"],mag_min, 20)):
        for x in lt.iterator(magnitud):
            if float(x["depth"]) <= prof_max:
                #meter x en el mapa
                fecha = x['time']
 
                if om.contains(mapa_fechas, fecha):
                    lt.addLast(om.get(mapa_fechas ,fecha)["value"], x)
        
                else:
                    lista_terremotos= lt.newList("SINGLE_LINKED", MENOR_MAYOR)
                    om.put(mapa_fechas,fecha, lista_terremotos)
                    lt.addLast(om.get(mapa_fechas,fecha)["value"], x)

    lista_resp= lt.newList()
    while lt.size(lista_resp) < 10:
        llave_max=om.maxKey(mapa_fechas)
        for x in lt.iterator(om.get(mapa_fechas, llave_max)["value"]):
       
            lt.addLast(lista_resp,x)
        om.deleteMax(mapa_fechas)
    final= lt.newList()
    for x in lt.iterator(lt.subList(lista_resp,1,3)):
        lt.addLast(final,x)
    for x in lt.iterator(lt.subList(lista_resp,8,3)):
        lt.addLast(final,x)
    
    total_diferents= om.size(mapa_fechas)+10
    total= om.size(mapa_fechas)+10
    res=[total_diferents,total,final]
    return res


def req_4(analyzer,sig, gap):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    lista= lt.newList()
    mapa=analyzer["fechaIndex"]
    while lt.size(lista)< 15:
        llave_max= om.maxKey(mapa)
        for x in lt.iterator(om.get(mapa, llave_max)["value"]):
            if float(x["sig"])> sig and float(x["gap"])< gap:
                lt.addLast(lista,x)
        om.deleteMax(mapa)



    if lt.size(lista)>15:
        merg.sort(lista, sort_por_fecha_des)
        lista= lt.subList(lista,1,15)

    merg.sort(lista, sort_por_fecha_des)
    



    return lista


def req_5(data_structs, min_depth, min_stations):
    """
    Función que soluciona el requerimiento 5
    """
    selected = lt.newList(datastructure="SINGLE_LINKED")

    magnitudes = om.valueSet(data_structs["earthquakes_by_time_magnitude"])

    results = 0

    for earthquakes in lt.iterator(magnitudes):
        earthquakes = om.valueSet(earthquakes)
        for earthquake in lt.iterator(earthquakes):
            if earthquake["depth"] >= min_depth and earthquake["nst"] >= min_stations:
                results += 1
                if lt.size(selected) < 20:
                    earthquake_data = {}
                    earthquake_data["Fecha y Hora"] = earthquake["time"]
                    earthquake_data["Magnitud"] = earthquake["mag"]
                    earthquake_data["Longitud"] = earthquake["long"]
                    earthquake_data["Latitud"] = earthquake["lat"]
                    earthquake_data["Profundidad"] = earthquake["depth"]
                    earthquake_data["Significancia"] = earthquake["sig"]
                    earthquake_data["Distancia azimutal"] = earthquake["gap"]
                    earthquake_data["# Estaciones"] = earthquake["nst"]
                    earthquake_data["Titulo"] = earthquake["title"]
                    earthquake_data["Intensidad máxima DYFI"] = earthquake["cdi"]
                    earthquake_data["Intensidad máxima instrumental"] = earthquake["mmi"]
                    earthquake_data["Algoritmo de cálculo"] = earthquake["magType"]
                    earthquake_data["Tipo"] = earthquake["type"]
                    earthquake_data["Código"] = earthquake["code"]
                    lt.addLast(selected, earthquake_data)

    return selected, results


def req_6(analyzer,año, lati,long, radio, numero_N_eventos):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    año_del_evento_inio= año+"-01-01T01:01"
    año_del_evento_inio=datetime.datetime.strptime(año_del_evento_inio, "%Y-%m-%dT%H:%M")
    año_del_evento_final= año+"-12-31T23:59"
    año_del_evento_final=datetime.datetime.strptime(año_del_evento_final, "%Y-%m-%dT%H:%M")

    lista_eventos_en_el_año= om.values(analyzer["fechaIndex"],año_del_evento_inio,año_del_evento_final)

    lista_radio_año= lt.newList()
    mapa_radio_año_ord= om.newMap("RBT",MENOR_MAYOR)

    for x in lt.iterator(lista_eventos_en_el_año):
        for y in lt.iterator(x):
            long1= y["long"]
            latitud1= y["lat"]
            if radio >= calcular_distancia_tierra(long1, latitud1, long, lati):
                lt.addLast(lista_radio_año,y)

                fecha = y['time']
 
                if om.contains(mapa_radio_año_ord, fecha):
                    lt.addLast(om.get(mapa_radio_año_ord ,fecha)["value"], y)
        
                else:
                    lista_terremotos= lt.newList("SINGLE_LINKED", MENOR_MAYOR)
                    om.put(mapa_radio_año_ord,fecha, lista_terremotos)
                    lt.addLast(om.get(mapa_radio_año_ord,fecha)["value"], y)
                

    evento_mas_sig= None
    ev_sig= 0
  
    for x in lt.iterator(lista_radio_año):
        if int(x["sig"])> ev_sig:
            ev_sig= int(x["sig"])
            evento_mas_sig= x
    
    print(evento_mas_sig["title"])
    print(lt.getElement(lista_radio_año, 1)["title"])
    merg.sort(lista_radio_año, sort_por_fecha_des)


    pos_evento_mas_sig= None
    a=0
    for x in lt.iterator(lista_radio_año):
        a+=1
        if evento_mas_sig["title"] == x["title"]:
            pos_evento_mas_sig=a

    if lt.size(lista_radio_año)> pos_evento_mas_sig+numero_N_eventos:
        mayores_eventos=  lt.subList(lista_radio_año,pos_evento_mas_sig,numero_N_eventos+1)
    if lt.size(lista_radio_año)< pos_evento_mas_sig+numero_N_eventos:
        posibles=lt.size(lista_radio_año)-pos_evento_mas_sig
        mayores_eventos=  lt.subList(lista_radio_año,pos_evento_mas_sig,posibles+1)


    lista_radio_año_reves=lt.newList()
    for x in lt.iterator(lista_radio_año):
        lt.addFirst(lista_radio_año_reves,x)
    # posicion al reves
    pos_evento_mas_sig2= None
    a2=0
    for x in lt.iterator(lista_radio_año_reves):
        a+=1
        if evento_mas_sig["title"] == x["title"]:
            pos_evento_mas_sig2=a2

    # cambiar lista radio año    YA
    # cambiar posicion          YA
    # cambiar menores eventos   YA
    if lt.size(lista_radio_año_reves)> pos_evento_mas_sig2+numero_N_eventos:
        menores_eventos=  lt.subList(lista_radio_año_reves,pos_evento_mas_sig2,numero_N_eventos)
    if lt.size(lista_radio_año_reves)< pos_evento_mas_sig2+numero_N_eventos:
        posibles=lt.size(lista_radio_año_reves)-pos_evento_mas_sig2
        menores_eventos=  lt.subList(lista_radio_año_reves,pos_evento_mas_sig2,numero_N_eventos)


    resp=lt.newList()
    for x in lt.iterator(menores_eventos):
        lt.addLast(resp,x)
    for x in lt.iterator(mayores_eventos):
        lt.addLast(resp,x)

    merg.sort(resp, sort_por_fecha_des)
    mas=evento_mas_sig
    ya=[mas,resp]
    return ya









def calcular_distancia_tierra(long1, latitud1, long2, latitud2):
    long1 = math.radians(float(long1))
    latitud1 = math.radians(float(latitud1))
    long2 = math.radians(float(long2))
    latitud2 = math.radians(float(latitud2))

    distancia = 2 * math.asin(
        math.sqrt(
            math.sin(0.5 * (long2 - long1))**2 +
            math.cos(long1) * math.cos(long2) * math.sin(0.5 * (latitud2 - latitud1))**2
        )
    ) * 6371

    return distancia







def req_7(data_structs, year, region, property, bins):
    earthquakes_in_zone = mp.get(data_structs["earthquakes_by_zone_year"], region)

    if earthquakes_in_zone is None:
        return None

    earthquakes_in_year = mp.get(me.getValue(earthquakes_in_zone), year)

    if earthquakes_in_year is None:
        return None

    earthquakes_in_year = me.getValue(earthquakes_in_year)

    earthquakes_by_property = om.newMap(omaptype="RBT")

    for earthquake in lt.iterator(earthquakes_in_year):
        exists = om.get(earthquakes_by_property, earthquake[property])
        if exists is not None:
            lst = me.getValue(exists)
            lt.addLast(lst, earthquake)
        else:
            lst = lt.newList(datastructure="SINGLE_LINKED")
            lt.addLast(lst, earthquake)
            om.put(earthquakes_by_property, earthquake[property], lst)

    min_property = om.minKey(earthquakes_by_property)
    max_property = om.maxKey(earthquakes_by_property)

    gap = round((max_property - min_property) / bins, 3)

    categories = []
    values = []

    current_min = min_property

    for i in range(bins):
        next = round(current_min + gap, 3)
        if i == bins - 1:
            next = max_property
        categories.append(f"{current_min}-{next}")

        amount = 0

        for lst in lt.iterator(om.values(earthquakes_by_property, current_min, next)):
            amount += lt.size(lst)

        values.append(amount)

        current_min = next

    merg.sort(earthquakes_in_year, sort_time)

    return earthquakes_in_year, categories, values


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDictsFecha(dict1, dict2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    if (dict1["time"] == dict2["time"]):
        return 0
    elif (dict1["time"] > dict2["time"]):
        return 1
    else:
        return -1
def compareDictsFecha2(dict1, dict2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    if (dict1["time"] == dict2["time"]):
        return 0
    elif (dict1["time"] < dict2["time"]):
        return 1
    else:
        return -1
    

def MAYOR_MENOR(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1








# Funciones de ordenamiento


def MENOR_MAYOR(mag1, mag2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    if (mag1 == mag2):
        return 0
    elif (mag1 > mag2):
        return 1
    else:
        return -1
    


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass



def sort_por_fecha_asc(data_1, data_2):
    return data_1["time"] <data_2["time"]


def sort_por_fecha_des(data_1, data_2):
    return data_1["time"] >data_2["time"]
def compare_desc(data_1, data_2):
    if data_1 > data_2:
        return -1
    elif data_1 == data_2:
        return 0
    return 1
def sort_time(data_1, data_2):
    return data_1["time"] < data_2["time"]