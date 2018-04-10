import pygame
from Objects import allSprites, Ball
from Config import *
from noise import pnoise1

class Camera:
	time = 0 #Updated externally
	def __init__(self, screen):
		self.screen = screen

		w, h = screen.get_size()
		Camera.size = (w, h)
		
		# Should actually do the math later
		self.background = pygame.Surface((w + 1000, h + 1000))
		self.background.fill((255, 255, 255))
		
		# Scene before shaking
		self.calmSurface = pygame.Surface((w + 1000, h + 1000))
		self.calmSurface.blit(self.background, (0, 0))
		self.kick = (0, 0)
		self.trauma = 0

	def applyTrauma(self, intensity):
		self.trauma = min(1, self.trauma + intensity)
	
	def applyKick(self, dir, intensity):
		self.trauma = min(1, self.trauma + intensity)
		x, y = self.kick
		nx, ny = dir
		magnitude = intensity*KICK_DISTANCE
		self.kick = (x - nx*magnitude, y - ny*magnitude)
		
	def getNoise(seed):
		return pnoise1(seed + Camera.time*SHAKE_FREQUENCY, SHAKE_OCTAVES)
	
	def updateDraw(self, dt):
		Ball.anyCollisions = False
		# Update all the sprites
		allSprites.clear(self.calmSurface, self.background)
		allSprites.update(dt, self, self.screen.get_rect())
		allSprites.draw(self.calmSurface)
		if Ball.anyCollisions:
			pygame.time.wait(20) # Waits 20 ms on collisions
		# Apply rotational screen shake
		shake = self.trauma**SHAKE_EXPONENT
		angle = Camera.getNoise(1)*MAX_SHAKE_ANGLE*shake
		shakeSurface = pygame.transform.rotate(self.calmSurface, angle)
		w, h = self.screen.get_size()
		rw, rh = shakeSurface.get_size()
		ox = (w - rw)/2
		oy = (h - rh)/2
		
		# Apply translational screen shake
		sx = Camera.getNoise(2)*MAX_SHAKE_DISTANCE*shake
		sy = Camera.getNoise(3)*MAX_SHAKE_DISTANCE*shake
		
		kx, ky = self.kick
		
		self.screen.blit(shakeSurface, (500 + ox + sx + kx, 500 + oy + sy + ky))
		'''
		pygame.draw.rect(self.screen, (248, 114, 23), pygame.Rect(0, 1080-1080*self.trauma, 50, 1080*self.trauma))
		pygame.draw.rect(self.screen, (21, 105, 199), pygame.Rect(50, 1080-1080*shake, 50, 1080*shake))
		'''
		pygame.display.flip()
		
		self.trauma = max(0, self.trauma - TRAUMA_DECAY_RATE*dt)
		decay = 2**(-dt*KICK_DECAY_RATE)
		self.kick = (kx*decay, ky*decay)