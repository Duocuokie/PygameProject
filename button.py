import pygame
from pygame.locals import *

class Button():
    def __init__(self, pos, sprites, id):
        self.position = pos
        self.image = sprites[0]
        self.rect = self.image.get_rect()
        self.id = id

    