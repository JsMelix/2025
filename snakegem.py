import pygame
import random

# Initialize Pygame
pygame.init()

# --- Game Constants ---
CELL_SIZE = 20  # Size of each cell in pixels
GRID_WIDTH = 20  # Number of cells in width
GRID_HEIGHT = 15 # Number of cells in height
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SNAKE_COLOR = GREEN
FOOD_COLOR = RED
BACKGROUND_COLOR = BLACK
GRID_COLOR = (50, 50, 50) # Optional grid lines

INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_SPEED = 10  # Frames per second (adjust for difficulty)
SPEED_INCREMENT_SCORE = 5 # Score points after which speed increases
SPEED_INCREMENT_VALUE = 1 # Increase FPS by this value after score threshold

FONT_SIZE = 30
FONT = pygame.font.Font(None, FONT_SIZE)

# --- Game Variables ---
snake = []
food_pos = None
direction = (1, 0)  # Initial direction: right
score = 0
game_state = "START_MENU" # "START_MENU", "PLAYING", "GAME_OVER"
snake_speed = INITIAL_SNAKE_SPEED
game_clock = pygame.time.Clock()

# --- Functions ---

def create_snake():
    """Creates the initial snake at the center of the grid."""
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    return [(start_x + i, start_y) for i in range(INITIAL_SNAKE_LENGTH)]

def generate_food():
    """Generates food at a random empty cell."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_grid(screen): # Optional, for visual aid
    """Draws grid lines on the screen."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_snake(screen, snake_list):
    """Draws the snake on the screen."""
    for segment in snake_list:
        rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SNAKE_COLOR, rect)

def draw_food(screen, food_position):
    """Draws the food on the screen."""
    rect = pygame.Rect(food_position[0] * CELL_SIZE, food_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, rect)

def display_text(screen, text, y_offset=0, color=WHITE):
    """Displays text on the screen, centered horizontally."""
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def start_menu_screen(screen):
    """Displays the start menu."""
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Pixel Snake", -50)
    display_text(screen, "Press any key to start", 20)
    pygame.display.flip()

def game_over_screen(screen):
    """Displays the game over screen."""
    screen.fill(BACKGROUND_COLOR)
    display_text(screen, "Game Over!", -50, RED)
    display_text(screen, f"Score: {score}", 0)
    display_text(screen, "Press any key to restart", 50)
    pygame.display.flip()

def game_loop(screen):
    """Main game loop logic."""
    global snake, food_pos, direction, score, game_state, snake_speed
    snake = create_snake()
    food_pos = generate_food()
    direction = (1, 0) # Initial direction: right
    score = 0
    game_state = "PLAYING"
    snake_speed = INITIAL_SNAKE_SPEED

    last_move_time = pygame.time.get_ticks()
    move_interval = 1000 / snake_speed # Milliseconds per move

    running_game = True
    while running_game:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
                game_state = "QUIT" # Indicate quit to main loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)

        if current_time - last_move_time > move_interval:
            last_move_time = current_time

            # Move the snake
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Collision detection
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake):
                game_state = "GAME_OVER"
                running_game = False
                continue # Skip game logic for this frame

            snake.insert(0, new_head) # Add new head

            # Check if food eaten
            if new_head == food_pos:
                score += 1
                food_pos = generate_food()
                if score % SPEED_INCREMENT_SCORE == 0:
                    snake_speed += SPEED_INCREMENT_VALUE
                    move_interval = 1000 / snake_speed # Update move interval for new speed

            else:
                snake.pop() # Remove tail if no food eaten

            # --- Drawing ---
            screen.fill(BACKGROUND_COLOR)
            # draw_grid(screen) # Optional grid lines
            draw_snake(screen, snake)
            draw_food(screen, food_pos)
            display_text(screen, f"Score: {score}", -SCREEN_HEIGHT // 2 + 20, GREEN) # Score at top
            pygame.display.flip()

        game_clock.tick(snake_speed * 60) # Limit frame rate, effectively controlling max speed

    return game_state # Return game state to main loop

# --- Main Game Function ---
def main():
    """Main function to run the game."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Snake")

    running = True
    current_game_state = "START_MENU"

    while running:
        if current_game_state == "START_MENU":
            start_menu_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN: # Any key press starts game
                    current_game_state = "PLAYING"

        elif current_game_state == "PLAYING":
            current_game_state = game_loop(screen) # game_loop returns next state

        elif current_game_state == "GAME_OVER":
            game_over_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN: # Any key press restarts
                    current_game_state = "PLAYING" # Back to playing to restart game_loop

        elif current_game_state == "QUIT": # From game_loop if player quit during game
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()