import pygame
from pygame.locals import *
from pygame.math import *
from gameObject import GameObject
import time

class Projectile(GameObject):
    def __init__(self, angle, pos):
        super().__init__()
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill((220, 175, 30))
        self.rect = self.image.get_rect()
        self.radius = 6

        self.rect.center = pos
        self.position = pos
        self.speed = 500
        self.angle = angle
        self.velocity = Vector2(self.speed, 0).rotate(-angle)

        self.damage = 5
        self.pierce = 0
        self.kb = 600
        self.layer = 0

        
    def update(self, camPos, delta):
        #self.rect.move_ip(self.velocity)
        self.position += self.velocity * delta
        self.updateImage(camPos)