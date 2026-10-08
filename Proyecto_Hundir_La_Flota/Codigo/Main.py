import TableroClase as tc
import BarcoClase as bc

#  Bucle de juego
while True:
    continuar = input("introduce 'continuar' si quieres seguir, cualquier otro input terminará el juego.")
    if continuar != "continuar":
        break
    tablero_rival = tc.Tablero()
    tablero_rival.colocar_barcos()
    tablero_rival.print_tablero()
    