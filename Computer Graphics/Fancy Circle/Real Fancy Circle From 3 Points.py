import pygame
from pygame.locals import *
import sys
import math

print "(Axis have constant scale of 255 units long.)"

tau = 2*math.pi
A = (0,0,0)
B = (1000, 2000, 3000)
C = (4000, 5000, 6000)
T = 100

#'''
A = input("Input a vector for A in the form '(a1, a2, a3)'")
B = input("Same for B.")
C = input("And for C.")
T = input("How fine would you like the resolution of the circle to be? (45 works fine)")
'''#'''

#--[[   Graphics Functions    ]]--#

def update():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
pygame.init()

infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((500,500))

def color(A): #Technically a vector function, but only used for colors
    a1, a2, a3 = scalar(A, scale)
    if abs(a1) > 255:
        a1 = 255
    if abs(a2) > 255:
        a2 = 255
    if abs(a3) > 255:
        a3 = 255
    return (abs(a1), abs(a2), abs(a3))

def cos(theta):
    return math.cos(theta*tau/360)

def sin(theta):
    return math.sin(theta*tau/360)

def r2(A, I = 0):
    x, y, z = A
    xc = x*cos(theta) + y*sin(theta)*sin(azimuth) - z*sin(theta)*cos(azimuth)
    yc = y*cos(azimuth) + z*sin(azimuth)
    if I:
        return (int(xc*scale + w/2), int(-yc*scale + h/2))
    return (xc*scale + w/2, -yc*scale + h/2)

def point(A):
    pygame.draw.circle(screen, color(A), r2(A, 1), 10)

def line(A,B, Color = (255,255,255)):
    pygame.draw.aaline(screen, color(Color), r2(A), r2(B))

#--[[   Vector Functions    ]]--#

def cross(A, B):
    a1, a2, a3 = A
    b1, b2, b3 = B
    return (a2*b3 - b2*a3, b1*a3 - a1*b3, a1*b2 - b1*a2)

def dot(A, B):
    a1, a2, a3 = A
    b1, b2, b3 = B
    return a1*b1 + a2*b2 + a3*b3

def magnitude(A):
    a1, a2, a3 = A
    return (a1**2 + a2**2 + a3**2)**0.5
    
def scalar(A, S):
    a1, a2, a3 = A
    return (a1*S, a2*S, a3*S)

def negative(A):
    a1, a2, a3 = A
    return (-a1, -a2, -a3)

def add(A, B):
    a1, a2, a3 = A
    b1, b2, b3 = B
    return (a1 + b1, a2 + b2, a3 + b3)

def normalize(A):
    return scalar(A, 1/magnitude(A))

def component(A, u):
    return scalar(u, dot(A, u))

def drawComponents(A, u1, u2, u3):
    A1 = component(A, u1)
    A2 = component(A, u2)
    A3 = component(A, u3)
    A12 = add(A1, A2)
    line(O, A1, scalar(u1, 255))
    line(A1, A12, scalar(u2, 255))
    line(A12, add(A12, A3), scalar(u3, 255))

O = (0,0,0)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)

#--[[    Circle Stuff    ]]--#

O = (0,0,0)
AB = add(B, negative(A))
AC = add(C, negative(A))
u1 = normalize(AB)
u3 = normalize(cross(u1, AC))
u2 = cross(u3, u1)
a1, a2 = dot(A, u1), dot(A, u2)
b1, b2 = dot(B, u1), dot(B, u2)
c1, c2 = dot(C, u1), dot(C, u2)
g1, h1 = 2*(b1 - a1), 2*(c1 - a1)
g2, h2 = 2*(b2 - a2), 2*(c2 - a2)
g3, h3 = b1**2 + b2**2 - a1**2 - a2**2, c1**2 + c2**2 - a1**2 - a2**2
y = (g1*h3 - g3*h1)/(g1*h2 - g2*h1)
x = (g3 - g2*y)/g1
z = dot(A, u3)
Center = add(add(scalar(u1, x), scalar(u2, y)), scalar(u3, z))
Radius = ((a1 - x)**2 + (a2 - y)**2)**0.5
farthest = max((magnitude(A), magnitude(B), magnitude(C))) + Radius
scale = 1000/farthest
Points = []
for t in range(T + 1):
    new1 = x + Radius*math.cos(t*tau/T)
    new2 = y + Radius*math.sin(t*tau/T)
    new3 = z
    Points.append(add(add(scalar(u1, new1), scalar(u2, new2)), scalar(u3, new3)))

#--[[    The graphing part    ]]--#

azimuth = 0
theta = 0
First = 1
while True:
    update()
    pygame.time.Clock().tick(30)
    key = pygame.key.get_pressed()
    '''
    for a in range(len(key)):
        if key[a] and a != 300:
            print a
    '''#'''
    keyW = key[119]
    keyA = key[97]
    keyS = key[115]
    keyD = key[100]
    if keyW or keyS or keyD or keyA or First:
        First = 0
        azimuth += keyW - keyS
        theta += keyA - keyD
        screen.fill((0,0,0))
        line(O, Red, scalar(Red, 1/scale))
        line(O, Green, scalar(Green, 1/scale))
        line(O, Blue, scalar(Blue, 1/scale))
        old = (0,0,0)
        for a in Points:
            line(Center, a, scalar(add(a, Center), 0.5))
            if old != (0,0,0):
                line(old, a, a)
            old = a
        drawComponents(A, u1, u2, u3)
        drawComponents(B, u1, u2, u3)
        drawComponents(C, u1, u2, u3)
        drawComponents(Center, u1, u2, u3)
        point(A)
        point(B)
        point(C)
        point(Center)
        pygame.display.flip()
