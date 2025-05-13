import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy

class Enemy2(Enemy):
    def __init__(self, pos, event):
        super().__init__(pos, event)
        self.id = 1
        self.sprite = pygame.Surface((64, 64))
        self.sprite.fill((190, 10, 13))
        self.radius = 28
        self.maxSpeed = 210
        self.acceleration = 2500
        self.hp = 60

        self.atk = 20

        self.kbResist = 0.8
        self.kb = 1350