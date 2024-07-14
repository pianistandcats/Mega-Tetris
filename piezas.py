import numpy as np

class Pieza:
    def __init__(self, posicion, tipo):
        self.posicion = posicion
        self.espacios = piezas[tipo]
        self.tipo = tipo
        self.giros = -1
    
    def giro(self, game_state, nxC):
        espacios2 = []
        if self.tipo == "o":
            return
        elif self.tipo == "i":
            for num in range(4):
                # print(range(4))
                # print(self.giros)
                new_espace = giros_i[self.giros+1][num]
                    
                print(f"mandioca {self.giros}")
                    
                espacios2.append(new_espace)
                if game_state[new_espace[0] + self.posicion[0], new_espace[1] + self.posicion[1]] == 1 or new_espace[0] + self.posicion[0] < 0:
                    return
                elif game_state[new_espace[0] + self.posicion[0], new_espace[1] + self.posicion[1]] == 1 or new_espace[0] + self.posicion[0] >= nxC:
                    return
            
        else:
            for esp in self.espacios:
                new_espace = np.array([0,0])
                    
                new_espace[1] = esp[0]
                new_espace[0] = esp[1] *-1
                
                espacios2.append(new_espace)
                if game_state[new_espace[0] + self.posicion[0], new_espace[1] + self.posicion[1]] == 1 or new_espace[0] + self.posicion[0] < 0:
                    return
                elif game_state[new_espace[0] + self.posicion[0], new_espace[1] + self.posicion[1]] == 1 or new_espace[0] + self.posicion[0] >= nxC:
                    return
                
        if self.giros != 2:
            self.giros += 1
            print(self.giros)
        else:
            self.giros = -1
            print(self.giros)
            
        
        self.espacios = espacios2
    
    def mover(self, estado, tx,ty):
        puede = True
        for pos in self.espacios:
            if estado[pos[0] + self.posicion[0], pos[1] + self.posicion[1] + 1] == 1 or pos[1] + self.posicion[1] + 1 >= ty:
                puede = False
                break
        
        if puede:
            if pos[1] + self.posicion[1] + 1 < ty:
                self.posicion[1] += 1
                return False
            elif pos[1] + self.posicion[1] + 1 >= ty:
                print("piso")
                return True
        else:
            print("pieza")
            return True
            
        
piezas = {
    "t": [np.array([0,0]),np.array([1,0]),np.array([-1,0]),np.array([0,-1])],
    "L": [np.array([0,0]),np.array([1,1]),np.array([0,-1]),np.array([0,1])],
    "Lin": [np.array([0,0]),np.array([-1,1]),np.array([0,-1]),np.array([0,1])],
    "i": [np.array([-1,2]),np.array([-1,1]),np.array([-1,0]),np.array([-1,-1])],
    "s": [np.array([0,0]),np.array([0,1]),np.array([1,0]),np.array([-1,1])],
    "z": [np.array([0,0]),np.array([0,-1]),np.array([1,0]),np.array([1,1])],
    "o": [np.array([0,0]),np.array([1,0]),np.array([0,1]),np.array([1,1])],
}

giros_i = [
    [np.array([-1,2]),np.array([-1,1]),np.array([-1,0]),np.array([-1,-1])],
    [np.array([-2,0]),np.array([-1,0]),np.array([0,0]),np.array([1,0])],
    [np.array([0,2]),np.array([0,1]),np.array([0,0]),np.array([0,-1])],
    [np.array([-2,1]),np.array([-1,1]),np.array([0,1]),np.array([1,1])],
    
]


def get_all(dict):
    todos = []
    for key, value in dict.items():
        todos.append(key)
    return todos