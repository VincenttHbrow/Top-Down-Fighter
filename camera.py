import pygame
from settings import *
import math as m


'''
This module is dedicated to getting the game to display correctly, and maybe even look nice.
'''


def camerafy(mapsurface, destsurface, zoom, direction):
    """
    Given a surface input, this function resizes and rotates it to reflect the player's position and direction.
    May also have some smoothing shit in here down the line.
    Not sure yet.
    """
    angle = m.radians(-direction)# I hate working with radians. Conversion is important.

    # zoompos is just the position to display the map at after map resize but before rotation.
    # mostly irrelevant ATP but might wanna fuck around with it later.
    zoompos = 0,0

    # all of this is to calculate the position to display the map in after rotation and zoom.
    x1 = zoompos[0]*m.cos(angle) - zoompos[1]*m.sin(angle)
    y1 = zoompos[0]*m.sin(angle) + zoompos[1]*m.cos(angle)
    calcpos = -x1, -y1

    # rotates and scales the map surface
    newsurface = pygame.transform.scale_by(mapsurface, (RESOLUTIONMULT*0.5)*zoom)
    newsurface = pygame.transform.rotate(newsurface, direction)
    newsurface = pygame.transform.scale_by(newsurface, (RESOLUTIONMULT*0.25)*zoom)

    # rect is important for it to rotate on center instead of from the top right or wherever
    newrect = newsurface.get_rect(center = (calcpos[0] + RESOLUTION[0]/2, calcpos[1] + RESOLUTION[1]/8*6))
    destsurface.blit(newsurface, newrect) # draw map on screen