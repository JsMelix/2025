import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Heart Shape")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw a heart shape using polygons
    pygame.draw.polygon(screen, RED, [
        (200, 100), (240, 150), (280, 150), (200, 250), (120, 150), (160, 150)
    ])

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
