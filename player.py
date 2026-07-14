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
    This class handles input and relays stuff to the camera module. 
    At this point it's probably mostly unnecessary but I'm not ready to deal with getting rid of it yet so whatever.
    """

    
    def __init__(self): # Standard init stuff
        self.dir = 0
        self.pos = 0, 0
        self.campos = 0, 0
        self.currentanim = 0

    def getmovement(self, occupied, maphandler): # Returns where the player input determines the PC should move
        if occupied <= 0:
            self.currentanim = 0 # Animation 0 is idle, Animation 1 is walk, 2 is attack
        keynum = 0 # Number of keys pressed
        keys = pygame.key.get_pressed()
        posmod = 0,0
        for key in KEYDIRS.keys(): # This for loop handles directional input
            if keys[key]:
                if occupied <= 0:
                    self.currentanim = 1
                posmov = (0,0)
                posmov = MOVESPEED*m.cos(m.radians(self.dir + KEYDIRS[key])), 0


                posmov =  posmov[0], MOVESPEED*m.sin(m.radians(self.dir + KEYDIRS[key]))
                keynum += 1

                if keynum > 0:
                    posmov = posmov[0]/keynum, posmov[1]/keynum
                    posmod = posmod[0] + posmov[0], posmod[1] + posmov[1]
        dirmod = pygame.mouse.get_rel()[0]*MOUSESENS # Change direction with mouse movement

        # This next block just resets the mouse to center of screen. Would do this every frame but I was
        # getting stuttering, so instead it's just when it gets to close to the edges
        mousepos = pygame.mouse.get_pos()
        if mousepos[0] > 1200 or mousepos[0] < 80 or mousepos[1] > 640 or mousepos[1] <80:
            pygame.mouse.set_pos([RESOLUTION[0]/2, RESOLUTION[1]/2]) # Reset cursor to center of screen

        self.campos = self.pos[0] - 0.5*(RENDERDIST), self.pos[1] - 0.5*(RENDERDIST)
        # campos is for display purposes; the camera displays the map's position wrong and this is a bandaid fix.

        if pygame.mouse.get_just_pressed()[0]: # Get attack input
            self.currentanim = 2
            occupied = 4

        if occupied > 0: # Don't accept new input when occupied
            return (0,0), 0, occupied
        else:
            return posmod, dirmod, 0