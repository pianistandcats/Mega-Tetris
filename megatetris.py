import pygame
import numpy as np
import time
from piezas import *
import random

import os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

clear()

class Tablero:
    def __init__(self, tamaño_x = 10, tamaño_y = 20, tamaño_cuadrado = 20, c_fondo = [(25,25,25)]):
        self.tamaño = tamaño_cuadrado
        self.tx, self.ty = 10,20
        
        self.witdh, self.heigth = tamaño_x*tamaño_cuadrado, tamaño_y*tamaño_cuadrado
        
        self.screen = pygame.display.set_mode((self.witdh,self.heigth))
        self.screen.fill(c_fondo[0]) 
        self.bg = c_fondo
        
        

class Game:
    def __init__(self, tablero):
        self.tablero = tablero
        self.game_state = np.zeros((self.tablero.tx+7,self.tablero.ty+7))
        self.pieza_state = np.zeros((self.tablero.tx+7,self.tablero.ty+7))
        
        self.pieza = Pieza(np.array([5,0]), "i")
        
        self.nivel = 1
        self.lineas_eliminadas = 0
        self.velocidad = self.tablero.tx
        self.d_tiempo = 1
        self.puntos = 00
        
        self.piezas_desordenadas = []
    
    def desordenar_piezas(self):
        self.piezas_desordenadas.clear()
        orden = []
        
        
        for index,valor in enumerate(piezas):
            numero = random.randint(0,len(piezas)-1)
            while numero in orden:
                numero = random.randint(0,len(piezas)-1)
            orden.append(numero)
        
        li = []
        # print(f"{orden}")
        
        for index,valor in enumerate(orden):
            n = orden[index]
            # print(n)
            li.append(get_all(piezas)[n])
        
        # print(f"{li}")
        self.piezas_desordenadas = li
           
    def actualizar_grafico(self):
        self.tablero.screen.fill(self.tablero.bg[(self.nivel - 1) % len(self.tablero.bg)])
        for y in range(0, self.tablero.ty):
            for x in range(0, self.tablero.tx):
                
                poly = [((x)   * self.tablero.tamaño,    y    * self.tablero.tamaño),
                        ((x+1) * self.tablero.tamaño,    y    * self.tablero.tamaño),
                        ((x+1) * self.tablero.tamaño, (y + 1) * self.tablero.tamaño),
                        ((x)   * self.tablero.tamaño, (y + 1) * self.tablero.tamaño),]
                
                if self.game_state[x,y] == 1:
                    pygame.draw.polygon(self.tablero.screen, (255,255,255), poly, 0)
                    
                elif self.pieza_state[x,y] == 1:
                    pygame.draw.polygon(self.tablero.screen, (0,255,0), poly, 0)
                
                else:
                    pygame.draw.polygon(self.tablero.screen, (50,50,50), poly, 1)
                    
    def eliminar_lineas(self):
        lineas_copletadas = 0
        for i in range(self.tablero.ty):
            if False in self.game_state[0:self.tablero.tx,i+1]:
                pass
                # print(str(game_state[0:nxC,i+1]) + " " + str(i))
            else:
                lineas_copletadas += 1
                g = self.game_state[0:self.tablero.tx,i+1].copy()
                # print(g)
                # print(game_state[0:nxC,i+1])
                for c in range(3):
                    self.game_state[0:self.tablero.tx,i+1] = 0
                    self.actualizar_grafico()
                    pygame.display.flip()
                    
                    time.sleep(0.3)
                    self.game_state[0:self.tablero.tx,i+1] = g
                    # print(game_state[0:nxC,i+1])

                    self.actualizar_grafico()
                    pygame.display.flip()
                    
                    time.sleep(0.3)
                self.game_state[0:self.tablero.tx,i+1] = 0
                self.actualizar_grafico()
                pygame.display.flip()
                
                for y in range(i, 0,-1):
                    self.game_state[0:self.tablero.tx,y+1] = self.game_state[0:self.tablero.tx,y]
                
                self.puntos += 100 + (100 * (lineas_copletadas -1) / 2)
                self.lineas_eliminadas += 1
                

                
                if self.puntos >= 1000 * self.nivel:
                   self.pasar_de_nivel() 
                    
                
    def pasar_de_nivel(self):
        self.nivel += 1
                    
        if self.nivel < 4:
            self.velocidad  /= self.nivel /2
            self.velocidad  = round(self.velocidad)
                        
            self.d_tiempo  *= self.nivel / 2
        else:
            self.velocidad  /= self.nivel /4
            self.velocidad  = round(self.velocidad)+1
                        
            self.d_tiempo  *= self.nivel / 2
        clear()
        print(f"Puntos: {self.puntos}")
        print(f"Linas eliminadas totales: {self.lineas_eliminadas}")
        print(f"Nivel: {self.nivel}")
                



pygame.init()
tablero = Tablero(10,20,25,[(25,25,25),(25,45,25),(25,25,45),(45,25,25)])
game = Game(tablero)

clock = pygame.time.Clock()

# Variables de control
left_pressed = 0
right_pressed = 0
down_pressed = 0


game.desordenar_piezas()
ciclos = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.pieza.giro(game.game_state, game.tablero.tx)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = 0
            if event.key == pygame.K_RIGHT:
                right_pressed = 0
            if event.key == pygame.K_DOWN:
                down_pressed = 0
            if event.key == pygame.K_0:
                game.pasar_de_nivel()
            
                
    # Obtener el estado de todas las teclas
    keys = pygame.key.get_pressed()
    
    sleep_time = 0.05 / game.d_tiempo
    
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
        game.pieza.mover_horizontal(game,-1,-1)
    if right_pressed == 1 or right_pressed > umbral:
        game.pieza.mover_horizontal(game,1,1)
    if down_pressed == 1 or down_pressed > umbral:
        game.pieza.caer(game)
    
    time.sleep(sleep_time)
    game.pieza_state =  np.zeros((game.tablero.tx+7,game.tablero.ty+7))
    for pos in game.pieza.espacios:
        game.pieza_state[pos[0] + game.pieza.posicion[0],pos[1] + game.pieza.posicion[1]] = 1 
    
    game.actualizar_grafico()
    
    if ciclos % (game.velocidad) == 0:
        game.pieza.caer(game)
    
    game.eliminar_lineas()

    pygame.display.flip()
    
    clock.tick(60)  # Limitar a 60 FPS
    ciclos +=1
    
pygame.quit()