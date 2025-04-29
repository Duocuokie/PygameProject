import pygame
from pygame.locals import *
from pygame.math import *
import math
from gameObject import GameObject

class Enemy(GameObject):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((32, 32))
        self.image.fill((220, 25, 30))
        self.rect = self.image.get_rect()
        
        self.rect.center = pos
        self.position = pos

        self.direction = Vector2(0, 0)
        
        self.radius = 12
        self.velocity = Vector2(0.0, 0.0)
        self.maxSpeed = 3.5
        self.acceleration = 60

    def findPlayer(self, playerPos):
        if Vector2(self.rect.center).distance_squared_to(Vector2(playerPos)) > 0:
            self.direction = (Vector2(playerPos) - Vector2(self.rect.center)).normalize()
        else:
            self.direction = Vector2(0,0)
        self.playerAngle = -math.degrees(math.atan2(self.direction[1], self.direction[0]))

    def applyAccel(self, dir, delta):
        self.velocity = self.velocity.move_towards(dir * self.maxSpeed, self.acceleration * delta)

    def update(self, camPos, playerPos, delta):
        self.findPlayer(playerPos)
        self.applyAccel(self.direction, delta)
        self.position += self.velocity
        self.rect.center = self.position + camPos