import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.normal_color = GRAY
        self.hover_color = RED

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect)
        
        # Button text
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Create buttons
start_button = Button(WINDOW_WIDTH//2 - 100, 250, 200, 50, "Start")
quit_button = Button(WINDOW_WIDTH//2 - 100, 350, 200, 50, "Quit")

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Draw title
    font = pygame.font.Font(None, 74)
    title = font.render("Main Menu", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
    screen.blit(title, title_rect)
    
    # Draw buttons
    start_button.draw(screen)
    quit_button.draw(screen)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if start_button.handle_event(event):
            print("Start button clicked!")
            # Add your game start logic here
        
        if quit_button.handle_event(event):
            running = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()

