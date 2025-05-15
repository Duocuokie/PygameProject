import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy

#fast slippery enemy

SPRITE = pygame.image.load("textures/enemy3.png")

class Enemy3(Enemy):
    def __init__(self, pos, event):
        super().__init__(pos, event)
        self.sprite = SPRITE
        self.id = 2
        self.radius = 6
        self.maxSpeed = 400
        self.acceleration = 300
        self.hp = 10

        self.spin = 0
        self.atk = 15

        self.kbResist = 2
        self.kb = 1100
        self.score = 15

    def update(self, camPos, playerPos, delta):
        self.findPlayer(playerPos)
        self.applyAccel(self.direction, delta)
        self.position += self.velocity * delta
        self.spin = (self.spin + 360 * delta) % 360
        self.rotation = self.spin
        self.updateImage(camPos)