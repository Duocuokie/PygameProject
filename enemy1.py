import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy

#basic enemy

SPRITE = pygame.image.load("textures/enemy1.png")

class Enemy1(Enemy):
    def __init__(self, pos, event):
        super().__init__(pos, event)
        self.sprite = SPRITE
        self.id = 0

        
        self.maxSpeed = 220
        self.acceleration = 2500
        self.hp = 25

        self.kb = 900