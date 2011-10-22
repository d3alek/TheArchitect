#! /usr/bin/env python

import pygame

from othersprites import Beetle, Wasp
from staticsprites import Flames, Coin, Key, Chest, Rock, Door

# map of sprite classes keyed on type
spriteClasses = {"flames": Flames,
                 "coin": Coin,
                 "key": Key,
                 "chest": Chest,
                 "rock": Rock,
                 "door": Door,
                 "beetle": Beetle,
                 "wasp": Wasp}

"""
Returns a sprite instance based on the given mapSprite.  If the registry
indicates that the sprite has been removed from the map, this method returns
None.
"""
def createSprite(mapSprite, rpgMap, eventBus, registry):
    spriteMetadata = registry.getMetadata(mapSprite.uid);
    if spriteMetadata:
        # allow any interactions with the map, eg. an open door
        spriteMetadata.applyMapActions(rpgMap)
        if spriteMetadata.isRemovedFromMap():
            return None
    if mapSprite.type in spriteClasses:
        spriteClass = spriteClasses[mapSprite.type]
        sprite = spriteClass()
        sprite.setup(mapSprite.uid, rpgMap, eventBus)
        return sprite
    print "sprite type not found:", mapSprite.type 
    return None

"""
Returns a sprite group for the given map.  This excludes any sprites that are
removed from the map.
"""
def createSpritesForMap(rpgMap, eventBus, registry):
    gameSprites = pygame.sprite.Group()
    if rpgMap.mapSprites:
        for mapSprite in rpgMap.mapSprites:
            sprite = createSprite(mapSprite, rpgMap, eventBus, registry)
            if sprite:
                sprite.initMovement(mapSprite.level, mapSprite.tilePoints)
                gameSprites.add(sprite)
    return gameSprites
