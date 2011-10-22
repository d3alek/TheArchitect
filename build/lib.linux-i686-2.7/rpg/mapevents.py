#! /usr/bin/env python

from pygame.locals import Rect
from view import TILE_SIZE

DUMMY_EVENT = 0
TILE_EVENT = 1
BOUNDARY_EVENT = 2

SCENE_TRANSITION = 1
REPLAY_TRANSITION = 2
BOUNDARY_TRANSITION = 3
GAME_OVER_TRANSITION = 4
END_GAME_TRANSITION = 5

EMPTY_LIST = []

"""
There are two parts to each map event:
1. The event itself, eg. a BoundaryEvent indicates that the player has breached a
map boundary.
2. A transition that describes what happens next, eg. a SceneTransition indicates
that we need to replace the current map with another map.

For example, a BoundaryEvent might result in a BoundaryTransition, when the
player walks off the edge of one map and onto another, OR a SceneTransition,
when the player walks out of a cave for example. 
"""
class MapEvent:
    def __init__(self, type, transition = None):
        self.type = type
        self.transition = transition

"""
Defines an event that doesn't do anything.
"""
class DummyEvent(MapEvent):
    def __init__(self, boundary = None):
        MapEvent.__init__(self, DUMMY_EVENT)
        self.boundary = boundary

"""
Defines an event that occurs when the player steps on a listed tile.
"""
class TileEvent(MapEvent):
    def __init__(self, transition, x, y, level):
        MapEvent.__init__(self, TILE_EVENT, transition)
        self.rect = Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.level = level

"""
Defines an event that occurs when the player walks off the edge of the map.
"""        
class BoundaryEvent(MapEvent):
    def __init__(self, transition, boundary, min, max = None):
        MapEvent.__init__(self, BOUNDARY_EVENT, transition)
        self.boundary = boundary
        if max:
            self.range = range(min, max + 1)
        else:
            self.range = [min]

"""
Transition base class.
"""
class Transition:
    def __init__(self, type, mapName = None):
        self.type = type
        self.mapName = mapName

"""
Defines a transition that occurs when we switch from one scene to another, eg.
when the player walks into a cave.
"""            
class SceneTransition(Transition):
    def __init__(self, mapName, x, y, level, direction, boundary = None):
        Transition.__init__(self, SCENE_TRANSITION, mapName)
        self.tilePosition = (x, y)
        self.level = level
        self.direction = direction
        self.boundary = boundary
        self.firstMap = False

"""
Defines a transition that occurs when the player loses a life and the scene is
reset.  Note that this is very similar to a scene transition.
"""        
class ReplayTransition(Transition):
    def __init__(self, mapName, px, py, level, direction, boundary = None):
        Transition.__init__(self, REPLAY_TRANSITION, mapName)
        self.pixelPosition = (px, py)
        self.level = level
        self.direction = direction
        self.boundary = boundary
        self.firstMap = False

"""
Defines a transition that occurs when the player walks off the edge of one map
and onto another.
"""        
class BoundaryTransition(Transition):
    def __init__(self, mapName, boundary, modifier = 0):
        Transition.__init__(self, BOUNDARY_TRANSITION, mapName)
        self.boundary = boundary
        self.modifier = modifier
        
class GameOverTransition(Transition):
    def __init__(self):
        Transition.__init__(self, GAME_OVER_TRANSITION)
        
class EndGameTransition(Transition):
    def __init__(self):
        Transition.__init__(self, END_GAME_TRANSITION)
    
