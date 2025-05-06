import pygame
from pygame.locals import *
from pygame.math import *
import math
from entity import Entity


PLAYERIMAGE = pygame.image.load("textures/Player.png")

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.sprite = PLAYERIMAGE
        self.radius = 12

        self.direction = Vector2(0, 0)
        self.mouseDir = [0, 0]

        self.maxSpeed = 400
        self.acceleration = 2900
        self.friction = 1700

        self.hp = 2000000
        self.invincTime = 1000

        self.charge = 0
        self.wasPressed = False

        self.event = None

    def applyAccel(self, dir, delta):
        self.velocity = self.velocity.move_towards(dir * self.maxSpeed, self.acceleration * delta)


    def applyFriction(self, delta):
        self.velocity = self.velocity.move_towards(Vector2(0, 0), self.friction * delta)

    def damage(self, dmg, damager):
        if self.lastHitTime + self.invincTime < pygame.time.get_ticks():
            pygame.time.wait(50)
            self.lastHitTime = pygame.time.get_ticks()
            self.hp = clamp(self.hp -  dmg, 0, 99999)
            dmgDir = Vector2(damager.position - self.position).normalize()
            print(dmgDir)
            self.velocity += dmgDir * -damager.kb * self.kbResist
            
        if self.hp == 0: 
           
            self.die()

    def update(self, camPos, delta):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        self.direction = Vector2(0, 0)
        self.direction[0] = int(keys[K_d]) - int(keys[K_a])
        self.direction[1] = int(keys[K_s]) - int(keys[K_w])

        

        if self.direction == [0, 0]:
            self.applyFriction(delta)
        else:
            self.direction = self.direction.normalize()
            self.applyAccel(self.direction, delta)

        if mouse[0]:
            self.charge += 10 * delta
            self.wasPressed = True
        else:
            if self.wasPressed:
                pygame.event.post(pygame.event.Event(self.event))
            else:
                self.charge = 0
            self.wasPressed = False

        self.position += self.velocity*delta


        self.mouseDir = (Vector2(pygame.mouse.get_pos()) - Vector2(self.rect.center))
        self.rotation = -math.degrees(math.atan2(self.mouseDir[1], self.mouseDir[0]))
        self.updateImage(camPos)