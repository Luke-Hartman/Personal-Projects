import pygame
from pygame.locals import *
from pygame import gfxdraw
import random
import sys

class Card(object):
    amount = 0
    color = ''
    pattern = ''
    shape = ''
    held = False
    inSet = False
    pos = ()
    def __init__(self, info, pos):
        self.amount = int(info[0]) + 1
        self.color = info[1]
        self.pattern = info[2]
        self.shape = info[3]
        self.pos = pos
    def __str__(self):
        return str(self.amount-1) + self.color + self.pattern + self.shape

pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
screen = pygame.display.set_mode((w,h),pygame.FULLSCREEN)
pygame.display.set_caption("Luke's Set Assistant")
images = {}
colors = ["Red", "Green","Purple"]
patterns = ["Empty", "Striped", "Solid"]
shapes = ["Diamond", "Pill", "Squigle"]
for a in range(3):
    for b in range(3):
        for c in range(3):
            im = pygame.image.load("Images/" + colors[a] + patterns[b] + shapes[c] + ".jpg")
            images[str(a) + str(b) + str(c)] = pygame.transform.scale(im, (50,100))

def isSpecial(a, b, c):
    if a == b == c:
        return True
    if a != b and a != c and b != c:
        return True
    return False

def isSet(card1, card2, card3):
    for a in range(4):
        if not isSpecial(str(card1)[a], str(card2)[a], str(card3)[a]):
            return False
    return True

def drawCard(card, top, left, force=False):
    width = 315
    height = 225
    if card.held and not force:
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(left, top, width, height))
    else:
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(left, top, width, height))
        if card.inSet:
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(left, top, width, height), 15)
        else:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(left, top, width, height), 3)
        if card.amount == 1:
            offsets = [130]
        if card.amount == 2:
            offsets = [80, 180]
        if card.amount == 3:
            offsets = [60, 130, 200]
        for a in range(card.amount):
            screen.blit(images[str(card)[1:]], (left + offsets[a], top + 60))

def getCoord(x, y):
    if 60<=x<=375:
        j = 0
    elif 430<=x<=745:    
        j = 1
    elif 800<=x<=1115:
        j = 2
    elif 1170<=x<=1485:
        j = 3
    elif 1540<=x<=1855:
        j = 4
    else:
        return (-1, -1)
    if 10<=y<=235:
        i = 0
    elif 280<=y<=505:
        i = 1
    elif 550<=y<=775:
        i = 2
    else:
        return (-1, -1)
    return (i, j)

def getCard(i, j):
    for card in cards:
        if card.pos == (i, j):
            return card

def redraw():
    if solved:
        screen.fill((50,50,50))
    else:
        screen.fill((100,0,0))
    left = 0
    top = 800
    width = 1920
    height = 280
    pygame.draw.rect(screen, (100,100,100), pygame.Rect(left, top, width, height))
    if creating:
        l = len(creatingCard)
        newCards = []
        for a in range(3):
            newCards.append(Card(creatingCard + str(a) + '0'*(3-l), creatingCoords))
            drawCard(newCards[a], top + 30, left + 430 + 370*a)

    for card in cards:
        i, j = card.pos
        left = j*370 + 60
        top = i*270 + 10
        drawCard(card, top, left)
    for i in range(3):
        for j in range(5):
            left = j*370 + 60
            top = i*270 + 10
            width = 315
            height = 225
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(left, top, width, height), 5)
    if holding:
        drawCard(heldCard, mpos[1], mpos[0], True)
    pygame.display.flip()

cards = []
holding = False
solved = False
occupied = [[False for j in range(5)] for i in range(3)]
creatingCard = ''
creatingCoords = (-1,-1)
creating = False
redraw()
mtog = True
mtog2 = True
keyTog = True
for card in cards:
    i, j = card.pos
    occupied[i][j] = True
while True:
    pygame.time.Clock().tick(60)
    mpos = pygame.mouse.get_pos()
    mclk = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    x, y = mpos
    if mclk[0] and not creating:
        if mtog:
            mtog = False
            i, j = getCoord(x, y)
            if i != -1 and occupied[i][j]:
                card = getCard(i, j)
                card.held = True
                holding = True
                heldCard = card
        if holding:
            redraw()
    if not mclk[0] and not creating:
        if holding:
            holding = False
            heldCard.held = False
            i, j = getCoord(x, y)
            if i != -1:
                if occupied[i][j]:
                    card = getCard(i, j)
                    card.pos = heldCard.pos
                else:
                    oldi, oldj = heldCard.pos
                    occupied[oldi][oldj] = False
                    occupied[i][j] = True
                heldCard.pos = (i, j)
            redraw()
        mtog = True
    if not holding and mclk[2] and mtog2 and not creating:
        mtog2 = False
        i, j = getCoord(x, y)
        if i != -1:
            if occupied[i][j]:
                cards.remove(getCard(i, j))
                solved = False
                for card in cards:
                    if card.inSet:
                        solved = True
                occupied[i][j] = False
            else:
                creating = True
                occupied[i][j] = True
                creatingCoords = (i, j)
            redraw()
    key = pygame.key.get_pressed()
    if key[52]:
        i, j = creatingCoords
        occupied[i][j] = False
        creatingCard = ''
        creating = False
        solved = False
        for card in cards:
            card.inSet = False
        redraw()
    if creating:
        if keyTog:
            keyTog = False
            if key[49]:
                creatingCard += '0'
            elif key[50]:
                creatingCard += '1'
            elif key[51]:
                creatingCard += '2'
            else:
                keyTog = True
            if keyTog == False:
                if len(creatingCard) == 4:
                    creating = False
                    cards.append(Card(creatingCard, creatingCoords))
                    creatingCard = ''
                    size = len(cards)
                    for first in range(size):
                        for second in range(size):
                            for third in range(size):
                                if solved or first == second or first == third or second == third:
                                    continue
                                if isSet(cards[first], cards[second], cards[third]):
                                    cards[first].inSet = True
                                    cards[second].inSet = True
                                    cards[third].inSet = True
                                    solved = True
                redraw()
        if not key[49] and not key[50] and not key[51]:
            keyTog = True
    if not mclk[2]:
        mtog2 = True
