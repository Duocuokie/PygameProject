import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy

class Enemy3(Enemy):
    def __init__(self, pos, event):
        super().__init__(pos, event)
        self.id = 2
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill((220, 210, 13))
        self.radius = 6
        self.maxSpeed = 400
        self.acceleration = 300
        self.hp = 10

        self.atk = 15

        self.kbResist = 2
        self.kb = 1100
        self.score = 15