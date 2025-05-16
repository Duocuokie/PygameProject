import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile

SPRITE = pygame.image.load("textures/shield.png")

#player shield

class ShieldProj(Projectile):
    def __init__(self, angle, pos):
        super().__init__(angle, pos)
        self.atk = 4
        self.kb = 1000
        self.pierce = None
        self.sprite = SPRITE
        self.radius = 36
        self.offsetAngle = 0
        self.position = pos + Vector2(-32, 0).rotate(-self.offsetAngle)
        self.hitCount = 0

    # shield is slightly behind the player
    def update(self, camPos, delta):
        self.position = self.position + Vector2(-32, 0).rotate(-self.offsetAngle)
        self.rotation = self.offsetAngle
        self.updateImage(camPos)