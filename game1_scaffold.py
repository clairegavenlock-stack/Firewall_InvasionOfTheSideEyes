import pygame
import sys
import math

# --- Pygame Setup ---

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

CLOCK = pygame.time.Clock()
score = 0
FONT = pygame.font.SysFont(None, 30)
HUD_COLOR = (255, 255, 255)

# PATH VARIABLES
PATH_Y = HEIGHT / 2 # Y position of the road
PATH_HEIGHT = 80
PATH_COLOR = (80, 80, 80)

# ENEMY VARIABLES
ENEMY_COLOR = (50, 250, 100)
ENEMY_IMAGE = pygame.image.load("enemy.jpg").convert_alpha()
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (30, 30))

# ------ ENEMY CLASS ---------
class Enemy:
    def __init__(self, path_y, speed, level):
        self.x = -20
        self.y = path_y
        self.speed = speed
        self.radius = 15

        # Level 1-2 starts with 2 Health, Level 3 starts with 3 Health etc.
        self.max_health = 2 + (level - 1) // 2
        self.health = self.max_health

        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        self.x = self.x + self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        #pygame.draw.circle(
        #    surface,
        #    ENEMY_COLOR,
        #    (int(self.x), int(self.y)),
        #    self.radius)
        surface.blit(self.image, self.rect)

        # Health Bar
        bar_width = 30
        bar_height = 5
        bar_x = int(self.x - bar_width // 2)
        bar_y = int(self.y - self.radius - 10)

        # Background 
        pygame.draw.rect(surface, (150, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))

        # Current health
        ratio = max(self.health, 0) / self.max_health
        pygame.draw.rect(surface, (0, 200, 0),
                        (bar_x, bar_y, int(bar_width * ratio), bar_height))

# ---- TOWER CLASS ------
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.size = 30
        self.cooldown = 5
        self.fire_rate = 35
    
    def get_target(self, enemies):
        # Find first enemy in range
        for e in enemies:
            dist = math.hypot(e.x - self.x, e.y - self.y)
            if dist <= self.range:
                return e
        return None
    
    def update(self, enemies, bullets):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        
        target = self.get_target(enemies)
        if target is not None:
            bullets.append(Bullet(self.x, self.y, target))
            self.cooldown = self.fire_rate
    
    def draw(self, surface):
        pygame.draw.rect(surface, (50, 150, 250),
                        (self.x - self.size//2, self.y - self.size//2,
                        self.size, self.size))
        pygame.draw.circle(surface, (100, 100, 200), (self.x, self.y),
                        self.range, 1)

# ---- BULLET CLASS -----
class Bullet:
    def __init__(self, x , y, target):
        self.x = x
        self.y = y
        self.speed = 5
        self.target = target
        self.radius = 5
        self.damage = 1
    
    def update(self):
        if self.target is None:
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

# --- Helper Functions ---
def draw_path(surface):
    rect = pygame.Rect(0, PATH_Y - PATH_HEIGHT // 2, WIDTH, PATH_HEIGHT)
    pygame.draw.rect(surface, PATH_COLOR, rect)

def draw_hud(surface, score, lives, level, money, tower_cost):
    text_score = FONT.render(f"Score: {score}", True, HUD_COLOR)
    text_lives = FONT.render(f"Lives: {lives}", True, HUD_COLOR)
    text_level = FONT.render(f"Level: {level}", True, HUD_COLOR)
    text_money = FONT.render(f"Money: {money}", True, HUD_COLOR)
    text_cost = FONT.render(f"Tower Cost: {tower_cost}", True, HUD_COLOR)

    surface.blit(text_score, (10, 10))
    surface.blit(text_lives, (10, 40))
    surface.blit(text_level, (10, 70))
    surface.blit(text_money, (10, 100))
    surface.blit(text_cost, (10, 130))

def can_place_tower_at(x, y):
    half_forbidden = PATH_HEIGHT // 2
    if abs(y - PATH_Y) <= half_forbidden:
        return False
    return True

def main():

    # Lists / Variables
    enemies = []
    bullets = []
    towers = []

    score = 0
    level = 1
    game_over = False

    tower_cost = 40
    kill_reward = 20

    money = 0
    lives = 0
    enemies_to_spawn = 3
    spawn_cooldown = 0
    time_between_spawns = 0

    message = ""
    message_timer = 0
    level_message = ""
    level_message_timer = 0

    def start_level(current_level):
        nonlocal enemies, towers, bullets
        nonlocal money, lives, enemies_to_spawn, spawn_cooldown, time_between_spawns
        nonlocal level_message, level_message_timer

        enemies = []
        towers = []
        bullets = []

        lives = 15
        money = 100 + (current_level - 1) * 20 # Start with more money each level

        enemies_to_spawn = 6 + current_level * 2
        spawn_cooldown = 0
        time_between_spawns = max(30, 55 - current_level * 3)

        level_message = f"Level {current_level}"
        level_message_timer = 180 # Shows for ~3 seconds (This will depend on your frames! e.g. currently 180 frames)

    start_level(level)

    # ----- MAIN GAME LOOP -----
    running = True
    while running:
        CLOCK.tick(60)  # 60 frames per second

        # Events loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                towers.append(Tower(mouse_x, mouse_y))

        # --- Update Game State ---
        if not game_over:
            if enemies_to_spawn > 0:
                if spawn_cooldown <= 0:
                    speed = 1.4 + 0.15 * (level -1)
                    enemies.append(Enemy(PATH_Y, speed, level))
                    enemies_to_spawn -= 1
                    spawn_cooldown = time_between_spawns
                else:
                    spawn_cooldown -= 1

            # ---- Updating Enemies ----
            for enemy in enemies:
                enemy.update()
                if enemy.x > WIDTH + enemy.radius:
                    enemies.remove(enemy)
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        break
            
            if not game_over and enemies_to_spawn == 0 and len(enemies) == 0:
                level += 1
                start_level(level)

        # ---- Updating Towers ----
        for tower in towers:
            if tower.cooldown > 0:
                tower.cooldown -= 1
            else:
                target = tower.get_target(enemies)
                if target is not None:
                    bullets.append(Bullet(tower.x, tower.y, target))
                    tower.cooldown = 60 # 30 frames means every 0.5 seconds at 60 fps

        # ---- Draw -----
        WIN.fill((30, 30, 30))  # dark background
        pygame.draw.rect(
            WIN,
            PATH_COLOR,
            (0, PATH_Y - PATH_HEIGHT // 2, WIDTH, PATH_HEIGHT)
        )
        for enemy in enemies:
            enemy.draw(WIN)
        for tower in towers:
            tower.draw(WIN)
        for bullet in bullets[:]:
            hit_enemy = None
            for enemy in enemies:
                dist = math.hypot(enemy.x - bullet.x, enemy.y - bullet.y)
                if dist < enemy.radius: # THIS MEANS YOUR BULLET IS INSIDE YOUR ENEMY RN
                    hit_enemy = enemy
                    break
            if hit_enemy:
                enemies.remove(hit_enemy)
                bullets.remove(bullet)
                score += 5
            bullet.update()
            bullet.draw(WIN)

        draw_hud(WIN, score, lives, level, money, tower_cost)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()