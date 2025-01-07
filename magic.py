from PIL import Image, ImageDraw

# Crear una imagen
width, height = 800, 600
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Función para dibujar un Rey Mago simple
def draw_king(x, y, color):
    
    # Cabeza
    draw.ellipse((x - 30, y - 30, x + 30, y + 30), fill=color)
    
    # Corona
    draw.polygon([(x - 25, y - 30), (x - 10, y - 60), (x, y - 30), 
                  (x + 10, y - 60), (x + 25, y - 30)], fill="gold")
    
    # Cuerpo
    draw.rectangle((x - 20, y + 30, x + 20, y + 110), fill="blue")
    
    # Regalo
    draw.rectangle((x - 15, y + 120, x + 15, y + 150), fill="red")
    draw.line((x - 15, y + 135, x + 15, y + 135), fill="yellow", width=3)
    draw.line((x, y + 120, x, y + 150), fill="yellow", width=3)

# Dibujar los tres Reyes Magos
draw_king(200, 200, "brown")  # Rey 1
draw_king(400, 200, "pink")   # Rey 2
draw_king(600, 200, "black")  # Rey 3

# Guardar la imagen
image.save("reyes_magos.png")
image.show()
