import turtle

def dibujar_hemisferio(t, inicio, radio, sentido):
    """
    Dibuja un hemisferio con varios arcos (simulando los surcos del cerebro).
    
    Parámetros:
      t: objeto turtle.Turtle.
      inicio: tupla (x, y) con la posición de inicio.
      radio: radio de los arcos.
      sentido: 1 para dibujar con arcos hacia la izquierda y -1 para el derecho.
    """
    t.penup()
    t.goto(inicio)
    t.pendown()
    # Ajustamos la dirección inicial: 90 grados (hacia arriba)
    t.setheading(90)
    
    # Se dibujan varios arcos superpuestos para simular los giros del cerebro.
    for i in range(6):
        # Dibuja un arco de 180° (media circunferencia)
        t.circle(sentido * radio, 180)
        # Rotamos un poco para cambiar el ángulo del siguiente arco
        t.right(30 * sentido)

def dibujar_cerebro():
    # Configuración de la ventana y del objeto turtle
    pantalla = turtle.Screen()
    pantalla.title("Dibujo de un cerebro con Turtle")
    pantalla.bgcolor("white")
    pantalla.setup(width=800, height=600)
    
    t = turtle.Turtle()
    t.speed(4)      # Velocidad de dibujo (1: lento, 10: rápido, 0: sin animación)
    t.width(3)
    t.color("purple")
    
    # Dibujar hemisferio izquierdo
    # Posición de inicio para el hemisferio izquierdo
    pos_izquierdo = (-100, 0)
    dibujar_hemisferio(t, pos_izquierdo, radio=50, sentido=1)
    
    # Dibujar hemisferio derecho
    # Posición de inicio para el hemisferio derecho
    pos_derecho = (100, 0)
    dibujar_hemisferio(t, pos_derecho, radio=50, sentido=-1)
    
    # Dibujar el cuerpo calloso (la conexión entre ambos hemisferios)
    t.penup()
    t.goto(-100, 0)
    t.pendown()
    t.setheading(0)  # Dirección hacia la derecha
    t.forward(200)
    
    # Finalizar dibujo
    pantalla.mainloop()

if __name__ == '__main__':
    dibujar_cerebro()
