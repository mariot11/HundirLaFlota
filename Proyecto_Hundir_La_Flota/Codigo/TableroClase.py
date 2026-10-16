import numpy as np
import BarcoClase as bc
from ResultadoDisparo import ResultadoDisparo

class Tablero:

    def __init__(self):
        # Esta es la matriz en la que pondremos los barcos
        self.matriz = np.full((10, 10), '□')

        # lista para posicionar los barcos y comprobar si se ha ganado
        self.lista_barcos = np.array([bc.Barco(4), bc.Barco(3), bc.Barco(3), bc.Barco(2), bc.Barco(2), 
                                bc.Barco(2), bc.Barco(1), bc.Barco(1), bc.Barco(1), bc.Barco(1)])
        
        # lista de índices para sacar posiciones de forma aleatoria
        self.lista_indices_colocacion = [(i , j) for i in range(10) for j in range(10)]
        self.lista_indices_disparos = [(i , j) for i in range(10) for j in range(10)]

        # diccionarios para acceder a los barcos mediante los índices y a los índices de cada barco
        self.dict_indices_barcos = {}
        self.dict_barcos_indices = {}

        # Lista de casillas adyacentes para la IA del rival
        self.lista_adyacentes = []
        self.ultimo_tocado = []

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

                    if not(np.isin(["▲","~"], self.matriz[fila_inicio : fila+1, colum]).any()):                       
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila_inicio - 1), min(len(self.matriz), fila + 2)
                        c_min, c_max = max(0, colum - 1), min(len(self.matriz[0]), colum + 2)
                        
                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # pinta el barco
                        self.matriz[fila_inicio : fila + 1, colum] = "▲"
                        
                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila_inicio, fila+1)})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila_inicio, fila + 1)]})
                        colocado = True

            case "S":
                # si el barco cabe en la matriz
                if (fila <= len(self.matriz) - longitud_barco):
                    fila_final = fila + longitud_barco

                    if not(np.isin(["▲","~"], self.matriz[fila : fila_final, colum]).any()):
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila - 1), min(len(self.matriz), fila_final + 1)
                        c_min, c_max = max(0, colum - 1), min(len(self.matriz[0]), colum + 2)

                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # pinta el barco
                        self.matriz[fila:fila_final,colum] = "▲"

                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(f,colum):objeto_barco for f in range(fila, fila_final,)})
                        self.dict_barcos_indices.update({objeto_barco: [(f, colum) for f in range(fila, fila_final,)]})
                        colocado = True
            case "E":
                # Si el barco cabe en la matriz
                if colum <= len(self.matriz[0]) - longitud_barco:
                    colum_final = colum + longitud_barco

                    if not np.isin(["▲", "~"], self.matriz[fila, colum : colum_final]).any():
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila - 1), min(len(self.matriz), fila + 2)
                        c_min, c_max = max(0, colum - 1), min(len(self.matriz[0]), colum_final + 1)

                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # Pinta el barco
                        self.matriz[fila, colum : colum_final] = "▲"

                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(fila, c): objeto_barco for c in range(colum, colum_final)})
                        self.dict_barcos_indices.update({objeto_barco: [(fila, c) for c in range(colum, colum_final)]})
                        colocado = True
            case "O":
                # Si el barco cabe en la matriz
                if colum >= longitud_barco - 1:
                    colum_inicio = colum - longitud_barco + 1

                    if not np.isin(["▲", "~"], self.matriz[fila, colum_inicio : colum + 1]).any():
                        # calcula los valores máximos y mínimos para pintar el barco y los márgenes
                        f_min, f_max = max(0, fila - 1), min(len(self.matriz), fila + 2)
                        c_min, c_max = max(0, colum_inicio - 1), min(len(self.matriz[0]), colum + 2)

                        # pinta las casillas de margen alrededor del barco
                        self.matriz[f_min : f_max, c_min : c_max] = "~"

                        # Pinta el barco
                        self.matriz[fila, colum_inicio : colum + 1] = "▲"

                        # actualiza diccionarios
                        self.dict_indices_barcos.update({(fila, c): objeto_barco for c in range(colum_inicio, colum + 1)})
                        self.dict_barcos_indices.update({objeto_barco: [(fila, c) for c in range(colum_inicio, colum + 1)]})
                        colocado = True
            case _:
                raise ValueError("El valor de la orientación debe ser 'N, S, E u O'")
        return colocado

    def disparar_aleatoriamente(self):
        # elige una posición aleatoria de la lista de posibles coordenadas para disparar
        indx_disparos = np.random.choice(len(self.lista_indices_disparos))
        fila, colum = self.lista_indices_disparos[indx_disparos]
        has_ganado, resultado  = self.disparar(fila, colum)

        #Si el resultado del disparo es un barco enemigo tocado, se actualiza la array de posiciones adyacentes
        if resultado == ResultadoDisparo.TOCADO:
            self.ultimo_tocado = [fila, colum]
            for i in [-1, 1]:
                if (fila +i, colum) in self.lista_indices_disparos:
                    self.lista_adyacentes.append((fila +i, colum))
            for j in [-1, 1]:
                if (fila, colum + j) in self.lista_indices_disparos:
                    self.lista_adyacentes.append((fila, colum + j))
        
        return(has_ganado, resultado, (fila, colum))

    def disparar_enemigo(self):
        # Si no hay adyacentes (no hay un barco tocado) hacer un disparo aleatorio normal
        if len(self.lista_adyacentes) == 0:
            has_ganado, resultado, coordenadas = self.disparar_aleatoriamente()
            return (has_ganado, resultado, coordenadas)
        # En caso contrario disparar aleatoriamente en una de las posiciones adyacentes
        else:
            index = np.random.choice(range(len(self.lista_adyacentes)))
            fila, colum = self.lista_adyacentes[index]
            has_ganado, resultado = self.disparar(fila, colum)
            self.lista_adyacentes.pop(index)

            # Si has hundido el barco, se reinicia todo para volver a realizar disparos aleatorios normales
            if resultado == ResultadoDisparo.HUNDIDO:
                self.lista_adyacentes = []
                self.ultimo_tocado = []

            # Si hemos vuelto a darle al barco se calcula la dirección del barco
            elif resultado == ResultadoDisparo.TOCADO:
                diff_fila = fila - self.ultimo_tocado[0]
                diff_colum = colum - self.ultimo_tocado[1]
                
                # Forzamos con np.sign a que el paso sea siempre -1, 0 o 1 exacto
                eje_barco = (int(np.sign(diff_fila)), int(np.sign(diff_colum)))

                if eje_barco[0] != 0:  # Movimiento horizontal
                    self.lista_adyacentes = [pos for pos in self.lista_adyacentes if pos[1] == colum]
                elif eje_barco[1] != 0:  # Movimiento vertical
                    self.lista_adyacentes = [pos for pos in self.lista_adyacentes if pos[0] == fila]

                # Actualizar la lista de adyacentes sabiendo la orientación del barco
                for i in [-1, 1]:
                    nueva_fila = fila + (eje_barco[0] * i)
                    nueva_colum = colum + (eje_barco[1] * i)
                    nueva_casilla = (nueva_fila, nueva_colum)
                    
                    if nueva_casilla in self.lista_indices_disparos:
                        if nueva_casilla not in self.lista_adyacentes:
                            self.lista_adyacentes.append(nueva_casilla)
                
                self.ultimo_tocado = [fila, colum]
                
            return (has_ganado, resultado, (fila, colum))

    
    def disparar(self, fila:int, colum:int):
        has_ganado = False
        resultado = ResultadoDisparo.ERROR
        casilla = self.matriz[fila, colum]

        #Si es una casilla a la que ya habíamos disparado, devuelve un error
        if (casilla == "⊞") or (casilla == "◐") or (casilla == "●"):
            raise Exception("Esta casilla ya había recibido un disparo previamente")

        #Si disparas al agua
        elif (casilla == "□") or (casilla == "~"):
            resultado = ResultadoDisparo.AGUA
            self.matriz[fila, colum] = "⊞"

        #Si disparas a un barco
        elif casilla == "▲":
            barco = self.dict_indices_barcos.get((fila, colum))
            resultado = barco.restar_vida()
            
            match resultado:
                
                case ResultadoDisparo.TOCADO:
                    self.matriz[fila, colum] = "◐"

                #Comprueba si el barco eliminado era el último para terminar el juego
                case ResultadoDisparo.HUNDIDO:
                    lista_indices_barco = np.array(self.dict_barcos_indices.get(self.dict_indices_barcos.get((fila,colum))))
                    f,c = np.column_stack(lista_indices_barco)
                    self.matriz[f,c] = "●"
                    barcos_hundidos = sum(1 for b in self.lista_barcos if b.esta_hundido())
                    if(barcos_hundidos == len(self.lista_barcos)):
                        has_ganado = True
        
        self.lista_indices_disparos.remove((fila,colum))
        return (has_ganado, resultado)

    def print_tablero(self):
        # Códigos de color ANSI
        AZUL = "\033[94m"
        VERDE = "\033[92m"
        NARANJA = "\033[93m"  # Amarillo brillante simulando naranja
        ROJO = "\033[91m"
        GRIS = "\033[90m"
        RESET = "\033[0m"

        print(f"\n{AZUL}Tablero del jugador:{RESET}", end= "\n\n")
        print(f"     {AZUL}0 1 2 3 4 5 6 7 8 9{RESET}")
        print(f"  {AZUL}-----------------------{RESET}")
        
        for fila in range(len(self.matriz)):
            fila_limpia = f"{AZUL}{str(fila)}{RESET} | "
            
            for colum in range(len(self.matriz[fila])):
                elemento = self.matriz[fila, colum]
                
                if elemento == "~":
                    fila_limpia += " □"  # Agua sin color
                elif elemento == "▲":
                    fila_limpia += f" {VERDE}▲{RESET}"  # Barcos en verde
                elif elemento == "⊞":
                    fila_limpia += f" {GRIS}⊞{RESET}"  # Fallos en gris
                elif elemento == "◐":
                    fila_limpia += f" {NARANJA}◐{RESET}" # Tocados en naranja
                elif elemento == "●":
                    fila_limpia += f" {ROJO}●{RESET}"  # Hundidos en rojo
                else:
                    fila_limpia += f" {elemento}"
                    
            print(fila_limpia)
            
        print(f"{AZUL}----------------------------------------------{RESET}")

    def print_tablero_enemigo(self):
        # Códigos de color ANSI
        ROJO = "\033[91m"
        VERDE = "\033[92m"
        GRIS = "\033[90m"
        RESET = "\033[0m"

        print(f"\n{ROJO}Tablero del rival:{RESET}", end= "\n\n")        
        print(f"     {ROJO}0 1 2 3 4 5 6 7 8 9{RESET}")
        print(f"  {ROJO}-----------------------{RESET}")
        
        for fila in range(len(self.matriz)):
            fila_limpia = f"{ROJO}{str(fila)}{RESET} | "
            
            for colum in range(len(self.matriz[fila])):
                elemento = self.matriz[fila, colum]
                
                # En el tablero enemigo los barcos '▲' y el agua '~' se ocultan como '□'
                if elemento == "~" or elemento == "▲":
                    fila_limpia += " □"
                elif elemento == "⊞":
                    fila_limpia += f" {GRIS}⊞{RESET}"  # Fallos en gris
                elif elemento == "◐" or elemento == "●":
                    fila_limpia += f" {VERDE}{elemento}{RESET}"  # Tocados y hundidos en verde
                else:
                    fila_limpia += f" {elemento}"
                    
            print(fila_limpia)
            
        print(f"{ROJO}----------------------------------------------{RESET}")
