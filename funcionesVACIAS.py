from configuracion import *
from principal import *
import random
import math

def lectura(listaNombres,listaAyuda):#Cargar las dos listas desde los archivos
    archivoPalabras = open("palabras.txt","r")
    lineasPalabras = archivoPalabras.readlines()
    for linea in lineasPalabras:
        linea = linea.replace("\n","")
        listaNombres.append(linea)


    archivoAyuda = open("sinonimos.txt","r")
    lineasAyuda = archivoAyuda.readlines()
    for linea in lineasAyuda:
        linea = linea.replace("\n","")
        listaAyuda.append(linea)

def cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaNombres, listaAyuda): #Vaciar posX, posY, letrasenpantalla y ocupados, luego llamar cargarLetras y cargarPosiciones
    posX = []
    posY = []
    letrasEnPantalla = []
    ocupados = []
    cargarLetras(palabra,letrasEnPantalla)
    cargarPosiciones(letrasEnPantalla,posX,posY,ocupados)
    pass

def cargarLetras(palabra, letrasEnPantalla):#Recorrer  palabra y apendear a letrasEnPantalla
   for letra in palabra:
       letrasEnPantalla.append(letra)


def cambiarPalabra(listaPalabra):#Devolver palabra elegida al azar
    return listaPalabra[random.randrange(len(listaPalabra))]
    pass

def cargarPosiciones(letras, posX, posY, ocupados):#Cargar listas posX y posY en ubicaciones aleatorias
    for i in letras:
        posX.append(random.randrange(800))
        posY.append(random.randrange(600))
    pass

def cargarAyuda(listaAyuda, listaPalabra, palabra):#Retornar sinonimo
    return listaAyuda[damePosicion(listaPalabra,palabra)]
    pass

def damePosicion(listaPalabra, palabra):#Devuelver la posicion de la palabra en listaPalabra
    for i in range(0,len(listaPalabra)):
        if listaPalabra[i] == palabra:
            return i


def estaCerca(elem, lista):#Control de superposicion
    pass

def esCorrecta(candidata, palabra):#comprobar palabra ingresada por teclado
    if candidata == palabra:
        return True
    else:
        return False


def puntuar(pal): #puntuacion
    pass


