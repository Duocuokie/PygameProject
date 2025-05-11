import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

class PlayerProj1(Projectile):
    def __init__(self, angle, pos, charge):
        super().__init__(angle, pos)
        self.atk = round(charge)
        self.pierce = int((charge ** 2 )/96 + 1)
        size = int(charge ** 2/16)
        self.sprite = pygame.Surface((16 + size, 16 + size))
        self.radius = 6 + size/2
        self.sprite.fill((20, 175, 230))
        print(self.atk, self.pierce)