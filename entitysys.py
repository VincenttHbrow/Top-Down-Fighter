import pygame
from settings import *
import math as m

# This checks for map collisions at all corners of rect
# Should be good unless I have entities bigger than 1 tile which I'm not planning on
def getmapcollide(rect, maphandler, vertical):
    modrect = pygame.rect.Rect(rect)
    if vertical:
        modrect.w -=2
    else:
        modrect.h -=2
    modrect.center = rect.center
    rectpoints = [modrect.topleft, modrect.topright, modrect.bottomleft, modrect.bottomright]
    if DEBUGMODE:
        print (rectpoints)
    collide = False
    for point in rectpoints:
        tile = maphandler.mapdata[int(point[1]/TILESIZE)][int(point[0]/TILESIZE)]
        if maphandler.tiledata[tile]:
            collide = True
    return collide

class Entity():
    '''
    This class is for any non-tile thing. 
    Anything interactable, anything living, etc.
    As it stands it just draws the player sprite, but will be used for more stuff in future. 
    '''
    def __init__(self, spritefile, pos = (0,0), dir = 0, player = None):
        self.sprite = pygame.image.load('sprites/' + spritefile + '.png').convert_alpha()
        self.animated = False # Just whether an object is a single frame or a spritesheet
        self.player = player # Player should be left empty UNLESS IT'S THE PLAYER CHARACTER
        self.dir = dir
        self.img = self.sprite # This is specifically the image to be drawn on the map at any given time.
        self.pos = pos
        self.rectsize = TILESIZE

        # This (should) divide the spritesheet into seperate frames within a nested list, sorted into animations by row.
        if spritefile[-5:] == 'sheet':
            self.rectsize = TILESIZE/2
            self.animated = True 
            self.currentanim = 0
            self.frame = 0
            self.frames = [] # Stores all the different frames extracted from the spritesheet
            for row in range(int(self.sprite.get_size()[1]/ENTITYSIZE)):
                animation = []
                for column in range (int(self.sprite.get_size()[0]/ENTITYSIZE)):
                    surface = pygame.surface.Surface((ENTITYSIZE, ENTITYSIZE))
                    surface.fill((0,255,0))
                    surface.set_colorkey((0,255,0))
                    surface.blit(self.sprite, (-column*ENTITYSIZE, -row*ENTITYSIZE))
                    animation.append(surface)
                self.frames.append(animation)
            self.img = self.frames[0][0]
        self.rect = self.img.get_rect(center = (self.pos[0]*TILESIZE + 0.5*TILESIZE, self.pos[1]*TILESIZE+ 0.5*TILESIZE))

    
    def draw(self, surface, nextframe, entities, maphandler): # Draws the entity's (rotated if applicable) image on the map
        # This is, again, only relevant if it's the player character's entity
        posmod = 0,0
        if self.dir > 360:
            self.dir -= 360
        if self.dir < 0:
            self.dir += 360
        if self.player != None:
            posmod, dirmod = self.player.getmovement(maphandler)
            self.dir += dirmod
            self.player.dir = self.dir
            self.player.pos = self.pos
            self.currentanim = self.player.currentanim

        
        # This is for animated entities switching frames if applicable
        if nextframe and self.animated:
            if not self.frame >= len(self.frames[self.currentanim] ) - 1:
                self.frame += 1
            else:
                self.frame = 0
            self.img = self.frames[self.currentanim][self.frame]

        # This is collisions stuff. Worth seeing if I can find a way to shrink the rects to 1 tile.
        for entity in entities:
            if not entity == self:
                if entity.rect.colliderect(self.rect):
                    movedir = m.atan2(self.pos[1]-entity.pos[1],self.pos[0] - entity.pos[0])

                    posmod = posmod[0] + MOVESPEED*m.cos(movedir), posmod[1] + MOVESPEED*m.sin(movedir)
                

        # This is again just to make sure shit is rotated right
        rotatedimg = pygame.transform.rotate(self.img, -self.dir) 
        self.mask = pygame.mask.from_surface(rotatedimg) # Don't know why I bother with this shit it doesn't work well at all
        self.rect = self.mask.get_rect(center = (self.pos[0]*TILESIZE + 0.5*TILESIZE, self.pos[1]*TILESIZE+ 0.5*TILESIZE))
        surface.blit(rotatedimg, self.rect)
        
        # This is scaling and centering the hitbox for collision detection
        center = self.rect.center
        self.rect.h = self.rectsize
        self.rect.w = self.rectsize
        self.rect.center = center  

        # This is to show hitboxes if in debug mode
        if DEBUGMODE:
            hitbox = pygame.surface.Surface((self.rect.w, self.rect.h))
            surface.blit(hitbox, self.rect)
        
        # This is map collisions
        posmodscaled = posmod[0]*TILESIZE, posmod[1]*TILESIZE

        if posmod != (0,0):
            self.rect.center = self.rect.center[0] + posmodscaled[0], self.rect.center[1]
            if getmapcollide(self.rect, maphandler, False):
                self.rect.center = self.rect.center[0] - posmodscaled[0], self.rect.center[1]
            else:
                self.pos = self.pos[0] + posmod[0], self.pos[1] 

            self.rect.center = self.rect.center[0], self.rect.center[1] + posmodscaled[1]
            if getmapcollide(self.rect, maphandler, True):
                self.rect.center = self.rect.center[0], self.rect.center[1] - posmodscaled[1]
            else:
                self.pos = self.pos[0], self.pos[1]  + posmod[1]
            
            if DEBUGMODE:
                print ("X collide: " + str(getmapcollide(self.rect, maphandler, False)) +\
                        "\nY collide :" + str(getmapcollide(self.rect, maphandler, True)))
                print (posmod)


class Entityhandler():
    '''
    This just handles the many instances of the Entity class concisely.
    '''
    def __init__(self, player):
        self.entities = [Entity('cratesprite', (3,3), 15), Entity('playersheet', (2,2), 0, player)]
        self.frame = 0 # Frame is just to keep track of when to shift animated entities' frames
    
    def draw(self, surface, maphandler): # Draws all the entites onto the map
        nextframe = False
        self.frame += 1
        if self.frame >= FPS/ANIMATIONSPEED:
            nextframe = True
            self.frame = 0

        for entity in self.entities:
            entity.draw(surface, nextframe, self.entities, maphandler)