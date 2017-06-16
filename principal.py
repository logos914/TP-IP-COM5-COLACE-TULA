#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from funcionesVACIAS import *
from extras import *
from configuracion import *
import os, random, sys, math, time


def main():
    #Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    #Preparar la ventana
    pygame.display.set_caption("Sinonimos")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    #tiempo total del juego
    segundos=TIEMPO_MAX
    fps=FPS_inicial

    #primer timer interno para letras de ayuda
    t0 = time.time()

    #inicializacion de variables
    puntos=0
    candidata = ""
    listaPalabra=[]
    listaAyuda=[]
    letrasEnPantalla = []
    posX=[]
    posY=[]
    ayuda=""
    ocupados=[]

    #Cargar datos en listaPalabra y listaAyudas desde los dos archivos
    lectura(listaPalabra, listaAyuda)


    cargaInicial=random.randint(0,len(listaPalabra))

    cargarPosiciones(listaPalabra[cargaInicial], posX, posY, ocupados) #Posiciones aleatorias dentro de los margenes establecidos
    palabra=listaPalabra[cargaInicial] #Primera palabra por default
    cargarLetras(listaPalabra[cargaInicial], letrasEnPantalla) #Caracteres que se muestran separados
    ayuda=listaAyuda[cargaInicial] #El primer sinonimo que coincide por indice con la primer palabra

    while segundos > fps/1000:
        #Segundo timer que compara con el primero
        t1 = time.time()

        #Buscar la tecla apretada del modulo de eventos de pygame
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return

            #Ver si fue apretada alguna tecla
            if e.type == KEYDOWN:
                letra = dameLetraApretada(e.key)
                candidata += letra
                if e.key == K_BACKSPACE:
                    candidata = candidata[0:len(candidata)-1]
                if e.key == K_RETURN :
                    if candidata=='1': #Siguiente palabra
                        palabra=cambiarPalabra(listaPalabra)
                        ayuda=cargarAyuda(listaAyuda, listaPalabra, palabra)
                        cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                        candidata=""
                        t0=t1 #Reiniciar el primer timer para volver a comparar con el segundo
                    else:
                        if(esCorrecta(candidata, palabra)): #acerto
                                    palabra=cambiarPalabra(listaPalabra)
                                    ayuda=cargarAyuda(listaAyuda,listaPalabra,palabra)
                                    cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                                    candidata=""
                                    puntos += puntuar(palabra)
                                    t0=t1
        screen.fill(COLOR_FONDO)

        segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000
        #Nuevo refresh
        dibujar(letrasEnPantalla, posX, posY, candidata, palabra, ayuda, segundos, t0, t1, screen, puntos)

        if(t1-t0>=16): #Cambiar la palabra
                palabra=cambiarPalabra(listaPalabra)
                ayuda=cargarAyuda(listaAyuda,listaPalabra,palabra)
                cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                candidata=""
                t0=t1
                dibujar(letrasEnPantalla, posX, posY, candidata, palabra, ayuda, segundos, t0, t1, screen, puntos) #Segundo llamado

        pygame.display.flip()

    while 1:
        #Esperar el QUIT del usuario
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return


if __name__ == '__main__':
    main()