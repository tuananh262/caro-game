import pygame
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Set the position of the game window to the center of the screen
from components.button import createPrimaryButton, createSecondaryButton
from screens import ScreenHome
from constans import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

def main_menu():
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    ScreenHome(SCREEN)

main_menu()