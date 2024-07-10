import numpy as np

class Pieza:
    def __init__(self, posicion, tipo):
        self.posicion = posicion
        self.espacios = piezas[tipo]
        self.tipo = tipo
    
    def mover(self, estado, tx,ty):
        puede = True
        for pos in self.espacios:
            if estado[pos[0] + self.posicion[0], pos[1] + self.posicion[1] + 1] == 1:
                puede = False
                break

        if puede:
            if self.posicion[1] < ty-1:
                self.posicion[1] += 1
                return False
            elif self.posicion[1] == ty-1:
                print("piso")
                return True
        else:
            print("pieza")
            return True
            
        
piezas = {
    "t": [np.array([0,0]),np.array([1,0]),np.array([-1,0]),np.array([0,-1])]
}