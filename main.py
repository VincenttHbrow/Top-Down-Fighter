import pygame
from settings import *
import mapsys
import camera
import math as m
import player


"""
Main game file. Contains main update loop.
Run this to play.
"""

# Crucial pygame initialisations
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
run = True

# Creating classes
player = player.Player()
maphandler = mapsys.Maphandler()

# Temp stuff, testing/demo purposes. Will find better systems to handle.
maphandler.load('testmap')
player.pos = 2,2


# Main loop
while run:
    # Standard pygame update stuff
    clock.tick(FPS)
    screen.fill((0,0,0))

    # Updating classes
    player.update(maphandler) # Gets and handles input and such
    camera.camerafy(maphandler.draw(), screen, 1, player.campos, player.dir ) # Draws the map, scaled and rotated

    for event in pygame.event.get(): # Check if game is closed basically, at least for now
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip() # Update screen