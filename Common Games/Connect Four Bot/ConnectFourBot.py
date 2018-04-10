import numpy as np
import random
import copy
import pygame
from pygame.locals import *
from PIL import Image
import sys

print "How fast would you like the bot to play? (Slower is harder)"
print "2 is less than half a second per turn. Easy"
print "3 is about 2 seconds or less. Medium"
print "4 is about 15 seconds or less. Hard"
print "Choose higher than 4 appreciating your mortality."
print "7 is up to an hour and a half per turn."
print "20+ is perfect play."

speed = input("Enter number here: ")

def findi(j, matrix):
    for i in range(6):
        if matrix[5 - i][j] == 0:
            return 5 - i
    return -1

def tog(turn):
    tog = turn - 1
    tog = 1 - tog
    return tog + 1

def check(i, j, matrix): #Safe way of getting a value from a matrix. (Doesn't crash)
    if i < 0 or j < 0 or i >= 6 or j >= 7:
        return -1
    return matrix[i][j]

def checkForEnd(i, j, turn, matrix):
    consecutive = 0
    for a in range(6):
        if check(a, j, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == 4:
                return 1
        else:
            consecutive = 0
    consecutive = 0
    for a in range(7):
        if check(i, a, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == 4:
                return 1
        else:
            consecutive = 0
    consecutive = 0
    for a in range(7):
        I = i + a - 3
        J = j - a + 3
        if check(I, J, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == 4:
                return 1
        else:
            consecutive = 0
    consecutive = 0
    for a in range(7):
        I = i + a - 3
        J = j + a - 3
        if check(I, J, matrix) == turn:
            consecutive = consecutive + 1
            if consecutive == 4:
                return 1
        else:
            consecutive = 0
    return 0

def appraise(matrix, turn): #also Flips players here.
    for j in range(7):
        i = findi(j, matrix)
        matrix2 = copy.deepcopy(matrix)
        matrix2[i][j] = turn
        if checkForEnd(i, j, turn, matrix2):
            if turn == 2:
                return 100
            return -100
    value = 0
    for j in range(7):
        I = findi(j, matrix)
        if I == 0:
            continue
        i = I - 1
        matrix2 = copy.deepcopy(matrix)
        matrix2[i][j] = 1
        if checkForEnd(i, j, 1, matrix2):
            value += -5
        matrix2[i][j] = 2
        if checkForEnd(i, j, 2, matrix2):
            value += 5
    for i in range(6):
        for j in range(7):
            if matrix[i][j]:
                n = tog(matrix[i][j])
                point = 1
                for a in (-1,0,1):
                    for b in (-1,0,1):
                        if a == 0 and b == 0:
                            continue
                        point = 1
                        for c in range(1, 4):
                            piece = check(i + c*a, j + c*b, matrix)
                            if piece == n or piece == -1:
                                point = 0
                                break
                        if point:
                            if n == 2: #This may seem weird. But it is flipped because at line 63 it flips the point to the enemy's number. Now it is flipped twice lol.
                                value += -1
                            else:
                                value += 1
    return value

def miniMax(matrix, turn, plies):
    for event in pygame.event.get(): #This is here because the bot spends a lot of time in this function.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if plies == 0:
        return appraise(matrix, turn)
    if turn == 2: #Flipped to 2 since bot is maximizing player.
        bestValue = -150
        for j in range(7):
            i = findi(j, matrix)
            if i == -1:
                continue
            matrix2 = copy.deepcopy(matrix)
            matrix2[i][j] = turn
            if checkForEnd(i, j, turn, matrix2):
                bestValue = 100
                break
            bestValue = max(bestValue, miniMax(matrix2, tog(turn), plies - 1))
        return bestValue
    else:
        bestValue = 150
        for j in range(7):
            i = findi(j, matrix)
            if i == -1:
                continue
            matrix2 = copy.deepcopy(matrix)
            matrix2[i][j] = turn
            if checkForEnd(i, j, turn, matrix2):
                bestValue = -100
                break
            bestValue = min(bestValue, miniMax(matrix2, tog(turn), plies - 1))
        return bestValue

pygame.init()
screen = pygame.display.set_mode((700,600))

Circ = [pygame.image.load("Images//Grey.jpg"),
        pygame.image.load("Images//Red.jpg"),
        pygame.image.load("Images//Black.jpg")]

def match():
    board = np.zeros((6,7))
    tclk = 1
    turn = 1
    waiting = 0
    for y in range(6):
        for x in range(7):
            screen.blit(Circ[0], [x*100,y*100])
    pygame.display.flip()
    while True:
        mpos = pygame.mouse.get_pos()
        mclk = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        mp = [0,0]
        J = mpos[0]/100
        I = mpos[1]/100
        if waiting and mclk and tclk:
            return 2
        if mclk and tclk and turn == 1:
            tclk = 0
            i = findi(J, board)
            if i == I:
                board[I][J] = 1
                turn = 2
                screen.blit(Circ[1], [J*100, I*100])
                if checkForEnd(I, J, 1, board):
                    pygame.display.flip()
                    R =  random.randint(1, 3)
                    image = Image.open("Images//RageQuit"+str(R)+".jpg")
                    image.show()
                    pygame.quit()
                    sys.exit()
        elif turn == 2: #The bot is the maximizing player.
            values = [0,0,0,0,0,0,0]
            for j in range(7):
                i = findi(j, board)
                if i == -1:
                    values[j] = -150
                    continue
                matrix2 = copy.deepcopy(board)
                matrix2[i][j] = 2
                if checkForEnd(i, j, 2, matrix2):
                    values[j] = 100
                    continue
                values[j] = miniMax(matrix2, 1, speed) #Usually have at 4
            ties = [0,0,0,0,0,0,0]
            print values
            Max = max(values)
            for j in range(7):
                if values[j] == Max:
                    ties[j] = 1
            while sum(ties) > 1:
                R = random.randint(0,6)
                if ties[R]:
                    ties[R] = 0
                    values[R] = values[R] - 1
            j = values.index(max(values))
            i = findi(j, board)
            board[i][j] = 2
            screen.blit(Circ[2], [j*100, i*100])
            turn = 1
            if checkForEnd(i, j, 2, board):
                print board
                R = random.randint(1, 6)
                image = Image.open("Images//Motivational"+str(R)+".jpg")
                image.show()
                print "Good Game!"
                waiting = 1
        elif mclk == 0:
            tclk = 1
        for j in range(7):
            if findi(j, board) != -1:
                playing = 1
                continue
        if playing == 0:
            print "Draw"
            return 0
        playing = 0
        pygame.display.flip()
while True:
    match()
