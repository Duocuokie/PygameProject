import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

SPRITE = pygame.image.load("textures/enemyProj.png")

#projectile for enemy 4

class EnemyProj1(Projectile):
    def __init__(self, angle, pos):
        super().__init__(angle, pos)
        self.sprite = SPRITE
        self.radius = 3

        self.speed = 460


        self.atk = 8
        self.pierce = 0
        self.kb = 1000
        self.layer = 1

