import math, numpy as np, pygame, sys
from pygame.locals import *


colors = [(0,0,0), (255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0), (255,0,255), (0,255,255), (127,127,127), (127,0,0), (0,0,127), (0,127,0), (127,127,0), (127,0,127), (0,127,127), (255,127,127)]
scale = 0
size = 0
#This is to avoid the crap that is python's matrix1 = matrix2
def copyMatrix(matrix):
    blank = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            blank[i][j] = matrix[i][j]
    return blank

def int2str(n):
    if n < 10:
        return "0" + str(int(n))
    else:
        return str(int(n))

def str2mat(string):
    L = int(math.sqrt(len(string)/2))
    matrix = np.zeros((L,L))
    for a in range(L):
        for b in range(L):
            c = 2*(a*L + b)
            n = int(string[c] + string[c + 1])
            matrix[a][b] = n
    return matrix

def str2lis(string):
    L = int(len(string)/2)
    lis = np.zeros((L))
    for a in range(L):
        c = 2*a
        n = int(string[c] + string[c+1])
        lis[a] = n
    return lis

def mat2str(matrix):
    L = len(matrix)
    string = ""
    for a in range(L):
        for b in range(L):
            n = matrix[a][b]
            string = string + int2str(n)
    return string

def lis2str(lis):
    string = ""
    for a in range(len(lis)):
        n = lis[a]
        string = string + int2str(n)
    return string
        
def check(i, j):
    if i >= size or i < 0 or j >= size or j < 0:
        return -1
    return board[i][j]

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
    up = check(coord[0] - 1, coord[1])
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
    down = check(coord[0] + 1, coord[1])
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
    left = check(coord[0], coord[1] - 1)
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
    right = check(coord[0], coord[1] + 1)
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
            if check(i, j) > 0:
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

def territory():
    territory = []
    C = -1
    for i in range(size):
        for j in range(size):
            if check(i, j) == 0:
                n = c2n(i, j)
                alreadygrouped = 0
                for a in range(len(territory)):
                    if gcheck(a, n, territory) == 0:
                        alreadygrouped = 1
                if alreadygrouped == 0:
                    C = C + 1
                    territory.append([n])
                    while True:
                        D = 0
                        for b in range(len(territory[C])):
                            E = 0
                            num = territory[C][b]
                            if up(C, num, territory):
                                territory[C].append(num - size)
                                E = 1
                                
                            if down(C, num, territory):
                                territory[C].append(num + size)
                                E = 1
                                
                            if left(C, num, territory):
                                territory[C].append(num - 1)
                                E = 1

                            if right(C, num, territory):
                                territory[C].append(num + 1)
                                E = 1
                                
                            if E:
                                D = 1
                                break                        
                        if D == 0 and E == 0:
                            break
    return territory

def score(territory):
    Score = np.zeros(players)
    for a in range(len(territory)):
        Claimed = 0
        for b in range(len(territory[a])):
            coord = n2c(territory[a][b])
            i = coord[0]
            j = coord[1]
            
            c = check(i - 1, j)
            if c > 0:
                if Claimed == 0:
                    Claimed = c
                elif Claimed != c:
                    Claimed = -1
                    break

            c = check(i + 1, j)
            if c > 0:
                if Claimed == 0:
                    Claimed = c
                elif Claimed != c:
                    Claimed = -1
                    break
                
            c = check(i, j - 1)
            if c > 0:
                if Claimed == 0:
                    Claimed = c
                elif Claimed != c:
                    Claimed = -1
                    break
                
            c = check(i, j + 1)
            if c > 0:
                if Claimed == 0:
                    Claimed = c
                elif Claimed != c:
                    Claimed = -1
                    break    
        if Claimed > 0:
            Oldscore = Score[int(Claimed - 1)]
            Score[int(Claimed - 1)] = Oldscore + len(territory[a])
    return Score

def liberties(a, groups):
    for b in range(len(groups[a])):
        coord = n2c(groups[a][b])
        i = coord[0]
        j = coord[1]
        if check(i + 1, j) == 0:
            return 1
        if check(i - 1, j) == 0:
            return 1
        if check(i, j + 1) == 0:
            return 1
        if check(i, j - 1) == 0:
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
    print("(Press Enter to save during a game)")
    ask = raw_input("Which file would you like to load? (No .txt) (Blank for new game.) ")
              
    if len(ask) > 0:
        f = open(ask + ".txt", "r")
        R = f.read()
        Vars = R.split()
        players = int(Vars[0])
        turn = int(Vars[1])
        board = str2mat(Vars[2])
        captured = str2lis(Vars[3])
        size = len(board)
    else:
        size = int(raw_input("What sized board would you like to use? "))
        players = int(raw_input("How many players? Current version supports 2 - 16! "))
        board = np.zeros((size,size))
        captured = np.zeros((players))
        turn = 1

    scale = int(raw_input("What scale would you like to use this game? (Each tile is 12*scale pixels) "))

    pygame.init()
    screen = pygame.display.set_mode((12*scale*size, 12*scale*(size + 1)))
    pygame.display.set_caption("Go by Luke Hartman v1.2")

    Tile = pygame.image.load("images/Background.png")
    Tile = pygame.transform.scale(Tile, (12*scale, 12*scale))
    
    box()
    redraw()
    Pass = 0
    ko = []
    for i in range(players):
        ko.append([-1,-1])
    while True:
        mclk = pygame.mouse.get_pressed()[0]
        key = pygame.key.get_pressed()
        if key[32] and kclk:
            Name = raw_input("Enter Name of Save File: ")
            f = open(Name+".txt", 'w')
            W = int2str(players) + " " + int2str(turn) + " " + mat2str(board) + " " + lis2str(captured)
            f.write(W)
            f.close()
            kclk = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if mclk and tclk:
            mpos = pygame.mouse.get_pos()
            j = mpos[0]/12/scale
            i = mpos[1]/12/scale
            tclk = 0
            if i == size:
                Pass = Pass + 1
                if Pass == players:
                    Score = score(territory())
                    print "Game Over"
                    for a in range(players):
                        print "player " + str(int(a + 1)) + " had " + str(int(captured[a])) + " captured pieces."
                    print ""
                    for a in range(players):
                        print "player " + str(int(a + 1)) + " had " + str(int(Score[a])) + " territory."
                    print ""
                    for a in range(players):
                        print "player " + str(int(a + 1)) + " has " + str(int(Score[a] - captured[a])) + " points!"
                    raw_input("Enter to start a new game. ")
                    break
                if turn == players:
                    turn = 1
                else:
                    turn = turn + 1
                box()
                pygame.display.flip()
                continue
            Pass = 0
            n = board[i][j]
            test = ko[turn - 1]
            fail = 1
            if test[0] != i or test[1] != j:
                fail = 0
            if n == 0 and fail == 0:
                oldboard = copyMatrix(board)
                board[i][j] = turn
                groups = group()
                newgroups = []
                canmove = 1
                for a in range(len(groups)):
                    coord = n2c(groups[a][0])
                    piece = board[coord[0]][coord[1]]
                    if piece != turn and liberties(a, groups) == 0:
                        captured[int(piece - 1)] = captured[int(piece - 1)] + len(groups[a])
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
                    if players < turn + 1:
                        turn = 1
                    else:
                        turn = turn + 1
                    box()
                    redraw()
                else:
                    board = copyMatrix(oldboard)
        if mclk == 0:
            tclk = 1
        if key[32] == 0:
            kclk = 1
