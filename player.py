import pygame
from pygame.locals import *
from pygame.math import *
import math
from entity import Entity


PLAYERIMAGE = pygame.image.load("textures/Player.png")

class Player(Entity):
    def __init__(self, event):
        super().__init__()
        self.sprite = PLAYERIMAGE
        self.radius = 12

        self.direction = Vector2(0, 0)
        self.mouseDir = [0, 0]

        self.maxSpeed = 410
        self.acceleration = 2200
        self.friction = 1500

        self.hp = 20
        self.invincTime = 1000

        self.charge = 0
        self.dash = 0
        self.wasPressed = False

        self.event = event

    def applyAccel(self, dir, delta):
        speed = self.maxSpeed
        accel = self.acceleration
        if self.charge != 0 :
            accel = 900
            speed = clamp((speed - 200 - (self.charge**2)/4), 0, 99999) + 100
        self.velocity = self.velocity.move_towards(dir * speed,  accel * delta)



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
        if self.rect.center == pygame.mouse.get_pos():
            self.mouseDir = Vector2(1, 0)
        else:
            self.mouseDir = (Vector2(pygame.mouse.get_pos()) - Vector2(self.rect.center)).normalize()
        self.rotation = -math.degrees(math.atan2(self.mouseDir[1], self.mouseDir[0]))

        self.direction = Vector2(0, 0)
        self.direction[0] = int(keys[K_d]) - int(keys[K_a])
        self.direction[1] = int(keys[K_s]) - int(keys[K_w])

        

        if mouse[0]:
            self.charge += 15 * delta
            self.wasPressed = True
        else:
            if self.wasPressed:
                pygame.event.post(pygame.event.Event(self.event))
                self.dash = self.charge
                
            else:
                self.charge = 0
            self.wasPressed = False

        if self.dash > 10:
            #self.dash = clamp(self.dash - 18 * delta, 0, 600)
            self.dash *=0.97
            self.velocity = (self.mouseDir * -self.dash)*25 + self.direction * (self.maxSpeed - 100)

        if self.direction == [0, 0]:
            self.applyFriction(delta)
        else:
            self.direction = self.direction.normalize()
            self.applyAccel(self.direction, delta)

        self.position += self.velocity*delta


        self.updateImage(camPos)