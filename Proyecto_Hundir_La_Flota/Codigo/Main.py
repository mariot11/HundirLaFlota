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

    for barco in tablero_player.lista_barcos:
        while True:
            print(tablero_player.print_tablero())
            coordenadas_input = input(f"Introduce las coordenadas del barco de longitud {barco.longitud} (del 0 al 9) y la orienciación (N,S,E,O) separado por comas 'fila,columna,orientación'")

            if(coordenadas_input == ""):
                tablero_player.randomizar_posicion_barco(barco)

            elif coordenadas_input.count(",") != 2:
                print("Error de formato, recuerda que tienes que separar los distintos valores por ','")

            else:
                fila_input, colum_input, orientacion_input = coordenadas_input.split(sep= ",")
                orientacion_input = orientacion_input.replace(" ", "").upper()
                fila_input = fila_input.replace(" ", "")
                colum_input = colum_input.replace(" ", "")

                # Prueba
                print(f"{fila_input}, {colum_input}, {orientacion_input}")
                fila_input = int(fila_input)
                colum_input = int(colum_input)

                tablero_player.intentar_colocar_barco(barco, fila_input, colum_input, orientacion_input)
                print(tablero_player.print_tablero())

                # try:
                #     fila_input = int(fila_input)
                #     colum_input = int(colum_input)

                #     tablero_player.intentar_colocar_barco(fila_input, colum_input, orientacion_input)
                #     print(tablero_player.print_tablero())
                #     break

                # except TypeError:
                #     print("Los valores introducidos para las coordenadas no son válidos")
                
                # except ValueError:
                #     print("El valor de la orientación debe ser uno de estos (N, S, E, O)")

                # except IndexError:
                #     print("Los valores de las coordenadas no están entre 0 y 9")

    print("Adiós")

    
    
    # tablero_rival.print_tablero_enemigo()
    