import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

CLOCK = pygame.time.Clock()

running = True
while running:
    CLOCK.tick(60)  # 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WIN.fill((30, 30, 30))  # dark background

    pygame.display.flip()

pygame.quit()
sys.exit()
