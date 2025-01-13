from art import text2art

def create_bat_art():
    bat = r"""
       /\                 /\
      //\\___   ___//\\
      \    o\ /o    /
       \       X       /
        \  ___|___  /
         \_________/"""
    return bat

def display_black_sabbath():
    text = "BLACK SABBATH"
    bat_art = create_bat_art()
    text_3d = text2art(text, font='block')  # Crear texto en 3D

    print("=" * 50)
    print(text_3d)  # Mostrar texto en 3D
    print("=" * 50)

    for _ in range(2):  # Dos murciélagos a los lados del texto
        print(bat_art.center(50))

if __name__ == "__main__":
    display_black_sabbath()