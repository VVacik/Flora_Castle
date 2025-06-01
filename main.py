import pygame
from level_manager import LevelManager

pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
fullscreen = False
level_manager = LevelManager()

dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1280, 720))

                    level_manager.recalc_layout(screen)

    level_manager.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

