import pygame
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


def is_empty(board):
    return board == [[' ']*len(board)]*len(board)


def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)


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
    tie = True
    winner = 'Winner: ' + player
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if tie == True and board[i][j] == ' ':
                tie = False
            if board[i][j] == player:
                # check horizontal
                if j + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i][j+k] == player:
                            count += 1
                    if count == 5:
                        return winner
                # check vertical
                if i + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i+k][j] == player:
                            count += 1
                    if count == 5:
                        return winner
                # check diagonal up
                if i - 4 >= 0 and j + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i-k][j+k] == player:
                            count += 1
                    if count == 5:
                        return winner
                # check diagonal down
                if i + 4 < BOARD_SIZE and j + 4 < BOARD_SIZE:
                    count = 1
                    for k in range(1, 5):
                        if board[i+k][j+k] == player:
                            count += 1
                    if count == 5:
                        return winner
    if tie:  # check tie
        return 'tie'
    return 'play'


def botMove(board):
    bestmove = best_move(board, 'O')
    board[bestmove[0]][bestmove[1]] = 'O'


def march(board, y, x, dy, dx, length):
    '''
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    '''
    yf = y + length*dy
    xf = x + length*dx
    # chừng nào yf,xf không có trong board
    while not is_in(board, yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf


def score_ready(scorecol):
    '''
    Khởi tạo hệ thống điểm

    '''
    sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1

    return sumcol


def sum_sumcol_values(sumcol):
    '''
    hợp nhất điểm của mỗi hướng
    '''

    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())


def score_of_list(lis, col):

    blank = lis.count(' ')
    filled = lis.count(col)

    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled


def row_to_list(board, y, x, dy, dx, yf, xf):
    '''
    trả về list của y,x từ yf,xf

    '''
    row = []
    while y != yf + dy or x != xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row


def score_of_row(board, cordi, dy, dx, cordf, col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    '''
    colscores = []
    y, x = cordi
    yf, xf = cordf
    row = row_to_list(board, y, x, dy, dx, yf, xf)
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5], col)
        colscores.append(score)

    return colscores


def score_of_col(board, col):
    '''
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    '''

    f = len(board)
    # scores của 4 hướng đi
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(len(board)):
        scores[(0, 1)].extend(score_of_row(
            board, (start, 0), 0, 1, (start, f-1), col))
        scores[(1, 0)].extend(score_of_row(
            board, (0, start), 1, 0, (f-1, start), col))
        scores[(1, 1)].extend(score_of_row(
            board, (start, 0), 1, 1, (f-1, f-1-start), col))
        scores[(-1, 1)].extend(score_of_row(board,
                                            (start, 0), -1, 1, (0, start), col))

        if start + 1 < len(board):
            scores[(1, 1)].extend(score_of_row(
                board, (0, start+1), 1, 1, (f-2-start, f-1), col))
            scores[(-1, 1)].extend(score_of_row(board,
                                                (f - 1, start + 1), -1, 1, (start+1, f-1), col))

    return score_ready(scores)


def score_of_col_one(board, col, y, x):
    '''
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(score_of_row(board, march(
        board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), col))

    scores[(1, 0)].extend(score_of_row(board, march(
        board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), col))

    scores[(1, 1)].extend(score_of_row(board, march(
        board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), col))

    scores[(-1, 1)].extend(score_of_row(board, march(board, y,
                                                     x, -1, 1, 4), 1, -1, march(board, y, x, 1, -1, 4), col))

    return score_ready(scores)


def possible_moves(board):
    '''
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    '''
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # cord: lưu các vị trí không đi
    cord = {}

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i, j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    '''
    for direction in directions:
        dy, dx = direction
        for coord in taken:
            y, x = coord
            for length in [1, 2, 3, 4]:
                move = march(board, y, x, dy, dx, length)
                if move not in taken and move not in cord:
                    cord[move] = False
    return cord


def TF34score(score3, score4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    '''
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False


def stupid_score(board, col, anticol, y, x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế 
    '''

    global colors
    M = 1000
    res, adv, dis = 0, 0, 0

    # tấn công
    board[y][x] = col
    # draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board, col, y, x)
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]

    # phòng thủ
    board[y][x] = anticol
    sumanticol = score_of_col_one(board, anticol, y, x)
    d = winning_situation(sumanticol)
    dis += d * (M-100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4 * \
        sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

    res = adv + dis

    board[y][x] = ' '
    return res


def winning_situation(sumcol):
    '''
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''

    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4]) >= 2 or (len(sumcol[4]) >= 1 and max(sumcol[4].values()) >= 2):
        return 4
    elif TF34score(sumcol[3], sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def best_move(board, col):
    '''
    trả lại điểm số của mảng trong lợi thế của từng màu
    '''
    if col == 'O':
        anticol = 'X'
    else:
        anticol = 'O'

    movecol = (0, 0)
    maxscorecol = ''
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi

    moves = possible_moves(board)

    for move in moves:
        y, x = move
        if maxscorecol == '':
            scorecol = stupid_score(board, col, anticol, y, x)
            maxscorecol = scorecol
            movecol = move
        else:
            scorecol = stupid_score(board, col, anticol, y, x)
            if scorecol > maxscorecol:
                maxscorecol = scorecol
                movecol = move
    return movecol
