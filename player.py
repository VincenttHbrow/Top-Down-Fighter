import pygame
import math as m
from settings import *


KEYDIRS = { # Dictionary containing what the modifiers to the player.dir should be to move in a given direction
    KEYS['FORWARD']: -90,
    KEYS['BACKWARD']: 90,
    KEYS['LEFT']: 180,
    KEYS['RIGHT']: 0
}


class Player():
    """
    This class handles input, position, direction, eventually states and maybe animation.
    """

    
    def __init__(self): # Standard init stuff
        self.dir = 0
        self.pos = 0, 0
        self.campos = 0, 0


    def update(self, maphandler): # Takes input, changes position and direction.
        keys = pygame.key.get_pressed()
        for key in KEYDIRS.keys(): # This for loop handles directional input
            if keys[key]:
                self.pos = self.pos[0] + 0.05*m.cos(m.radians(self.dir + KEYDIRS[key])), self.pos[1]
                self.tile = maphandler.mapdata[round(self.pos[1])][round(self.pos[0])]
                if maphandler.tiledata[self.tile]:
                    self.pos = self.pos[0] - 0.05*m.cos(m.radians(self.dir + KEYDIRS[key])), self.pos[1]

                self.pos =  self.pos[0], self.pos[1] + 0.05*m.sin(m.radians(self.dir + KEYDIRS[key]))
                self.tile = maphandler.mapdata[round(self.pos[1])][round(self.pos[0])]
                if maphandler.tiledata[self.tile]:
                    self.pos = self.pos[0], self.pos[1] - 0.05*m.sin(m.radians(self.dir + KEYDIRS[key]))
                # There is probably a more efficient way of doing this, but this is it for now.
                # Basically, move player the X-component of their movement vector, if they collide 
                # with a solid tile, move them back. Rinse and repeat for Y-component.

        self.dir += pygame.mouse.get_rel()[0]*MOUSESENS # Change direction with mouse movement

        if self.dir > 360: # This is just to make sure number don't get too big. Just seems prudent.
            self.dir = self.dir - 360
        elif self.dir < 0:
            self.dir = self.dir + 360

        self.campos = self.pos[0] - 0.5*len(maphandler.mapdata[0]), self.pos[1] - 0.5*len(maphandler.mapdata)
        # campos is for display purposes; the camera displays the map's position wrong and this is a bandaid fix.