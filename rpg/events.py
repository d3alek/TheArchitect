#! /usr/bin/env python

class Event():    
    def getMetadata(self):
        pass

class DoorOpeningEvent(Event):
    pass

class PlayerFootstepEvent(Event):
    pass

class MapTransitionEvent(Event):
    pass

class LifeLostEvent(Event):
    pass

class EndGameEvent(Event):
    pass

class WaspZoomingEvent(Event):
    pass

class BeetleCrawlingEvent(Event):
    pass

# ==============================================================================

class MetadataEvent(Event):
    
    def __init__(self, metadata):
        self.metadata = metadata
        
    def getMetadata(self):
        return self.metadata
        
class CoinCollectedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)

class KeyCollectedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)

class DoorOpenedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)

# ==============================================================================

class SpriteMetadata:
    
    def __init__(self, uid):
        self.uid = uid
    
    # placeholder method    
    def isRemovedFromMap(self):
        return False
    
    # placeholder method
    def applyMapActions(self, rpgMap):
        pass
    
class CoinMetadata(SpriteMetadata):
    
    def __init__(self, uid, collected = True):
        SpriteMetadata.__init__(self, uid)
        self.collected = collected

    def isRemovedFromMap(self):
        return self.collected
        
class KeyMetadata(SpriteMetadata):

    def __init__(self, uid, collected = True):
        SpriteMetadata.__init__(self, uid)
        self.collected = collected
        
    def isRemovedFromMap(self):
        return self.collected

class DoorMetadata(SpriteMetadata):
    
    def __init__(self, uid, x, y, level, open = True):
        SpriteMetadata.__init__(self, uid)
        self.x, self.y = x, y
        self.level = level
        self.open = open

    def isRemovedFromMap(self):
        return self.open
    
    # makes the corresponding tile available for this level
    def applyMapActions(self, rpgMap):
        rpgMap.addLevel(self.x, self.y + 1, self.level)
