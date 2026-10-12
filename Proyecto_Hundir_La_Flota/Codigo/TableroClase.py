import numpy as np
import BarcoClase as bc
from ResultadoDisparo import ResultadoDisparo

class Tablero:

    def __init__(self):
        # Esta es la matriz en la que pondremos los barcos
        self.matriz = np.full((10, 10), ' ')

        # lista para posicionar los barcos y comprobar si se ha ganado
        self.lista_barcos = np.array([bc.Barco(4), bc.Barco(3), bc.Barco(3), bc.Barco(2), bc.Barco(2), 
                                bc.Barco(2), bc.Barco(1), bc.Barco(1), bc.Barco(1), bc.Barco(1)])
        
        # lista de índices para sacar posiciones de forma aleatoria
        self.lista_indices_colocacion = [(i , j) for i in range(10) for j in range(10)]
        self.lista_indices_disparos = [(i , j) for i in range(10) for j in range(10)]

        # diccionarios para acceder a los barcos mediante los índices y a los índices de cada barco
        self.dict_indices_barcos = {}
        self.dict_barcos_indices = {}

        pass
    
    def colocar_barcos(self, index:int = 0):
        # recorre la lista de barcos e intenta colocarlos en el tablero de forma aleatoria
        for index in range(index, len(self.lista_barcos)):
            self.randomizar_posicion_barco(self.lista_barcos[index])
        return True

    def randomizar_posicion_barco(self, objeto_barco:object):
        # variable de parada del bucle
        colocado = False
        
        while not colocado:
            # elegimos una posición que no haya sido seleccionada antes
            indx = np.random.choice(len(self.lista_indices_colocacion))
            fila, colum = self.lista_indices_colocacion[indx]
            orientaciones = ["N","S","E","O"]
            
            # mientras queden orientaciones posibles por probar se ejecuta este bucle
            
            while (len(orientaciones) > 0):
                
                orientacion = np.random.choice(orientaciones)
                
                if self.intentar_colocar_barco(objeto_barco, fila, colum, orientacion):
                    # si ha podido colocar el barco, elimina la posición de la lista de coordenadas posibles y sale del bucle
                    self.lista_indices_colocacion.remove((fila,colum))
                    colocado = True
                    break
                
                else:
                    # Si no ha podido colocar el barco en esa orientación, la elimina del pool de orientaciones y vuelve a comprobar con otra
                    orientaciones.remove(orientacion)
        
        return colocado

    
    def intentar_colocar_barco(self, objeto_barco:object, fila:int, colum:int, orientacion:str):
        colocado = False
        longitud_barco = objeto_barco.longitud
        
        match orientacion:
            case "N":
                # si el barco cabe en la matriz
                if (fila >= longitud_barco-1):
                    fila_inicio =  fila-longitud_barco+1 

                    if not(np.isin(["O","~"], self.matriz[fila_inicio : fila+1, colum]).any()):                       
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila_inicio - 1), min(len(self.matriz), fila + 2)
                        c_min, c_max = max(0, colum - 1), min(len(self.matriz[0]), colum + 2)
                        
                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # pinta el barco
                        self.matriz[fila_inicio : fila + 1, colum] = "O"
                        
                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila_inicio, fila+1)})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila_inicio, fila + 1)]})
                        colocado = True

            case "S":
                # si el barco cabe en la matriz
                if (fila <= len(self.matriz) - longitud_barco):
                    fila_final = fila + longitud_barco

                    if not(np.isin(["O","~"], self.matriz[fila : fila_final, colum]).any()):
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila - 1), min(len(self.matriz), fila_final + 1)
                        c_min, c_max = max(0, colum - 1), min(len(self.matriz[0]), colum + 2)

                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # pinta el barco
                        self.matriz[fila:fila_final,colum] = "O"

                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila, fila_final,)})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila, fila_final,)]})
                        colocado = True
            case "E":
                # Si el barco cabe en la matriz
                if colum <= len(self.matriz[0]) - longitud_barco:
                    colum_final = colum + longitud_barco

                    if not np.isin(["O", "~"], self.matriz[fila, colum : colum_final]).any():
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila - 1), min(len(self.matriz), fila + 2)
                        c_min, c_max = max(0, colum - 1), min(len(self.matriz[0]), colum_final + 1)

                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # Pinta el barco
                        self.matriz[fila, colum : colum_final] = "O"

                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(fila, c): objeto_barco for c in range(colum, colum_final)})
                        self.dict_barcos_indices.update({objeto_barco: [(fila, c) for c in range(colum, colum_final)]})
                        colocado = True
            case "O":
                # Si el barco cabe en la matriz
                if colum >= longitud_barco - 1:
                    colum_inicio = colum - longitud_barco + 1

                    if not np.isin(["O", "~"], self.matriz[fila, colum_inicio : colum + 1]).any():
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila - 1), min(len(self.matriz), fila + 2)
                        c_min, c_max = max(0, colum_inicio - 1), min(len(self.matriz[0]), colum + 2)

                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # Pinta el barco
                        self.matriz[fila, colum_inicio : colum + 1] = "O"

                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(fila, c): objeto_barco for c in range(colum_inicio, colum + 1)})
                        self.dict_barcos_indices.update({objeto_barco: [(fila, c) for c in range(colum_inicio, colum + 1)]})
                        colocado = True
            case _:
                raise ValueError("El valor de la orientación debe ser 'N, S, E u O'")
        return colocado
    
    def disparar(self, fila:int, colum:int):
        has_ganado = False
        casilla = self.matriz[fila, colum]
        if (casilla == "-") or (casilla.upper() == "X"):
            return "ocupado"
        elif casilla == " ":
            self.matriz[fila, colum] = "-"
            self.lista_indices_disparos.remove((fila,colum))
        elif casilla == "O":
            barco = self.indices_.get((fila, colum))
            resultado = barco.restar_vida()
            match resultado:
                case ResultadoDisparo.TOCADO:
                    self.matriz[fila, colum] = "x"
                case ResultadoDisparo.HUNDIDO:
                    lista_indices_barco = np.array(self.dict_barcos_indices.get(self.dict_indices_barcos.get((fila,colum))))
                    f,c = np.column_stack(lista_indices_barco)
                    self.matriz[f,c] = "X"
                    barcos_hundidos = sum(1 for b in self.lista_barcos if b.esta_hundido())
                    if(barcos_hundidos == len(self.lista_barcos)):
                        has_ganado = True
        return has_ganado

    def print_tablero(self):
        print(self.matriz)

    def print_tablero_enemigo(self):
        print(np.where((self.matriz == "~") | (self.matriz == "O"), " ", self.matriz))
