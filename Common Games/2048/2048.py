import random
import copy
import sys
import pygame
from pygame.locals import *
def shiftL(matrix, score, win):
    for i in range(4):
        combined = [0]*4
        for j in range(4):
            value = matrix[i][j]
            if value == 0:
                continue
            J = j
            while True:
                J += -1
                if J == -1:
                    break
                if matrix[i][J] == 0:
                    matrix[i][J] = value
                    matrix[i][J + 1] = 0
                elif matrix[i][J] == value and combined[J] == 0:
                    matrix[i][J] = value + 1
                    matrix[i][J + 1] = 0
                    combined[J] = 1
                    score += 2**(value + 1)
                    if value + 1 == 11 and win == 0:
                        win = 1
                        print "Congratulations! You win!"
                        print "Don't worry, you can keep playing until your inevitable end!"
                else:
                    break
    return (matrix, score, win)

def shiftR(matrix, score, win):
    for i in range(4):
        combined = [0]*4
        for j in (3,2,1,0):
            value = matrix[i][j]
            if value == 0:
                continue
            J = j
            while True:
                J += 1
                if J == 4:
                    break
                if matrix[i][J] == 0:
                    matrix[i][J] = value
                    matrix[i][J - 1] = 0
                elif matrix[i][J] == value and combined[J] == 0:
                    matrix[i][J] = value + 1
                    matrix[i][J - 1] = 0
                    combined[J] = 1
                    score += 2**(value + 1)
                    if value + 1 == 11 and win == 0:
                        win = 1
                        print "Congratulations! You win!"
                        print "Don't worry, you can keep playing until your inevitable end!"
                else:
                    break
    return (matrix, score, win)

def shiftU(matrix, score, win):
    for j in range(4):
        combined = [0]*4
        for i in range(4):
            value = matrix[i][j]
            if value == 0:
                continue
            I = i
            while True:
                I += -1
                if I == -1:
                    break
                if matrix[I][j] == 0:
                    matrix[I][j] = value
                    matrix[I + 1][j] = 0
                elif matrix[I][j] == value and combined[I] == 0:
                    matrix[I][j] = value + 1
                    matrix[I + 1][j] = 0
                    combined[I] = 1
                    score += 2**(value + 1)
                    if value + 1 == 11 and win == 0:
                        win = 1
                        print "Congratulations! You win!"
                        print "Don't worry, you can keep playing until your inevitable end!"
                else:
                    break
    return (matrix, score, win)

def shiftD(matrix, score, win):
    for j in range(4):
        combined = [0]*4
        for i in (3,2,1,0):
            value = matrix[i][j]
            if value == 0:
                continue
            I = i
            while True:
                I += 1
                if I == 4:
                    break
                if matrix[I][j] == 0:
                    matrix[I][j] = value
                    matrix[I - 1][j] = 0
                elif matrix[I][j] == value and combined[I] == 0:
                    matrix[I][j] = value + 1
                    matrix[I - 1][j] = 0
                    combined[I] = 1
                    score += 2**(value + 1)
                    if value + 1 == 11 and win == 0:
                        win = 1
                        print "Congratulations! You win!"
                        print "Don't worry, you can keep playing until your inevitable end!"
                else:
                    break
    return (matrix, score, win)

def randPlace(matrix):
    r = random.randint
    if r(0,9) == 0:
        n = 2
    else:
        n = 1
    while True:
        i = r(0,3)
        j = r(0,3)
        if matrix[i][j] == 0:
            matrix[i][j] = n
            return matrix

def redraw():
    pygame.draw.rect(screen, (187,173,160), pygame.Rect(0, 0, 750, 850))
    b = screen.blit
    for i in range(4):
        for j in range(4):
            b(Images[matrix[i][j]], (10 + 185*j, 10 + 185*i))
    myfont = pygame.font.SysFont("ariel", 100)
    label = myfont.render("Score: " + str(score), 1, (249,246,242))
    b(label, (50,765))
    pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode((750,850))
pygame.display.set_caption("2048 by Luke Hartman")
pygame.draw.rect(screen, (187,173,160), pygame.Rect(0, 0, 750, 850))

l = pygame.image.load
Images = [l("Images/0.jpg"),
          l("Images/2.jpg"),
          l("Images/4.jpg"),
          l("Images/8.jpg"),
          l("Images/16.jpg"),
          l("Images/32.jpg"),
          l("Images/64.jpg"),
          l("Images/128.jpg"),
          l("Images/256.jpg"),
          l("Images/512.jpg"),
          l("Images/1024.jpg"),
          l("Images/2048.jpg"),
          l("Images/4096.jpg")]

while True:
    matrix = [[0,0,0,0],
              [0,0,0,0],
              [0,0,0,0],
              [0,0,0,0]]
    randPlace(matrix)
    randPlace(matrix)
    score = 0
    redraw()
    Pressed = 1
    waiting = 0
    win = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        if waiting:
            if key[13]:
                break
            continue
        if key[273] or key[274] or key[275] or key[276]:
            c = copy.deepcopy
            before = c(matrix)
            if Pressed == 0:
                if key[273]:
                    R = shiftU(matrix, score, win)
                    matrix = R[0]
                    score = R[1]
                    win = R[2]
                elif key[274]:
                    R = shiftD(matrix, score, win)
                    matrix = R[0]
                    score = R[1]
                    win = R[2]
                elif key[275]:
                    R = shiftR(matrix, score, win)
                    matrix = R[0]
                    score = R[1]
                    win = R[2]
                elif key[276]:
                    R = shiftL(matrix, score, win)
                    matrix = R[0]
                    score = R[1]
                    win = R[2]
                if before != matrix:
                    randPlace(matrix)
                    redraw()
                else:
                    test = c(matrix)
                    Pass = 0
                    if before != shiftU(test,0,1)[0]:
                        Pass = 1
                        test = c(matrix)
                    elif before != shiftD(test,0,1)[0]:
                        Pass = 1
                        test = c(matrix)
                    elif before != shiftR(test,0,1)[0]:
                        Pass = 1
                        test = c(matrix)
                    elif before == shiftL(test,0,1)[0]:
                        print "You attained a score of: " + str(score)
                        print "Press enter to play again!"
                        waiting = 1
            Pressed = 1
        else:
            Pressed = 0
