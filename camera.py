import pygame
from settings import *
import math as m

def camerafy(mapsurface, destsurface, zoom, pos, direction):
    angle = m.radians(-direction)
    zoompos = (pos[0]+0.5)*RESOLUTIONMULT*zoom*TILESIZE, (pos[1]+0.5)*RESOLUTIONMULT*zoom*TILESIZE
    x1 = zoompos[0]*m.cos(angle) - zoompos[1]*m.sin(angle)
    y1 = zoompos[0]*m.sin(angle) + zoompos[1]*m.cos(angle)

    calcpos = -x1, -y1
    dot = pygame.surface.Surface((TILESIZE*RESOLUTIONMULT,TILESIZE*RESOLUTIONMULT))
    dot.fill((255,0,0))

    newsurface = pygame.transform.scale_by(mapsurface, RESOLUTIONMULT*zoom)
    newsurface = pygame.transform.rotate(newsurface, direction)
    newrect = newsurface.get_rect(center = (calcpos[0] + RESOLUTION[0]/2, calcpos[1] + RESOLUTION[1]/8*6))
    destsurface.blit(newsurface, newrect)

    destsurface.blit(dot,(RESOLUTION[0]/2 - TILESIZE*RESOLUTIONMULT/2, RESOLUTION[1]/8*6 - TILESIZE*RESOLUTIONMULT /2))