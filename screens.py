import pygame
import sys
from components.button import createPrimaryButton, createSecondaryButton, createSmallText, createBigText
from constans import BACKGROUND_COLOUR, CENTER_X, WHITE, YELLOW, SQUARE_SIZE, SMALL_FONT_SIZE
from game import initialGame, drawBoard, checkWin, botMove


def ScreenInstruction(SCREEN):
    while True:
        INSTRUCTION_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        instructionText = ["The goal of Caro game is",
                           "to be the first player", "to get five in a row."]
        for i in range(len(instructionText)):
            ins = createSmallText(pos=(450, (SMALL_FONT_SIZE*2) * (i+1)),
                                  text_input=instructionText[i], background_color=WHITE)
            ins.update(SCREEN)

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
        MENU_TEXT = createBigText(
            pos=(CENTER_X, 175), text_input="CARO", text_color=YELLOW, background_color=BACKGROUND_COLOUR)
        MENU_TEXT.update(SCREEN)
        PLAY_BUTTON = createPrimaryButton(
            pos=(CENTER_X, 400), text_input="PLAY")
        INSTRUCTION_BUTTON = createPrimaryButton(
            pos=(CENTER_X, 550), text_input="INSTRUCTIONS")
        QUIT_BUTTON = createPrimaryButton(
            pos=(CENTER_X, 700), text_input="QUIT")
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
        drawBoard(board, SCREEN)
        pygame.display.update()
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // SQUARE_SIZE
                    col = pos[0] // SQUARE_SIZE
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        check_win = checkWin(board, 'X')
                        if check_win != 'play':
                            winner = check_win
                            game_over = True
                        botMove(board)
                        check_win = checkWin(board, 'O')
                        if check_win != 'play':
                            winner = check_win
                            game_over = True
            drawBoard(board, SCREEN)
            pygame.display.update()
            if game_over: break
        
        pygame.time.wait(3000)
        ScreenEndGame(SCREEN, winner)


def ScreenEndGame(SCREEN, winner):
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(WHITE)

        if winner is not None:
            WIN = createPrimaryButton((450, 300), (winner))
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
