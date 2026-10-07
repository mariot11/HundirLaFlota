import numpy as np
import BarcoClase as bc
from ResultadoDisparo import ResultadoDisparo

class Tablero:
    matriz = np.full((10, 10), ' ')

    lista_barcos = [bc.Barco(4), bc.Barco(3), bc.Barco(3), bc.Barco(2), bc.Barco(2), 
                        bc.Barco(2), bc.Barco(1), bc.Barco(1), bc.Barco(1), bc.Barco(1)]

    lista_indices = [(i , j) for i in range(10) for j in range(10)]

    dict_indices_barcos = {}
    dict_barcos_indices = {}

    def __init__(self):
        pass
    
    def colocar_barcos(self):
        for barco in self.lista_barcos:
            # colocar_barco(barco)
            pass

    def randomizar_posicion_barco(self, objeto_barco:object):
        colocado = False
        while not colocado:

            fila, colum = np.random.choice(self.lista_indices)
            orientaciones = ["N","S","E","O"]
            orientacion = np.random.choice(orientaciones)
            
            while (len(orientaciones) > 0):

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
                    if("O" not in self.matriz[fila-3 : fila+1, colum]):
                        self.matriz[fila-3 : fila+1, colum] = "O"
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila-3, fila+1)})
                        # self.dict_barcos_indices.update({objeto_barco:[(fila-3,colum)].append((f,colum) for f in range(fila-2,fila+1))})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila - 3, fila + 1)]})
                        colocado = True
            case "S":
                if (fila <= 6):
                    if("O" not in self.matriz[fila:fila+4,colum]):
                        self.matriz[fila:fila+4,colum] = "O"
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila, fila+4)})
                        colocado = True
            case "E":
                if (colum <= 6):
                    if("O" not in self.matriz[fila,colum:colum+4]):
                        self.matriz[fila,colum:colum+4] = "O"
                        self.dict_indices_barcos.update({(fila,c):objeto_barco for c in range(colum, colum+4)})
                        colocado = True
            case "O":
                if (colum >= 3):
                    if("O" not in self.matriz[fila, colum-3 : colum+1]):
                        self.matriz[fila, colum-3 : colum+1] = "O"
                        self.dict_indices_barcos.update({(fila,c):objeto_barco for c in range(colum-3, colum+1)})
                        colocado = True
        return colocado
    
    def disparar(self, fila:int, columna:int):
        casilla = self.matriz[fila, columna]
        if (casilla == "-") or (casilla.upper() == "X"):
            return "ocupado"
        elif casilla == " ":
            self.matriz[fila, columna] = "-"
            self.lista_indices.remove((fila,columna))
        elif casilla == "O":
            barco = self.indices_.get((fila, columna))
            resultado = barco.restar_vida()
            match resultado:
                case ResultadoDisparo.TOCADO:
                    self.matriz[fila, columna] = "x"
                case ResultadoDisparo.HUNDIDO:
                    pass
                    # ponerle X grandes a todo el barco