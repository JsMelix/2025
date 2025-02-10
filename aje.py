import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
light_brown = (240, 217, 181)
dark_brown = (181, 136, 99)

# Load images
pieces = {}
piece_names = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
for name in piece_names:
    pieces[name] = pygame.image.load(f'{name}.png')

# Initial board setup
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

selected_piece = None
selected_pos = None

def draw_board():
    for row in range(8):
        for col in range(8):
            color = light_brown if (row + col) % 2 == 0 else dark_brown
            pygame.draw.rect(screen, color, pygame.Rect(col * 100, row * 100, 100, 100))
            piece = board[row][col]
            if piece:
                screen.blit(pieces[piece], (col * 100, row * 100))

def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos[0] // 100, mouse_pos[1] // 100
    return (x, y)

def move_piece(start_pos, end_pos):
    piece = board[start_pos[1]][start_pos[0]]
    board[start_pos[1]][start_pos[0]] = None
    board[end_pos[1]][end_pos[0]] = piece

# Game loop
running = True
while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = get_square_under_mouse()
            if selected_piece:
                move_piece(selected_pos, pos)
                selected_piece = None
                selected_pos = None
            else:
                selected_pos = pos
                selected_piece = board[pos[1]][pos[0]]
    pygame.display.flip()

pygame.quit()
sys.exit()