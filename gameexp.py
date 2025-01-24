import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los Enemigos")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Clase del Jugador
class Jugador:
    def __init__(self):
        self.tamaño = 30
        self.x = ANCHO // 2
        self.y = ALTO - 50
        self.velocidad = 5
        
    def dibujar(self):
        pygame.draw.rect(ventana, AZUL, (self.x, self.y, self.tamaño, self.tamaño))
        
    def mover(self, dx):
        self.x += dx * self.velocidad
        # Mantener dentro de los límites
        self.x = max(0, min(ANCHO - self.tamaño, self.x))

# Clase del Enemigo
class Enemigo:
    def __init__(self):
        self.radio = random.randint(10, 20)
        self.x = random.randint(0, ANCHO - self.radio)
        self.y = -self.radio
        self.velocidad = random.randint(3, 5)
        
    def dibujar(self):
        pygame.draw.circle(ventana, ROJO, (self.x, self.y), self.radio)
        
    def mover(self):
        self.y += self.velocidad
        
    def colision(self, jugador):
        # Detectar colisión entre círculo y rectángulo
        distancia_x = abs(self.x - (jugador.x + jugador.tamaño/2))
        distancia_y = abs(self.y - (jugador.y + jugador.tamaño/2))
        
        if distancia_x > (jugador.tamaño/2 + self.radio): return False
        if distancia_y > (jugador.tamaño/2 + self.radio): return False
        
        if distancia_x <= (jugador.tamaño/2): return True
        if distancia_y <= (jugador.tamaño/2): return True
        
        dx = distancia_x - jugador.tamaño/2
        dy = distancia_y - jugador.tamaño/2
        return (dx**2 + dy**2) <= (self.radio**2)

# Variables del juego
jugador = Jugador()
enemigos = []
reloj = pygame.time.Clock()
puntaje = 0
game_over = False

# Bucle principal del juego
ejecutando = True
while ejecutando:
    ventana.fill(NEGRO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.mover(-1)
    if teclas[pygame.K_RIGHT]:
        jugador.mover(1)
        
    # Generar enemigos
    if random.random() < 0.03 and not game_over:
        enemigos.append(Enemigo())
        
    # Actualizar enemigos
    for enemigo in enemigos[:]:
        enemigo.mover()
        if enemigo.y > ALTO:
            enemigos.remove(enemigo)
            puntaje += 1
        else:
            if enemigo.colision(jugador):
                game_over = True
                
    # Dibujar elementos
    jugador.dibujar()
    for enemigo in enemigos:
        enemigo.dibujar()
        
    # Mostrar puntaje
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    ventana.blit(texto, (10, 10))
    
    # Mostrar Game Over
    if game_over:
        texto_game_over = fuente.render("GAME OVER - Presiona R para reiniciar", True, BLANCO)
        ventana.blit(texto_game_over, (ANCHO//2 - 200, ALTO//2))
        
        if teclas[pygame.K_r]:
            jugador = Jugador()
            enemigos = []
            puntaje = 0
            game_over = False
    
    pygame.display.update()
    reloj.tick(60)

pygame.quit()