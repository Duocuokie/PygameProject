import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

SPRITE = pygame.image.load("textures/playerProj.png")

# player projectile   scales based on charge

class PlayerProj1(Projectile):
    def __init__(self, angle, pos, charge):
        super().__init__(angle, pos)
        self.sprite = SPRITE
        self.atk = round(charge)
        self.pierce = int((charge ** 2 )/96 + 1)
        size = charge/16
        self.scale = [0.25 + size, 0.25 + size]
    
        self.radius = 4 + (size*16)/2
