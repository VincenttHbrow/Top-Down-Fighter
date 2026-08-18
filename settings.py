import pygame


'''
This module is just data storage of important constants, for easy alteration throughout development
'''

# Important game/display variables
FPS = 60 # Target frames per second
RESOLUTION = 1920, 1080 # Take a guess
TILESIZE = 16 # How large of tiles are to be used in tilesets
ENTITYSIZE = 16 # Resolution of entities, scales to tilesize.
ANIMATIONSPEED = 12 # FPS of animated sprites
MOVESPEED = 0.05*60/FPS
RENDERDIST = 12 # number of tiles around the player to render also affects camera zoom
DEBUGMODE = False
CAMERA = True
FULLSCREEN = False
WEAPONXOFFSET = 5
WEAPONYOFFSET = 7

# Input stuff
MOUSESENS = 0.25 # Mouse sensitivity multiplier. 0.3 or 0.25 is a good baseline.
KEYS = { # Dictionary containing keys so rebinding actions is easy
    'FORWARD' : pygame.K_w,
    'LEFT': pygame.K_a,
    'RIGHT': pygame.K_d,
    'BACKWARD': pygame.K_s,
}

WEAPONDATA = { # For storing damage reach speed etc.
    # Size is measured from image center to weapon tip, can be negative.
    'spear':{
        'size': 9
    },
    'sword':{
        'size': 3
    }
}