import os
from datetime import datetime

# Ruta del archivo donde se almacenarán las canciones
RUTA_ARCHIVO = "registro_canciones.txt"

def registrar_cancion(cancion, artista):
    # Obtiene la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Verifica si el archivo ya existe
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w") as archivo:
            archivo.write("Registro de Canciones\n")
            archivo.write("="*30 + "\n")
    
    # Escribe la canción en el archivo
    with open(RUTA_ARCHIVO, "a") as archivo:
        archivo.write(f"[{fecha_actual}] {cancion} - {artista}\n")
    print(f"Canción registrada: {cancion} - {artista}")

def mostrar_historial():
    # Lee y muestra el historial de canciones
    if os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "r") as archivo:
            print(archivo.read())
    else:
        print("No hay historial registrado.")

# Menú interactivo
def menu():
    while True:
        print("\n--- Registro de Canciones ---")
        print("1. Registrar una canción")
        print("2. Ver historial de canciones")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            cancion = input("Nombre de la canción: ")
            artista = input("Artista: ")
            registrar_cancion(cancion, artista)
        elif opcion == "2":
            mostrar_historial()
        elif opcion == "3":
            print("¡Adiós!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
