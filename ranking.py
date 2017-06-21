import pygame
from pygame.locals import *
from configuracion import *

def leerRanking(listaRankingNombre,listaRankingPuntos):
    archivoRankingNombre = open("ranking_nombre.txt","r")
    lineasRankingNombre = archivoRankingNombre.readlines()
    for linea in lineasRankingNombre[0:9]:
        linea = linea.replace("\n","")
        listaRankingNombre.append(linea)
    archivoRankingNombre.close()

    archivoRankingPuntos = open("ranking_puntos.txt","r")
    lineasRankingPuntos = archivoRankingPuntos.readlines()
    for linea in lineasRankingPuntos[0:9]:
        linea = int(linea.replace("\n",""))
        listaRankingPuntos.append(linea)
    archivoRankingPuntos.close()


def entraEnRanking(puntos,listaRankingNombre,listaRankingPuntos):
    for r in range(len(listaRankingPuntos)):
        if puntos > listaRankingPuntos[r]:
            for s in range(len(listaRankingPuntos)-1,r,-1):
                listaRankingPuntos[s] = listaRankingPuntos[s-1]
                listaRankingNombre[s] = listaRankingNombre[s-1]

            listaRankingPuntos[r] = puntos
            listaRankingNombre[r] = ""
            return r
    return False


def escribirNuevoRanking(pos,nombre, puntos,listaRankingNombre,listaRankingPuntos):
    listaRankingNombre[pos] = puntos
    listaRankingNombre[pos] = nombre

    archivoRankingNombre = open("ranking_nombre.txt","w")
    archivoRankingNombre.seek(0)
    archivoRankingNombre.truncate()
    for linea in listaRankingNombre:
        archivoRankingNombre.write(linea)
        archivoRankingNombre.write("\n")
    archivoRankingNombre.close()

    archivoRankingPuntos = open("ranking_puntos.txt","w")
    archivoRankingPuntos.seek(0)
    archivoRankingPuntos.truncate()
    for linea in listaRankingPuntos:
        archivoRankingPuntos.write(str(linea))
        archivoRankingPuntos.write("\n")
    archivoRankingPuntos.close()




def imprimirRankingMerecido(listaRankingNombre,listaRankingPuntos,screen,pos,nombreuser,puntos):
    font = pygame.font.Font(None, 30)  #Inicializar fuentes (para escribir)

    y = 100
    for r in range(len(listaRankingPuntos)):

        if r == pos:
            screen.blit(font.render("Pos: "+ str(r+1), 1, COLOR_LETRAS), (50,y))
            screen.blit(font.render(nombreuser[0:10], 1, COLOR_LETRAS), (200,y))
            screen.blit(font.render("       Puntos: " + str(puntos), 1, COLOR_LETRAS), (450,y))
            y = y + 30

        else:

            screen.blit(font.render("Pos: "+ str(r +1), 1, COLOR_LETRAS), (50,y))
            screen.blit(font.render(listaRankingNombre[r][0:10], 1, COLOR_LETRAS), (200,y))
            screen.blit(font.render("       Puntos: " + str(listaRankingPuntos[r]), 1, COLOR_LETRAS), (450,y))
            y = y + 30

def imprimirRanking(listaRankingNombre,listaRankingPuntos,screen):
    font = pygame.font.Font(None, 30)  #Inicializar fuentes (para escribir)

    y = 100
    for r in range(len(listaRankingPuntos)):



        screen.blit(font.render("Pos: "+ str(r +1), 1, COLOR_LETRAS), (50,y))
        screen.blit(font.render(listaRankingNombre[r][0:10], 1, COLOR_LETRAS), (200,y))
        screen.blit(font.render("       Puntos: " + str(listaRankingPuntos[r]), 1, COLOR_LETRAS), (450,y))
        y = y + 30

