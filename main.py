import pygame
from settings import *
import mapsys
import camera
import math as m
import player
import entitysys
from pygame._sdl2 import Window, Renderer, Texture


"""
Main game file. Contains main update loop.
Run this to play.
"""

# Crucial pygame initialisations
pygame.init()
screen = Window('TDF',RESOLUTION)
renderer = Renderer(screen)
if FULLSCREEN:
    screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)


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
    renderer.draw_color = (0,0,0,255)
    renderer.clear()
    if DEBUGMODE:
        print('fps: ' + str(clock.get_fps()))

    # Updating classes
    drawnmap = maphandler.draw(player)
    entityhandler.draw(drawnmap, maphandler)

    if CAMERA: # Displays map in the corner of the screen if camera is off, for debugging
        newsurface = camera.camerafy(drawnmap, renderer, 1.5, player.dir, player.pos) # Draws the map, scaled and rotated

    else:
        screen.blit(drawnmap, (0,0))

    for event in pygame.event.get(): # Check if game is closed basically, at least for now
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    renderer.present()
    #pygame.display.flip() # Update screen