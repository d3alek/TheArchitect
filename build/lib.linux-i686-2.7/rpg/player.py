#!/usr/bin/env python

import events

from sprites import *
from view import UP, DOWN, LEFT, RIGHT
from spriteframes import DirectionalFrames
from events import PlayerFootstepEvent, LifeLostEvent

#DUMMY_EVENT = events.DummyEvent()
PLAYER_FOOTSTEP_EVENT = PlayerFootstepEvent()
LIFE_LOST_EVENT = LifeLostEvent()

DIAGONAL_TICK = 3

NO_BOUNDARY = 0

"""
Valid movement combinations - movement is keyed on direction bits and is stored
as a tuple (px, py, direction, diagonal)
""" 
MOVEMENT = {UP: (0, -MOVE_UNIT, UP, False),
            DOWN: (0, MOVE_UNIT, DOWN, False),
            LEFT: (-MOVE_UNIT, 0, LEFT, False),
            RIGHT: (MOVE_UNIT, 0, RIGHT, False),
            UP + LEFT: (-MOVE_UNIT, -MOVE_UNIT, UP, True),
            UP + RIGHT: (MOVE_UNIT, -MOVE_UNIT, UP, True),
            DOWN + LEFT: (-MOVE_UNIT, MOVE_UNIT, DOWN, True),
            DOWN + RIGHT: (MOVE_UNIT, MOVE_UNIT, DOWN, True)}

def getMovement(directionBits):
    if directionBits in MOVEMENT:
        return MOVEMENT[directionBits]
    return None

"""
An animated player controlled sprite.  This provides movement + masking by
extending MaskSprite, but all animation functionality is encapsulated here.
"""        
class Player(RpgSprite):
    
    def __init__(self, spriteFrames, position = (0, 0)):
        RpgSprite.__init__(self, spriteFrames, position)
        # view rect is the scrolling window onto the map
        self.viewRect = Rect((0, 0), pygame.display.get_surface().get_size())
        # movement
        self.movement = None
        self.deferredMovement = None
        # counters
        self.coinCount = None
        self.keyCount = None
        self.lives = None
        self.ticks = 0
        
    """
    Base rect for the player extends beyond the bottom of the sprite image.
    """
    def getBaseRectTop(self, baseRectHeight):
        return self.mapRect.bottom + BASE_RECT_EXTEND - baseRectHeight
    
    """
    The view rect is entirely determined by what the player is doing.  Sometimes
    we move the view, sometimes we move the player - it just depends where the
    player is on the map.
    """
    def updateViewRect(self):
        # centre self.rect in the view
        px, py = (self.viewRect.width - self.rect.width) // 2, (self.viewRect.height - self.rect.height) // 2
        self.rect.topleft = (px, py)
        self.viewRect.topleft = (self.mapRect.left - px, self.mapRect.top - py)
        rpgMapRect = self.rpgMap.mapRect
        if rpgMapRect.contains(self.viewRect):
            return
        # the requested view falls partially outside the map - we need to move
        # the sprite instead of the view
        px, py = 0, 0
        if self.viewRect.left < 0:
            px = self.viewRect.left
        elif self.viewRect.right > rpgMapRect.right:
            px = self.viewRect.right - rpgMapRect.right
        if self.viewRect.top < 0:
            py = self.viewRect.top
        elif self.viewRect.bottom > rpgMapRect.bottom:
            py = self.viewRect.bottom - rpgMapRect.bottom
        self.rect.move_ip(px, py)
        self.viewRect.move_ip(-px, -py)
    
    """
    Moves the player + updates the view rect.  The control flow is as follows:
    > Check for deferred movement and apply if necessary.
    > Otherwise, check the requested movement is valid.
    > If valid, apply the requested movement.
    > If not valid, attempt to slide/shuffle the player.
    > If still not valid, check for a change in direction.
    """
    def handleMovement(self, directionBits):
        movement = getMovement(directionBits)
        # no movement
        if not movement:
            return self.viewRect
        # check for deferred movement
        if movement == self.movement:
            self.ticks = (self.ticks + 1) % DIAGONAL_TICK
            if self.deferredMovement:
                level, direction, px, py = self.deferredMovement
                self.wrapMovement(level, direction, px, py)
                return
        else:
            self.ticks = 0
        # otherwise apply normal movement
        self.movement = movement
        px, py, direction, diagonal = movement
        # is the requested movement valid?
        newBaseRect = self.baseRect.move(px, py)
        valid, level = self.rpgMap.isMoveValid(self.level, newBaseRect)
        if valid:
            # if movement diagonal we only move 2 out of 3 ticks
            if diagonal and self.ticks == 0:
                self.deferMovement(level, direction, px, py)
            else:
                self.wrapMovement(level, direction, px, py)
            return
        # movement invalid but we might be able to slide or shuffle
        if diagonal:
            valid = self.slide(movement)
        else:
            valid = self.shuffle(movement)
        # movement invalid - apply a stationary change of direction if required
        if not valid and self.spriteFrames.direction != direction:
            self.setDirection(direction);
    
    """
    Slides the player. If the player is attempting to move diagonally, but is
    blocked, the vertical or horizontal component of their movement may still
    be valid.
    """
    def slide(self, movement):
        px, py, direction, diagonal = movement
        # check if we can slide horizontally
        xBaseRect = self.baseRect.move(px, 0)
        valid, level = self.rpgMap.isMoveValid(self.level, xBaseRect)
        if valid:
            #self.movement = movement
            self.deferMovement(level, direction, px, 0)
            return valid
        # check if we can slide vertically
        yBaseRect = self.baseRect.move(0, py)
        valid, level = self.rpgMap.isMoveValid(self.level, yBaseRect)                
        if valid:
            #self.movement = movement
            self.deferMovement(level, direction, 0, py)
        return valid
        
    """
    Shuffles the player.  Eg. if the player is attempting to move up, but is
    blocked, we will 'shuffle' the player left/right if there is valid movement
    available to the left/right.  This helps to align the player with steps,
    doorways, etc.
    """
    def shuffle(self, movement):
        px, py, direction, diagonal = movement
        # check if we can shuffle horizontally
        if px == 0:
            valid, level, shuffle = self.rpgMap.isVerticalValid(self.level, self.baseRect)
            if valid:
                #self.movement = movement
                self.deferMovement(level, direction, px + shuffle * MOVE_UNIT, 0)
            return valid
        # check if we can shuffle vertically
        valid, level, shuffle = self.rpgMap.isHorizontalValid(self.level, self.baseRect)
        if valid:
            #self.movement = movement
            self.deferMovement(level, direction, 0, py + shuffle * MOVE_UNIT)
        return valid
    
    """
    Calls applyMovement and performs some additional operations.
    """      
    def wrapMovement(self, level, direction, px, py):
        self.deferredMovement = None
        self.applyMovement(level, direction, px, py)
        self.updateViewRect()
    
    """
    Stores the deferred movement and calls applyMovement with px, py = 0 for a
    'running on the spot' effect.
    """
    def deferMovement(self, level, direction, px, py):
        # store the deferred movement
        self.deferredMovement = (level, direction, px, py)
        self.applyMovement(level, direction, 0, 0)
    
    """
    Applies valid movement.
    """
    def applyMovement(self, level, myDirection, px, py):
        # move the player to its new location
        self.level = level
        self.doMove(px, py)
        # animate the player
        self.clearMasks()
        self.image, frameIndex = self.spriteFrames.advanceFrame(direction = myDirection)
        if frameIndex == 1 or frameIndex == 3:
            self.eventBus.dispatchPlayerFootstepEvent(PLAYER_FOOTSTEP_EVENT)
        self.applyMasks()
    
    """
    Sets the direction without moving anywhere.
    """
    def setDirection(self, direction):
        self.applyMovement(self.level, direction, 0, 0)
        
    """
    Checks the requested movement falls within the map boundary.  If not, returns
    a boundary event containing information on the breach. 
    """ 
    def getBoundaryEvent(self):
        #testMapRect = self.mapRect.move(px, py)
        if self.rpgMap.mapRect.contains(self.mapRect):
            # we're within the boundary
            return None
        boundary = self.getBoundary()
        if boundary in self.rpgMap.boundaryEvents:
            tileRange = self.getTileRange(boundary)
            for event in self.rpgMap.boundaryEvents[boundary]:
                testList = [i in event.range for i in tileRange]
                if all(testList):
                    return event
        print "boundary!"
        return None
    
    """
    Returns the boundary that has been breached.
    """
    def getBoundary(self):
        boundary = NO_BOUNDARY
        rpgMapRect = self.rpgMap.mapRect
        if self.mapRect.left < 0:
            boundary = LEFT
        elif self.mapRect.right > rpgMapRect.right:
            boundary = RIGHT
        if self.mapRect.top < 0:
            boundary = UP
        elif self.mapRect.bottom > rpgMapRect.bottom:
            boundary = DOWN
        return boundary

    def getTileRange(self, boundary):
        tx1, ty1 = self.getTilePoint(self.baseRect.left, self.baseRect.top)
        tx2, ty2 = self.getTilePoint(self.baseRect.right - 1, self.baseRect.bottom - 1)
        print "(%s, %s) -> (%s, %s)" % (tx1, ty1, tx2, ty2)
        if boundary == UP or boundary == DOWN:
            return range(tx1, tx2 + 1)
        return range(ty1, ty2 + 1)
    
    def getTilePoint(self, px, py):
        return px // TILE_SIZE, py // TILE_SIZE
            
    """
    Processes events triggered via event tiles.
    """
    def processEvents(self):
        if self.level in self.rpgMap.tileEvents:
            for event in self.rpgMap.tileEvents[self.level]:
                if self.baseRect.colliderect(event.rect):
                    return event
        return None
    
    """
    Processes collisions with other sprites in the given sprite collection.
    """
    def processCollisions(self, sprites):
        # if there are less than two sprites then self is the only sprite
        if len(sprites) < 2:
            return False
        for sprite in sprites:
            if sprite.isIntersecting(self):
                return sprite.processCollision(self)
        return False

    """
    Processes interactions with other sprites in the given sprite collection.
    """
    def processActions(self, sprites):
        # if there are less than two sprites then self is the only sprite
        if len(sprites) < 2:
            return
        for sprite in sprites:
            if sprite.isIntersecting(self):
                sprite.processAction(self)
    
    """
    Gets the current view of the map.
    """            
    def getMapView(self):
        return self.rpgMap.getMapView(self.viewRect)
                        
    """
    Handles action input from the user.
    """
    def handleAction(self, sprites):
        self.processActions(sprites)
                    
    def incrementCoinCount(self, n = 1):
        self.coinCount.incrementCount(n)
        
    def incrementKeyCount(self, n = 1):
        self.keyCount.incrementCount(n)
        
    def getCoinCount(self):
        return self.coinCount.count;

    def getKeyCount(self):
        return self.keyCount.count;

    def loseLife(self, n = -1):
        self.eventBus.dispatchLifeLostEvent(LIFE_LOST_EVENT)
        self.lives.incrementCount(n)
        
    def gameOver(self):
        return self.lives.noneLeft()
        
"""
Extends the player sprite by defining a set of frame images.
"""    
class Ulmo(Player):
    
    framesImage = None
    
    def __init__(self):
        if Ulmo.framesImage is None:          
            imagePath = os.path.join(SPRITES_FOLDER, "ulmo-frames.png")
            Ulmo.framesImage = view.loadScaledImage(imagePath, None)
        animationFrames = view.processMovementFrames(Ulmo.framesImage)
        spriteFrames = DirectionalFrames(animationFrames, 6)
        Player.__init__(self, spriteFrames, (1, 4))
        