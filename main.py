import pygame

# initializes pygame
pygame.init()

# creates view
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Heart of the Cards")

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False