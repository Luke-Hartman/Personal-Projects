import numpy as np
import pygame
from pygame.locals import *
import sys
import Config

pygame.init()
infoObject = pygame.display.Info()

#'''
w = infoObject.current_w
h = infoObject.current_h
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
'''
w = infoObject.current_w/2
h = infoObject.current_h/2
screen = pygame.display.set_mode((w, h))
'''#'''

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
clock = pygame.time.Clock()

def cos(ang):
    return np.cos(ang*np.pi/180)
def sin(ang):
    return np.sin(ang*np.pi/180)
def tan(ang):
    return sin(ang)/cos(ang)
def arctan(r):
    return np.arctan(r)/np.pi*180

def rotate(A, theta, phi): # Normalize b/c otherwise it decays over time
    a1, a2, a3 = A
    return [cos(theta)*(cos(phi)*a1 + sin(phi)*a2),
            cos(theta)*(cos(phi)*a2 - sin(phi)*a1),
            cos(theta)*a3 - sin(theta)*(a1**2 + a2**2)**0.5]

def pitchBasis(basis, pitch): # Forward goes down
    f, u, r = basis
    fp = add(scale(f, cos(pitch)), scale(u, -sin(pitch)))
    up = add(scale(f, sin(pitch)), scale(u,  cos(pitch)))
    return fp, up, r

def yawBasis(basis, yaw): # If forward points up, countclockwise.
    f, u, r = basis
    fy = add(scale(f, cos(yaw)), scale(u, -sin(yaw)))
    ry = add(scale(f, sin(yaw)), scale(u,  cos(yaw)))
    return fy, u, ry

def rollBasis(basis, roll):
    f, u, r = basis
    ur = add(scale(u, cos(roll)), scale(r, -sin(roll)))
    rr = add(scale(r, sin(roll)), scale(u,  cos(roll)))
    return f, ur, rr

def turnBasis(basis, phi): # A turn is a rotation around z axis. (Phi turn)
    f, u, r = basis
    return [rotate(f, 0, phi), rotate(u, 0, phi), rotate(r, 0, phi)]

def cross(A, B):
    a1, a2, a3 = A
    b1, b2, b3 = B
    return (a2*b3 - b2*a3, b1*a3 - a1*b3, a1*b2 - b1*a2)

def dot(A, B):
    return sum(A[i]*B[i] for i in range(len(A)))

def cross(A, B):
    a1, a2, a3 = A
    b1, b2, b3 = B
    return (a2*b3 - b2*a3, b1*a3 - a1*b3, a1*b2 - b1*a2)

def scale(A, b):
    return[a*b for a in A]

def magnitude(A):
    return dot(A, A)**0.5

def normalize(A):
    m = magnitude(A)
    if m == 0:
        return [0 for a in A]
    return scale(A, 1/magnitude(A))

def add(A, B):
    return [A[i] + B[i] for i in range(len(A))]

def negative(A):
    return [-a for a in A]

def distance(A, B):
    return magnitude(add(A, negative(B)))

def createBasis(f):
    r = normalize(cross(f, [0,0,1]))
    u = cross(r, f)
    return (f, u, r)

def decompose(A, basis):
    f, u, r = basis
    return [dot(f, A), dot(u, A), dot(r, A)]

def recompose(x, y, z, basis):
    f, u, r = basis
    return add(add(scale(f, x), scale(u, y)), scale(r, z))

def project(A, direction): # Component of A in direction (normalizes direction) as a vector
    d = normalize(direction)
    return scale(d, dot(A, d))
    
# v is the vector to draw, o is the view position, f is the forward view direction
def r2(v, o, basis, integer=False):
    x, y, z = v
    radius = (w**2 + h**2)**0.5/2
    g = add(v, negative(o))
    f, u, r = basis
    F = dot(g, f)
    R = dot(g, r)
    U = dot(g, u)
    #'''
    # This is Eli's suggested fix of rounding out view cone
    conversion = radius/Config.FOV*2 # The last factors after conversion are experimentally determined.
    xPix = w/2 + arctan(R/F)*conversion*(R**2 + F**2)**0.25/F**0.5
    yPix = h/2 - arctan(U/F)*conversion*(U**2 + F**2)**0.25/F**0.5
    '''
    # Old way
    conversion = radius/F/tan(Config.FOV/2)
    xPix = R*conversion + w/2
    yPix = -U*conversion + h/2
    '''#'''
    if integer:
        xPix = int(xPix)
        yPix = int(yPix)
    return (xPix, yPix)

def drawLine(A, B, o, basis, color=Config.lineColor, thickness=1):
    f = basis[0]
    if dot(add(A, negative(o)), f) > 0 and dot(add(B, negative(o)), f) > 0:
        #pygame.draw.aaline(screen, color, r2(A, o, basis), r2(B, o, basis))
        pygame.draw.line(screen, color, r2(A, o, basis), r2(B, o, basis), thickness)
        
        

#Kill me eventually
def drawCircle(A, radius, o, basis, color=(255,255,255)):
    pygame.draw.circle(screen, color, r2(A, o, basis, True), int(radius))

def update():
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                kill()
                sys.exit()
    clock.tick(Config.fps)
    move = pygame.mouse.get_rel()
    return move

def getKeys():
    return pygame.key.get_pressed()

def wipe():
    screen.fill(Config.backgroundColor)

def kill():
    pygame.quit()
