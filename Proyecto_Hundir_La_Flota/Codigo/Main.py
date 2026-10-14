import TableroClase as tc
import BarcoClase as bc


def separar_coordenadas(texto_input, num_elementos):
    """
    Separa un string por comas, limpia espacios y convierte los elementos numéricos a enteros.
    """
    coordenadas = texto_input.split(sep=",")
    
    if len(coordenadas) != num_elementos:
        raise ValueError("Número de elementos incorrecto")
        
    # Limpiamos espacios de todas las partes
    coordenadas_sueltas = [coordenada.replace(" ", "") for coordenada in coordenadas]
    
    return coordenadas_sueltas

#  Bucle de juego
while True:
    print("introduce 'continuar' si quieres seguir, cualquier otro input terminará el juego.")
    continuar = input(">> ")

    if continuar != "continuar":
        break
    tablero_rival = tc.Tablero()
    tablero_rival.colocar_barcos()

    tablero_player = tc.Tablero()
    todos_colocados = False

    # Bucle que sirve para colocar los barcos del player
    for i in range(len(tablero_player.lista_barcos)):
        # En el caso de que se hayan colocado todos los barcos de forma aleatoria usando colocar_barcos() no debe continuar el bucle
        if todos_colocados == True:
            tablero_player.print_tablero()
            break

        # Guardamos el barco correspondiente a cada iteración del bucle
        barco = tablero_player.lista_barcos[i]
        barco_colocado = False

        # Mientras no hayamos colocado el barco el bucle debe seguir ejecutándose
        while barco_colocado != True:
            print(f"\nIntroduce las coordenadas del barco de longitud {barco.longitud} (del 0 al 9) y la orientación (N,S,E,O)\n"
                    "separado por comas 'fila,columna,orientación', si no introduces nada se calculará aleatoriamente la posición.\n"
                    "Escribe 'aleatorio' si quieres que se coloquen todos los barcos de forma aleatoria.")

            coordenadas_input = input(">> ")

            # Si el usuario escribe aleatorio, se deben colocar todos los barcos automáticamente de una
            if coordenadas_input == "aleatorio":
                tablero_player.colocar_barcos(i)
                todos_colocados = True
                break
            
            # Si el usuario no introduce ningún valor, el barco correspondiente se coloca aleatoriamente 
            elif coordenadas_input == "":
                barco_colocado = tablero_player.randomizar_posicion_barco(barco)
                tablero_player.print_tablero()

            else:
                try:
                    # separamos el input en diferentes variables y las limpiamos
                    coordenadas_lista = separar_coordenadas(coordenadas_input, 3)
                    fila_input = coordenadas_lista[0]
                    colum_input = coordenadas_lista[1]
                    orientacion_input = coordenadas_lista[2].upper()

                    # Intentamos colocar el barco en las coordenadas que le hemos pasado y guardamos el resultado (booleano) para saber si lo ha conseguido
                    barco_colocado = tablero_player.intentar_colocar_barco(barco, fila_input, colum_input, orientacion_input)
                    tablero_player.print_tablero()
                
                except:
                    print("Los valores introducidos no son válidos o falta alguna coma", end = "\n\n")

            if not barco_colocado:
                print("El barco no puede ser colocado en esa posición/orientación, prueba con otra", end = "\n\n")

    # Una vez terminado el bucle de colocación de barcos empieza el bucle de disparos
    gana_jugador = False
    gana_rival = False

    # Mientras nadie gane seguir disparando
    while (not gana_jugador) and (not gana_rival):
        disparo_player = False
        while not disparo_player:
            print("Introduce las coordenadas para el disparo (del 0 al 9) separando por comas 'fila,columna'. Si no introduces nada " \
            "se disparará a una casilla aleatoria.")
            coordenadas_input_disparo = input(">> ")

            # Si no introduces nada, disparar aleatoriamente
            if coordenadas_input_disparo == "":
                gana_jugador, resultado, coordenadas_disparo = tablero_rival.disparar_aleatoriamente()
                print(f"El jugador ha disparado a la casilla ({coordenadas_disparo[0]}, {coordenadas_disparo[1]}) y el resultado ha sido {resultado.name}")
                tablero_rival.print_tablero_enemigo()
                disparo_player = True
            
            else:
                try:
                    coordenadas_lista = separar_coordenadas(coordenadas_input_disparo, 2)
                    fila_input_disparo = int(coordenadas_lista[0])
                    colum_input_disparo = int(coordenadas_lista[1])

                    # Disparamos en las coordenadas obtenidas
                    gana_jugador = tablero_rival.disparar(fila_input_disparo, colum_input_disparo)[0]
                    disparo_player = True
                    tablero_rival.print_tablero_enemigo()
                
                except IndexError:
                    print("Las coordenadas que introdujiste no se encuentran dentro del tablero 10x10 (tienen que ser números entre 0 y 9)")
                except ValueError:
                    print("Error de formato: recuerda separar 2 valores por comas (ej: 3,4)")
                except Exception:
                    print("La casilla ya había sido disparada previamente")
        
        if gana_jugador:
            break

        print("\nTurno de disparar del enemigo: ")
        input("\nPulsa enter para continuar\n>>>")
        gana_rival, resultado, coordenadas_disparo = tablero_player.disparar_rival()
        print(f"El enemigo ha disparado a la casilla ({coordenadas_disparo[0]}, {coordenadas_disparo[1]}) y el resultado ha sido {resultado.name}")
        tablero_player.print_tablero()

    if gana_jugador:
        print("\nEnhorabuena, has ganado")
    else:
        print("\nLos siento, has perdido")
    print("Adiós")

