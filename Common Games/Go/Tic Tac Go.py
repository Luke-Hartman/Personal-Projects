import numpy as np, math, pygame, sys
from pygame.locals import *

colors = [(0,0,0), (255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0), (255,0,255), (0,255,255), (127,127,127), (127,0,0), (0,0,127), (0,127,0), (127,127,0), (127,0,127), (0,127,127), (255,127,127)]
scale = 0
size = 0

board = np.zeros((size,size))

def copyMatrix(matrix):
    blank = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            blank[i][j] = matrix[i][j]
    return blank

def next(n): #Simply a function to change turn.
    if n + 1 > players:
        return 1
    return n + 1

def check(i, j, matrix): #Safe way of getting a value from a matrix. (Doesn't crash)
    if i < 0 or j < 0 or i >= size or j >= size:
        return -1
    return matrix[i][j]

def checkforend(i, j, turn, matrix):
    consecutive = 0
    for a in range(row*2 - 1):
        if check(i + a - row + 1, j, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == row:
                return 1
        else:
            consecutive = 0
    consecutive = 0
    for a in range(row*2 - 1):
        if check(i, j + a - row + 1, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == row:
                return 1
        else:
            consecutive = 0
    consecutive = 0
    for a in range(row*2 - 1):
        I = i + a - 3
        J = j - a + 3
        if check(I, J, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == row:
                return 1
        else:
            consecutive = 0
    consecutive = 0
    for a in range(row*2 - 1):
        I = i + a - 3
        J = j + a - 3
        if check(I, J, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == row:
                return 1
        else:
            consecutive = 0
    return 0

def c2n(i, j):
    return int(size*i + j)

def n2c(num):
    i = int(math.floor(num/size))
    j = int(num - i*size)
    return [i, j]

def up(a, num, groups):
    pos = n2c(groups[a][0])
    t = board[pos[0]][pos[1]]
    coord = n2c(num)
    up = check(coord[0] - 1, coord[1], board)
    if up == t:
        for b in range(len(groups[a])):
            if groups[a][b] == (num - size):
                return 0
        return 1
    return 0

def down(a, num, groups):
    pos = n2c(groups[a][0])
    t = board[pos[0]][pos[1]]
    coord = n2c(num)
    down = check(coord[0] + 1, coord[1], board)
    if down == t:
        for b in range(len(groups[a])):
            if groups[a][b] == (num + size):
                return 0
        return 1
    return 0

def left(a, num, groups):
    pos = n2c(groups[a][0])
    t = board[pos[0]][pos[1]]
    coord = n2c(num)
    left = check(coord[0], coord[1] - 1, board)
    if left == t:
        for b in range(len(groups[a])):
            if groups[a][b] == (num - 1):
                return 0
        return 1
    return 0

def right(a, num, groups):
    pos = n2c(groups[a][0])
    t = board[pos[0]][pos[1]]
    coord = n2c(num)
    right = check(coord[0], coord[1] + 1, board)
    if right == t:
        for b in range(len(groups[a])):
            if groups[a][b] == (num + 1):
                return 0
        return 1
    return 0

def gcheck(a, num, matrix):
    for b in range(len(matrix[a])):
        if matrix[a][b] == num:
            return 0
    return 1

def group():
    groups = []
    C = -1
    for i in range(size):
        for j in range(size):
            if check(i, j, board) > 0:
                n = c2n(i, j)
                alreadygrouped = 0
                for a in range(len(groups)):
                    if gcheck(a, n, groups) == 0:
                        alreadygrouped = 1
                if alreadygrouped == 0:
                    C = C + 1
                    groups.append([n])
                    while True:
                        D = 0
                        for b in range(len(groups[C])):
                            E = 0
                            num = groups[C][b]
                            if up(C, num, groups):
                                groups[C].append(num - size)
                                E = 1
                                
                            if down(C, num, groups):
                                groups[C].append(num + size)
                                E = 1
                                
                            if left(C, num, groups):
                                groups[C].append(num - 1)
                                E = 1

                            if right(C, num, groups):
                                groups[C].append(num + 1)
                                E = 1
                                
                            if E:
                                D = 1
                                break                        
                        if D == 0 and E == 0:
                            break
    return groups

def liberties(a, groups):
    for b in range(len(groups[a])):
        coord = n2c(groups[a][b])
        i = coord[0]
        j = coord[1]
        if check(i + 1, j, board) == 0:
            return 1
        if check(i - 1, j, board) == 0:
            return 1
        if check(i, j + 1, board) == 0:
            return 1
        if check(i, j - 1, board) == 0:
            return 1
    return 0
def box():
    l = 0
    t = 12*scale*size
    w = 12*scale*size
    h = 12*scale*size
    pygame.draw.rect(screen, colors[int(turn - 1)], pygame.Rect(l, t, w, h))

def redraw():
    for i in range(size):
        for j in range(size):
            pos = [j*12*scale, i*12*scale]
            n = board[i][j]
            screen.blit(Tile, pos)
            if n > 0:
                pygame.draw.circle(screen, colors[int(n - 1)], (j*12*scale + 6*scale, i*12*scale + 6*scale), 6*scale)
    pygame.display.flip()

while True:
    turn = 1
    size = input("What sized board would you like to use? ")
    players = input("How many players? Current version supports 2 - 16! ")
    board = np.zeros((size,size))
    ko = []
    for i in range(players):
        ko.append([-1,-1])
    row = input("How many consecutive pieces to win? ")
    scale = int(raw_input("What scale would you like to use this game? (Each tile is 12*scale pixels) "))

    pygame.init()
    screen = pygame.display.set_mode((12*scale*size, 12*scale*(size + 1)))
    pygame.display.set_caption("Tic Tac Go by Luke Hartman")

    Tile = pygame.image.load("images/Background.png")
    Tile = pygame.transform.scale(Tile, (12*scale, 12*scale))
    
    box()
    redraw()
    while True:
        mclk = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if mclk and tclk:
            mpos = pygame.mouse.get_pos()
            j = mpos[0]/12/scale
            i = mpos[1]/12/scale
            tclk = 0
            if check(i, j, board) == 0:
                test = ko[turn - 1]
                fail = 1
                if test[0] != i or test[1] != j:
                    fail = 0
                if fail:
                    continue
                board[i][j] = turn
                oldboard = copyMatrix(board)
                board[i][j] = turn
                groups = group()
                newgroups = []
                canmove = 1
                for a in range(len(groups)):
                    coord = n2c(groups[a][0])
                    piece = board[coord[0]][coord[1]]
                    if piece != turn and liberties(a, groups) == 0:
                        if len(groups[a]) == 1:
                            ko[int(piece - 1)] = coord
                    else:
                        newgroups.append(groups[a])
                newboard =  np.zeros((size,size))
                for a in range(len(newgroups)):
                    for b in range(len(newgroups[a])):
                        coord = n2c(newgroups[a][b])
                        x = coord[0]
                        y = coord[1]
                        newboard[x][y] = board[x][y]
                board = copyMatrix(newboard)
                for a in range(len(newgroups)):
                    coord = n2c(newgroups[a][0])
                    piece = board[coord[0], coord[1]]
                    if piece == turn:
                        if liberties(a, newgroups) == 0:
                            canmove = 0
                if canmove:
                    newboard =  np.zeros((size,size))
                    for a in range(len(newgroups)):
                        for b in range(len(newgroups[a])):
                            coord = n2c(newgroups[a][b])
                            x = coord[0]
                            y = coord[1]
                            newboard[x][y] = board[x][y]
                    board = copyMatrix(newboard)
                    restart = 0
                    if checkforend(i, j, turn, board):
                        print "Player " + str(turn) + " wins!"
                        pygame.quit()
                        restart = 1
                    turn = next(turn)
                    box()
                    redraw()
                    if restart:
                        break
        if mclk == 0:
            tclk = 1
