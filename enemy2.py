import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy

#big slow enemy

SPRITE = pygame.image.load("textures/enemy2.png")

class Enemy2(Enemy):
    def __init__(self, pos, event):
        super().__init__(pos, event)
        self.sprite = SPRITE
        self.id = 1
        self.radius = 28
        self.maxSpeed = 160
        self.acceleration = 2500
        self.hp = 60

        self.atk = 17

        self.kbResist = 0.8
        self.kb = 1050
        self.score = 25