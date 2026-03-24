import pygame
from settings import *
import mapsys
import camera
import math as m


pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
cameradir = 0
playerpos = 0,0

run = True
maphandler = mapsys.Map()
maphandler.load('testmap')

while run:
    clock.tick(FPS)
    screen.fill((0,0,0))

    camera.camerafy(maphandler.draw(), screen, 1, playerpos,cameradir )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerpos = playerpos[0] + 0.05*m.cos(m.radians(cameradir - 90)), playerpos[1] + 0.05*m.sin(m.radians(cameradir - 90))
        print (cameradir)


    cameradir += pygame.mouse.get_rel()[0]/2

    pygame.display.flip()