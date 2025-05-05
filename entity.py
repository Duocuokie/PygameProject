import pygame
from pygame.locals import *
from pygame.math import *
from gameObject import GameObject

#class for entities like players and eneies

class Entity(GameObject):
    def __init__(self):
        super().__init__()
        self.hp = 10
        self.atk = 10
        self.kbResist = 1
        self.layer = 0

        self.velocity = Vector2(0.0, 0.0)



    def damage(self, dmg, damager):
        self.hp = clamp(self.hp -  dmg, 0, 99999)
        dmgDir = Vector2(damager.position - self.position).normalize()
        print(dmgDir)
        self.velocity += dmgDir * -500 * self.kbResist
        
        if self.hp == 0: 
           
            self.die()

    def die(self):
        self.kill()


    def update(self, camPos, delta):
        self.updateImage(camPos)