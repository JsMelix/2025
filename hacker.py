from PIL import Image, ImageDraw, ImageFont

def create_pixel_art_text(text, output_file="hacker_pixel_art.png"):
    # Configuración de la imagen
    font_size = 10  # Tamaño de fuente para el texto pixelado
    scale = 10  # Escala para ampliar el arte pixelado
    font_path = "arial.ttf"  # Fuente predeterminada (puedes cambiarla a una fuente pixel art si tienes una)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        print("No se encontró la fuente especificada. Usando fuente predeterminada.")
        font = ImageFont.load_default()

    # Calcular el tamaño del texto
    text_width, text_height = font.getbbox(text)[2:]  # Cambiar a getbbox para calcular correctamente

    # Crear la imagen final con un fondo negro
    image = Image.new("RGB", (text_width * scale, text_height * scale), "black")
    draw = ImageDraw.Draw(image)

    # Dibujar el texto escalado
    for x in range(0, text_width):
        for y in range(0, text_height):
            draw.text((x * scale, y * scale), text, fill="lime", font=font)

    # Guardar la imagen
    image.save(output_file)
    print(f"Imagen guardada como {output_file}")

# Ejecución del programa
if __name__ == "__main__":
    create_pixel_art_text("HACKER")
