import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Set the position of the game window to the center of the screen

pygame.init()
screen = pygame.display.set_mode((640, 480))  # Create a game window with the specified dimensions
pygame.display.set_caption('My Game')  # Set the title of the game window

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic and draw graphics here

    pygame.display.update()

pygame.quit()
