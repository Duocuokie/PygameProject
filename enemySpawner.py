import pygame
from pygame.math import *
import random
from enemy import Enemy
from enemy1 import Enemy1
from enemy2 import Enemy2
from enemy3 import Enemy3

enemyList = [Enemy1, Enemy2, Enemy3]

class EnemySpawner():
    def __init__(self, event):
        self.time = 0
        self.capTime = 0
        self.entityCap = {
            0 : [5, 0, 0],
            10 : [12, 0, 0],
            25 : [7, 2, 0],
            35 : [10, 3, 0],
            50 : [7, 2, 1],
            60 : [10, 2, 5]
            }
        self.capKeys = self.entityCap.keys()
        self.entityCount = [0, 0, 0]
        self.event = event

    def spawn(self, pos, group):
        if self.time in self.capKeys:
            self.capTime = self.time
        caps = self.entityCap[self.capTime]
        for e in range(len(caps)):
            if self.entityCount[e] < caps[e]:
                randPos = Vector2(1000, 0).rotate(random.uniform(0, 360.0)) + pos
                newEnemy = enemyList[e](randPos, self.event)
                group.add(newEnemy)
                self.entityCount[e] += 1
        return group