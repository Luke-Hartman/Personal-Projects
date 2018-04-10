import random, copy, time

Template = [[0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
                
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
                
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0]]

Medium = [[0,0,8, 0,1,6, 3,0,0],
          [0,3,0, 0,0,8, 6,0,0],
          [0,0,9, 3,7,0, 0,2,0],

          [2,0,0, 0,0,3, 1,4,8],
          [8,0,0, 0,2,0, 0,0,9],
          [6,1,4, 7,0,0, 0,0,2],

          [0,4,0, 0,9,7, 2,0,0],
          [0,0,6, 5,0,0, 0,1,0],
          [0,0,2, 4,6,0, 9,0,0]]

Easy = [[6,0,0, 1,0,8, 2,0,3],
        [0,2,0, 0,4,0, 0,9,0],
        [8,0,3, 0,0,5, 4,0,0],
           
        [5,0,4, 6,0,7, 0,0,9],
        [0,3,0, 0,0,0, 0,5,0],
        [7,0,0, 8,0,3, 1,0,2],
           
        [0,0,1, 7,0,0, 9,0,6],
        [0,8,0, 0,3,0, 0,2,0],
        [3,0,2, 9,0,4, 0,0,5]]

Hard = [[2,0,0, 0,0,1, 0,4,3],
        [0,0,0, 0,6,0, 0,0,0],
        [0,0,0, 4,9,0, 0,8,0],
           
        [8,0,0, 7,0,0, 0,0,2],
        [6,9,0, 0,0,0, 0,1,7],
        [0,0,4, 0,0,9, 8,0,0],
           
        [0,7,0, 6,4,0, 0,0,0],
        [0,0,0, 0,8,0, 0,0,0],
        [1,4,0, 0,0,2, 0,0,8]]

Impossible = [[4,0,0, 5,0,0, 1,0,0],
              [0,0,0, 0,0,7, 0,0,0],
              [0,0,8, 3,0,0, 0,0,4],

              [0,0,0, 0,0,2, 0,0,3],
              [0,7,0, 0,0,0, 0,2,0],
              [0,0,6, 8,0,0, 4,0,0],

              [0,1,0, 0,0,3, 0,0,0],
              [0,0,0, 9,0,0, 0,0,0],
              [0,2,0, 0,0,0, 8,4,7]]

Impossiblest = [[0,0,0, 0,8,3, 9,0,0],
                [1,0,0, 0,0,0, 0,3,0],
                [0,0,4, 0,0,0, 0,7,0],
                
                [0,4,2, 0,3,0, 0,0,0],
                [6,0,0, 0,0,0, 0,0,4],
                [0,0,0, 0,7,0, 0,1,0],
                
                [0,2,0, 0,0,0, 0,0,0],
                [0,8,0, 0,0,9, 2,0,0],
                [0,0,0, 2,5,0, 0,0,6]]
def box(coord):
    done = [0,0]
    box = [0,0]
    for i in range(3):
        for j in range(2):
            if coord[j] < (i + 1)*3 and done[j] == 0:
                box[j] = i
                done[j] = 1
    return box

def check(coord, n, board):
    if n == 0:
        return 0
    Box = box(coord)
    for i in range(3):
        for j in range(3):
            if board[i + Box[0]*3][j + Box[1]*3] == n:
                return 0
    for i in range(9):
        if board[coord[0]][i] == n:
            return 0
        if board[i][coord[1]] == n:
            return 0
    return 1

def place(board):
    for i in range(9):
        for j in range(9):
            Options = [0,0,0,0,0,0,0,0,0,0]
            if board[i][j]:
                continue
            for test in range(1, 10):
                if check([i, j], test, board):
                    Options[test] = 1
                    if sum(Options) > 1:
                        break
            if sum(Options) == 1:
                board[i][j] = Options.index(1)
                return 1
    return 0

def filled(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return 0
    print board
    return 1

def maybe(board):
    possible = []
    for i in range(9):
        for j in range(9):
            for test in range(1, 10):
                if board[i][j] == 0:
                    if check([i, j], test, board):
                        possible.append([i, j, test])
    return possible

def solve(board):
    start = time.time()
    while True:
        if place(board) == 0:
            break
    if filled(board):
        print "Time taken: " + str(time.time() - start)
        return 1
    #By here the board is "Mostly Solved"
    #The rest is basically a brute force attack on it! (Except worse since it is random...)

    possibilities = maybe(board)
    #start with checking 1 assumption of correctness. Then 2.
    length = len(possibilities)
    C = 0.0
    print board
    for a in possibilities:
        C += 1.0
        print str(round(C/length*100, 1)) + "%"
        #i = a[0] Mainly for human understanding.
        #j = a[1]
        #n = a[2]
        hypboard = copy.deepcopy(board)
        hypboard[a[0]][a[1]] = a[2]
        while True:
            if place(hypboard) == 0:
                break
        if filled(hypboard):
            print "Time taken: " + str(time.time() - start)
            return 1
        possibilities2 = maybe(hypboard)
        for b in possibilities2:
            hypboard2 = copy.deepcopy(hypboard)
            hypboard2[b[0]][b[1]] = b[2]
            while True:
                if place(hypboard2) == 0:
                    break
            if filled(hypboard2):
                print "Time taken: " + str(time.time() - start)
                return 1
    print "Failed... Sorry for making you wait!"
