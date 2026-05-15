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
        

    def draw(self, player): # Draws an unscaled map based on whatever file is loaded
        surface = pygame.surface.Surface((RENDERDIST*TILESIZE, RENDERDIST*TILESIZE))
        # Creates a surface that's cropped to be the same size as the map is, so as to rotate properly.

        # This is the offset WITHIN a given tile
        self.offset = -(player.pos[0] - round(player.pos[0])), -(player.pos[1] - round(player.pos[1]))
        # Half the draw distance
        halfdist = 0.5*RENDERDIST
        # This isn't actually the player's tile, it's just the offset on the tile-level
        self.playertile = round(player.pos[0] - halfdist), round(player.pos[1] - halfdist)

        if DEBUGMODE:
            print("playertile:" + str(self.playertile))

        # This loop draws each tile in its correct position on the above created surface.
        for row in range(RENDERDIST):
            if 0 < row + self.playertile[1]  and row + self.playertile[1] < len(self.mapdata):
                for tile in range(RENDERDIST):
                    if 0 < tile + self.playertile[0] and tile + self.playertile[0] < len(self.mapdata[row + self.playertile[1]]):
                        if not self.mapdata[int(row + self.playertile[1])][int(tile + self.playertile[0])] == '0':
                            surface.blit(self.tiles[int(self.mapdata[row + self.playertile[1]][tile + self.playertile[0]])],\
                                         ((tile + self.offset[0])*TILESIZE,(row + self.offset[1])*TILESIZE))


        return surface.convert_alpha()