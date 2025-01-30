import pygame
import math
import random

# Inicializar Pygame
pygame.init()

# Constantes del juego
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 3
FOV = math.pi / 3

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREY = (40, 40, 40)

# Estados del juego
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Raycaster:
    def __init__(self, map_data):
        self.map = map_data
        self.wall_textures = {
            1: pygame.Surface((64, 64)),
            2: pygame.Surface((64, 64))
        }
        self._generate_textures()
    
    def _generate_textures(self):
        for tex in self.wall_textures.values():
            tex.fill((random.randint(50,200), random.randint(50,200), random.randint(50,200)))

class Player:
    def __init__(self, pos):
        self.pos = list(pos)
        self.angle = 0.0
        self.health = 100
        self.ammo = 50
        self.weapon = "Pistol"
        self.score = 0

class Enemy:
    def __init__(self, pos):
        self.pos = list(pos)
        self.health = 100
        self.speed = 1.0
        self.sprite = pygame.Surface((20, 20))
        self.sprite.fill(RED)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.level = 1
        self.init_game()
    
    def init_game(self):
        self.map = [
            [1,1,1,1,1,1,1],
            [1,0,0,0,0,0,1],
            [1,0,1,0,2,0,1],
            [1,0,0,0,0,0,1],
            [1,0,2,0,1,0,1],
            [1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1]
        ]
        self.player = Player((3.5, 3.5))
        self.enemies = [Enemy((2.5, 2.5)) for _ in range(3)]
        self.raycaster = Raycaster(self.map)
        self.bullets = []
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("RETRO DOOM", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        menu_items = [
            ("Start Game", (WIDTH//2 - 100, HEIGHT//2)),
            ("Quit", (WIDTH//2 - 100, HEIGHT//2 + 60))
        ]
        
        for text, pos in menu_items:
            btn = pygame.Rect(pos[0], pos[1], 200, 50)
            color = RED if btn.collidepoint(pygame.mouse.get_pos()) else DARK_GREY
            pygame.draw.rect(self.screen, color, btn)
            
            font = pygame.font.Font(None, 36)
            text_surf = font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=btn.center)
            self.screen.blit(text_surf, text_rect)
    
    def cast_ray(self, pos, angle):
        ray_dir = (math.cos(angle), math.sin(angle))
        map_pos = (int(pos[0]), int(pos[1]))
        delta_dist = (
            abs(1 / ray_dir[0]) if ray_dir[0] != 0 else float('inf'),
            abs(1 / ray_dir[1]) if ray_dir[1] != 0 else float('inf')
        )
        
        step = [0, 0]
        side_dist = [0.0, 0.0]
        hit_side = 0
        
        if ray_dir[0] < 0:
            step[0] = -1
            side_dist[0] = (pos[0] - map_pos[0]) * delta_dist[0]
        else:
            step[0] = 1
            side_dist[0] = (map_pos[0] + 1.0 - pos[0]) * delta_dist[0]
            
        if ray_dir[1] < 0:
            step[1] = -1
            side_dist[1] = (pos[1] - map_pos[1]) * delta_dist[1]
        else:
            step[1] = 1
            side_dist[1] = (map_pos[1] + 1.0 - pos[1]) * delta_dist[1]
            
        while True:
            if side_dist[0] < side_dist[1]:
                side_dist[0] += delta_dist[0]
                map_pos = (map_pos[0] + step[0], map_pos[1])
                hit_side = 0
            else:
                side_dist[1] += delta_dist[1]
                map_pos = (map_pos[0], map_pos[1] + step[1])
                hit_side = 1
                
            if map_pos[0] < 0 or map_pos[1] < 0 or map_pos[0] >= len(self.map[0]) or map_pos[1] >= len(self.map):
                break
                
            if self.map[map_pos[1]][map_pos[0]] > 0:
                distance = (map_pos[0] - pos[0] + (1 - step[0])/2) / ray_dir[0] if hit_side == 0 else \
                          (map_pos[1] - pos[1] + (1 - step[1])/2) / ray_dir[1]
                return distance, self.map[map_pos[1]][map_pos[0]], hit_side
        
        return float('inf'), 0, 0
    
    def draw_3d_view(self):
        # Dibujar paredes
        for x in range(WIDTH):
            ray_angle = self.player.angle - FOV/2 + (x/WIDTH) * FOV
            distance, wall_id, side = self.cast_ray(self.player.pos, ray_angle)
            
            if distance < float('inf'):
                wall_height = HEIGHT / (distance + 0.0001)
                color = self.raycaster.wall_textures[wall_id].get_at((x%64, int(wall_height%64)))
                color = [c//2 if side else c for c in color]
                pygame.draw.line(self.screen, color, 
                               (x, HEIGHT//2 - wall_height//2),
                               (x, HEIGHT//2 + wall_height//2))
        
        # Dibujar enemigos
        for enemy in sorted(self.enemies, key=lambda e: -math.hypot(e.pos[0]-self.player.pos[0], e.pos[1]-self.player.pos[1])):
            dx = enemy.pos[0] - self.player.pos[0]
            dy = enemy.pos[1] - self.player.pos[1]
            distance = math.hypot(dx, dy)
            
            angle_to_player = math.atan2(dy, dx) - self.player.angle
            if angle_to_player < -math.pi:
                angle_to_player += 2*math.pi
            elif angle_to_player > math.pi:
                angle_to_player -= 2*math.pi
            
            if abs(angle_to_player) < FOV/2:
                screen_x = int((angle_to_player + FOV/2) * WIDTH / FOV)
                size = min(500, int(HEIGHT / distance * 100))
                
                sprite_rect = pygame.Rect(
                    screen_x - size//2,
                    HEIGHT//2 - size//2,
                    size, size
                )
                
                self.screen.blit(pygame.transform.scale(enemy.sprite, (size, size)), sprite_rect)
    
    def draw_weapon(self):
        # Dibujar arma en primer plano
        weapon = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.rect(weapon, DARK_GREY, (50, 50, 100, 50))
        self.screen.blit(weapon, (WIDTH//2 - 100, HEIGHT - 200))
    
    def draw_hud(self):
        # Health bar
        pygame.draw.rect(self.screen, RED, (20, HEIGHT-80, 200, 30))
        pygame.draw.rect(self.screen, GREEN, (20, HEIGHT-80, 2*self.player.health, 30))
        
        # Info text
        font = pygame.font.Font(None, 36)
        texts = [
            f"Ammo: {self.player.ammo}",
            f"Level: {self.level}",
            f"Health: {self.player.health}%"
        ]
        
        for i, text in enumerate(texts):
            text_surf = font.render(text, True, WHITE)
            self.screen.blit(text_surf, (20 + 200*i, HEIGHT-40))
        
        self.draw_weapon()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_speed = PLAYER_SPEED * 0.1
        rot_speed = 0.05
        
        if keys[pygame.K_w]:
            self.player.pos[0] += math.cos(self.player.angle) * move_speed
            self.player.pos[1] += math.sin(self.player.angle) * move_speed
        if keys[pygame.K_s]:
            self.player.pos[0] -= math.cos(self.player.angle) * move_speed
            self.player.pos[1] -= math.sin(self.player.angle) * move_speed
        if keys[pygame.K_a]:
            self.player.angle -= rot_speed
        if keys[pygame.K_d]:
            self.player.angle += rot_speed
        
        if keys[pygame.K_SPACE]:
            if len(self.bullets) < 3 and self.player.ammo > 0:
                self.bullets.append({
                    'pos': list(self.player.pos),
                    'angle': self.player.angle,
                    'distance': 0
                })
                self.player.ammo -= 1
        
        self.player.angle %= 2 * math.pi
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet['pos'][0] += math.cos(bullet['angle']) * 0.3
            bullet['pos'][1] += math.sin(bullet['angle']) * 0.3
            bullet['distance'] += 0.3
            
            for enemy in self.enemies[:]:
                if math.hypot(bullet['pos'][0]-enemy.pos[0], bullet['pos'][1]-enemy.pos[1]) < 0.5:
                    enemy.health -= 25
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.player.score += 100
                    try:
                        self.bullets.remove(bullet)
                    except ValueError:
                        pass
                    break
            
            if bullet['distance'] > 10:
                try:
                    self.bullets.remove(bullet)
                except ValueError:
                    pass
    
    def update_enemies(self):
        for enemy in self.enemies:
            dx = self.player.pos[0] - enemy.pos[0]
            dy = self.player.pos[1] - enemy.pos[1]
            distance = math.hypot(dx, dy)
            
            if distance > 0.5:
                enemy.pos[0] += dx/distance * enemy.speed * 0.05
                enemy.pos[1] += dy/distance * enemy.speed * 0.05
            else:
                self.player.health -= 0.1
    
    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.state == MENU:
                    mouse_pos = pygame.mouse.get_pos()
                    if (WIDTH//2 - 100) <= mouse_pos[0] <= (WIDTH//2 + 100):
                        if (HEIGHT//2) <= mouse_pos[1] <= (HEIGHT//2 + 50):
                            self.state = PLAYING
                        elif (HEIGHT//2 + 60) <= mouse_pos[1] <= (HEIGHT//2 + 110):
                            pygame.quit()
                            return
            
            if self.state == MENU:
                self.draw_menu()
                
            elif self.state == PLAYING:
                self.handle_input()
                self.update_bullets()
                self.update_enemies()
                
                self.screen.fill(BLACK)
                self.draw_3d_view()
                self.draw_hud()
                
                # Dibujar balas
                for bullet in self.bullets:
                    x = int(bullet['pos'][0] * 100)
                    y = int(bullet['pos'][1] * 100)
                    pygame.draw.circle(self.screen, GREEN, (x, y), 3)
                
                if self.player.health <= 0:
                    self.state = GAME_OVER
                    
            elif self.state == GAME_OVER:
                self.screen.fill(BLACK)
                font = pygame.font.Font(None, 72)
                text = font.render("GAME OVER", True, RED)
                text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(text, text_rect)
                
                restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
                pygame.draw.rect(self.screen, RED, restart_btn)
                btn_font = pygame.font.Font(None, 36)
                btn_text = btn_font.render("Restart", True, WHITE)
                self.screen.blit(btn_text, (restart_btn.x + 60, restart_btn.y + 15))
                
                if pygame.mouse.get_pressed()[0]:
                    if restart_btn.collidepoint(pygame.mouse.get_pos()):
                        self.__init__()
                        self.state = PLAYING

            pygame.display.flip()

if __name__ == "__main__":
    Game().run()