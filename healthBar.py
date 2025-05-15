import pygame
from pygame.locals import *

HEALTH = pygame.image.load("textures/healthBar.png")
BASE = pygame.image.load("textures/healthBarBase.png")

#displays player health

class HealthBar():
    def __init__(self, position):
        super().__init__()
        self.backSprite = BASE
        self.frontSprite = HEALTH
        self.image = self.backSprite.copy()
        self.image.blit(self.frontSprite, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    #the lendth of the top bar is determined by player health
    def update(self, hp):
        offset = ((hp/50) *128)
        self.image = self.backSprite.copy()
        shiftBar = self.frontSprite.copy()
        self.image.blit(shiftBar, (0, 0), (0, 0, offset, 32))
