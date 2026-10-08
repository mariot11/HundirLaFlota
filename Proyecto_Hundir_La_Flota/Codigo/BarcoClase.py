import numpy as np
from ResultadoDisparo import ResultadoDisparo

# orientaciones = ["N","S","E","O"]

class Barco:
    '''
    Si no le pasas una posición y una orientación, estas se calculan aleatoriamente
    '''
    def __init__(self, longitud:int, coordenada_fila:int = None, coordenada_colum:int = None, orientacion:str = None):
        self.longitud = longitud
        self.vida = longitud
        self.posicion_fila = coordenada_fila
        self.posicion_colum = coordenada_colum
        self.orientacion = orientacion

    def restar_vida(self):
        if self.vida == 0:
            return ResultadoDisparo.FALLO
        else:
            self.vida -= 1
            if self.vida > 0:
                return ResultadoDisparo.TOCADO
            elif self.vida == 0:
                return ResultadoDisparo.HUNDIDO

    def esta_hundido(self):
        if self.vida == 0:
            return True
        return False        
        