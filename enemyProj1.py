import pygame
from pygame.locals import *
from pygame.math import *
from projectile import Projectile


class EnemyProj1(Projectile):
    def __init__(self, angle, pos):
        super().__init__(angle, pos)
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill((230, 160, 220))
        self.radius = 3

        self.speed = 460


        self.atk = 10
        self.pierce = 0
        self.kb = 1000
        self.layer = 1

        
    def update(self, camPos, delta):
        #self.rect.move_ip(self.velocity)
        self.position += self.velocity * delta
        self.updateImage(camPos)