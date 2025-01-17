import random

def mostrar_palabra(palabra, letras_adivinadas):
    return " ".join([letra if letra in letras_adivinadas else "_" for letra in palabra])

def jugar_ahorcado():
    palabras = ["python", "programacion", "desarrollo", "juego", "codigo"]
    palabra = random.choice(palabras)
    letras_adivinadas = set()
    intentos = 6  # Número de intentos permitidos

    print("¡Bienvenido al juego del Ahorcado!")
    print("Adivina la palabra secreta.")
    
    while intentos > 0:
        print("\n" + mostrar_palabra(palabra, letras_adivinadas))
        print(f"Te quedan {intentos} intentos.")
        letra = input("Introduce una letra: ").lower()

        if len(letra) != 1 or not letra.isalpha():
            print("Por favor, introduce una única letra.")
            continue

        if letra in letras_adivinadas:
            print("Ya adivinaste esa letra.")
        elif letra in palabra:
            print(f"¡Bien hecho! La letra '{letra}' está en la palabra.")
            letras_adivinadas.add(letra)
        else:
            print(f"La letra '{letra}' no está en la palabra.")
            letras_adivinadas.add(letra)
            intentos -= 1

        if all(letra in letras_adivinadas for letra in palabra):
            print(f"\n¡Felicidades! Adivinaste la palabra: {palabra}")
            break
    else:
        print(f"\nLo siento, te quedaste sin intentos. La palabra era: {palabra}")

if __name__ == "__main__":
    jugar_ahorcado()
