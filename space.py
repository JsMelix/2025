import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")
# You'll need to provide your own icon file
# icon = pygame.image.load("icon.png")
# pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('player.png')  # Replace with your image
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = pygame.image.load('enemy.png')  # Replace with your image
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_x_change = 0.3
enemy_y_change = 40

# Bullet
bullet_img = pygame.image.load('bullet.png')  # Replace with your image
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 0.7
bullet_state = "ready"  # "ready" - can't see bullet, "fire" - bullet is moving

score = 0

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    enemy_x += enemy_x_change
    if enemy_x <= 0:
        enemy_x_change = 0.3
        enemy_y += enemy_y_change
    elif enemy_x >= 736:
        enemy_x_change = -0.3
        enemy_y += enemy_y_change

    # Bullet movement
    if bullet_state == "fire":
        bullet_y -= bullet_y_change
        fire_bullet(bullet_x, bullet_y)
        if bullet_y <= 0:
            bullet_state = "ready"
            bullet_y = 480

    # Collision
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_state = "ready"
        bullet_y = 480
        score += 1
        print(score)
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)

    pygame.display.update()