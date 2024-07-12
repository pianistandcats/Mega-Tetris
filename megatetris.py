import pygame
import numpy as np
import time
from piezas import *
import random

pygame.init()

witdh, heigth = 700, 700
screen = pygame.display.set_mode((witdh,heigth))

bg = 25,25,25

screen.fill(bg)

nxC, nyC = 31,31

dimCW = witdh / nxC
dimCH = heigth / nyC


clock = pygame.time.Clock()
game_state = np.zeros((nxC+7,nyC+7))
pieza_state = np.zeros((nxC+7,nyC+7))

pieza = Pieza(np.array([15,0]), "t")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pieza.giro(game_state, nxC)
                print("Arriba")
        
    # Obtener el estado de todas las teclas
    keys = pygame.key.get_pressed()
    
    sleep_time = 0.3
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT]:
        # print("Izquierda")
        puede = True
        for esp in pieza.espacios:
            if game_state[esp[0] + pieza.posicion[0] -1, esp[1] + pieza.posicion[1]] == 1 or esp[0] + pieza.posicion[0] - 1 < 0:
                puede = False
                print("toca isquierda")
                break
            else:
                print(str(game_state[esp[0] + pieza.posicion[0] -1,0]), str([esp[0] + pieza.posicion[0] -1,0]))
            
        if puede:
            pieza.posicion[0] -= 1
    if keys[pygame.K_RIGHT]:
        # print("Derecha")
        puede = True
        for esp in pieza.espacios:
            if game_state[esp[0] + pieza.posicion[0] +1, esp[1] + pieza.posicion[1]] == 1 or esp[0] + pieza.posicion[0] + 1 >= nxC:
                puede = False
                print("toca derecha")
                break
            else:
                print(str(game_state[esp[0] + pieza.posicion[0]]), str([esp[0] + pieza.posicion[0],0]))
             
            
        if puede:
            pieza.posicion[0] += 1
        
    if keys[pygame.K_DOWN]:
        # print("Abajo")
        sleep_time = 0
    
    
    screen.fill(bg)
    time.sleep(sleep_time)
    pieza_state =  np.zeros((nxC+7,nyC+7))
    for pos in pieza.espacios:
        pieza_state[pos[0] + pieza.posicion[0],pos[1] + pieza.posicion[1]] = 1 
    
    for y in range(0, nxC):
        for x in range(0, nyC):
            
            poly = [((x)   * dimCW,    y    * dimCH),
                    ((x+1) * dimCW,    y    * dimCH),
                    ((x+1) * dimCW, (y + 1) * dimCH),
                    ((x)   * dimCW, (y + 1) * dimCH),]
            
            if game_state[x,y] == 1:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)
            elif pieza_state[x,y] == 1:
                if pieza.posicion[0] == x and pieza.posicion[1] == y:
                    pygame.draw.polygon(screen, (0,255,0), poly, 0)
                else:
                    pygame.draw.polygon(screen, (0,0,255), poly, 0)
            else:
                pygame.draw.polygon(screen, (50,50,50), poly, 1)
    
    if pieza.mover(game_state, nxC,nyC):
        for pos in pieza.espacios:
            game_state[pos[0] + pieza.posicion[0],pos[1] + pieza.posicion[1]] = 1
        pieza.posicion = np.array([15,0])
        pieza.tipo = get_all(piezas)[random.randint(0,6)]
        pieza.espacios = piezas[pieza.tipo]
        pieza.giros = 2
    
    pygame.display.flip()

    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()