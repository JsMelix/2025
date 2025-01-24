import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Halo-inspired Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Load assets
player_img = pygame.image.load("player_spartan.png")  # Add a placeholder image
enemy_img = pygame.image.load("enemy_covenant.png")  # Add a placeholder image
bullet_img = pygame.image.load("bullet.png")  # Add a placeholder image

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
bullet_img = pygame.transform.scale(bullet_img, (10, 10))

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 5
        self.shield = 100

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(-100, -40)))
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Groups
player = Player()
player_group = pygame.sprite.GroupSingle(player)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Spawn enemies
def spawn_enemy():
    enemy = Enemy()
    enemies.add(enemy)


# Main Game Loop
running = True
spawn_timer = 0

while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update player
    player_group.update(keys)

    # Spawn enemies every second
    spawn_timer += 1
    if spawn_timer > FPS:
        spawn_enemy()
        spawn_timer = 0

    # Update enemies and bullets
    enemies.update()
    bullets.update()

    # Collision detection
    for enemy in pygame.sprite.groupcollide(enemies, bullets, True, True):
        print("Enemy hit!")

    if pygame.sprite.spritecollide(player, enemies, True):
        player.shield -= 10
        if player.shield <= 0:
            print("Game Over!")
            running = False

    # Draw everything
    player_group.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)

    # Draw HUD
    pygame.draw.rect(screen, BLUE, (10, 10, player.shield * 2, 20))
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
