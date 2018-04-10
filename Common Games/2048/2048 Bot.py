import random
import copy
import sys
import pygame
from pygame.locals import *

N = input("How fast would you like this to play? (do 1 or 2) ")

r = random.randint
c = copy.deepcopy

def shift(matrix, score, move):
    if move == 0: #Left
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
                    else:
                        break
    if move == 1: #Right
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
                    else:
                        break
    if move == 2: #Up
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
                    else:
                        break
    if move == 3: #Down
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
                    else:
                        break
    return (matrix, score)

def check(matrix, i, j):
    if i > 3 or j > 3 or i < 0 or j < 0:
        return -1
    return matrix[i][j]

def branch(matrix, used, index, node):
    for a in used:
        if a == index:
            return -1
    i = index[0]
    j = index[1]
    Base = check(matrix, i, j)
    if  Base == -1:
        print "or here"
        return -1
    used.append(index)
    branches = [0]
    Check = check(matrix, i + 1, j)
    if 0 < Check <= node:
        branches.append(branch(matrix, used, (i + 1, j), Check))
    Check = check(matrix, i, j + 1)
    if 0 < Check <= node:
        branches.append(branch(matrix, used, (i, j + 1), Check))
    Check = check(matrix, i - 1, j)
    if 0 < Check <= node:
        branches.append(branch(matrix, used, (i - 1, j), Check))
    Check = check(matrix, i, j - 1)
    if 0 < Check <= node:
        branches.append(branch(matrix, used, (i, j - 1), Check))
    Max = max(branches)
    return 2**Base + Max

'''
original appraise for not-needing-to-remake-it purposes!
def appraise(matrix):
    Max = max(max(matrix))
    Indexes = []
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == Max:
                Indexes.append((i, j))
    L = len(Indexes)
    Choices = []
    for index in Indexes:  
        Choices.append(branch(matrix, [], index, Max))
    return max(Choices)
'''

def appraise(matrix):
    #Adding small ammendments now (Modifiers scale based on the largest number to stay ubiquitously (Word of the day) valued.) 
    #Testing having absurd penalties to try and ensure conformist behaviors.
    Max = max(max(matrix))
    
    #1st Ammendment:
    Ammendment1 = -float(Max)/2
    # WAS "Thou shalt not have 2's surrounded by larger numbers." (-25 each or a eight of max)
    # NOW "Thou shalt not have numbers surrounded by larger numbers." (So that they cannot combine.)
    
    #2nd Ammendment:
    Ammendment2 = Max*4
    # Thou shalt attempteth to have ye' largest in teh corner. (+50 or equal to max)
    
    #3rd Ammendment:
    Ammendment3 = 5
    # Thou shalt value blank spaces. (+5 each)

    value = 0
    Indexes = []
    for i in range(4):
        for j in range(4):
            cell = matrix[i][j]
            if cell == Max:
                Indexes.append((i, j))
            elif cell == 0:
                value += Ammendment3
            elif (-1 < check(matrix, i + 1, j) < cell + 1 or -1 < check(matrix, i, j + 1) < cell + 1 or -1 < check(matrix, i - 1, j) < cell + 1 or -1 < check(matrix, i, j - 1) < cell +1) is False:
                value += Ammendment1
    L = len(Indexes)
    Choices = []
    for index in Indexes:
        modifier = 0
        for i in (0,3): #Ammendment 2
            for j in (0,3):
                if index == (i, j):
                    modifier = Ammendment2
        Choices.append(branch(matrix, [], index, Max) + modifier)
    value += max(Choices)
    return value

def expectimax(n, matrix):
    if n == 0:
        return appraise(matrix)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    addvalue = 0
    z = 0
    for i in range(4):
        for j in range(4):
            if matrix[i][j]:
                continue
            z += 1
            values = [0]*4
            best = [0]*2
            for place in range(2):
                for move in range(4):
                    matrix2 = c(matrix)
                    matrix2[i][j] = place + 1
                    values[move] = expectimax(n - 1, matrix2)
                best[place] = max(values)
            addvalue += best[0]*0.9 + best[1]*0.1
    return float(addvalue)/(z + 1)

def randPlace(matrix):
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
    while True:
        before = c(matrix)
        values = [0]*4
        for move in range(4):
            R = shift(c(matrix), score, move)
            if R[0] != before:
               values[move] = expectimax(N, R[0])
        I = values.index(max(values))
        R = shift(c(matrix), score, I)
        matrix = R[0]
        score = R[1]
        if before != matrix:
            randPlace(matrix)
            redraw()
        else:
            print "Attained a score of: " + str(score)
            break
