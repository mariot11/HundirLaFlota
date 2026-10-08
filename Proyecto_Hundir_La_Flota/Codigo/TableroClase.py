import numpy as np
import BarcoClase as bc
from ResultadoDisparo import ResultadoDisparo

class Tablero:
    matriz = np.full((10, 10), ' ')

    lista_barcos = np.array([bc.Barco(4), bc.Barco(3), bc.Barco(3), bc.Barco(2), bc.Barco(2), 
                        bc.Barco(2), bc.Barco(1), bc.Barco(1), bc.Barco(1), bc.Barco(1)])

    lista_indices = [(i , j) for i in range(10) for j in range(10)]

    dict_indices_barcos = {}
    dict_barcos_indices = {}

    def __init__(self):
        pass
    
    def colocar_barcos(self):
        for barco in self.lista_barcos:
            self.randomizar_posicion_barco(barco)

    def randomizar_posicion_barco(self, objeto_barco:object):
        colocado = False
        while not colocado:

            indx = np.random.choice(len(self.lista_indices))
            fila, colum = self.lista_indices[indx]
            orientaciones = ["N","S","E","O"]
            
            while (len(orientaciones) > 0):
                orientacion = np.random.choice(orientaciones)
                if self.intentar_colocar_barco(objeto_barco, fila, colum, orientacion):
                    self.lista_indices.remove((fila,colum))
                    colocado = True
                    break
                
                else:
                    orientaciones.remove(orientacion)

    
    def intentar_colocar_barco(self, objeto_barco:object, fila:int, colum:int, orientacion:str):
        colocado = False

        match orientacion:
            case "N":
                if (fila >= 3):
                    # if not(np.isin(["O","~"], self.matriz[fila-3 : fila+1, colum]).any()):
                    if("O" not in self.matriz[fila-3 : fila+1, colum]):
                        self.matriz[fila-3 : fila+1, colum] = "O"
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila-3, fila+1)})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila - 3, fila + 1)]})
                        colocado = True
            case "S":
                if (fila <= 6):
                    if("O" not in self.matriz[fila:fila+4,colum]):
                        self.matriz[fila:fila+4,colum] = "O"
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila, fila+4)})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila, fila + 4)]})
                        colocado = True
            case "E":
                if (colum <= 6):
                    if("O" not in self.matriz[fila,colum:colum+4]):
                        self.matriz[fila,colum:colum+4] = "O"
                        self.dict_indices_barcos.update({(fila,c):objeto_barco for c in range(colum, colum+4)})
                        self.dict_barcos_indices.update({objeto_barco: [(fila, c) for c in range(colum, colum + 4)]})
                        colocado = True
            case "O":
                if (colum >= 3):
                    if("O" not in self.matriz[fila, colum-3 : colum+1]):
                        self.matriz[fila, colum-3 : colum+1] = "O"
                        self.dict_indices_barcos.update({(fila,c):objeto_barco for c in range(colum-3, colum+1)})
                        self.dict_barcos_indices.update({objeto_barco: [(fila, c) for c in range(colum - 3, colum + 1)]})
                        colocado = True
        return colocado
    
    def disparar(self, fila:int, colum:int):
        has_ganado = False
        casilla = self.matriz[fila, colum]
        if (casilla == "-") or (casilla.upper() == "X"):
            return "ocupado"
        elif casilla == " ":
            self.matriz[fila, colum] = "-"
            self.lista_indices.remove((fila,colum))
        elif casilla == "O":
            barco = self.indices_.get((fila, colum))
            resultado = barco.restar_vida()
            match resultado:
                case ResultadoDisparo.TOCADO:
                    self.matriz[fila, colum] = "x"
                case ResultadoDisparo.HUNDIDO:
                    lista_indices = np.array(self.dict_barcos_indices.get(self.dict_indices_barcos.get((fila,colum))))
                    f,c = np.column_stack(lista_indices)
                    self.matriz[f,c] = "X"
                    barcos_hundidos = sum(1 for b in self.lista_barcos if b.esta_hundido())
                    if(barcos_hundidos == len(self.lista_barcos)):
                        has_ganado = True
        return has_ganado

    def print_tablero(self):
        print(self.matriz)
