import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy

class Enemy1(Enemy):
    def __init__(self, pos, event):
        super().__init__(pos, event)
        self.id = 0


        
        self.maxSpeed = 220
        self.acceleration = 2500
        self.hp = 25

        self.kb = 900