import pygame
from pygame.locals import *
from pygame.math import *

#sprites in the game scene

class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite = pygame.Surface((16, 16)) 
        self.image = self.sprite.copy()
        self.position = Vector2(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.rotation = 0
        self.scale = [1, 1]
        self.camPos = Vector2(0,0)


    #updates the objects sprite
    #chests for rotation scale and camera position
    def updateImage(self, camPos):
        prevCenter = self.position
        self.image = self.sprite.copy()
        if self.scale != [1, 1]:
            newSize = [int(self.scale[0] * self.sprite.get_width()), int(self.scale[1] * self.sprite.get_height())]
            
            self.image = pygame.transform.scale(self.image, newSize)
        if self.rotation != 0:
            self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = prevCenter + camPos

    def update(self, camPos, delta):
        self.updateImage(camPos)
