#! /usr/bin/env python

"""
Registry class that stores the state of the game.  A save game feature could be
implemented by serializing this class.
"""
class Registry:
    
    def __init__(self):
        # a map of sprite metadata keyed on uid 
        self.spriteMetadata = {}

    def registerMetadata(self, spriteMetadata):
        self.spriteMetadata[spriteMetadata.uid] = spriteMetadata
        
    def getMetadata(self, uid):
        if uid in self.spriteMetadata:
            return self.spriteMetadata[uid]
        return None
    
    # ==========================================================================
         
    def coinCollected(self, coinCollectedEvent):
        self.registerMetadata(coinCollectedEvent.getMetadata())
        
    def keyCollected(self, keyCollectedEvent):
        self.registerMetadata(keyCollectedEvent.getMetadata())
        
    def doorOpened(self, doorOpenedEvent):
        self.registerMetadata(doorOpenedEvent.getMetadata())