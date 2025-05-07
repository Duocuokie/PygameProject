import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

class PlayerProj1(Projectile):
    def __init__(self, angle, pos, charge):
        super().__init__(angle, pos)
        self.atk = int(charge)