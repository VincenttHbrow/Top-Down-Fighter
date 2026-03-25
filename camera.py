import pygame
from settings import *
import math as m


'''
This module is dedicated to getting the game to display correctly, and maybe even look nice.
'''


def camerafy(mapsurface, destsurface, zoom, pos, direction):
    """
    Given a surface input, this function resizes and rotates it to reflect the player's position and direction.
    May also have some smoothing shit in here down the line.
    Not sure yet.
    """
    angle = m.radians(-direction)# I hate working with radians. Conversion is important.

    # zoompos is just the position to display the map at after map resize but before rotation
    zoompos = (pos[0]+0.5)*RESOLUTIONMULT*zoom*TILESIZE, (pos[1]+0.5)*RESOLUTIONMULT*zoom*TILESIZE
    # The 0.5's are temporary to center player without rect

    # all of this is to calculate the position to display the map in after rotation and zoom.
    x1 = zoompos[0]*m.cos(angle) - zoompos[1]*m.sin(angle)
    y1 = zoompos[0]*m.sin(angle) + zoompos[1]*m.cos(angle)
    calcpos = -x1, -y1

    # dot shit is temporary just to give some indication of where the player is, draws red box.
    dot = pygame.surface.Surface((TILESIZE*RESOLUTIONMULT,TILESIZE*RESOLUTIONMULT))
    dot.fill((255,0,0))

    # rotates and scales the map surface
    newsurface = pygame.transform.scale_by(mapsurface, RESOLUTIONMULT*zoom)
    newsurface = pygame.transform.rotate(newsurface, direction)
    # rect is important for it to rotate on center instead of from the top right or wherever
    newrect = newsurface.get_rect(center = (calcpos[0] + RESOLUTION[0]/2, calcpos[1] + RESOLUTION[1]/8*6))
    destsurface.blit(newsurface, newrect) # draw map on screen

    # again temporary stuff just so the player looks like something
    destsurface.blit(dot,(RESOLUTION[0]/2 - TILESIZE*RESOLUTIONMULT/2, RESOLUTION[1]/8*6 - TILESIZE*RESOLUTIONMULT /2))