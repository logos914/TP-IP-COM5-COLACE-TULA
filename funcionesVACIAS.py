from configuracion import *
from principal import *
import random
import math

def lectura(listaNombres,listaAyuda):#Cargar las dos listas desde los archivos

    archivoPalabras = open("paises.txt","r")
    archivoAyuda = open("capitales.txt","r")

    lineasPalabras = archivoPalabras.readlines()
    lineasAyuda = archivoAyuda.readlines()

    for linea in lineasPalabras:
        linea = linea.replace("\n","")
        listaNombres.append(linea)
    archivoPalabras.close()

    for linea in lineasAyuda:
        linea = linea.replace("\n","")
        listaAyuda.append(linea)
    archivoAyuda.close()




def vaciarLista(lista): # Esta función deja con cero elementos la lista que se pasa como argumento
    for i in range(len(lista)):
        lista.pop()

def cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaNombres, listaAyuda): #Vaciar posX, posY, letrasenpantalla y ocupados, luego llamar cargarLetras y cargarPosiciones
    vaciarLista(posX)
    vaciarLista(letrasEnPantalla)
    vaciarLista(ocupados)
    vaciarLista(posY)
    cargarLetras(palabra,letrasEnPantalla)
    cargarPosiciones(letrasEnPantalla,posX,posY,ocupados)

def cargarLetras(palabra, letrasEnPantalla):#Recorrer  palabra y apendear a letrasEnPantalla
   for letra in palabra:
       letrasEnPantalla.append(letra)


def fueUsadaLaPalabra(pos,posicionesOcupadas): # Indica si una palabra fue utilizada comparada por su posición
    for i in range(0,len(posicionesOcupadas)):
        if posicionesOcupadas[i] == pos:
            return True
    return False

def cambiarPalabra(listaPalabra,posicionesOcupadas):#Devolver palabra elegida al azar
    contador = 0
    candidatoOcupar = random.randint(0,len(listaPalabra)-1)
    while (fueUsadaLaPalabra(candidatoOcupar,posicionesOcupadas) and contador < len(listaPalabra)): #Si la palabra fue utilizada, seguirá probando un random hasta encontrar una que no haya sido utilizada
        candidatoOcupar = random.randint(0,len(listaPalabra)-1)
        contador = contador + 1
    if (contador >= len(listaPalabra)): # El que no se repitan las palabras, puede provocar que en algún momento nuestro diccionario se acabe. Entonces si esto ocurre que el juego deje de ejecutarse
        print("No hay más palabras para adivinar")
        pygame.quit()
    posicionesOcupadas.append(candidatoOcupar) # Añade el registro de la posición ocupada
    return listaPalabra[candidatoOcupar]


def cargarPosiciones(letras, posX, posY, ocupados):#Cargar listas posX y posY en ubicaciones aleatorias
    for i in letras:
        posibleX = random.randrange(50,750)
        while (estaCerca(posibleX,ocupados)): # Busca una posición lejana para la letra, si no la encuentra seguirá buscando un random que si lo esté
            posibleX = random.randrange(50,750)
          #  print("No encuentro uno lejos") # SE USABA PARA DEBBUGEAR
        posX.append(posibleX)
        ocupados.append(posibleX) # añade el registro de la posición ocupada para que no se vuelva a utilizar
        posY.append(random.randrange(50,500))
    pass

def cargarAyuda(listaAyuda, listaPalabra, palabra):#Retornar sinonimo
    return listaAyuda[damePosicion(listaPalabra,palabra)]


def damePosicion(listaPalabra, palabra):#Devuelve la posicion de la palabra en listaPalabra
    for i in range(0,len(listaPalabra)):
        if listaPalabra[i] == palabra:
            return i


def estaCerca(elem, lista):        # Control de superposicion (elem es el candidato a utilizar esa posición, lista debe contener el listado con las posiciones utilizadas)

    for i in lista:                # Por cada lugar de la lista
        if (i > elem):             # Si la pos del lugar es más grande que el candidato actual
            if (i - elem) <= 10:    # Y la diferencia es menor que diez
                return True        #Entonces está cerca
        else:
            if (i < elem):          # Si la pos del lugar es más pequeña que el candidato actual
                if (elem - i) <= 10: # Y la diferencia es menor que diez
                    return True     #Entonces está cerca

            else:
                if (i == elem):     # Si la pos del lugar es igual al candidato actual
                    return True     #Entonces está cerca
    return False                    # Si supera todo el bucle, entonces está lejos






def esCorrecta(candidata, palabra):#comprobar palabra ingresada por teclado
    if candidata == palabra:
        return True
    else:
        return False


def puntuar(palabra): #puntuacion

    puntos=0
    for i in range(len(palabra)): # por cada letra
        if i == "a" or i == "e" or i == "i" or i == "o" or i == "u": # si son vocales
            puntos += 1 #suma un punto
        else:
            if i == "j" or i == "k" or i == "q" or i == "w" or i == "x" or i == "y" or i == "z": #si son letras dificiles
                puntos += 5                                         #suma 5 puntos
            else:
                puntos +=2       #en los demás casos suma 2 puntos
    return puntos

def cambiarTiempo(penalidades,penaliza):
    if penaliza is False:
        penalidades += 5
        return penalidades
    else:
        penalidades -= 5
        return penalidades

