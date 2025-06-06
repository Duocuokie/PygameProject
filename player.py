import pygame
from pygame.locals import *
from pygame.math import *
import math
from entity import Entity
import audio

PLAYERIMAGE = pygame.image.load("textures/Player.png")

#player object

class Player(Entity):
    def __init__(self, event):
        super().__init__()
        self.sprite = PLAYERIMAGE
        self.radius = 12
        

        self.direction = Vector2(0, 0)
        self.mouseDir = [0, 0]

        self.maxSpeed = 350
        self.acceleration = 2300
        self.friction = 1400

        self.hp = 50
        self.invincTime = 1000
        self.shield = None

        self.charge = 0
        self.dash = 0
        self.wasPressed = False

        self.event = event

    #accelerates player to max speed
    def applyAccel(self, dir, delta):
        speed = self.maxSpeed
        accel = self.acceleration
        #slows when charging
        if self.charge != 0 :
            accel = 900
            speed = clamp((speed - 200 - (self.charge**2)/4), 0, 99999) + 120
        self.velocity = self.velocity.move_towards(dir * speed,  accel * delta)


    #stops player
    def applyFriction(self, delta):
        self.velocity = self.velocity.move_towards(Vector2(0, 0), self.friction * delta)

    #hurts player
    def damage(self, dmg, damager):
        if self.dash < 20:
            if self.lastHitTime + self.invincTime < pygame.time.get_ticks():
                audio.SfxObjs[2].play()
                pygame.time.wait(50)
                self.lastHitTime = pygame.time.get_ticks()
                self.hp = clamp(self.hp -  dmg, 0, 99999)
                dmgDir = Vector2(damager.position - self.position).normalize()
                self.velocity += dmgDir * -damager.kb * self.kbResist
                self.charge = 0
                
        if self.hp == 0: 
            audio.SfxObjs[3].play()
            self.die()



    def update(self, camPos, delta):
        #gets input
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if self.rect.center == pygame.mouse.get_pos():
            self.mouseDir = Vector2(1, 0)
        else:
            #rotate to mouse
            self.mouseDir = (Vector2(pygame.mouse.get_pos()) - Vector2(self.rect.center)).normalize()
        self.rotation = -math.degrees(math.atan2(self.mouseDir[1], self.mouseDir[0]))

        self.direction = Vector2(0, 0)
        self.direction[0] = int(keys[K_d]) - int(keys[K_a])
        self.direction[1] = int(keys[K_s]) - int(keys[K_w])

        
        #charging and attacking
        if mouse[0]:
            self.charge += 20 * delta
            if not self.wasPressed:
                audio.SfxObjs[0].play()
            self.wasPressed = True
        else:
            #release
            if self.wasPressed:
                self.dash = self.charge
                audio.SfxObjs[0].stop()
                audio.SfxObjs[1].play()
                pygame.event.post(pygame.event.Event(self.event))
                
            else:
                self.charge = 0
            self.wasPressed = False

        #increasing size
        self.scale = [1 + self.charge/32, 1 + self.charge/32]
        self.radius = 12 * self.scale[0]

        #pushed player away from mouse
        if self.dash > 5:
            self.dash *= 1 - 2 * delta
            self.velocity = (self.mouseDir * -self.dash)*22 + self.direction * (self.maxSpeed - 100)
 

        #move direction
        if self.direction == [0, 0]:
            self.applyFriction(delta)
        else:
            self.direction = self.direction.normalize()
            self.applyAccel(self.direction, delta)

        self.position += self.velocity*delta


        self.updateImage(camPos)