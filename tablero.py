def crear_tablero(filas, columnas):
    """Crea un tablero vacío con dimensiones especificadas."""
    return [[" " for _ in range(columnas)] for _ in range(filas)]

def mostrar_tablero(tablero):
    """Muestra el tablero en un formato fácil de leer."""
    for fila in tablero:
        print("| " + " | ".join(fila) + " |")
        print("-" * (len(fila) * 4 + 1))

def escribir_en_tablero(tablero, fila, columna, valor):
    """Escribe un valor en una posición específica del tablero."""
    if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
        tablero[fila][columna] = valor
    else:
        print("Coordenadas fuera del rango. Inténtalo de nuevo.")

def main():
    # Dimensiones del tablero
    filas = 5
    columnas = 5

    # Crear tablero
    tablero = crear_tablero(filas, columnas)

    while True:
        # Mostrar el tablero actual
        mostrar_tablero(tablero)
        
        # Pedir coordenadas al usuario
        print("Escribe en el tablero:")
        try:
            fila = int(input("Fila (0 a {}): ".format(filas - 1)))
            columna = int(input("Columna (0 a {}): ".format(columnas - 1)))
            valor = input("Valor (1 carácter): ")
            
            # Validar que el valor sea un solo carácter
            if len(valor) != 1:
                print("El valor debe ser un único carácter.")
                continue
            
            # Escribir en el tablero
            escribir_en_tablero(tablero, fila, columna, valor)
        
        except ValueError:
            print("Entrada inválida. Por favor, ingresa números para las coordenadas.")
        
        # Preguntar si desea continuar
        continuar = input("¿Quieres seguir escribiendo? (s/n): ").lower()
        if continuar != "s":
            break

if __name__ == "__main__":
    main()
