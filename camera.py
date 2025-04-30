import pygame
from pygame.locals import *
from pygame.math import *

class Camera():
    def __init__(self):
        self.position = Vector2(0, 0)

    def update(self, targetPos, halfScreenSize):
        self.position = self.position.lerp(-targetPos + (halfScreenSize), 0.1)