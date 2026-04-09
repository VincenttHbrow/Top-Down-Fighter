import pygame
from settings import *
import math as m


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

        # This (should) divide the spritesheet into seperate frames within a nested list, sorted into animations by row.
        if spritefile[-5:] == 'sheet':
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
        if self.player != None:
            self.dir = self.player.dir
            self.pos = self.player.pos
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
                if entity.rect.collidepoint(self.rect.center):
                    movedir = m.atan2(self.pos[1]-entity.pos[1],self.pos[0] - entity.pos[0])
                    self.pos = self.pos[0] + 0.05*m.cos(movedir), self.pos[1]

                    self.tile = maphandler.mapdata[round(self.pos[1])][round(self.pos[0])]
                    if maphandler.tiledata[self.tile]:
                         self.pos = self.pos[0] - 0.05*m.cos(movedir), self.pos[1]

                    self.pos = self.pos[0], self.pos[1] + 0.05*m.sin(movedir)
                    self.tile = maphandler.mapdata[round(self.pos[1])][round(self.pos[0])]
                    if maphandler.tiledata[self.tile]:
                        self.pos = self.pos[0], self.pos[1] - 0.05*m.sin(movedir)


        # This is again just to make sure shit is rotated right
        rotatedimg = pygame.transform.rotate(self.img, -self.dir) 
        self.mask = pygame.mask.from_surface(rotatedimg) # Don't know why I bother with this shit it doesn't work well at all
        self.rect = self.mask.get_rect(center = (self.pos[0]*TILESIZE + 0.5*TILESIZE, self.pos[1]*TILESIZE+ 0.5*TILESIZE))
        surface.blit(rotatedimg, self.rect)


class Entityhandler():
    '''
    This just handles the many instances of the Entity class concisely.
    '''
    def __init__(self, player):
        self.entities = [Entity('cratesprite', (3,3), 0), Entity('playersheet', (0,0), 0, player)]
        self.frame = 0 # Frame is just to keep track of when to shift animated entities' frames
    
    def draw(self, surface, maphandler): # Draws all the entites onto the map
        nextframe = False
        self.frame += 1
        if self.frame >= FPS/ANIMATIONSPEED:
            nextframe = True
            self.frame = 0

        for entity in self.entities:
            entity.draw(surface, nextframe, self.entities, maphandler)