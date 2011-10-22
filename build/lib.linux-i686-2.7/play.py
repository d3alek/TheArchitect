#! /usr/bin/env python

from pygame.locals import *

import pygame

# initialise pygame before we import anything else
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

import rpg.states

FRAMES_PER_SEC = 60

def playMain():
    # get the first state
    currentState = rpg.states.startGame()
    # start the main loop
    clock = pygame.time.Clock()    
    while True:
        clock.tick(FRAMES_PER_SEC)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == KEYDOWN and event.key == K_x:
                # mute sound handler
                rpg.states.soundHandler.toggleSound()
        # detect key presses    
        keyPresses = pygame.key.get_pressed()
        # delegate key presses to the current state
        newState = currentState.execute(keyPresses)
        # flush sounds
        rpg.states.soundHandler.flush()
        # change state if necessary
        if newState:
            currentState = newState

# this calls the testMain function when this script is executed
if __name__ == '__main__': playMain()
