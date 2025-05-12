import pygame
from pygame.locals import *
from pygame.math import *
import math
import random
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, event):
        super().__init__()
        self.id = None

        self.sprite = pygame.Surface((32, 32))
        self.sprite.fill((220, 25, 30))
        self.rect = self.image.get_rect()
        self.radius = 12
        
        self.rect.center = pos
        self.position = pos
        self.direction = Vector2(0, 0)
        
        self.velocity = Vector2(0.0, 0.0)
        self.maxSpeed = 260
        self.acceleration = 3000

        self.kb = 1000
        self.event = event

    def findPlayer(self, playerPos):
        if Vector2(self.rect.center).distance_squared_to(Vector2(playerPos)) > 0:
            self.direction = (Vector2(playerPos) - Vector2(self.rect.center)).normalize()
        else:
            self.direction = Vector2(0,0)
        self.playerAngle = -math.degrees(math.atan2(self.direction[1], self.direction[0]))

    def applyAccel(self, dir, delta):
        self.velocity = self.velocity.move_towards(dir * self.maxSpeed, self.acceleration * delta)

    def softCollide(self, enemy):
        scDir = Vector2(enemy.position - self.position)
        if scDir == Vector2(0, 0):
            scDir = Vector2(1, 0).rotate(random.uniform(0, 360.0))
        else: scDir.normalize()
        self.velocity += -scDir * 8

    def die(self):
        pygame.event.post(pygame.event.Event(self.event, {"enemy" : self}))
        self.kill()

    def update(self, camPos, playerPos, delta):
        self.findPlayer(playerPos)
        self.applyAccel(self.direction, delta)
        self.position += self.velocity * delta
        self.updateImage(camPos)