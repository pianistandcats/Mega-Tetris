import pygame
import numpy as np
import time
from piezas import *

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
    
    screen.fill(bg)
    time.sleep(0.1)
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
                pygame.draw.polygon(screen, (0,0,255), poly, 0)
            else:
                pygame.draw.polygon(screen, (50,50,50), poly, 1)
    
    if pieza.mover(game_state, nxC,nyC):
        for pos in pieza.espacios:
            game_state[pos[0] + pieza.posicion[0],pos[1] + pieza.posicion[1]] = 1
        pieza.posicion = np.array([15,0])
    
    pygame.display.flip()

    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()