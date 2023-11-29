import sys

import pygame

# initializes pygame
pygame.init()

# creates view
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()


# Title and Icon
pygame.display.set_caption("Heart of the Cards")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
