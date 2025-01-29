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
CYAN = (0, 255, 255)
DARK_BLUE = (10, 10, 50)
SPACE_BLUE = (25, 25, 112)
STAR_COLORS = [(255, 255, 255), (200, 200, 255), (255, 255, 200), (200, 220, 255)]

# High score file
HIGH_SCORE_FILE = "highscore.txt"

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Snake")
clock = pygame.time.Clock()

# Generate starfield background
def create_starfield():
    starfield = pygame.Surface((WIDTH, HEIGHT))
    starfield.fill(DARK_BLUE)
    
    # Draw distant stars
    for _ in range(150):
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)
        size = random.choice([1, 1, 1, 2])
        color = random.choice(STAR_COLORS)
        pygame.draw.circle(starfield, color, (x, y), size)
    
    # Draw nebula effect
    for _ in range(20):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(10, 30)
        alpha = random.randint(50, 100)
        nebula = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(nebula, (*random.choice(STAR_COLORS), alpha), (radius, radius), radius)
        starfield.blit(nebula, (x-radius, y-radius), special_flags=pygame.BLEND_RGBA_ADD)
    
    return starfield

STARFIELD = create_starfield()

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

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, SPACE_BLUE, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, SPACE_BLUE, (0, y), (WIDTH, y), 1)

def start_menu():
    high_score = load_high_score()
    
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Space Snake", True, CYAN)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))

    start_button = Button("Start", WIDTH//2 - 75, HEIGHT//2, 150, 50, SPACE_BLUE, CYAN)
    quit_button = Button("Quit", WIDTH//2 - 75, HEIGHT//2 + 80, 150, 50, SPACE_BLUE, CYAN)

    while True:
        screen.blit(STARFIELD, (0, 0))
        
        # Draw rotating planet
        pygame.draw.circle(screen, (100, 100, 200), (WIDTH//4, HEIGHT//2), 40)
        pygame.draw.circle(screen, (80, 80, 180), (WIDTH//4 + 10, HEIGHT//2 - 10), 15)
        
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
    title_text = title_font.render("Game Over", True, CYAN)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))

    retry_button = Button("Retry", WIDTH//2 - 75, HEIGHT//2, 150, 50, SPACE_BLUE, CYAN)
    menu_button = Button("Menu", WIDTH//2 - 75, HEIGHT//2 + 80, 150, 50, SPACE_BLUE, CYAN)

    while True:
        screen.blit(STARFIELD, (0, 0))
        
        # Draw cosmic effect
        pygame.draw.circle(screen, (150, 150, 255), (WIDTH//2, HEIGHT//2), 100, 3)
        
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
            snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
            dx, dy = 1, 0
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            score = 0
            speed = FPS
            level = 1

            running = True
            while running:
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

                new_head = (snake[0][0] + dx, snake[0][1] + dy)

                if (new_head in snake or
                    new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                    running = False
                    break

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
                screen.blit(STARFIELD, (0, 0))
                draw_grid()

                # Draw snake
                for i, segment in enumerate(snake):
                    color = CYAN if i == 0 else (0, 100, 200)
                    rect = pygame.Rect(segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
                    pygame.draw.rect(screen, color, rect)

                # Draw food
                food_rect = pygame.Rect(food[0]*GRID_SIZE, food[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
                pygame.draw.circle(screen, CYAN, food_rect.center, GRID_SIZE//2 - 1)

                # Add star twinkle
                if random.random() < 0.01:
                    x = random.randint(0, WIDTH-1)
                    y = random.randint(0, HEIGHT-1)
                    pygame.draw.circle(screen, WHITE, (x, y), 2)

                # Draw UI
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