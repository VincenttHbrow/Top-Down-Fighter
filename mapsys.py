import pygame
from settings import *

class Map():
    def __init__(self):
        pass

    def load(self, mapname):
        self.mapfile = open((mapname + ".txt"), 'r')
        self.mapdata = self.mapfile.read().splitlines()
        # insert tileset loading system involving (mapname + ".png")
        # the following is placeholder tileset loading
        wall = pygame.image.load('wall.png')
        floor = pygame.image.load('floor.png')
        self.tiles = [0,wall,floor]
        self.tiledata = {1: True,
                         2: False}
        print ('Map successfully loaded! \nMapdata:')
        print (self.mapdata)
        
    def draw(self):
        surface = pygame.surface.Surface((len(self.mapdata[0])*TILESIZE, len(self.mapdata)*TILESIZE))
        for row in range(len(self.mapdata)):
            for tile in range(len(self.mapdata[row])):
                if not self.mapdata[row][tile] == '0':
                    surface.blit(self.tiles[int(self.mapdata[row][tile])], (tile*16, row*16))
        return surface