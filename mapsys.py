import pygame
from settings import *


class Maphandler(): 
    '''
    This class handles map-related variables, reads map files, draws tiles, etc.
    IMPORTANT: Top-left tile of any map file MUST be void for it to display correctly.
    '''

    
    def __init__(self):
        pass
    

    def load(self, mapname):
        self.mapfile = open((mapname + ".txt"), 'r')
        self.mapdata = self.mapfile.read().splitlines()

        # Insert tileset loading system, (maybe?) involving (mapname + ".png")

        # The following is placeholder tileset loading
        wall = pygame.image.load('wall.png')
        floor = pygame.image.load('floor.png')
        self.tiles = [0,wall,floor]
        self.tiledata = {'0': False,
                         '1': True,
                         '2': False}
        
        # Terminal message for when map done loading. Not super important.
        print ('Map successfully loaded! \nMapdata:\n' + str(self.mapdata))
        

    def draw(self): # Draws an unscaled map based on whatever file is loaded
        surface = pygame.surface.Surface((len(self.mapdata[0])*TILESIZE, len(self.mapdata)*TILESIZE))
        # Creates a surface that's cropped to be the same size as the map is, so as to rotate properly.

        # This loop draws each tile in its correct position on the above created surface.
        for row in range(len(self.mapdata)):
            for tile in range(len(self.mapdata[row])):
                if not self.mapdata[row][tile] == '0': # 0 is 'void' tile. 
                    surface.blit(self.tiles[int(self.mapdata[row][tile])], (tile*TILESIZE, row*TILESIZE))
        return surface