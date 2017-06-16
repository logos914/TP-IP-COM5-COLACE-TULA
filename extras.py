import pygame
from pygame.locals import *
from configuracion import *

def dameLetraApretada(key):
    if key == K_a:
        return("a")
    elif key == K_b:
        return("b")
    elif key == K_c:
        return("c")
    elif key == K_d:
        return("d")
    elif key == K_e:
        return("e")
    elif key == K_f:
        return("f")
    elif key == K_g:
        return("g")
    elif key == K_h:
        return("h")
    elif key == K_i:
        return("i")
    elif key == K_j:
        return("j")
    elif key == K_k:
        return("k")
    elif key == K_l:
        return("l")
    elif key == K_m:
        return("m")
    elif key == K_n:
        return("n")
    elif key == K_o:
        return("o")
    elif key == K_p:
        return("p")
    elif key == K_q:
        return("q")
    elif key == K_r:
        return("r")
    elif key == K_s:
        return("s")
    elif key == K_t:
        return("t")
    elif key == K_u:
        return("u")
    elif key == K_v:
        return("v")
    elif key == K_w:
        return("w")
    elif key == K_x:
        return("x")
    elif key == K_y:
        return("y")
    elif key == K_z:
        return("z")
    elif key == K_SPACE:
       return(" ")
    elif key == K_1:
       return("1")
    else:
        return("")

def dibujar(letrasEnPantalla, posX, posY, candidata, palabra, ayuda, segundos, t0, t1, screen, puntos):
    font = pygame.font.Font(None, 30)
    for i in range(len(letrasEnPantalla)):
                screen.blit(font.render(letrasEnPantalla[i],0,(255,100,0),COLOR_FONDO),(posX[i], posY[i]))

    for i in range(len(candidata)):
            screen.blit(font.render(candidata[i], 1, COLOR_LETRAS), (250+20*2*i,560))
    for i in range(len(palabra)):
            screen.blit(font.render("_", 1, (200,255,0)), (250+20*2*i,570))

    screen.blit(font.render(ayuda, 1, COLOR_LETRAS), (340,10))
    pygame.draw.line(screen, (255,255,255), (0, ALTO-70) , (ANCHO, ALTO-70), 5)

    ren4 = font.render("Tiempo: " + str(int(segundos)), 1, (80, 200, 40))
    ren5 = font.render("Ayuda: ", 1, (180, 200, 40))
    ren6 = font.render("Puntos: " + str(puntos), 1, COLOR_PUNTOS)

    #letras que saca de pantalla y ubica sobre los guiones
    if(t1-t0>=6):
            posX[0]=250
            posY[0]=UBIC_AYUDA_Y

    if(t1-t0>=12):
            ren2 = ren4 = font.render("Tiempo: " + str(int(segundos)), 1, (255, 255, 0))
            posX[1]=290
            posY[1]=UBIC_AYUDA_Y

    #saca de los margenes
    if(t1-t0>=15):
            for i in range(len(posX)):
                posX[i]=POS_OCULTA
                posY[i]=POS_OCULTA
    if(int(segundos<5)):
        ren4 = font.render("Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL)

    screen.blit(ren4, (10, 10))
    screen.blit(ren5, (250, 10))
    screen.blit(ren6, (650, 10))