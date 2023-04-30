import pygame
import sys
from components.button import get_font, createPrimaryButton, createSecondaryButton
from constans import BACKGROUND_COLOUR, CENTER_X, WHITE, YELLOW, SQUARE_SIZE
from game import initialGame, drawBoard, checkWin, checkTie, botMove


def ScreenInstruction(SCREEN):
    while True:
        INSTRUCTION_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        instructionText = ["The goal of Caro game is",
                           "to be the first player", "to get five in a row."]
        for i in range(len(instructionText)):
            ins = get_font(30).render(instructionText[i], True, "Black")
            insRect = ins.get_rect(center=(450, 200 + i * 50))
            SCREEN.blit(ins, insRect)

        INSTRUCTION_BACK = createSecondaryButton(
            pos=(450, 800), text_input="BACK")
        INSTRUCTION_BACK.changeColor(INSTRUCTION_MOUSE_POS, SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTION_BACK.checkForInput(INSTRUCTION_MOUSE_POS):
                    ScreenHome(SCREEN)

        pygame.display.update()


def ScreenHome(SCREEN):
    while True:
        SCREEN.fill(BACKGROUND_COLOUR)
        mousePos = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("CARO", True, YELLOW)
        MENU_RECT = MENU_TEXT.get_rect(center=(CENTER_X, 175))
        PLAY_BUTTON = createPrimaryButton(
            pos=(CENTER_X, 400), text_input="PLAY")
        INSTRUCTION_BUTTON = createPrimaryButton(
            pos=(CENTER_X, 550), text_input="INSTRUCTIONS")
        QUIT_BUTTON = createPrimaryButton(
            pos=(CENTER_X, 700), text_input="QUIT")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, INSTRUCTION_BUTTON, QUIT_BUTTON]:
            button.changeColor(mousePos, SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mousePos):
                    ScreenGame(SCREEN)
                if INSTRUCTION_BUTTON.checkForInput(mousePos):
                    ScreenInstruction(SCREEN)
                if QUIT_BUTTON.checkForInput(mousePos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def ScreenGame(SCREEN):
    while True:
        SCREEN.fill(WHITE)
        game_over, winner, board = initialGame()
        while not game_over:
            drawBoard(board, SCREEN)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // SQUARE_SIZE
                    col = pos[0] // SQUARE_SIZE
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        if checkWin(board, 'X'):
                            winner = 'X'
                            game_over = True
                            break
                        elif checkTie(board):
                            game_over = True
                            break
                        botMove(board)
                        if checkWin(board, 'O'):
                            winner = 'O'
                            game_over = True
                        elif checkTie(board):
                            game_over = True

        ScreenEndGame(SCREEN, winner)


def ScreenEndGame(SCREEN, winner):
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(WHITE)

        if winner is not None:
            WIN = createPrimaryButton((450, 300), ("WINNER: " + winner))
            WIN.changeColor(mouse_pos, SCREEN)
            REPLAY = createPrimaryButton((450, 450), "REPLAY")
            REPLAY.changeColor(mouse_pos, SCREEN)
            BACK = createSecondaryButton((450, 600), "BACK")
            BACK.changeColor(mouse_pos, SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if REPLAY.checkForInput(mouse_pos):
                        ScreenGame(SCREEN)
                    if BACK.checkForInput(mouse_pos):
                        ScreenHome(SCREEN)
        else:
            TIED = createPrimaryButton((450, 300), "TIED")
            TIED.update(SCREEN)
            REPLAY = createPrimaryButton((450, 450), "REPLAY")
            REPLAY.changeColor(mouse_pos, SCREEN)
            BACK = createSecondaryButton((450, 600), "BACK")
            BACK.changeColor(mouse_pos, SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if REPLAY.checkForInput(mouse_pos):
                        ScreenGame(SCREEN)
                    if BACK.checkForInput(mouse_pos):
                        ScreenHome(SCREEN)
        pygame.display.update()
