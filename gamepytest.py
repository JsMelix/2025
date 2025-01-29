import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# High score file
HIGH_SCORE_FILE = "highscore.txt"

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Snake")
clock = pygame.time.Clock()

# Load high score
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# Game states
START_MENU = 0
PLAYING = 1
GAME_OVER = 2

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

def start_menu():
    high_score = load_high_score()
    
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Pixel Snake", True, GREEN)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))

    start_button = Button("Start", WIDTH//2 - 75, HEIGHT//2, 150, 50, BLUE, GREEN)
    quit_button = Button("Quit", WIDTH//2 - 75, HEIGHT//2 + 80, 150, 50, BLUE, GREEN)

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)

        # High score display
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 60))
        screen.blit(score_text, score_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in [start_button, quit_button]:
            button.is_hovered = button.rect.collidepoint(mouse_pos)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    return
                elif quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(15)

def game_over(score):
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Game Over", True, RED)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))

    retry_button = Button("Retry", WIDTH//2 - 75, HEIGHT//2, 150, 50, BLUE, GREEN)
    menu_button = Button("Menu", WIDTH//2 - 75, HEIGHT//2 + 80, 150, 50, BLUE, GREEN)

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)

        # Score display
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {score}   High Score: {high_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 60))
        screen.blit(score_text, score_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in [retry_button, menu_button]:
            button.is_hovered = button.rect.collidepoint(mouse_pos)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.rect.collidepoint(event.pos):
                    return PLAYING
                elif menu_button.rect.collidepoint(event.pos):
                    return START_MENU

        pygame.display.update()
        clock.tick(15)

def main():
    game_state = START_MENU

    while True:
        if game_state == START_MENU:
            start_menu()
            game_state = PLAYING

        if game_state == PLAYING:
            # Game initialization
            snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
            dx, dy = 1, 0
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            score = 0
            speed = FPS
            level = 1

            # Main game loop
            running = True
            while running:
                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and dy == 0:
                            dx, dy = 0, -1
                        elif event.key == pygame.K_DOWN and dy == 0:
                            dx, dy = 0, 1
                        elif event.key == pygame.K_LEFT and dx == 0:
                            dx, dy = -1, 0
                        elif event.key == pygame.K_RIGHT and dx == 0:
                            dx, dy = 1, 0

                # Move snake
                new_head = (snake[0][0] + dx, snake[0][1] + dy)

                # Check collisions
                if (new_head in snake or
                    new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                    running = False
                    break

                # Check food collision
                if new_head == food:
                    score += 1
                    if score % 3 == 0:
                        speed += 2
                        level += 1
                    food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                    while food in snake:
                        food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                else:
                    snake.pop()

                snake.insert(0, new_head)

                # Drawing
                screen.fill(BLACK)

                # Draw snake
                for i, segment in enumerate(snake):
                    color = YELLOW if i == 0 else GREEN
                    rect = pygame.Rect(segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
                    pygame.draw.rect(screen, color, rect)

                # Draw food
                food_rect = pygame.Rect(food[0]*GRID_SIZE, food[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
                pygame.draw.rect(screen, RED, food_rect)

                # Draw score and level
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Score: {score}   Level: {level}", True, WHITE)
                screen.blit(score_text, (10, 10))

                pygame.display.update()
                clock.tick(speed)

            game_state = GAME_OVER

        if game_state == GAME_OVER:
            action = game_over(score)
            game_state = action

if __name__ == "__main__":
    main()