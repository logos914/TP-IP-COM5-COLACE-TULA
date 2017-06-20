#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from funcionesVACIAS import *
from extras import *
from configuracion import *
import os, random, sys, math, time
from ranking import *






def main():
    #Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mixer.init()


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
    posicionesOcupadas = []
    nombreuser=""
    listaRankingNombre=[]
    listaRankingPuntos=[]
    nada = []


    song= pygame.mixer.Sound("song.wav")
    song.play()
    tecla = pygame.mixer.Sound("sou.wav")
    pasar = pygame.mixer.Sound("pasar.wav")
    corre = pygame.mixer.Sound("correcta.wav")





    #Cargar datos en listaPalabra y listaAyudas desde los dos archivos
    lectura(listaPalabra, listaAyuda)

    #Cargar datos en listaRankingNombre y listaRankingPuntos desde los dos archivos del ranking
    leerRanking(listaRankingNombre,listaRankingPuntos)


    cargaInicial=random.randint(0,len(listaPalabra)-1) # ACA NO DEBERIA SER MENOS 1 ??? PORQUE SINO TE PODES PASAR DEL INDEX DE LISTAPALABRA
    posicionesOcupadas.append(cargaInicial)
    cargarPosiciones(listaPalabra[cargaInicial], posX, posY, ocupados) #Posiciones aleatorias dentro de los margenes establecidos
    palabra=listaPalabra[cargaInicial] #Primera palabra por default
    cargarLetras(listaPalabra[cargaInicial], letrasEnPantalla) #Caracteres que se muestran separados
    ayuda=listaAyuda[cargaInicial] #El primer sinonimo que coincide por indice con la primer palabra

    while segundos > fps/1000:
        print("principal loop  ",segundos)
        #Segundo timer que compara con el primero

        t1 = time.time()

        #Buscar la tecla apretada del modulo de eventos de pygame
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return

            #Ver si fue apretada alguna tecla

            if e.type == KEYDOWN:
                tecla.play()
                letra = dameLetraApretada(e.key)
                candidata += letra
                if e.key == K_BACKSPACE:
                    candidata = candidata[0:len(candidata)-1]
                if e.key == K_RETURN :
                    if candidata=='1': #Siguiente palabra
                        pasar.play()
                        palabra=cambiarPalabra(listaPalabra,posicionesOcupadas)
                        ayuda=cargarAyuda(listaAyuda, listaPalabra, palabra)
                        cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                        candidata=""
                        t0=t1 #Reiniciar el primer timer para volver a comparar con el segundo

                    else:
                        if(esCorrecta(candidata, palabra)): #acerto
                                    corre.play()
                                    palabra=cambiarPalabra(listaPalabra,posicionesOcupadas)
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
                palabra=cambiarPalabra(listaPalabra,posicionesOcupadas)
                ayuda=cargarAyuda(listaAyuda,listaPalabra,palabra)
                cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                candidata=""
                t0=t1
                dibujar(letrasEnPantalla, posX, posY, candidata, palabra, ayuda, segundos, t0, t1, screen, puntos) #Segundo llamado

        pygame.display.flip()





    screen.fill(COLOR_FONDO)            #Limpiar pantalla
    pygame.display.flip()               #Actualizar pantalla
    song.stop()                         #Detener musica
    segundos = 30                       #Dar 30 segundos para ver ranking y escribir nombre
    #pygame.key.set_repeat(2500,5000)

    resultado = entraEnRanking(puntos,listaRankingNombre,listaRankingPuntos)



    if (resultado is not False): #Si merece estar en el ranking


        while segundos > fps/1000:          #Nuevo bucle para ver ranking y escribir nombre
            #t1 = time.time()                #ESTO ES NECESARIO ????

            print("loop    ",segundos)      #DEBUGGEANDO
            font = pygame.font.Font(None, 30)   #Inicializar fuentes (para escribir)

            screen.fill(COLOR_FONDO)        #Limpiar pantalla cada vez que itere el ciclo


            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return






            if e.type == KEYDOWN:
                tecla.play()
                letra = dameLetraApretada(e.key)
                print (letra)
                nombreuser += letra
                pygame.time.wait(100)       # para que no aparezcan mas letras que las presionadas
                if e.key == K_BACKSPACE:
                    nombreuser = nombreuser[0:len(nombreuser)-1]
                if e.key == K_RETURN :
                    escribirNuevoRanking(resultado,nombreuser,puntos,listaRankingNombre,listaRankingPuntos)
                    pygame.quit()
                    return

            screen.blit(font.render("Ingresa tu nombre", 1, COLOR_LETRAS), (50,500))



            imprimirRankingMerecido(listaRankingNombre,listaRankingPuntos,screen,resultado,nombreuser,puntos)






            dibujar(nada, nada, nada, nombreuser, "", "Ingresa tu nombre", segundos, segundos, segundos, screen, puntos) #Segundo llamado



            segundos = TIEMPO_RANKING - pygame.time.get_ticks()/1000
            pygame.display.flip()

    else:
        while segundos > fps/1000:          #Nuevo bucle para ver ranking y escribir nombre
            #t1 = time.time()                #ESTO ES NECESARIO ????

            print("loop    ",segundos)      #DEBUGGEANDO
            font = pygame.font.Font(None, 30)   #Inicializar fuentes (para escribir)

            screen.fill(COLOR_FONDO)        #Limpiar pantalla cada vez que itere el ciclo


            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return






            imprimirRanking(listaRankingNombre,listaRankingPuntos,screen)






            dibujar(nada, nada, nada, nombreuser, "", "Más suerte para la próxima", segundos, segundos, segundos, screen, puntos) #Segundo llamado



            segundos = TIEMPO_RANKING - pygame.time.get_ticks()/1000
            pygame.display.flip()

    while 1:



        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return



if __name__ == '__main__':
    main()