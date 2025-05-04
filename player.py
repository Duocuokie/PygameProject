import pygame
from pygame.locals import *
from pygame.math import *
import math
from entity import Entity

PLAYERIMAGE = pygame.image.load("textures/Player.png")

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.position = Vector2(0, 0)

        self.sprite = PLAYERIMAGE
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.radius = 12
        self.direction = Vector2(0, 0)
        self.mouseDir = [0, 0]

        self.velocity = Vector2(0.0, 0.0)
        self.maxSpeed = 6
        self.acceleration = 60
        self.friction = 30

    def applyAccel(self, dir, delta):
        self.velocity = self.velocity.move_towards(dir * self.maxSpeed, self.acceleration * delta)


    def applyFriction(self, delta):
        self.velocity = self.velocity.move_towards(Vector2(0, 0), self.friction * delta)

    def update(self, camPos, delta):
        keys = pygame.key.get_pressed()
        self.direction = Vector2(0, 0)
        self.direction[0] = int(keys[K_d]) - int(keys[K_a])
        self.direction[1] = int(keys[K_s]) - int(keys[K_w])

        if self.direction == [0, 0]:
            self.applyFriction(delta)
        else:
            self.direction = self.direction.normalize()
            self.applyAccel(self.direction, delta)


        self.position += self.velocity


        self.mouseDir = (Vector2(pygame.mouse.get_pos()) - Vector2(self.rect.center))
        self.rotation = -math.degrees(math.atan2(self.mouseDir[1], self.mouseDir[0]))
        self.updateImage(camPos)