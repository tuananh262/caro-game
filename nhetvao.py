import pygame
import random
import math
from button import Button

# initialize pygame
pygame.init()

# set the dimensions of the window
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
BOARD_SIZE = 5
SQUARE_SIZE = WINDOW_WIDTH // BOARD_SIZE

# set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# set the font
FONT_SIZE = 48
font = pygame.font.SysFont('calibri', FONT_SIZE)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# create the board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# set the starting player
current_player = 'X'

# set the game state
game_over = False
winner = None

# define the maximum depth of the search tree
MAX_DEPTH = 1

# draw the board
def draw_board():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            rect = pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(window, BLACK, rect, 1)
            if board[i][j] == 'X':
                text = font.render('X', True, RED)
                text_rect = text.get_rect(center=rect.center)
                window.blit(text, text_rect)
            elif board[i][j] == 'O':
                text = font.render('O', True, RED)
                text_rect = text.get_rect(center=rect.center)
                window.blit(text, text_rect)

# check for a win
def check_win(player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                # check horizontal
                if j + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i][j+k] == player:
                            count += 1
                    if count == 5:
                        return True
                # check vertical
                if i + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i+k][j] == player:
                            count += 1
                    if count == 5:
                        return True
                # check diagonal up
                if i - 4 >= 0 and j + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i-k][j+k] == player:
                            count += 1
                    if count == 5:
                        return True
                # check diagonal down
                if i + 4 < BOARD_SIZE and j + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i+k][j+k] == player:
                            count += 1
                    if count == 5:
                        return True
    return False


# function to check if the game is tied
def check_tie():
     for i in range(BOARD_SIZE):
         for j in range(BOARD_SIZE):
             if board[i][j] == ' ':
                 return False
     return True

def score_board():
    if check_win('O'):
        return 1
    elif check_win('X'):
        return -1
    else:
        return 0

def minimax(depth, alpha, beta, is_maximizing):
    score = score_board()
    if score != 0 or depth == MAX_DEPTH:
        return score
    
    if is_maximizing:
        max_score = -math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(depth+1, alpha, beta, False)
                    board[i][j] = ' '
                    max_score = max(max_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return max_score
    else:
        min_score = math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(depth+1, alpha, beta, True)
                    board[i][j] = ' '
                    min_score = min(min_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return min_score

def bot_move():
    best_score = -math.inf
    best_move = None
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(0, -math.inf, math.inf, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    board[best_move[0]][best_move[1]] = 'O'

def run_game():
    game_over = False
    # current_player = 'X'
    winner = None
    window.fill(WHITE)
    
    while not game_over:
        draw_board()
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
                    if check_win('X'):
                        winner = 'X'
                        game_over = True
                        break
                    elif check_tie():
                        game_over = True
                        break
                    bot_move()
                    if check_win('O'):
                        winner = 'O'
                        game_over = True
                    elif check_tie():
                        game_over = True
    mouse_pos=pygame.mouse.get_pos()
    window.fill(WHITE) 
    if winner is not None:
        WIN = Button(image=None, pos=(450, 300), text_input=winner+" WIN", font=get_font(75), base_color="RED", hovering_color=None)
        WIN.update(window)
        REPLAY = Button(image=None, pos=(450, 450), text_input="REPLAY", font=get_font(75), base_color="Yellow", hovering_color="Grey")
        REPLAY.changeColor(mouse_pos)
        REPLAY.update(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY.checkForInput(mouse_pos):
                    run_game()
        BACK = Button(image=None, pos=(450, 600), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Grey")
        BACK.changeColor(mouse_pos)
        BACK.update(window)

        pygame.display.update()
        
    else:
        TIED = Button(image=None, pos=(450, 300), text_input="TIED", font=get_font(75), base_color="Blue", hovering_color=None)
        TIED.update(window)
        REPLAY = Button(image=None, pos=(450, 450), text_input="REPLAY", font=get_font(75), base_color="Yellow", hovering_color="Grey")
        REPLAY.changeColor(mouse_pos)
        REPLAY.update(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY.checkForInput(mouse_pos):
                    run_game()
        BACK = Button(image=None, pos=(450, 600), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Grey")
        BACK.changeColor(mouse_pos)
        BACK.update(window)
        
        pygame.display.update()
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
# run_game()