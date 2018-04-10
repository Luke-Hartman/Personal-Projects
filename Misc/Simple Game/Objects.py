import pygame
from pygame import gfxdraw
from numpy import log
from Config import *

allSprites = pygame.sprite.Group()
players = pygame.sprite.Group()

pygame.mixer.init()
hitSound = pygame.mixer.Sound(HIT_SOUND)
shootSound = pygame.mixer.Sound(SHOOT_SOUND)
shootSound.set_volume(0.25)

pygame.mixer.set_reserved(1)
musicChannel = pygame.mixer.Channel(0)
backgroundMusic = pygame.mixer.Sound(BACKGROUND_MUSIC)
backgroundMusic.set_volume(0.1)
musicChannel.play(backgroundMusic, -1)

class Ball(pygame.sprite.Sprite):
	ballsCreated = 0
	verbose = False
	anyCollisions = False
	
	def __init__(self, pos, vel, color, radius, mass, name=None):
		pygame.sprite.Sprite.__init__(self)
		Ball.ballsCreated += 1
		if name is None:
			name = 'Ball' + str(Ball.ballsCreated)
		self.defaultImage = pygame.Surface((2*radius, 2*radius))
		self.image = self.defaultImage
		self.image.set_colorkey((0,0,0)) # This means that it will not draw black pixels
		self.imageQueue = []
		
		pygame.draw.circle(self.image, color, (radius, radius), radius, 0)
		self.rect = self.image.get_rect()
		
		self.pos = pos
		self.vel = vel
		self.color = color
		self.radius = radius
		self.mass = mass
		self.name = name
		allSprites.add(self)
		self.rect.center = pos

	def update(self, dt, camera, validRect):
		x, y = self.pos
		vx, vy = self.vel
		self.pos = (x + vx*dt, y + vy*dt)
		self.rect.center = self.pos
		others = pygame.sprite.spritecollide(self, allSprites, False, collided=pygame.sprite.collide_circle)
		for other in others:
			if self != other:
				if Ball.verbose:
					print(self, "collided with", other)
				intensity = self.collide(other, dt)
				camera.applyTrauma(intensity)
		if len(self.imageQueue) > 0:
			self.image = self.imageQueue.pop()
		else:
			self.image = self.defaultImage
		if not self.rect.colliderect(validRect):
			self.leaveArea()
		
	def collide(self, other, dt):
		Ball.anyCollisions = True
		vx, vy = self.vel
		wx, wy = other.vel
		Ax, Ay = self.pos
		Bx, By = other.pos
		
		# First positions the balls
		# Math is done in frame where other is at pos=vel=(0,0)
		vx -= wx
		vy -= wy
		x = Ax - Bx
		y = Ay - By
		
		a = vx**2 + vy**2
		b = 2*(x*vx + y*vy)
		c = x**2 + y**2 - (self.radius + other.radius)**2
		t = (-b - (b**2 - 4*a*c)**0.5)/(2*a) # Negative root because it already happened

		self.pos = (Ax + (vx + wx)*t, Ay + (vy + wy)*t)
		other.pos = (Bx + wx*t, By + wy*t)
		
		# Now updates velocity
		x1, y1 = self.pos
		x2, y2 = other.pos
		
		ox = self.pos[0] - other.pos[0]
		oy = self.pos[1] - other.pos[1]
		o = (ox**2 + oy**2)**0.5
		nx = ox/o
		ny = oy/o
		vn = vx*nx + vy*ny
		
		# If you want to rederive this, use the center of mass frame
		v1 = vn*(self.mass - other.mass)/(self.mass + other.mass)
		v2 = 2*vn*self.mass/(self.mass + other.mass)
		
		self.vel = (v1*nx + wx, v1*ny + wy)
		other.vel = (v2*nx + wx, v2*ny + wy)
		
		# Now moves the balls for the lost time after moving the balls back outside of each other
		self.pos = (self.pos[0] - self.vel[0]*t, self.pos[1] - self.vel[1]*t)
		other.pos = (other.pos[0] - other.vel[0]*t, other.pos[1] - other.vel[1]*t)

		self.rect.center = self.pos
		other.rect.center = other.pos
		
		dm1 = ((self.vel[0] - (vx + wx))**2 + (self.vel[1] - (vy + wy))**2)**0.5*self.mass
		dm2 = ((other.vel[0] - wx)**2 + (other.vel[1] - wy)**2)**0.5*other.mass
		intensity = min(1, (dm1 + dm2)/150000*TRAUMA_MUL)
		
		# Play sounds
		channel = pygame.mixer.find_channel()
		channel.set_volume(intensity)
		channel.play(hitSound)
		
		# Short flash animation
		flash = pygame.Surface((2*self.radius, 2*self.radius))
		flash.set_colorkey((0,0,0))
		pygame.draw.circle(flash, FLASH_COLOR, (self.radius, self.radius), self.radius, 0)
		self.imageQueue.append(flash)
		
		flash = pygame.Surface((2*other.radius, 2*other.radius))
		flash.set_colorkey((0,0,0))
		pygame.draw.circle(flash, FLASH_COLOR, (other.radius, other.radius), other.radius, 0)
		other.imageQueue.append(flash)
			
		return intensity
			
	def leaveArea(self):
		self.kill()
		if Ball.verbose:
			print('Killed', self)
	
	def __str__(self):
		return self.name
		
class Player(Ball):
	def __init__(self, playerID, joystick):
		pos = PLAYER_STARTS[playerID]
		vel = (0, 0)
		color = PLAYER_COLORS[playerID]
		radius = PLAYER_RADIUS
		mass = PLAYER_MASS
		name = 'Player' + str(playerID)
		super().__init__(pos, vel, color, radius, mass, name)
		
		players.add(self)
		self.joystick = joystick
		joystick.init()
		self.cooldowns = [0, 0] # Ready to fire!

	def update(self, dt, camera, screen):
		super().update(dt, camera, screen) # Does normal update
		# Fire left stick
		self.cooldowns[0] = max(0, self.cooldowns[0] - dt)
		x = self.joystick.get_axis(0)
		y = self.joystick.get_axis(1)
		mag = (x**2 + y**2)**0.5
		if mag > 0.5 and self.cooldowns[0] == 0:
			dir = (x/mag, y/mag)
			self.shootDir(dir, 0)
		# Fire right stick
		self.cooldowns[1] = max(0, self.cooldowns[1] - dt)
		x = self.joystick.get_axis(4)
		y = self.joystick.get_axis(3)
		mag = (x**2 + y**2)**0.5
		if mag > 0.5 and self.cooldowns[1] == 0:
			dir = (x/mag, y/mag)
			self.shootDir(dir, 1)
	
	# Channel 0 is left stick, 1 is right stick
	def shootDir(self, dir, channel): # This should always get normalized vectors!
		if(self.cooldowns[channel] > 0): # Not ready to fire
			return -1 # Returns -1 if it doesn't fire
		nx, ny = dir
		x, y = self.pos
		vx, vy = self.vel
		d = PLAYER_RADIUS + PROJECTILE_RADIUS + 20
		
		# Create the projectile
		pos = (x + nx*d, y + ny*d)
		vel = (vx + nx*PROJECTILE_VELOCITY, vy + ny*PROJECTILE_VELOCITY)
		color = self.color
		radius = PROJECTILE_RADIUS
		mass = PROJECTILE_MASS
		projectile = Ball(pos, vel, color, radius, mass, name=self.name+"'s Projectile")
		if len(pygame.sprite.spritecollide(projectile, allSprites, False, collided=pygame.sprite.collide_circle)) > 1:
			projectile.kill()
			return -1
		
		
		shootSound.play()
		# Apply recoil
		recoil = PROJECTILE_MASS*PROJECTILE_VELOCITY/PLAYER_MASS
		self.vel = (vx - nx*recoil, vy - ny*recoil)
		intensity = PROJECTILE_MASS*PROJECTILE_VELOCITY/300000*TRAUMA_MUL # Notice this is half as intense as collisions
		
		# Set cooldown before another shot can be fired
		self.cooldowns[channel] = PLAYER_COOLDOWN
		return intensity