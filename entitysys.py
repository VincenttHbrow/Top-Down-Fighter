import pygame
from settings import *
import math as m

def getmapcollide(rect, pos, maphandler, vertical):
    '''
    This checks for map collisions at all corners of rect centered on the sprites map position 
    (as opposed to its screen position).
    Should be good unless I have entities bigger than 1 tile which I'm not planning on.
    '''
    modrect = pygame.rect.Rect(rect)
    if vertical: # This bit used to be so 1x1 Tile hitboxes could fit through single-tile gaps.
        modrect.w -=0
    else:
        modrect.h -=0
    modrect.center = pos[0]*TILESIZE,pos[1]*TILESIZE
    rectpoints = [modrect.topleft, modrect.topright, modrect.bottomleft, modrect.bottomright]
    collide = False
    for point in rectpoints:
        tile = maphandler.mapdata[int(point[1]/TILESIZE)][int(point[0]/TILESIZE)]
        if maphandler.tiledata[tile]:
            collide = True
    if DEBUGMODE:
        word = 'X: '
        if vertical:
            word = "Y: "
        print ('rectpoints:' + str(rectpoints) + "\n collide " + word + str(collide))
    return collide

class Entity():
    '''
    This class is for any non-tile thing. 
    Anything interactable, anything living, etc.
    As it stands it just draws the player sprite, but will be used for more stuff in future. 
    '''
    def __init__(self, spritefile, pos = (0,0), dir = 0, ai = None, player = None):
        self.sprite = pygame.image.load('sprites/' + spritefile + '.png').convert_alpha()
        self.animated = False # Just whether an object is a single frame or a spritesheet
        self.player = player # Player should be left empty UNLESS IT'S THE PLAYER CHARACTER
        self.ai = ai
        self.dir = dir
        self.img = self.sprite # This is specifically the image to be drawn on the map at any given time.
        self.pos = pos
        self.rectsize = TILESIZE - 2
        self.occupied = 0 # Occupied is the number of frames in an uncancellable animation
        self.invulnerable = 0 # Number of (animation not engine) frames where an entity can't take damage
        self.weapon = None
        self.weaponimg = None # Image associated with the weapon
        if self.player != None: # Temp code to equip player with spear
            self.weapon = 'spear'

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
        self.rect = self.img.get_rect(center = (self.pos[0]*TILESIZE, self.pos[1]*TILESIZE))

    
    def draw(self, surface, nextframe, entities, maphandler): # Draws the entity's (rotated if applicable) image on the map
        # This is, again, only relevant if it's an enemy, NPC, or PC.
        posmod = 0,0
        if self.dir > 360:
            self.dir -= 360
        if self.dir < 0:
            self.dir += 360

        # Ask AI class what to do
        if self.ai != None:
            if not self.occupied:
                input = self.ai.update(self.pos, self.dir)
                if input[2] != self.currentanim: # Resets animation frame to 0 when switching animations.
                    self.frame = -1
                posmod, dirmod, self.currentanim = input
                self.dir = self.dir + dirmod

        # Get input from player for PC entity
        if self.player != None:
            input = self.player.getmovement(self.occupied, maphandler)
            posmod, dirmod, self.occupied = input
            self.dir += dirmod
            self.player.dir = self.dir
            self.player.pos = self.pos
            if self.player.currentanim != self.currentanim: # Resets animation frame to 0 when switching animations.
                self.frame = -1
            self.currentanim = self.player.currentanim

        
        # This is for animated entities switching frames if applicable, as well as counting occupied and invul. frames
        if nextframe:
            if self.occupied > 0:
                self.occupied -= 1
            if self.invulnerable > 0:
                self.invulnerable -= 1
            if self.animated:
                if not self.frame >= len(self.frames[self.currentanim] ) - 1:
                    self.frame += 1
                else:
                    self.frame = 0
                self.img = self.frames[self.currentanim][self.frame]

        # This is collisions stuff.
        for entity in entities:
            if not entity == self:
                movedir = m.atan2(self.pos[1]-entity.pos[1],self.pos[0] - entity.pos[0])
                if entity.rect.colliderect(self.rect):
                    posmod = posmod[0] + MOVESPEED*m.cos(movedir), posmod[1] + MOVESPEED*m.sin(movedir)
            
                dmgframes = [1,2,5,6]
                if entity.weapon !=None and entity.currentanim > 1 and \
                    entity.frame in dmgframes and self.invulnerable <= 0:
                    # Handles checks for getting hit

                    weapsize = WEAPONDATA[entity.weapon]['size']
                    diroffset = m.cos(m.radians(-entity.dir - 90)), m.sin(m.radians(-entity.dir - 90))
                    linestart = entity.weaprect.center[0]-8*diroffset[0], entity.weaprect.center[1]+8*diroffset[1]
                    lineend = entity.weaprect.center[0]+weapsize*diroffset[0], entity.weaprect.center[1]-weapsize*diroffset[1]
                    if DEBUGMODE: # Draws attack hitbox
                        pygame.draw.line(surface, (255,0,0), linestart, lineend)
                    if self.rect.clipline(linestart, lineend):
                        self.occupied = 2
                        self.invulnerable = 2
                        posmod = posmod[0] + 4*MOVESPEED*m.cos(movedir), posmod[1] + 4*MOVESPEED*m.sin(movedir)
                

        # This is again just to make sure shit is rotated right
        rotatedimg = pygame.transform.rotate(self.img, -self.dir).convert_alpha()
        self.rect = rotatedimg.get_rect(center = ((self.pos[0] - maphandler.playertile[0] + maphandler.offset[0])*TILESIZE,\
                                                 (self.pos[1] - maphandler.playertile[1] + maphandler.offset[1])*TILESIZE))

        if self.weapon != None: # This is for drawing the weapon
            if self.weaponimg == None:
                self.weaponimg = pygame.image.load(('weapons/' + self.weapon + '.png'))
            else:
                rotatedweap = pygame.transform.rotate(self.weaponimg, -self.dir + 45).convert_alpha()
                self.weaprect = rotatedweap.get_rect(center = ((self.pos[0] - maphandler.playertile[0] + maphandler.offset[0])*TILESIZE,\
                                                 (self.pos[1] - maphandler.playertile[1] + maphandler.offset[1])*TILESIZE))
                self.weaprect = self.weaprect.move(m.cos(m.radians(self.dir))*WEAPONXOFFSET, m.sin(m.radians(self.dir))*WEAPONXOFFSET)
                self.weaprect = self.weaprect.move(m.cos(m.radians(self.dir-90))*WEAPONYOFFSET, m.sin(m.radians(self.dir-90))*WEAPONYOFFSET)
                if self.currentanim == 2: # Moves the weapon around for the animation
                    movedist = round(1.6*abs(m.sin(((m.pi*self.frame+1)/4)))*2)*2
                    self.weaprect = self.weaprect.move(m.cos(m.radians(self.dir - 90))*movedist, m.sin(m.radians(self.dir - 90))*movedist)
                surface.blit(rotatedweap, self.weaprect)

        surface.blit(rotatedimg, self.rect)
        
        # This is scaling and centering the hitbox for collision detection
        center = self.rect.center
        self.rect.h = self.rectsize
        self.rect.w = self.rectsize
        self.rect.center = center  

        # This is to show hitboxes if in debug mode
        if DEBUGMODE:
            hitbox = pygame.surface.Surface((self.rect.w, self.rect.h))
            hitbox.fill((0,255,0))
            surface.blit(hitbox, self.rect)
        
        # This is map collisions
        if posmod != (0,0):
            self.pos = self.pos[0] + posmod[0], self.pos[1]
            if getmapcollide(self.rect, self.pos, maphandler, False):
                self.pos = self.pos[0] - posmod[0], self.pos[1]

            self.pos = self.pos[0], self.pos[1] + posmod[1]
            if getmapcollide(self.rect, self.pos, maphandler, True):
                self.pos = self.pos[0], self.pos[1] - posmod[1]
            
            # More debugging stuff
            if DEBUGMODE:
                tile = maphandler.mapdata[int(self.rect.center[1]/TILESIZE)][int(self.rect.center[0]/TILESIZE)]
                print (#"X collide: " + str(getmapcollide(self.rect, self.pos, maphandler, False)) +\
                        #"\nY collide :" + str(getmapcollide(self.rect, self.pos, maphandler, True)) +\
                        "\nHitbox Center:" + str(int(self.rect.center[0]/TILESIZE)) + ',' + str(int(self.rect.center[0]/TILESIZE)) +\
                        "\nTile:" + tile + "\nPosition: " + str(self.pos))
                print ('position modified by ' + str(posmod))


class AI():
    def __init__(self, caution, reaction, movespeed, player):
        self.caution = caution
        self.reaction = reaction
        self.player = player
        self.movespeed = movespeed

    def update(self, epos, dir):
        # direction update part
        ypos1 = self.player.pos[1]
        ypos2 = epos[1]
        xpos1 = self.player.pos[0]
        xpos2 = epos[0]
        targetdir = m.atan2(ypos1 - ypos2 , xpos1 - xpos2)
        targetdir = targetdir*180/m.pi + 90
        if targetdir < 0:
            targetdir = targetdir + 360
        dirmod =  -(dir - targetdir)
        if dirmod > 180:
            dirmod = 180 - dirmod
        if dirmod < -180:
            dirmod = -180 - dirmod
        
        if abs(dirmod) > self.reaction:
            dirmod = dirmod/abs(dirmod)*self.reaction

        # position update part
        movement = self.movespeed*m.cos(m.radians(dir + dirmod - 90)), self.movespeed*m.sin(m.radians(dir + dirmod - 90))
        currentanim = 0
        dist = m.sqrt(round(xpos1 - xpos2)**2 + round(ypos1 - ypos2)**2)
        posmod = 0,0
        if  dist < self.caution - 0.5:
            posmod = -movement[0], -movement[1]
            currentanim = 1
        elif dist > self.caution + 0.5:
            posmod = movement[0], movement[1]
            currentanim = 1


        return posmod, dirmod, currentanim



class Entityhandler():
    '''
    This just handles the many instances of the Entity class concisely.
    '''
    def __init__(self, player):
        self.entities = [Entity('playersheet', (3,3), 0, None, player), Entity('cratesprite', (4,4), 15), \
                         Entity('enemysheet', (5,5), 0, AI(1.6, 0.75, 0.025,player))] 
        self.frame = 0 # Frame is just to keep track of when to shift animated entities' frames
    
    def draw(self, surface, maphandler): # Draws all the entites onto the map
        nextframe = False
        self.frame += 1
        if self.frame >= FPS/ANIMATIONSPEED:
            nextframe = True
            self.frame = 0

        for entity in self.entities:
            entity.draw(surface, nextframe, self.entities, maphandler)