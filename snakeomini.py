import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Constantes globales
PIXEL_SIZE = 20           # Tamaño de cada bloque (estilo pixel art)
GRID_WIDTH = 30           # Número de bloques horizontalmente
GRID_HEIGHT = 20          # Número de bloques verticalmente
WINDOW_WIDTH = PIXEL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = PIXEL_SIZE * GRID_HEIGHT

# Colores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BASE_BG = (10, 40, 10)      # Color base del fondo (tono oscuro)
GRID_BG = (20, 70, 20)      # Color de las líneas de la cuadrícula

# Configuración de la ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake en Pixel Art")
clock = pygame.time.Clock()

# Configuración de fuentes
font_small = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 40)

def draw_text(surface, text, font, color, center):
    """Dibuja un texto centrado en la superficie."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=center)
    surface.blit(text_obj, text_rect)

def draw_background(surface):
    """
    Dibuja el fondo con un color base y una cuadrícula para lograr
    un estilo pixel art.
    """
    surface.fill(BASE_BG)
    # Líneas verticales
    for x in range(0, WINDOW_WIDTH, PIXEL_SIZE):
        pygame.draw.line(surface, GRID_BG, (x, 0), (x, WINDOW_HEIGHT))
    # Líneas horizontales
    for y in range(0, WINDOW_HEIGHT, PIXEL_SIZE):
        pygame.draw.line(surface, GRID_BG, (0, y), (WINDOW_WIDTH, y))

def start_menu():
    """Muestra el menú de inicio hasta que el jugador inicie el juego."""
    while True:
        draw_background(screen)
        draw_text(screen, "Snake en Pixel Art", font_large, GREEN, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        draw_text(screen, "Presiona SPACE para iniciar", font_small, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        draw_text(screen, "Usa las flechas para mover", font_small, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Inicia el juego

        clock.tick(15)

def game_over_screen(score):
    """Muestra la pantalla de Game Over y espera a que el jugador decida reiniciar o salir."""
    while True:
        screen.fill(BLACK)
        draw_text(screen, "Juego Terminado", font_large, RED, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        draw_text(screen, f"Puntaje: {score}", font_small, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        draw_text(screen, "Presiona R para reiniciar o Q para salir", font_small, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Reinicia el juego
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(15)

def get_random_food_position(snake):
    """Devuelve una posición aleatoria para la comida que no esté ocupada por la serpiente."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def main_game():
    # Inicializa la serpiente en el centro del grid
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, 0)  # La serpiente se quedará quieta hasta que se presione una tecla
    score = 0
    food = get_random_food_position(snake)
    speed = 10  # Velocidad inicial (cuadros por segundo)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Actualiza la dirección según la tecla presionada
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Si la serpiente aún no se mueve (sin input), se espera
        if direction == (0, 0):
            clock.tick(speed)
            continue

        # Calcula la nueva posición de la cabeza de la serpiente
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Verifica colisiones con los bordes
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            break  # Fin del juego

        # Verifica colisión con la propia serpiente
        if new_head in snake:
            break  # Fin del juego

        # Actualiza la serpiente
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            speed = min(25, speed + 0.5)  # Incrementa la velocidad (con un máximo)
            food = get_random_food_position(snake)
        else:
            snake.pop()  # Remueve la cola si no se comió comida

        # Dibuja el fondo, la comida y la serpiente
        draw_background(screen)

        # Dibuja la comida
        food_rect = pygame.Rect(food[0] * PIXEL_SIZE, food[1] * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        # Dibuja la serpiente
        for segment in snake:
            segment_rect = pygame.Rect(segment[0] * PIXEL_SIZE, segment[1] * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            pygame.draw.rect(screen, GREEN, segment_rect)
            pygame.draw.rect(screen, DARK_GRAY, segment_rect, 1)  # Borde para resaltar el pixel art

        # Dibuja el puntaje
        score_text = font_small.render(f"Puntaje: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        pygame.display.flip()
        clock.tick(speed)

    return score

def main():
    while True:
        start_menu()
        score = main_game()
        game_over_screen(score)

if __name__ == "__main__":
    main()
