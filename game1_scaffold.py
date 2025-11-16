import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

CLOCK = pygame.time.Clock()

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

running = True
while running:
    CLOCK.tick(60)  # 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WIN.fill((30, 30, 30))  # dark background

    #enemy_x = enemy_x + ENEMY_SPEED
    #if enemy_x > WIDTH: # Go back when you've reached end of screen
    #    enemy_x = -20

    for enemy in enemies:
        enemy.update()

    pygame.draw.rect(
        WIN,
        PATH_COLOR,
        (0, PATH_Y - PATH_HEIGHT // 2, WIDTH, PATH_HEIGHT)
    )

    for enemy in enemies:
        enemy.draw(WIN)

    pygame.display.flip()

pygame.quit()
sys.exit()
