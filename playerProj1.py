import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

class PlayerProj1(Projectile):
    def __init__(self, angle, pos, charge):
        super().__init__(angle, pos)
        self.sprite = pygame.Surface((8, 8))
        self.atk = round(charge)
        self.pierce = int((charge ** 2 )/96 + 1)
        size = charge/8
        self.scale = [1 + size, 1 + size]
    
        self.radius = 4 + (size*16)/2
        self.sprite.fill((20, 175, 230))
        print(self.atk, self.pierce)