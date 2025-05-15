import pygame
from pygame.locals import *
from pygame.math import *

#abstrace camera that stores the offset for the came objects

class Camera():
    def __init__(self):
        self.position = Vector2(0, 0)

    #lerps to target
    def update(self, targetPos, halfScreenSize):
        self.position = self.position.lerp(-targetPos + (halfScreenSize), 0.1)