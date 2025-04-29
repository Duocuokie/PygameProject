import pygame
from pygame.locals import *
from pygame.math import *
from gameObject import GameObject

class Projectile(GameObject):
    def __init__(self, angle, pos):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        
        self.image.fill((220, 175, 30))
        self.rect = self.image.get_rect()
        self.radius = 6
        self.rect.center = pos
        self.position = pos
        self.speed = 500
        self.angle = angle
        self.velocity = Vector2(self.speed, 0).rotate(-angle)
        print(self.velocity)
        
    def update(self, camPos, delta):
        #self.rect.move_ip(self.velocity)
        self.position += self.velocity * delta
        self.rect.center = self.position + camPos