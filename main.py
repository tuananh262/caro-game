import pygame, sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Set the position of the game window to the center of the screen
from button import Button
# Import game module
from nhetvao import run_game
import random
import math


pygame.init()

SCREEN = pygame.display.set_mode((900, 900))

pygame.display.set_caption("Tic Tac Toe")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        run_game()
        main_menu()
        pygame.display.update()

    
def INSTRUCTION():
    while True:
        INSTRUCTION_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        INSTRUCTION_TEXT = get_font(14).render("The goal of Caro game is to be the first player to get five in a row our given map. ", True, "Black")
        INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(450, 260))
        SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)

        INSTRUCTION_BACK = Button(image=None, pos=(450, 600), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        INSTRUCTION_BACK.changeColor(INSTRUCTION_MOUSE_POS)
        INSTRUCTION_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTION_BACK.checkForInput(INSTRUCTION_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CARO", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 175))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(450, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        INSTRUCTION_BUTTON = Button(image=pygame.image.load("assets/INSTRUCTION Rect.png"), pos=(450, 550), 
                            text_input="INSTRUCTION", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(450, 700), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, INSTRUCTION_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if INSTRUCTION_BUTTON.checkForInput(MENU_MOUSE_POS):
                    INSTRUCTION()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()