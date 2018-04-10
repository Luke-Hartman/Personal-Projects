from Objects import allSprites, Ball
import pygame
from pygame.locals import *
from Objects import allSprites, Ball, Player, players
from Camera import Camera
from Config import *
from random import random
import numpy as np
import sys

def createRandomBall():
	w, h = Camera.size
	x = random()*w
	y = random()*h
	
	difficulty = 2**(DIFFICULTY_RATE*Camera.time)
	
	radius = int(((BASE_RADIUS - MIN_RADIUS)*random() + MIN_RADIUS)*difficulty)
	mass = radius**2*DENSITY
	v = ((BASE_MOMENTUM - MIN_MOMENTUM)*random() + MIN_MOMENTUM)/mass*difficulty
	color = tuple(150 + int(105*random()) for i in range(3))
	angle = 2*np.pi*random()
	nx = np.cos(angle)
	ny = np.sin (angle)
	vel = (nx*v, ny*v)
	
	# Which wall should the ball spawn on
	for sx, dx, sy, dy in [
	(-radius, 0, -radius, radius*2 + h),    # Top left going down
	(-radius, radius*2 + w, -radius, 0),    # Top left going right 
	(w + radius, 0, -radius, radius*2 + h), # Top right going down
	(-radius, radius*2 + w, h + radius, 0)  # Bottom left going right
	]:
		t = (nx*(sy - y) - ny*(sx - x))/(-nx*dy + ny*dx)
		B = (sx + sy - x - y + (dx + dy)*t)/(nx + ny)
		if 0 <= t <= 1 and B < 0:
			pos = (sx + dx*t, sy + dy*t)
			break
	newBall = Ball(pos, vel, color, radius, mass)
	if len(pygame.sprite.spritecollide(newBall, allSprites, False, collided=pygame.sprite.collide_circle)) > 1:
		newBall.kill()
		return False
	return True
			
def runSurvival(camera):
	Camera.time = 0
	allSprites.empty()
	next = 0
	playerCount = pygame.joystick.get_count()
	for a in range(playerCount):
		Player(a, pygame.joystick.Joystick(a))
	while True:
		dt = pygame.time.Clock().tick(120)/1000 # Time in seconds since last
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
		Camera.time += dt

		if Camera.time >= next:
			next += random()*BASE_DELAY - (Camera.time - next)
			while not createRandomBall():
				pass
		
		camera.updateDraw(dt)
		if len(players.sprites()) == 1:
			print("Finished round!")
			break