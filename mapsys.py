import pygame
from settings import *


class Maphandler(): 
    '''
    This class handles map-related variables, reads map files, draws tiles, etc.
    IMPORTANT: Top-left tile of any map file MUST be void for it to display correctly.
    '''

    
    def __init__(self):
        pass
    

    def load(self, mapname, tileset):
        '''
        Loads the map and tileset from disk.
        The first line of the mapfile is whether a given tile is solid. '0' is passable, '1' is solid. 
        Just goes through the tiles in order. Tile 0 is always void, leaving tilesets having 9 tiles.
        This means that the tileset resolution should be 16x144.
        Additionally, because tilesets and solid tiles are stored separately, one map using a given tileset
        could have different wall/floor tiles than another map with that same tileset.
        Not sure if that's useful yet.
        '''
        self.mapfile = open(('maps/' + mapname + ".txt"), 'r')
        self.mapdata = self.mapfile.read().splitlines()
        self.tiledata = {}
        # This is again just putting whether or not tileset should be solid in a dictionary
        for tile in range(len(self.mapdata[0])):
            solid = False
            if self.mapdata[0][tile] == '1':
                solid = True
            self.tiledata[str(tile)] = solid
        self.mapdata.remove(self.mapdata[0])

        # Tile loading system, creates 9 individual tiles from 1 larger tileset image.
        self.tileset = pygame.image.load('tilesets/' + tileset + '.png')
        self.tiles = [0]
        for tile in range(9):
            tilesurface = pygame.surface.Surface((TILESIZE, TILESIZE))
            tilesurface.blit(self.tileset, (-(tile*TILESIZE), 0))
            self.tiles.append(tilesurface)

        
        # Terminal message for when map done loading. Not super important.
        print ('Map successfully loaded! \nMapdata:\n' + str(self.mapdata)+ '\nTiledata:\n'+\
               str(self.tiledata))
        

    def draw(self): # Draws an unscaled map based on whatever file is loaded
        surface = pygame.surface.Surface((len(self.mapdata[0])*TILESIZE, len(self.mapdata)*TILESIZE))
        # Creates a surface that's cropped to be the same size as the map is, so as to rotate properly.

        # This loop draws each tile in its correct position on the above created surface.
        for row in range(len(self.mapdata)):
            for tile in range(len(self.mapdata[row])):
                if not self.mapdata[row][tile] == '0': # 0 is 'void' tile. 
                    surface.blit(self.tiles[int(self.mapdata[row][tile])], (tile*TILESIZE, row*TILESIZE))
        return surface