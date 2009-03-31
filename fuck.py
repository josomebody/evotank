import os, pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480), FULLSCREEN)
background = pygame.image.load('/home/jo/evotank/images/bg.png').convert()
tank = pygame.image.load('/home/jo/evotank/images/goodtank.png').convert_alpha()

key = K_x
theta = 0
while key != K_q:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			key = event.key
			if key == K_LEFT:
				theta += 1
			elif key == K_RIGHT:
				theta -= 1
				
			drawable = pygame.transform.rotate(tank, theta)
			height = tank.get_height() / 2
			screen.blit(background, (0,0))
			screen.blit(drawable, (320-height, 200-height))
			pygame.display.flip()
