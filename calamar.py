import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def squid_game():
    print("\033[1;31m" + """
    ░██████╗░██████╗░██╗░░░██╗██╗██████╗░  ░█████╗░██╗░░░░░░█████╗░███╗░░░███╗███████╗░█████╗░██████╗░
    ██╔═══██╗██╔══██╗██║░░░██║██║██╔══██╗  ██╔══██╗██║░░░░░██╔══██╗████╗░████║██╔════╝██╔══██╗██╔══██╗
    ██║██╗██║██████╔╝██║░░░██║██║██║░░██║  ██║░░╚═╝██║░░░░░███████║██╔████╔██║█████╗░░██║░░██║██████╔╝
    ╚██████╔╝██╔══██╗██║░░░██║██║██║░░██║  ██║░░██╗██║░░░░░██╔══██║██║╚██╔╝██║██╔══╝░░██║░░██║██╔══██╗
    ░╚═██╔═╝░██║░░██║╚██████╔╝██║██████╔╝  ╚█████╔╝███████╗██║░░██║██║░╚═╝░██║███████╗╚█████╔╝██║░░██║
    ░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═╝╚═════╝░  ░╚════╝░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝
    """ + "\033[0m")
    
    input("Presiona ENTER para comenzar...")
    clear_screen()
    
    posicion_jugador = 0
    meta = 20
    vidas = 3
    
    while posicion_jugador < meta and vidas > 0:
        # Generar estado aleatorio (1 = Luz Verde, 0 = Luz Roja)
        estado_luz = random.randint(0, 1)
        duracion = random.uniform(1.0, 3.0)
        
        # Luz Verde
        if estado_luz == 1:
            print("\033[1;32m" + "███ LUZ VERDE ███" + "\033[0m")
            start_time = time.time()
            input("¡Corre! Presiona ENTER para avanzar: ")
            reaction_time = time.time() - start_time
            
            if reaction_time > duracion:
                print("\033[1;31m¡Demasiado lento! La luz cambió...")
                vidas -= 1
            else:
                avance = random.randint(1, 3)
                posicion_jugador += avance
                print(f"\nAvanzaste {avance} metros! Posición actual: {posicion_jugador}/{meta}")
        
        # Luz Roja
        else:
            print("\033[1;31m" + "███ LUZ ROJA ███" + "\033[0m")
            print("¡Detente completamente!")
            time.sleep(duracion)
            
            # Detección de movimiento (simulada)
            movimiento = random.randint(0, 10)
            if movimiento > 7:  # 30% de probabilidad de ser detectado
                print("\033[1;31m¡Te moviste! (-1 vida)")
                vidas -= 1
                print(f"Vidas restantes: {vidas}\033[0m")
            else:
                print("\033[1;32m¡Perfecto! Nadie se movió\033[0m")
        
        print("-" * 50)
        time.sleep(1)
        clear_screen()
    
    # Resultado final
    if posicion_jugador >= meta:
        print("\033[1;32m" + """
        ░█████╗░██╗░░░██╗███████╗███╗░░██╗██╗░░██╗███████╗██████╗░
        ██╔══██╗██║░░░██║██╔════╝████╗░██║██║░██╔╝██╔════╝██╔══██╗
        ██║░░██║██║░░░██║█████╗░░██╔██╗██║█████═╝░█████╗░░██████╔╝
        ██║░░██║██║░░░██║██╔══╝░░██║╚████║██╔═██╗░██╔══╝░░██╔══██╗
        ╚█████╔╝╚██████╔╝███████╗██║░╚███║██║░╚██╗███████╗██║░░██║
        ░╚════╝░░╚═════╝░╚══════╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
        """ + "\033[0m")
    else:
        print("\033[1;31m" + """
        ███████╗██████╗░███████╗███████╗███╗░░██╗░██████╗
        ██╔════╝██╔══██╗██╔════╝██╔════╝████╗░██║██╔════╝
        █████╗░░██████╔╝█████╗░░█████╗░░██╔██╗██║╚█████╗░
        ██╔══╝░░██╔══██╗██╔══╝░░██╔══╝░░██║╚████║░╚═══██╗
        ██║░░░░░██║░░██║███████╗███████╗██║░╚███║██████╔╝
        ╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚══╝╚═════╝░
        """ + "\033[0m")

if __name__ == "__main__":
    squid_game()