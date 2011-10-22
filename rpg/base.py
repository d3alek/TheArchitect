#!/usr/bin/env python

import os, pygame

from pygame.locals import RLEACCEL

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

IMAGES_FOLDER = "images"

# == PRIMITIVE IMAGE METHODS ==

def createRectangle(dimensions, colour = None):
    rectangle = pygame.Surface(dimensions).convert()
    if colour is not None:
        rectangle.fill(colour)
    return rectangle
    
def createShadedRectangle(dimensions, colour, reverseShaded = False):
    rectangle = createRectangle(dimensions, colour)
    maxX = dimensions[0] - 1
    maxY = dimensions[1] - 1
    if reverseShaded:
        colour1, colour2 = BLACK, WHITE
    else:
        colour1, colour2 = WHITE, BLACK
    pygame.draw.line(rectangle, colour1, (0, 0), (maxX, 0))
    pygame.draw.line(rectangle, colour1, (0, 0), (0, maxY))
    pygame.draw.line(rectangle, colour2, (maxX, maxY), (maxX, 0))
    pygame.draw.line(rectangle, colour2, (maxX, maxY), (0, maxY))
    return rectangle

def createOutlineRectangle(dimensions, fillColour, outlineColour):
    rectangle = createRectangle(dimensions, fillColour)
    maxX = dimensions[0] - 1
    maxY = dimensions[1] - 1
    pygame.draw.line(rectangle, outlineColour, (0, 0), (maxX, 0))
    pygame.draw.line(rectangle, outlineColour, (0, 0), (0, maxY))
    pygame.draw.line(rectangle, outlineColour, (maxX, maxY), (maxX, 0))
    pygame.draw.line(rectangle, outlineColour, (maxX, maxY), (0, maxY))
    return rectangle

def drawText(source, text, textSize, textColour, dropShadow = False, copy = False):
    if copy:
        rectangle = pygame.Surface(source.get_size()).convert()
        rectangle.blit(source, (0, 0))
    else:
        rectangle = source
    font = pygame.font.Font(None, textSize)
    if dropShadow:
        fontText = font.render(text, 1, BLACK)
        position = fontText.get_rect(centerx = rectangle.get_width() / 2 + 2, centery = rectangle.get_height() / 2 + 2)
        rectangle.blit(fontText, position)
    fontText = font.render(text, 1, textColour)
    position = fontText.get_rect(centerx = rectangle.get_width() / 2, centery = rectangle.get_height() / 2)
    rectangle.blit(fontText, position)
    return rectangle

def loadImage(imagePath, colourKey = None):
    # fullName = os.path.join(folder, name)
    try:
        image = pygame.image.load(imagePath)
    except pygame.error, message:
        print "Cannot load image: ", os.path.abspath(imagePath)
        raise SystemExit, message
    image = image.convert()
    if colourKey is not None:
        image.set_colorkey(colourKey, RLEACCEL)
    return image
        
