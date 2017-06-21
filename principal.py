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
    posicionesOcupadas = []     # Lista de las posiciones de listaPalbra y listaAyuda ya utilizadas
    nombreuser=""               # variable con el nombre de usuario, se usa para el ranking
    listaRankingNombre=[]       # Lista que guarda los nombres del top 10
    listaRankingPuntos=[]       # Lista que guarda los puntajes del top 10
    nada = []                   # Una lista vacia para utilizar de forma auxiliar
    penalidades = 0             # Variable que incorpora el tiempo de penalidad o premio por acertar o no


    song= pygame.mixer.Sound("song.ogg")        # Musica del juego, carga el archivo
    song.set_volume(0.2)                        # Establecer el volumen como una cortina de fondo, bajito
    song.play()                                 # Darle play a la musica
    tecla = pygame.mixer.Sound("sou.ogg")       # Efecto de sonido para cuando se presiona una tecla
    pasar = pygame.mixer.Sound("pasar.ogg")     # Efecto de sonido cuando se hace pasapalabra
    corre = pygame.mixer.Sound("correcta.ogg")  # Efecto de sonido cuando se aciera a la palabra





    #Cargar datos en listaPalabra y listaAyudas desde los dos archivos
    lectura(listaPalabra, listaAyuda)

    #Cargar datos en listaRankingNombre y listaRankingPuntos desde los dos archivos del ranking
    leerRanking(listaRankingNombre,listaRankingPuntos)


    cargaInicial=random.randint(0,len(listaPalabra)-1)                 # ACA NO DEBERIA SER MENOS 1 PORQUE SINO TE PODES PASAR DEL INDEX DE LISTAPALABRA
    posicionesOcupadas.append(cargaInicial)                            # La primera palabra debe ser guardada, en el listado de posicionesOcupadas
    cargarPosiciones(listaPalabra[cargaInicial], posX, posY, ocupados) #Posiciones aleatorias dentro de los margenes establecidos
    palabra=listaPalabra[cargaInicial]                                 #Primera palabra por default
    cargarLetras(listaPalabra[cargaInicial], letrasEnPantalla)         #Caracteres que se muestran separados
    ayuda=listaAyuda[cargaInicial]                                     #El primer sinonimo que coincide por indice con la primer palabra

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
                tecla.play()
                letra = dameLetraApretada(e.key)
                candidata += letra
                if e.key == K_BACKSPACE:
                    candidata = candidata[0:len(candidata)-1]   # Al presionar la tecla retroceso (backspace) elimina el último elemento de la lista o string candidata
                if e.key == K_RETURN :
                    if candidata=='1': #Siguiente palabra
                        pasar.play()
                        palabra=cambiarPalabra(listaPalabra,posicionesOcupadas)
                        ayuda=cargarAyuda(listaAyuda, listaPalabra, palabra)
                        cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                        candidata=""
                        t0=t1 #Reiniciar el primer timer para volver a comparar con el segundo
                        if segundos > 5:                                    # Si todavía quedan más de 5 segundos, aplicar penalidad
                            penalidades = cambiarTiempo(penalidades,True)   # Si quedan menos de 5 segundos no se aplica para que no haya inconveniente
                                                                            # en ejectar el bucle donde se muestra el ranking. De paso el usuario puede
                                                                            # aproecharse y pasar palabras las veces que pueda en 5 segundos.

                    else:
                        if(esCorrecta(candidata, palabra)): #acerto
                                    corre.play()
                                    palabra=cambiarPalabra(listaPalabra,posicionesOcupadas)
                                    ayuda=cargarAyuda(listaAyuda,listaPalabra,palabra)
                                    cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                                    candidata=""
                                    puntos += puntuar(palabra)
                                    t0=t1
                                    penalidades = cambiarTiempo(penalidades,False)  # 5 segundos de regalo, por acertar la palabra

        screen.fill(COLOR_FONDO)

        segundos = penalidades + TIEMPO_MAX - pygame.time.get_ticks()/1000  #Se modificó esta formula para que aplique permanente las penalidades o premios en tiempo

        #Nuevo refresh
        dibujar(letrasEnPantalla, posX, posY, candidata, palabra, ayuda, segundos, t0, t1, screen, puntos)

        if(t1-t0>=16): #Cambiar la palabra
                palabra=cambiarPalabra(listaPalabra,posicionesOcupadas)
                ayuda=cargarAyuda(listaAyuda,listaPalabra,palabra)
                cargarListas(posX, posY, letrasEnPantalla, ocupados, palabra, ayuda, listaPalabra, listaAyuda)
                candidata=""
                t0=t1
                dibujar(letrasEnPantalla, posX, posY, candidata, palabra, ayuda, segundos, t0, t1, screen, puntos) #Segundo llamado
                penalidades = cambiarTiempo(penalidades,True)               # Si pasó el tiempo y no acertó aplica penalidad
        pygame.display.flip()






    screen.fill(COLOR_FONDO)                # Limpiar pantalla
    pygame.display.flip()                   # Actualizar pantalla
    song.set_volume(0)                      # Que la música no se escuche más
    segundos = 9999999                      # Dar muchos segundos para que sea siempre mayor al tiempo transcurrido hasta que termina de jugar
                                            #y no haya problema en ver ranking y escribir nombre

    # Resultado es la posicion que ocupa en el ranking, o es False si no entra al ranking
    resultado = entraEnRanking(puntos,listaRankingNombre,listaRankingPuntos)



    if (resultado is not False): #Si merece estar en el ranking


        while segundos > fps/1000:          #Nuevo bucle para ver ranking y escribir nombre



            font = pygame.font.Font(None, 30)   #Inicializar fuentes (para escribir)

            screen.fill(COLOR_FONDO)        #Limpiar pantalla cada vez que itere el ciclo


            for e in pygame.event.get():    #evento que escucha si se produjo el evento que sale del programa
                if e.type == QUIT:
                    pygame.quit()
                    return






            if e.type == KEYDOWN:           #evento que escucha las letras presionadas
                tecla.play()
                letra = dameLetraApretada(e.key)
                print (letra)
                nombreuser += letra
                pygame.time.wait(100)       # para que no se repitan letras si el usuario tarda menos de 100 milisegundos en levantar el dedo de la tecla
                if e.key == K_BACKSPACE:
                    nombreuser = nombreuser[0:len(nombreuser)-1]    # Borra el último caracter si escribió backspace
                if e.key == K_RETURN :
                    escribirNuevoRanking(resultado,nombreuser,puntos,listaRankingNombre,listaRankingPuntos) # Al darle enter, ingresar los datos definitivamente al ranking
                    pygame.quit()                                                                           # Salir del programa
                    return

            screen.blit(font.render("Ingresa tu nombre", 1, COLOR_LETRAS), (50,500))    # Cartel que le dice al usuario que puede ingresar su nombre


            # Funcion que muestra el ranking y en vivo la posicion que ocupa el usuario y cambia su nombre conforme lo tipea
            imprimirRankingMerecido(listaRankingNombre,listaRankingPuntos,screen,resultado,nombreuser,puntos)





            # Reutilizar la funcion que dibuja con valores especificos.
                # No se necesitan letras sueltas por ahi. Entonces,
                # nada para la letrasEnPantalla
                # nada para posiciones con PosX y posY
                # ahora la candidata es el nombre del usuario
                # no hay palabra que adivinar asi que "" (nada)
                # En la ayuda puede mostrar un cartel que diga "Ingresa tu nombre"
                # en segundos que muestren los segundos que quedan para que complete su nombre
                # en t0 o t1 ya no tiene importancia la distancia entre el momento actual y el momento de la aparición de la palabra. se le pasa el valor de segundos
                # screen es el puntero que maneja la pantalla, hay que pasarlo
                # se quieren mostrar los puntos actuales, asi que tambien se pasan los puntos
            dibujar(nada, nada, nada, nombreuser, "", "Ingresa tu nombre", segundos, segundos, segundos, screen, puntos) #Segundo llamado


            # Esta es la formular de segundos restantes para esta parte del programa
            segundos = TIEMPO_RANKING - pygame.time.get_ticks()/1000

            # Actualizar pantalla
            pygame.display.flip()


    else:       #Si NO merece estar en el ranking
        while segundos > fps/1000:          #Nuevo bucle para ver ranking y escribir nombre



            font = pygame.font.Font(None, 30)   #Inicializar fuentes (para escribir)

            screen.fill(COLOR_FONDO)        #Limpiar pantalla cada vez que itere el ciclo


            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

            # no hace falta esperar que el usuario tipee nada aquí



             # Funcion que muestra SOLO el ranking
            imprimirRanking(listaRankingNombre,listaRankingPuntos,screen)




            # Reutilizar la funcion que dibuja con valores especificos.
                # No se necesitan letras sueltas por ahi. Entonces,
                # nada para la letrasEnPantalla
                # nada para posiciones con PosX y posY
                # ahora la candidata es el nombre del usuario PERO NO PUEDE ESCRIBIRLO PORQUE NO ENTRO AL RANKING
                # no hay palabra que adivinar asi que "" (nada)
                # En la ayuda puede mostrar un cartel que diga "Más suerte para la próxima"
                # en segundos que muestren los segundos que quedan hasta que se cierre el programa
                # en t0 o t1 ya no tiene importancia la distancia entre el momento actual y el momento de la aparición de la palabra. se le pasa el valor de segundos
                # screen es el puntero que maneja la pantalla, hay que pasarlo
                # se quieren mostrar los puntos actuales, asi que tambien se pasan los puntos
            dibujar(nada, nada, nada, nombreuser, "", "Más suerte para la próxima", segundos, segundos, segundos, screen, puntos) #Segundo llamado



            # Esta es la formular de segundos restantes para esta parte del programa
            segundos = TIEMPO_RANKING - pygame.time.get_ticks()/1000

            # Actualizar pantalla
            pygame.display.flip()

    while 1:



        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return



if __name__ == '__main__':
    main()