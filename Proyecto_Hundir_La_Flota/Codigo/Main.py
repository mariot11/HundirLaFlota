import TableroClase as tc
import BarcoClase as bc

#  Bucle de juego
while True:
    continuar = input("introduce 'continuar' si quieres seguir, cualquier otro input terminará el juego.")
    if continuar != "continuar":
        break
    tablero_rival = tc.Tablero()
    tablero_rival.colocar_barcos()

    tablero_player = tc.Tablero()
    tablero_player.print_tablero()
    todos_colocados = False

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
            coordenadas_input = input(f"Introduce las coordenadas del barco de longitud {barco.longitud} (del 0 al 9) y la orienciación (N,S,E,O) separado por comas 'fila,columna,orientación', si no introduces nada se calulará aleatoriamente la posición. Escribe aleatorio si quieres que se coloquen todos los barcos de forma aleatoria: ")

            # Si el usuario escribe aleatorio, se deben colocar todos los barcos automáticamente de una
            if coordenadas_input == "aleatorio":
                tablero_player.colocar_barcos(i)
                todos_colocados = True
                break
            
            # Si el usuario no introduce ningún valor, el barco correspondiente se coloca aleatoriamente 
            elif coordenadas_input == "":
                barco_colocado = tablero_player.randomizar_posicion_barco(barco)
                tablero_player.print_tablero()

            # Si no se han separado bien las coordenadas por comas se avisa
            elif coordenadas_input.count(",") != 2:
                print("Error de formato, recuerda que tienes que separar los distintos valores por ','")

            else:
                try:
                    # separamos el input en diferentes variables y las limpiamos
                    fila_input, colum_input, orientacion_input = coordenadas_input.split(sep= ",")
                    orientacion_input = orientacion_input.replace(" ", "").upper()
                    fila_input = fila_input.replace(" ", "")
                    colum_input = colum_input.replace(" ", "")

                    # Convertimos en ints las coordenadas introduucidas
                    fila_input = int(fila_input)
                    colum_input = int(colum_input)

                    # Intentamos colocar el barco en las coordenadas que le hemos pasado y guardamos el resultado (booleano) para saber si lo ha conseguido
                    barco_colocado = tablero_player.intentar_colocar_barco(barco, fila_input, colum_input, orientacion_input)
                    tablero_player.print_tablero()
                
                except:
                    print("Los valores introducidos no son válidos")

            if barco_colocado == False:
                print("El barco no puede ser colocado en esa posición/orientación, prueba con otra")

                # try:
                #     fila_input = int(fila_input)
                #     colum_input = int(colum_input)

                #     tablero_player.intentar_colocar_barco(fila_input, colum_input, orientacion_input)
                #     print(tablero_player.print_tablero())
                #     break

                # except TypeError:
                #     print("Los valores introducidos para las coordenadas no son válidos")
                
                # except ValueError:
                #     print("Al menos uno de los valores no ha sido introducido de forma correcta")

                # except IndexError:
                #     print("Los valores de las coordenadas no están entre 0 y 9")

    print("Adiós")

    
    
    # tablero_rival.print_tablero_enemigo()
    