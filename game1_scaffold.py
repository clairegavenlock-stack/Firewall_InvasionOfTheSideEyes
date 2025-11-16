import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

CLOCK = pygame.time.Clock()
score = 0
font = pygame.font.SysFont(None, 30)

# PATH VARIABLES
PATH_Y = HEIGHT / 2 # Y position of the road
PATH_HEIGHT = 80
PATH_COLOR = (80, 80, 80)

# ENEMY VARIABLES
#enemy_x = 0
#enemy_y = PATH_Y
#ENEMY_SPEED = 2
ENEMY_COLOR = (50, 250, 100)
ENEMY_IMAGE = pygame.image.load("enemy.jpg").convert_alpha()
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (30, 30))

# ------ ENEMY CLASS ---------
class Enemy:
    def __init__(self, path_y):
        self.x = -20
        self.y = path_y
        self.speed = 2
        self.radius = 15

        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def update(self):
        self.x = self.x + self.speed
        if self.x > WIDTH:
            self.x = -20

        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        #pygame.draw.circle(
        #    surface,
        #    ENEMY_COLOR,
        #    (int(self.x), int(self.y)),
        #    self.radius
        surface.blit(self.image, self.rect)
        

# ---- Create Enemies -----
enemies = [Enemy(PATH_Y) for _ in range(3)]

for i, e in enumerate(enemies):
    e.x = -20 - i * 150 # Spreading it out to the left

# ---- TOWER CLASS ------
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.size = 30
        self.cooldown = 10
    
    def get_target(self, enemies):
        # Find first enemy in range
        for e in enemies:
            dist = math.hypot(e.x - self.x, e.y - self.y)
            if dist <= self.range:
                return e
        return None
    
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

# Lists
bullets = []
towers = []

# ----- MAIN GAME LOOP -----
running = True
while running:
    CLOCK.tick(60)  # 60 frames per second

    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            towers.append(Tower(mouse_x, mouse_y))

    # ---- Updating Enemies ----
    for enemy in enemies:
        enemy.update()

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
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
