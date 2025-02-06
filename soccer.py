import pygame
import math

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600  # Screen dimensions
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Field color
BALL_RADIUS = 15
FIELD_COLOR = GREEN
LINE_COLOR = WHITE
BALL_COLOR = BLACK
LINE_WIDTH = 5
GOAL_WIDTH = 150  # Goal width
GOAL_HEIGHT = 50    # Goal height
FRICTION = 0.98    # Simulate friction (0.98 is a good starting point, lower values = more friction)
MAX_SPEED = 15  # Limit the maximum speed of the ball
MIN_SPEED_THRESHOLD = 0.1  # Stop the ball when it's very slow. Important!

# --- Screen Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Soccer with Pygame")
clock = pygame.time.Clock()

# --- Classes ---
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = 0
        self.y_speed = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2) # white outline

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # --- Boundary Collisions ---
        # Left and Right
        if self.x - self.radius <= 0:  # Left boundary
            self.x = self.radius
            self.x_speed = -self.x_speed * 0.8  # Bounce with some energy loss
        elif self.x + self.radius >= WIDTH:  # Right boundary
            self.x = WIDTH - self.radius
            self.x_speed = -self.x_speed * 0.8

        # Top and Bottom
        if self.y - self.radius <= 0: #top boundary
            self.y = self.radius
            self.y_speed = -self.y_speed * 0.8
        elif self.y + self.radius >= HEIGHT: # Bottom boundary
            self.y = HEIGHT - self.radius
            self.y_speed = -self.y_speed * 0.8


        # Friction (apply it after collision)
        self.x_speed *= FRICTION
        self.y_speed *= FRICTION

        # Stop the ball if its speed is too low
        if abs(self.x_speed) < MIN_SPEED_THRESHOLD and abs(self.y_speed) < MIN_SPEED_THRESHOLD:
            self.x_speed = 0
            self.y_speed = 0

    def kick(self, angle, power):
        # Convert angle from degrees to radians.  Pygame's trig functions use radians.
        angle_rad = math.radians(angle)

        # Calculate the x and y components of the velocity.
        self.x_speed = power * math.cos(angle_rad)
        self.y_speed = -power * math.sin(angle_rad)   # Negative because y-axis is inverted in Pygame
        self.y_speed = max(-MAX_SPEED, min(self.y_speed, MAX_SPEED)) #limit the ball speed
        self.x_speed = max(-MAX_SPEED, min(self.x_speed, MAX_SPEED))


# --- Function to Draw the Field ---
def draw_field():
    screen.fill(FIELD_COLOR)
    # Center Circle
    pygame.draw.circle(screen, LINE_COLOR, (CENTER_X, CENTER_Y), 50, LINE_WIDTH)
    # Center Line
    pygame.draw.line(screen, LINE_COLOR, (CENTER_X, 0), (CENTER_X, HEIGHT), LINE_WIDTH)

    # Left Penalty Area
    pygame.draw.rect(screen, LINE_COLOR, (0, CENTER_Y - 100, 100, 200), LINE_WIDTH)
    # Right Penalty Area
    pygame.draw.rect(screen, LINE_COLOR, (WIDTH - 100, CENTER_Y - 100, 100, 200), LINE_WIDTH)

    # Left Goal
    pygame.draw.rect(screen, LINE_COLOR, (0, CENTER_Y - GOAL_WIDTH // 2, 10, GOAL_WIDTH), LINE_WIDTH)  # corrected placement
    # Right Goal
    pygame.draw.rect(screen, LINE_COLOR, (WIDTH - 10, CENTER_Y - GOAL_WIDTH// 2, 10, GOAL_WIDTH), LINE_WIDTH) #corrected placement


# --- Game Objects ---
ball = Ball(CENTER_X, CENTER_Y, BALL_RADIUS, BALL_COLOR)

# --- Game Loop ---
running = True
kicking = False  # Track if the mouse button is held down
kick_start_pos = None  # Store the initial mouse position when kicking

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                kicking = True
                kick_start_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and kicking:
                kicking = False
                kick_end_pos = pygame.mouse.get_pos()
                # Calculate the kick direction and power.
                dx = kick_start_pos[0] - kick_end_pos[0]  # Note the subtraction order
                dy = kick_start_pos[1] - kick_end_pos[1]
                distance = math.sqrt(dx**2 + dy**2)  # Use the distance formula
                angle = math.degrees(math.atan2(-dy, dx))  # Calculate the angle, -dy because of inverted y-axis

                power = min(distance / 2, MAX_SPEED)  # Limit the kick power
                ball.kick(angle, power)


    # --- Game Logic ---
    ball.move()

    # --- Drawing ---
    draw_field()
    ball.draw()

    # --- Kicking Visualization (Draw a line while mouse is down) ---
    if kicking:
        pygame.draw.line(screen, (255, 0, 0), kick_start_pos, pygame.mouse.get_pos(), 3)


    # --- Update Display ---
    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
