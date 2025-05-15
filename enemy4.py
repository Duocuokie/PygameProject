import pygame
from pygame.locals import *
from pygame.math import *
from enemy import Enemy
from enemyProj1 import EnemyProj1

#shoots projectiles at player

class Enemy4(Enemy):
    def __init__(self, pos, event, fireEvent):
        super().__init__(pos, event)
        self.id = 3

        self.sprite = pygame.Surface((32, 32))
        self.sprite.fill((190, 20, 210))
        self.radius = 12

        self.cooldown = 1750
        self.lastFire = 0

        self.score = 20
        
        self.maxSpeed = 400
        self.acceleration = 2000
        self.friction = 2000
        self.hp = 25
        #for when to fire a projectile
        self.fireEvent = fireEvent
        self.kb = 900

    def update(self, camPos, playerPos, delta):
        if Vector2(self.rect.center).distance_squared_to(playerPos) > 40000:
            self.findPlayer(playerPos)
            self.applyAccel(self.direction, delta)
        #only fires when off cooldown
        elif self.lastFire + self.cooldown < pygame.time.get_ticks():
            self.applyFriction(delta)
            self.lastFire = pygame.time.get_ticks()
            pygame.event.post(pygame.event.Event(self.fireEvent, {"enemy": self}))
        else:
            self.applyFriction(delta)
            
        self.position += self.velocity * delta
        self.updateImage(camPos)
