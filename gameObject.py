import pygame
from pygame.locals import *
from pygame.math import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.position = Vector2(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.rotation = 0
        self.scale = [1, 1]
        self.camPos = Vector2(0,0)




    def update(self, camPos, delta):
        prevCenter = self.position
        self.image = pygame.Surface((16, 16))
        if self.rotation != 0:
            self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = prevCenter + camPos
        #self.rect.move_ip(camPos)
