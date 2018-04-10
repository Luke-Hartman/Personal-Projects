import pygame
from Objects import allSprites, players, Ball, Player
from Camera import Camera
from Config import *
from Survival import runSurvival
from pygame.locals import *
import random

import sys

Ball.verbose = False

pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
screen = pygame.display.set_mode((w,h),pygame.FULLSCREEN)

camera = Camera(screen)
while True:
	runSurvival(camera)

'''
Ball((300, 300), (15, 15), (0, 0, 255), 100, 100)
Ball((650, 600), (-300, -300), (0, 255, 0), 50, 25)
#Ball((900, 900), (0, 0), (255, 0, 255), 200, 10000)
Ball((900, 900), (0, 0), (255, 0, 255), PLAYER_RADIUS, PLAYER_MASS)
'''#'''
'''
while True:
	allSprites.empty()
	Ball((w/2, h/2), (0, 0), (255, 0, 255), 200, 1000)

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
		camera.updateDraw(dt)
		
		if playerCount > 1 or len(players.sprites()) == 1 or len(players.sprites()) == 0:
			print("Finished round!")
			break
'''