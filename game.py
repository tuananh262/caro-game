import pygame
import math
from constans import BOARD_SIZE, SQUARE_SIZE, BLACK, RED

pygame.init()
# set the font
FONT_SIZE = 48
font = pygame.font.SysFont('calibri', FONT_SIZE)


def initializeBoard():
    return [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def initialGame():
    # initialize pygame: game_over = false, winner = none, board = emptyBoard
    return False, None, initializeBoard()


# define the maximum depth of the search tree
MAX_DEPTH = 1


def drawBoard(board, SCREEN):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            rect = pygame.Rect(j * SQUARE_SIZE, i *
                               SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            if board[i][j] == 'X':
                text = font.render('X', True, RED)
                text_rect = text.get_rect(center=rect.center)
                SCREEN.blit(text, text_rect)
            elif board[i][j] == 'O':
                text = font.render('O', True, RED)
                text_rect = text.get_rect(center=rect.center)
                SCREEN.blit(text, text_rect)


def checkWin(board, player):
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
def checkTie(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                return False
    return True


def scoreBoard(board):
    if checkWin(board, 'O'):
        return 1
    elif checkWin(board, 'X'):
        return -1
    else:
        return 0


def minimax(board, depth, alpha, beta, is_maximizing):
    score = scoreBoard(board)
    if score != 0 or depth == MAX_DEPTH:
        return score

    if is_maximizing:
        max_score = -math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth+1, alpha, beta, False)
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
                    score = minimax(board, depth+1, alpha, beta, True)
                    board[i][j] = ' '
                    min_score = min(min_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return min_score


def botMove(board):
    best_score = -math.inf
    best_move = None
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    board[best_move[0]][best_move[1]] = 'O'
