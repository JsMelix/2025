import turtle

# Configuración de la pantalla
screen = turtle.Screen()
screen.title("Criptomoneda Doge")
screen.bgcolor("white")

# Crear el objeto turtle
t = turtle.Turtle()
t.speed(3)

# Función para dibujar un círculo lleno
def dibujar_circulo(tortuga, radio, color_relleno, color_borde, ancho_borde=2):
    tortuga.penup()
    tortuga.goto(0, -radio)
    tortuga.pendown()
    tortuga.color(color_borde, color_relleno)
    tortuga.width(ancho_borde)
    tortuga.begin_fill()
    tortuga.circle(radio)
    tortuga.end_fill()

# Dibujar la moneda principal (círculo dorado)
dibujar_circulo(t, 200, "gold", "goldenrod", 3)

# Dibujar un borde externo para la moneda
dibujar_circulo(t, 210, "", "darkgoldenrod", 5)

# Escribir el texto "DOGE" en el centro de la moneda
t.penup()
t.goto(0, -50)
t.color("black")
t.write("DOGE", align="center", font=("Arial", 48, "bold"))
t.hideturtle()

# Crear un segundo objeto turtle para dibujar la cara del Doge
cara = turtle.Turtle()
cara.speed(3)
cara.hideturtle()

# Función para dibujar un ojo (círculo blanco con pupila negra)
def dibujar_ojo(x, y):
    cara.penup()
    cara.goto(x, y)
    cara.pendown()
    cara.color("white")
    cara.begin_fill()
    cara.circle(30)
    cara.end_fill()
    
    cara.penup()
    cara.goto(x, y + 15)
    cara.pendown()
    cara.color("black")
    cara.begin_fill()
    cara.circle(10)
    cara.end_fill()

# Dibujar ojo izquierdo y derecho
dibujar_ojo(-70, 50)
dibujar_ojo(70, 50)

# Dibujar la nariz (círculo negro)
cara.penup()
cara.goto(0, 20)
cara.pendown()
cara.color("black")
cara.begin_fill()
cara.circle(15)
cara.end_fill()

# Mantener la ventana abierta hasta que se cierre manualmente
turtle.done()
