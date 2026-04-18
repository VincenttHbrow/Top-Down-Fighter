import pygame
from settings import *
import mapsys
import camera
import math as m
import player
import entitysys


"""
Main game file. Contains main update loop.
Run this to play.
"""

# Crucial pygame initialisations
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
pygame.event.set_grab(True) # locks cursor to game window
pygame.mouse.set_visible(False)
run = True

# Creating classes
player = player.Player()
maphandler = mapsys.Maphandler()
entityhandler = entitysys.Entityhandler(player)

# Temp stuff, testing/demo purposes. Will find better systems to handle.
maphandler.load('testmap', 'tileset2')
player.pos = 2,2


# Main loop
while run:
    # Standard pygame update stuff
    clock.tick(FPS)
    screen.fill((0,0,0))

    # Updating classes
    drawnmap = maphandler.draw()
    entityhandler.draw(drawnmap, maphandler)
    camera.camerafy(drawnmap, screen, 1, player.campos, player.dir ) # Draws the map, scaled and rotated

    for event in pygame.event.get(): # Check if game is closed basically, at least for now
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    pygame.display.flip() # Update screen