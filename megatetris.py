import pygame
import numpy as np
import time
from piezas import *
import random



pygame.init()


bg = 25,25,25

tamaño = 25

nxC, nyC = 10,20
witdh, heigth = nxC*tamaño, nyC*tamaño
screen = pygame.display.set_mode((witdh,heigth))
screen.fill(bg)



dimCW = witdh / nxC
dimCH = heigth / nyC


clock = pygame.time.Clock()
game_state = np.zeros((nxC+7,nyC+7))
pieza_state = np.zeros((nxC+7,nyC+7))

# for pos in range(nyC):
#     if pos != 0:
#         game_state[pos,nxC-1] = 1


pieza = Pieza(np.array([5,0]), "i")

# Variables de control
left_pressed = 0
right_pressed = 0
down_pressed = 0

velocidad = nxC
d_tiempo = 1

puntos = 0


def caer(v,d_tiempo):
    if pieza.mover(game_state, nxC,nyC):
        for pos in pieza.espacios:
            game_state[pos[0] + pieza.posicion[0],pos[1] + pieza.posicion[1]] = 1
        pieza.posicion = np.array([5,0])
        pieza.tipo = get_all(piezas)[random.randint(0,6)]
        pieza.espacios = piezas[pieza.tipo]
        pieza.giros = -1
        
    else:
        return v, d_tiempo

def mover(cuanto, direccion):
    puede = True
    if direccion == -1: 
        for esp in pieza.espacios:
            if game_state[esp[0] + pieza.posicion[0] -1, esp[1] + pieza.posicion[1]] == 1 or esp[0] + pieza.posicion[0] - 1 < 0:
                puede = False
                # print("toca isquierda")
                break
    elif direccion == 1: 
        for esp in pieza.espacios:
            if game_state[esp[0] + pieza.posicion[0] +1, esp[1] + pieza.posicion[1]] == 1 or esp[0] + pieza.posicion[0] + 1 >= nxC:
                puede = False
                # print("toca derecha")
                break
            
    if puede:
        pieza.posicion[0] += cuanto

def eliminar_lineas():
    for i in range(nyC):
        if False in game_state[0:nxC,i+1]:
            pass
            # print(str(game_state[0:nxC,i+1]) + " " + str(i))
        else:
            g = game_state[0:nxC,i+1].copy()
            # print(g)
            # print(game_state[0:nxC,i+1])
            for c in range(3):
                game_state[0:nxC,i+1] = 0
                actualizar_grafico()
                pygame.display.flip()
                
                time.sleep(0.3)
                game_state[0:nxC,i+1] = g
                # print(game_state[0:nxC,i+1])

                actualizar_grafico()
                pygame.display.flip()
                
                time.sleep(0.3)
            game_state[0:nxC,i+1] = 0
            actualizar_grafico()
            pygame.display.flip()
            
            for y in range(i, 0,-1):
                game_state[0:nxC,y+1] = game_state[0:nxC,y]
            
            puntos += 100
            print(f"Puntuacion: {puntos}")

def actualizar_grafico():
    screen.fill(bg)
    for y in range(0, nyC):
        for x in range(0, nxC):
            
            poly = [((x)   * tamaño,    y    * tamaño),
                    ((x+1) * tamaño,    y    * tamaño),
                    ((x+1) * tamaño, (y + 1) * tamaño),
                    ((x)   * tamaño, (y + 1) * tamaño),]
            
            if game_state[x,y] == 1:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)
            elif pieza_state[x,y] == 1:
                # if pieza.posicion[0] == x and pieza.posicion[1] == y:
                #     pygame.draw.polygon(screen, (0,255,0), poly, 0)
                # else:
                #     pygame.draw.polygon(screen, (0,0,255), poly, 0)
                pygame.draw.polygon(screen, (0,255,0), poly, 0)
            
            else:
                pygame.draw.polygon(screen, (50,50,50), poly, 1)

ciclos = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pieza.giro(game_state, nxC)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = 0
            if event.key == pygame.K_RIGHT:
                right_pressed = 0
            if event.key == pygame.K_DOWN:
                down_pressed = 0
                
    # Obtener el estado de todas las teclas
    keys = pygame.key.get_pressed()
    
    sleep_time = 0.05 / d_tiempo
    
    if keys[pygame.K_ESCAPE]:
        running = False
        
    if keys[pygame.K_LEFT]:
        left_pressed += 1
        
    if keys[pygame.K_RIGHT]:
        right_pressed += 1
        
    if keys[pygame.K_DOWN]:
        down_pressed += 1
    
    # umbral = round((d_tiempo/1.3) +1)
    # if umbral > 10:
    #     umbral = 10
    umbral = 6
    
        
    # print(f"umbral de: {umbral}")
    
    if left_pressed == 1 or left_pressed > umbral:
        mover(-1,-1)
    if right_pressed == 1 or right_pressed > umbral:
        mover(1,1)
    if down_pressed == 1 or down_pressed > umbral:
        caer(velocidad,d_tiempo)
    
    time.sleep(sleep_time)
    pieza_state =  np.zeros((nxC+7,nyC+7))
    for pos in pieza.espacios:
        pieza_state[pos[0] + pieza.posicion[0],pos[1] + pieza.posicion[1]] = 1 
    
    actualizar_grafico()
    
    if ciclos % velocidad == 0:
        caer(velocidad,d_tiempo)
    
    eliminar_lineas()

    pygame.display.flip()
    
    clock.tick(60)  # Limitar a 60 FPS
    ciclos +=1

pygame.quit()