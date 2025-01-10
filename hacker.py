from PIL import Image, ImageDraw, ImageFont

def create_pixel_art_text(text, output_file="hacker_pixel_art.png"):
    # Configuración de la imagen
    font_size = 8  # Tamaño base de píxel
    scale = 10  # Escala para agrandar la imagen
    font_path = "arial.ttf"  # Cambia a una fuente pixel art si tienes una

    # Crear una imagen temporal para calcular el tamaño del texto
    temp_image = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        print("No se encontró la fuente especificada. Usando fuente predeterminada.")
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font=font)

    # Crear la imagen final con el tamaño adecuado
    image = Image.new("RGB", (text_width * scale, text_height * scale), "black")
    draw = ImageDraw.Draw(image)

    # Dibujar el texto
    for x in range(scale):
        for y in range(scale):
            draw.text((x, y), text, fill="lime", font=font)


            image.save("out.png","d.png")