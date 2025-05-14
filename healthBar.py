import pygame
from pygame.locals import *

class HealthBar():
    def __init__(self, position):
        super().__init__()
        self.backSprite = pygame.Surface((128, 32))
        self.backSprite.fill((120, 30, 230))
        self.frontSprite = pygame.Surface((128, 32))
        self.frontSprite.fill((32, 230, 50))
        self.image = self.backSprite.copy()
        self.image.blit(self.frontSprite, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def update(self, hp):
        offset = ((hp/50) *128) - 128
        self.image = self.backSprite.copy()
        shiftBar = self.frontSprite.copy()
        self.image.blit(shiftBar, (offset, 0))
