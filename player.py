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
        self.currentanim = 0


    def update(self, maphandler): # Takes input, changes position and direction.
        self.currentanim = 0
        keys = pygame.key.get_pressed()
        for key in KEYDIRS.keys(): # This for loop handles directional input
            if keys[key]:
                self.currentanim = 1
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

        # This next block just resets the mouse to center of screen. Would do this every frame but I was
        # getting stuttering, so instead it's just when it gets to close to the edges
        mousepos = pygame.mouse.get_pos()
        if mousepos[0] > 1200 or mousepos[0] < 80 or mousepos[1] > 640 or mousepos[1] <80:
            pygame.mouse.set_pos([RESOLUTION[0]/2, RESOLUTION[1]/2]) # Reset cursor to center of screen

        if self.dir > 360: # This is just to make sure number don't get too big. Just seems prudent.
            self.dir = self.dir - 360
        elif self.dir < 0:
            self.dir = self.dir + 360

        self.campos = self.pos[0] - 0.5*len(maphandler.mapdata[0]), self.pos[1] - 0.5*len(maphandler.mapdata)
        # campos is for display purposes; the camera displays the map's position wrong and this is a bandaid fix.