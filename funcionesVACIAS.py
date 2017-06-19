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
    archivoPalabras.close()


    archivoAyuda = open("sinonimos.txt","r")
    lineasAyuda = archivoAyuda.readlines()
    for linea in lineasAyuda:
        linea = linea.replace("\n","")
        listaAyuda.append(linea)
    archivoAyuda.close()

def cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaNombres, listaAyuda): #Vaciar posX, posY, letrasenpantalla y ocupados, luego llamar cargarLetras y cargarPosiciones

    for i in range(len(posX)):
        posX.pop()
    for i in range(len(posY)):
        posY.pop()
    for i in range(len(letrasEnPantalla)):
        letrasEnPantalla.pop()
    for i in range(len(ocupados)):
        ocupados.pop()
    cargarLetras(palabra,letrasEnPantalla)
    cargarPosiciones(letrasEnPantalla,posX,posY,ocupados)


def cargarLetras(palabra, letrasEnPantalla):#Recorrer  palabra y apendear a letrasEnPantalla
   for letra in palabra:
       letrasEnPantalla.append(letra)


def fueUsadaLaPalabra(pos,posicionesOcupadas):
    for i in range(0,len(posicionesOcupadas)):
        if posicionesOcupadas[i] == pos:
            return True
    return False

def cambiarPalabra(listaPalabra,posicionesOcupadas):#Devolver palabra elegida al azar
    contador = 0
    candidatoOcupar = random.randint(0,len(listaPalabra)-1)
    while (fueUsadaLaPalabra(candidatoOcupar,posicionesOcupadas) and contador < len(listaPalabra)):
        candidatoOcupar = random.randint(0,len(listaPalabra)-1)
        contador = contador + 1
    if (contador >= len(listaPalabra)):
        print("Te fuiste a la mierda, no hay más palabras")
        pygame.quit()
    posicionesOcupadas.append(candidatoOcupar)
    return listaPalabra[candidatoOcupar]


def cargarPosiciones(letras, posX, posY, ocupados):#Cargar listas posX y posY en ubicaciones aleatorias
    for i in letras:
        posibleX = random.randrange(50,750)
        while (estaCerca(posibleX,ocupados)):
            posibleX = random.randrange(50,750)
            print("No encuentro uno lejos")
        posX.append(posibleX)
        ocupados.append(posibleX)
        posY.append(random.randrange(50,500))
    pass

def cargarAyuda(listaAyuda, listaPalabra, palabra):#Retornar sinonimo
    return listaAyuda[damePosicion(listaPalabra,palabra)]


def damePosicion(listaPalabra, palabra):#Devuelver la posicion de la palabra en listaPalabra
    for i in range(0,len(listaPalabra)):
        if listaPalabra[i] == palabra:
            return i


def estaCerca(elem, lista):#Control de superposicion

    for i in lista:
        if (i > elem):
            if (i - elem) <= 3:
                return True
        else:
            if (i < elem):
                if (elem - i) <= 3:
                    return True

            else:
                if (i == elem):
                    return True
    return False






def esCorrecta(candidata, palabra):#comprobar palabra ingresada por teclado
    if candidata == palabra:
        return True
    else:
        return False


def puntuar(palabra): #puntuacion

    puntos=0
    for i in range(len(palabra)):
        if i == "a" or i == "e" or i == "i" or i == "o" or i == "u":
            puntos += 1
        else:
            if i == "j" or i == "k" or i == "q" or i == "w" or i == "x" or i == "y" or i == "z":
                puntos += 5
            else:
                puntos +=2
    return puntos