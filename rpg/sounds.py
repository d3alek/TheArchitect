#!/usr/bin/env python

import os
import pygame

SOUNDS_FOLDER = "sounds"

BEETLE_SOUND_TICKS = 15

def getSound(name, volume):
    soundPath = os.path.join(SOUNDS_FOLDER, name)
    sound = pygame.mixer.Sound(soundPath)
    sound.set_volume(volume)
    return sound

pickupSound = getSound("pickup.wav", 1.0)
doorSound = getSound("door.wav", 1.0)
swooshSound = getSound("swoosh.wav", 0.4)
lifeLostSound = getSound("lifelost.wav", 1.0)
endGameSound = getSound("endgame.wav", 0.6)
footstepSound = getSound("footstep.wav", 0.5)
waspSound = getSound("wasp.wav", 0.8)
beetleSound = getSound("beetle.wav", 0.2)

"""
Listens for specific events and builds up a set of sounds that are played back
when flush is called.
"""
class SoundHandler:
    
    def __init__(self):
        self.sounds = set()
        # properties required for 
        self.nextSound = None
        self.soundOn = True
        self.ready = True
        self.count = 0
            
    def coinCollected(self, coinCollectedEvent):
        self.sounds.add(pickupSound)
        
    def keyCollected(self, keyCollectedEvent):
        self.sounds.add(pickupSound)
        
    def doorOpening(self, doorOpeningEvent):
        self.sounds.add(doorSound)
        
    def playerFootstep(self, playerFootstepEvent):
        self.sounds.add(footstepSound)
        
    def mapTransition(self, mapTransitionEvent):
        self.sounds.add(swooshSound)
        
    def endGame(self, endGameEvent):
        self.sounds.add(endGameSound)
        
    def lifeLost(self, lifeLostEvent):
        self.sounds.add(lifeLostSound)
    
    def waspZooming(self, waspZoomingEvent):
        self.sounds.add(waspSound)
    
    """
    Additional logic here to prevent a 'log jam' of beetle crawling sounds
    """    
    def beetleCrawling(self, beetleCrawlingEvent):
        # if we already have a next sound, ignore it
        if self.nextSound:
            return
        # if ready, add the sound to the set for immediate playback
        if self.ready:
            self.sounds.add(beetleSound)
            self.ready = False
            self.count = 0
            return
        # we're not ready yet - store the sound for later
        self.nextSound = beetleSound
        
    def handleNextSound(self):
        self.count = (self.count + 1) % BEETLE_SOUND_TICKS
        if self.count == 0:
            if self.nextSound:
                self.sounds.add(self.nextSound)
                self.nextSound = None
            else:
                self.ready = True
        
    def flush(self):
        self.handleNextSound()
        # play sounds
        for sound in self.sounds:
            if self.soundOn:
                sound.play()
        self.sounds.clear()
        
    def toggleSound(self):
        self.soundOn = not self.soundOn
        