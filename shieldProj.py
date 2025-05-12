import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

class ShieldProj(Projectile):
    def __init__(self, angle, pos):
        super().__init__(angle, pos)
        self.atk = 2
        self.kb = 1000
        self.pierce = None
        self.sprite = pygame.Surface((48, 48))
        self.radius = 32
        self.sprite.fill((20, 200, 50, 100))
        self.position = pos + Vector2(-24, 0).rotate(-angle)

    def update(self, camPos, delta):
        self.position = self.position + Vector2(-24, 0).rotate(-self.angle)
        self.updateImage(camPos)