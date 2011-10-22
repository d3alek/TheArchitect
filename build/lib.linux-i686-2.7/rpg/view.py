#!/usr/bin/env python

from pygame.transform import scale

from base import *

SCALAR = 2

TILE_SIZE = 16 * SCALAR

VIEW_WIDTH = TILE_SIZE * 12
VIEW_HEIGHT = TILE_SIZE * 8

# 0, 51, 102, 153, 204, 255
TRANSPARENT_COLOUR = GREEN
TRANSPARENT_COLOUR_WITH_ALPHA = (0, 255, 0, 255)

NONE = 0
UP = 1
DOWN = 2
LEFT = 4
RIGHT = 8

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

SPRITES_FOLDER = "sprites"

def loadScaledImage(imagePath, colourKey = None, scalar = SCALAR):
    img = loadImage(imagePath, colourKey)
    return scale(img, (img.get_width() * scalar, img.get_height() * scalar))
        
def createDuplicateSpriteImage(spriteImage):
    # transparency is set on the duplicate - this allows us to draw over
    # the duplicate image with areas that are actually transparent
    # img = spriteImage.convert(spriteImage.image)
    img = createRectangle((spriteImage.get_width(), spriteImage.get_height()))
    img.blit(spriteImage, (0, 0))
    img.set_colorkey(TRANSPARENT_COLOUR, RLEACCEL)
    return img

# process animation frames from the composite image
def processMovementFrames(framesImage, numFrames = 4):
    # work out width + height
    framesRect = framesImage.get_rect()
    width = framesRect.width // numFrames
    height = framesRect.height // len(DIRECTIONS)
    # map of image lists for animation keyed on direction
    animationFrames = {}
    row = 0
    for direction in DIRECTIONS:
        frames = []
        rowOffsetY = row * height
        for i in range(numFrames):
            img = framesImage.subsurface(i * width, rowOffsetY, width, height)
            frames.append(img)
        animationFrames[direction] = frames
        row += 1
        #animationFrames[direction + OFFSET] = originalFrames
    return animationFrames

# create a copy of the given animation frames
def copyMovementFrames(animationFrames):
    # map of image lists for animation keyed on direction
    animationFramesCopy = {}
    for direction in DIRECTIONS:
        framesCopy = []
        frames = animationFrames[direction]
        for i in range(len(frames)):
            img = createDuplicateSpriteImage(frames[i])
            framesCopy.append(img)
        animationFramesCopy[direction] = framesCopy
        #animationFrames[direction + OFFSET] = originalFrames
    return animationFramesCopy

# process animation frames from the composite image
def processStaticFrames(framesImage, numFrames = 4):
    framesRect = framesImage.get_rect()
    width = framesRect.width // numFrames
    height = framesRect.height
    # map of images for animation
    animationFrames = []
    for i in range(numFrames):
        img = framesImage.subsurface((i * width, 0), (width, height))
        #animationFrames.append(createDuplicateSpriteImage(img))
        animationFrames.append(img)
    return animationFrames

# create a copy of the given animation frames
def copyStaticFrames(animationFrames):
    # map of image lists for animation keyed on direction
    animationFramesCopy = []
    for i in range(len(animationFrames)):
        img = createDuplicateSpriteImage(animationFrames[i])
        animationFramesCopy.append(img)
    return animationFramesCopy

def createBaseRectImage(baseRect):
    return createRectangle((baseRect.width, baseRect.height), RED)

def createTransparentRect(dimensions):
    transparentRect = createRectangle(dimensions, TRANSPARENT_COLOUR)
    transparentRect.set_colorkey(TRANSPARENT_COLOUR, RLEACCEL)
    return transparentRect

def processFontImage(fontImage, charWidth, rows = 1):
    charImages = []
    charHeight = fontImage.get_height() // rows
    for i in range(rows):
        x, y = 0, i * charHeight
        while x < fontImage.get_width():
            charImage = fontImage.subsurface((x, y), (charWidth, charHeight))
            charImages.append(charImage)
            x += charWidth
    return charImages
