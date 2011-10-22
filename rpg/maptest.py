#! /usr/bin/env python

import unittest
import pygame
import parser
import view

from pygame.locals import Rect

# initialize everything
pygame.init()
screen = pygame.display.set_mode((1, 1))

# this feels a bit hacky - is there a better way to do it?
parser.MAPS_FOLDER = "../maps"
parser.TILES_FOLDER = "../tiles"

rpgMap = parser.loadRpgMap("islands")

class SpriteInfo:

    def __init__(self, mapRect, level):
        self.mapRect = mapRect
        self.level = level
        
    def move(self, px, py):
        self.mapRect.move_ip(px, py)
        # pseudo z order that is used to test if one sprite is behind another
        self.z = int(self.mapRect.bottom + self.level * 32)
        

class GetMasksTest(unittest.TestCase):
    
    def testLevel1(self):                          
        rect = Rect(10 * view.TILE_SIZE + 2, 1 * view.TILE_SIZE + 8, 30, 48)
        spriteInfo = SpriteInfo(rect, 1)
        spriteInfo.move(0, 0)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(2, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(2, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(2, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        
    def testLevel2(self):
        rect = Rect(10 * view.TILE_SIZE + 8, 1 * view.TILE_SIZE + 2, 24, 48)
        spriteInfo = SpriteInfo(rect, 2)
        spriteInfo.move(0, 0)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(1, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
    
    def testLevel3(self):
        rect = Rect(10 * view.TILE_SIZE + 8, 1 * view.TILE_SIZE + 2, 24, 48)
        spriteInfo = SpriteInfo(rect, 3)
        spriteInfo.move(0, 0)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))
        spriteInfo.move(0, 16)
        self.assertEqual(0, len(rpgMap.getMasks(spriteInfo)))

class MovementValidTest(unittest.TestCase):
    
    def testRow1(self):
        rect = Rect(3 * view.TILE_SIZE + 4, 5 * view.TILE_SIZE + 4, 24, 24)
        baseRect = rect.move(0, 0)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(16, 0)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(32, 0)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2.5), rpgMap.isMoveValid(2, baseRect))

    def testRow2(self):
        rect = Rect(3 * view.TILE_SIZE + 4, 5 * view.TILE_SIZE + 4, 24, 24)
        baseRect = rect.move(0, 16)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(16, 16)
        self.assertEqual(4, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(32, 16)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2.5), rpgMap.isMoveValid(2, baseRect))
        self.assertEqual((True, 2.5), rpgMap.isMoveValid(2.5, baseRect))
        self.assertEqual((False, 3), rpgMap.isMoveValid(3, baseRect))

    def testRow3(self):
        rect = Rect(3 * view.TILE_SIZE + 4, 5 * view.TILE_SIZE + 4, 24, 24)
        baseRect = rect.move(0, 32)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2), rpgMap.isMoveValid(2, baseRect))
        self.assertEqual((False, 2.5), rpgMap.isMoveValid(2.5, baseRect))
        baseRect = rect.move(16, 32)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2), rpgMap.isMoveValid(2, baseRect))
        self.assertEqual((False, 2.5), rpgMap.isMoveValid(2.5, baseRect))
        baseRect = rect.move(32, 32)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 2), rpgMap.isMoveValid(2, baseRect))
        self.assertEqual((True, 2.0), rpgMap.isMoveValid(2.5, baseRect))
        
    def testLevel1(self):
        rect = Rect(10 * view.TILE_SIZE + 4, 2 * view.TILE_SIZE + 4, 24, 24)
        baseRect = rect.move(0, 0)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 1), rpgMap.isMoveValid(1, baseRect))
        baseRect = rect.move(0, 16)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 1), rpgMap.isMoveValid(1, baseRect))
        baseRect = rect.move(0, 32)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 1), rpgMap.isMoveValid(1, baseRect))
        baseRect = rect.move(0, 48)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 1), rpgMap.isMoveValid(1, baseRect))
        baseRect = rect.move(0, 64)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 1), rpgMap.isMoveValid(1, baseRect))
    
    def testLevel2(self):
        rect = Rect(10 * view.TILE_SIZE + 4, 2 * view.TILE_SIZE + 4, 24, 24)
        baseRect = rect.move(0, 0)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(0, 16)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(0, 32)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(0, 48)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
        baseRect = rect.move(0, 64)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 2), rpgMap.isMoveValid(2, baseRect))
    
    def testLevel3(self):
        rect = Rect(10 * view.TILE_SIZE + 4, 2 * view.TILE_SIZE + 4, 24, 24)
        baseRect = rect.move(0, 0)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 3), rpgMap.isMoveValid(3, baseRect))
        baseRect = rect.move(0, 16)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 3), rpgMap.isMoveValid(3, baseRect))
        baseRect = rect.move(0, 32)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((True, 3), rpgMap.isMoveValid(3, baseRect))
        baseRect = rect.move(0, 48)
        self.assertEqual(2, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 3), rpgMap.isMoveValid(3, baseRect))
        baseRect = rect.move(0, 64)
        self.assertEqual(1, len(rpgMap.getRectTiles(baseRect)))
        self.assertEqual((False, 3), rpgMap.isMoveValid(3, baseRect))

if __name__ == "__main__":
    unittest.main()   
