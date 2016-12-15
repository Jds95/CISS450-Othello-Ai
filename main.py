
# ------------------------------------------
# Authors: Jesse Simpson and Micahel Thomas
# ------------------------------------------

# ------------------------------------------
# File: main.py
# ------------------------------------------
import os, copy
# 8 directions
dirx = [-1, 1, 0, 0, -1, 1, -1, 1]
diry = [-1, 1, -1, 1, 1, -1, 0, 0]

# Starting min value
minEvalBoard = -1000000 

# Starting max value
maxEvalBoard = 1000000

def MakeMove(board, size, x, y, player): 
    total = 0
    board[y][x] = player
    for d in range(8):
        ctr = 0
        for i in range(size):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > size - 1 or dy < 0 or dy > size - 1:
                ctr = 0; break
            elif board[dy][dx] == player:
                break
            elif board[dy][dx] == ' ':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            board[dy][dx] = player
        total += ctr
    return (board, total)

def ValidMove(board, size, x, y, player):
    # Check for Invalid move less than 0 or greater than our index
    if x < 0 or x > size - 1 or y < 0 or y > size - 1:
        return False
    if board[y][x] != ' ':
        return False
    
    total = 0
    for d in range(8):
        ctr = 0
        for i in range(size):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > size - 1 or dy < 0 or dy > size - 1:
                ctr = 0; break
            elif board[dy][dx] == player:
                break
            elif board[dy][dx] == ' ':
                ctr = 0; break
            else:
                ctr += 1
        total += ctr
        
    #(boardTemp, total) = MakeMove(copy.deepcopy(board), size, x, y, player)
    if total == 0:
        return False
    return True

def Corners(board, size):
    t = size - 1
    #weight = 50 # should only be used if we also compute if we could take the
                 #corner next turn or so...(ie grade the squares near the corner)
    topLeft = 0 if board[0][0] == ' ' else 1 if board[0][0] == black else -1
    topRight = 0 if board[0][t] == ' ' else 1 if board[0][t] == black else -1
    botLeft = 0 if board[t][0] == ' ' else 1 if board[t][0] == black else -1
    botRight = 0 if board[t][t] == ' ' else 1 if board[t][t] == black else -1
    
    if topLeft+topRight+botLeft+botRight == 0: 
        return 0
    return 100 * (topLeft + topRight + botLeft + botRight) / \
           (abs(topLeft) + abs(topRight) + abs(botLeft) + abs(botRight))

def PieceCount(board, size):
    black = 0
    white = 0
    for r in board:
        for c in r:
            if c == ' ':
                pass
            if c == black:
                black += 1
            else:
                white += 1
    return 100 * (black - white)/(black + white)
    
def Mobility(board, size):
    black = 0
    white = 0
    for x, r in enumerate(board):
        for y, c in enumerate(r):
            if ValidMove(board, size, x, y, 'B'):
                black += 1
            if ValidMove(board, size, x, y, 'W'):               
                white += 1
    if (black + white == 0):
        return 0
    return 100 * (black - white) / (black + white)

def StabilityTest0(board, size, player, x, y):
    ret = 0
    for d in range(4):
        side1 = 0
        side2 = 0
        # looking for opponent pieces that can take this
        for i in range(size - 2):
            # one side
            if (not side1):
                dx = x + dirx[2*d] * (i + 1)
                dy = y + diry[2*d] * (i + 1)
                if dx < 0 or dx > size - 1 or dy < 0 or dy > size - 1:
                    side1 = 0
                elif board[dy][dx] == ' ':
                    side1 = 0
                elif board[dy][dx] == player:
                    side1 = 0
                elif abs(dy - y) <= 1 and abs(dx - x) <= 1:
                    side1 = 1
            if (not side2):
                # other side
                dx = x + dirx[2*d+1]
                dy = y + diry[2*d+1]
                if dx < 0 or dx > size - 1 or dy < 0 or dy > size - 1:
                    side2 = 0
                elif board[dy][dx] == ' ':
                    side2 = 0
                elif board[dy][dx] == player:
                    side2 = 0
                else:
                    side2 = 1
            if (side1 and side2):
                side1 = 0
                side2 = 0
                break
        if (side1 or side2):
            ret += 1
            break # remove if we want to count the same piece
                  # more than once, ie. recognize pieces are super
                  # unstable
    return ret

def StabilityTest1RowCalc(board, size, player, y, L, R):
    ret = 0
    
    contiguous = True
    endpoint = -1
    if L:
        for x in range(1, size - 1, 1):
            if board[x][y] != player:
                contiguous = False
                endpoint = x
                break
            ret += 1
            if x == size - 2:
                if contiguous:
                    endpoint = size - 2
                else:
                    endpoint = size - 3
    
    contiguous = True
    if R:
        for x in range(size - 1, 0, -1):
            if x > endpoint:
                if board[x][y] != player:
                    contiguous = False
                    endpoint = x
                    break
                ret += 1
            else:
                break
    return ret

def StabilityTest1ColCalc(board, size, player, x, T, B):
    ret = 0
    
    contiguous = True
    endpoint = -1
    if T:
        for y in range(1, size - 1, 1):
            if board[x][y] != player:
                contiguous = False
                endpoint = y
                break
            ret += 1
            if y == size - 2:
                if contiguous:
                    endpoint = size - 2
                else:
                    endpoint = size - 3
    
    contiguous = True
    if B:
        for y in range(size - 1, 0, -1):
            if y > endpoint:
                if board[x][y] != player:
                    contiguous = False
                    endpoint = y
                    break
                ret += 1
            else:
                break
    return ret
    

def StabilityTest1(board, size, player, x, y):
    ret = 0

    topLeft = 1 if board[0][0] == player else 0 
    topRight = 1 if board[0][size-1] == player else 0
    botLeft = 1 if board[size-1][0] == player else 0
    botRight = 1 if board[size-1][size-1] == player else 0

    ret += StabilityTest1RowCalc(board, size, player, 0, topLeft, topRight)
    ret += StabilityTest1RowCalc(board, size, player, size-1, botLeft, botRight)
    ret += StabilityTest1ColCalc(board, size, player, 0, topLeft, botLeft)
    ret += StabilityTest1ColCalc(board, size, player, size-1, topRight, botRight)
    ret += topLeft + topRight + botLeft + botRight
    return ret


def Stability(board, size, player):
    total = 0
    stable = 0     #stable + 1
    semiStable = 0 #semistable +0
    unstable = 0   #unstable -1
    for x in range(size):
        for y in range(size):
            if board[x][y] is player:
                total += 1
                #check the piece's stability
                unstable += StabilityTest0(board, size, player, x, y)
    stable += StabilityTest1(board, size, player, x, y)
    unstable = total - stable - semiStable

    return 100 * (stable - unstable) / (total)

def EvalBoard(board, size, player):
    #tot = 0
    #for y in range(size):
    #    for x in range(size):
    #        if board[y][x] == player:
    #            # Corner check
    #            if (x == 0 or x == size - 1) and (y == 0 or y == size - 1):
    #                tot += 4
    #            # Side Check
    #            elif (x == 0 or x == size - 1) or (y == 0 or y == size - 1):
    #                tot += 2
    #            else:
    #                tot += 1
    #return tot
    return PieceCount(board, size) + Corners(board, size) \
          + Mobility(board, size)  #+ Stability(board, size, player) + 

# Test to see if part of tree we are at is out of moves
def noMoveCheck(board, size, player):
    for y in range(size):
        for x in range(size):
            if ValidMove(board, size, x, y, player):
                return False
    return True

def AlphaBeta(board, size, player, depth, alpha, beta, maximizingPlayer):

    if depth == 0 or noMoveCheck(board, size, player):
        return EvalBoard(board, size, player)
    if maximizingPlayer:
        v = minEvalBoard
        for y in range(size):
            for x in range(size):
                if ValidMove(board, size, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), size, x, y, player)
                    v = max(v, AlphaBeta(boardTemp, size, 'W', depth - 1, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break # beta cut-off
        return v
    else: # minimizingPlayer
        v = maxEvalBoard
        for y in range(size):
            for x in range(size):
                if ValidMove(board, size, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), size, x, y, player)
                    v = min(v, AlphaBeta(boardTemp, size, 'B', depth - 1, alpha, beta, True))
                    beta = min(beta, v)
                    if beta <= alpha:
                        break # alpha cut-off
        return v

def BestMove(board, size, player, depth):
    maxPoints = -10000
    mx = -1; my = -1
    for y in range(size):
        for x in range(size):
            if ValidMove(board, size, x, y, player):
                #(boardTemp, totctr) = MakeMove(copy.deepcopy(board), size, x, y, player)
                points = AlphaBeta(board, size, player, depth, minEvalBoard, maxEvalBoard, player=='B') # True inidicates maximizing our move
                if points > maxPoints:
                    maxPoints = points
                    mx = x; my = y
    return [my, mx]

def get_move(board_size, board_state, turn, time_left, opponent_time_left):

    if time_left > 240000:
        move = BestMove(board_state, board_size, turn, 6)
    elif time_left > 160000:
        move = BestMove(board_state, board_size, turn, 4)
    elif time_left > 80000:
        move = BestMove(board_state, board_size, turn, 3)
    else:
        move = BestMove(board_state, board_size, turn, 2)        

    if move != [-1, -1]:
        return move
    else:
        return None

# def InitBoard(size):
#     if size % 2 == 0: # if board size is even
#         z = (size - 2) / 2
#         board[z][z] = 'B'
#         board[size - 1 - z][z] = 'W'        
#         board[z][size - 1 - z] = 'W'
#         board[size - 1 - z][size - 1 - z] = 'B'

# def PrintBoard():
#     m = len(str(8 - 1))
#     for y in range(8):
#         row = ''
#         for x in range(8):
#             row += board[y][x] 
#             row += ' ' * m
#         print row + ' ' + str(y)
#     print
#     row = ''
#     for x in range(8):
#         row += str(x).zfill(m) + ' '
#     print row + '\n'

# def swap_turn(turn):
#     if turn == 'B':
#         return 'W'
#     else:
#         return 'B'

# bsize = 8 #input()
# board = [[' ' for x in range(bsize)] for y in range(bsize)]
# InitBoard(bsize)
# while True:
#     print
#     PrintBoard()
#     turn = 'B'        
#     (x, y) = get_move(bsize, board, turn, 1000000, 1000000)
#     if not (x == -1 and y == -1):
#             (board, totctr) = MakeMove(board, bsize, x, y, turn)
#             print 'User played (X Y): ' + str(x) + ' ' + str(y)
#             print '# of pieces taken: ' + str(totctr)
#     turn = swap_turn(turn)
#     print
#     PrintBoard()
#     (x, y) = get_move(bsize, board, turn, 1000000, 1000000)
#     if not(x == -1 and y == -1):
#         (board, totctr) = MakeMove(board, bsize, x, y, turn)
#         print 'AI played (X Y): ' + str(x) + ' ' + str(y)
#         print '# of pieces taken: ' + str(totctr)
