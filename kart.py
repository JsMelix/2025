import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kart Racing")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Kart class
class Kart(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.steering = 3  # Degrees per frame
        self.angle = 0

    def update(self, keys):
        # Acceleration
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        else:
            self.speed = max(self.speed - self.deceleration, 0)

        # Steering
        if keys[pygame.K_LEFT]:
            self.angle += self.steering * self.speed / self.max_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.steering * self.speed / self.max_speed

        # Movement
        rad = math.radians(self.angle)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)

        # Keep kart within screen bounds (basic)
        self.x = max(0, min(self.x, screen_width))
        self.y = max(0, min(self.y, screen_height))

        self.rect.center = (int(self.x), int(self.y))

        # Rotate the image
        self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rotated_rect)

# Track (very basic)
track_color = (100, 100, 100)  # Gray
track_rect = pygame.Rect(100, 100, screen_width - 200, screen_height - 200)

# Create kart
kart = Kart("kart.png", screen_width // 2, screen_height // 2)  # Replace with your image
all_sprites = pygame.sprite.Group()
all_sprites.add(kart)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Update
    kart.update(keys)

    # Draw
    screen.fill(white)
    pygame.draw.rect(screen, track_color, track_rect)  # Draw track
    kart.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()