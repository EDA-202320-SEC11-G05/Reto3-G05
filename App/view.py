"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
from tabulate import tabulate
default_limit = 1000
sys.setrecursionlimit(default_limit*1000)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
terremotosfile = "Data/temblores-utf8-small.csv"
#terremotosfile = "Data/temblores-utf8-large.csv"



def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control= controller.new_controller()

    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    controller.load_data(control, terremotosfile)
    return control["magIndex"]


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, ini, fini):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    res= controller.req_1(control, ini, fini)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     TOTAL:        "+str(res[0]))
    print(tabulate(lt.iterator(res[1])))
    print(tabulate(lt.iterator(res[2])))
    

def print_req_2(control,ini, fini):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    res= controller.req_2(control,ini, fini)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     TOTAL DIFERENTES:        "+str(res[0]))
    print("     TOTAL:        "+str(res[1]))
    for x in lt.iterator(res[3]):
        if lt.size(x) >6:
            primeros= lt.subList(x,1,3)
            ultimos= lt.subList(x,lt.size(x)-2,3)
            uni= lt.newList()
            for x in lt.iterator(primeros):
                lt.addLast(uni,x)
            for x in lt.iterator(ultimos):
                lt.addLast(uni,x)
            print(tabulate(lt.iterator(uni)))
        else:
            print(tabulate(lt.iterator(x)))
    for x in lt.iterator(res[2]):
        if lt.size(x) >6:
            primeros= lt.subList(x,1,3)
            ultimos= lt.subList(x,lt.size(x)-2,3)
            uni= lt.newList()
            for x in lt.iterator(primeros):
                lt.addLast(uni,x)
            for x in lt.iterator(ultimos):
                lt.addLast(uni,x)
            print(tabulate(lt.iterator(uni)))
        else:
            print(tabulate(lt.iterator(x)))
    
    

def print_req_3(control, mag_min, prof_max):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    res= controller.req_3(control,mag_min, prof_max )
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     TOTAL DIFERENTES:        "+str(res[0]))
    print("     TOTAL:        "+str(res[1]))
    print(tabulate(lt.iterator(res[2])))
    

    
    


def print_req_4(control,sig, gap):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    res= controller.req_4(control,sig, gap)

    print(tabulate(lt.iterator(res)))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(analyzer,año, lati,long, radio, numero_N_eventos):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    res= controller.req_6(analyzer,año, lati,long, radio, numero_N_eventos)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     EVENTO MAS SIGNIFICATIVO:        ")
    print(res[0])
    print("     EVENTO CERCA:        ")
    print(tabulate(lt.iterator(res[1])))
    
    


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:

            ini= input(" Desde que fecha desea consultar:   ")
            fini= input(" Hasta que fecha desea consultar:   ")
            print_req_1(control, ini, fini)

        elif int(inputs) == 3:
            ini= float(input(" Desde que magnitud desea consultar:   "))
            fini= float(input(" Hasta que magnitud desea consultar:   "))
            print_req_2(control, ini, fini)

        elif int(inputs) == 4:
            mag_min= float(input(" Minimo de magnitud que desea consultar:   "))
            prof_max= float(input(" Maximo de profundidad que desea consultar:   "))
            print_req_3(control, mag_min, prof_max)

        elif int(inputs) == 5:
            sig= int(input("  Ingrese el sig mínimo:      "))
            gap= int(input("  Ingrese el gap máximo:      "))
            print_req_4(control,sig, gap)

        elif int(inputs) == 6: 
            print_req_5(control)

        elif int(inputs) == 7:
            año= input(" Ingrese el año:     ")
            lati= input("Ingese latitud:        ")
            long= input("Ingrese longitud:      ")
            radio= float(input("ingrese radio:      "))
            numero_N_eventos= int(input("Ingrese numero N de elementos:     "))
            print_req_6(control,año, lati,long, radio, numero_N_eventos)
            

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
