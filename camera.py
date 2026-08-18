import pygame
from settings import *
import math as m
from pygame._sdl2 import Window, Renderer, Texture

'''
This module is dedicated to getting the game to display correctly, and maybe even look nice.
'''


def camerafy(texture, renderer, zoom, direction, pos):
    """
    Given a surface input, this function resizes and rotates it to reflect the player's position and direction.
    May also have some smoothing shit in here down the line.
    Not sure yet.
    """
    texture = Texture.from_surface(renderer, texture) # makes img into sdl2 texture
    angle = -direction # angle is just the player direction inversed

    targetrect = texture.get_rect() # need this so the texture stretches properly into a square
    targetrect.w = (RESOLUTION[0]*zoom)
    targetrect.h = (RESOLUTION[0]*zoom)
    sizediff = (RESOLUTION[0] - targetrect.w)/2,(RESOLUTION[0] - targetrect.w)/2
    targetrect.center = targetrect.center[0] + sizediff[0]  ,targetrect.center[1] + sizediff[1] 
    # makes sure rect is centered
    texture.draw(None, targetrect, angle) # rotates, scales, and draws the map surface