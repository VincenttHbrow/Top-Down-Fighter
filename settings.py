import pygame


'''
This module is just data storage of important constants, for easy alteration throughout development
'''

# Important game/display variables
FPS = 60 # Target frames per second
RESOLUTION = 1280, 720 # Take a guess
TILESIZE = 16 # How large of tiles are to be used in tilesets
ENTITYSIZE = 16 # Resolution of entities, scales to tilesize.
RESOLUTIONMULT = 8 # How high to scale up the map and whatnot
ANIMATIONSPEED = 12 # FPS of animated sprites
MOVESPEED = 0.05
RENDERDIST = 14
DEBUGMODE = False
CAMERA = True
FULLSCREEN = True

# Input stuff
MOUSESENS = 0.3 # Mouse sensitivity multiplier. 0.3 or 0.25 is a good baseline.
KEYS = { # Dictionary containing keys so rebinding actions is easy
    'FORWARD' : pygame.K_w,
    'LEFT': pygame.K_a,
    'RIGHT': pygame.K_d,
    'BACKWARD': pygame.K_s,
}