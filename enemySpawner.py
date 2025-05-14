import pygame
from pygame.math import *
import random
from enemy import Enemy
from enemy1 import Enemy1
from enemy2 import Enemy2
from enemy3 import Enemy3
from enemy4 import Enemy4

enemyList = [Enemy1, Enemy2, Enemy3, Enemy4]

class EnemySpawner():
    def __init__(self, dieEvent, fireEvent):
        self.time = 70
        self.capTime = 0
        self.entityCap = {
            0 : [5, 0, 0, 0],
            10 : [12, 0, 0, 0],
            25 : [7, 2, 0, 0],
            35 : [10, 3, 0, 0],
            50 : [7, 2, 1, 0],
            60 : [10, 2, 5, 0],
            75 : [8, 2, 2, 1],
            85 : [9, 2, 1, 3],
            100 : [12, 3, 2, 3],
            120: [15, 3, 4, 4],
            140 : [16, 4, 5, 5],
            200 : [20, 5, 7, 7]
            }
        self.capKeys = self.entityCap.keys()
        self.entityCount = [0, 0, 0, 0]
        self.dieEvent = dieEvent
        self.fireEvent = fireEvent

    def spawn(self, pos, group):
        if self.time in self.capKeys:
            self.capTime = self.time
        caps = self.entityCap[self.capTime]
        for e in range(len(caps)):
            if self.entityCount[e] < caps[e]:
                randPos = Vector2(1000, 0).rotate(random.uniform(0, 360.0)) + pos
                if e != 3 :
                    newEnemy = enemyList[e](randPos, self.dieEvent)
                else:
                    newEnemy = enemyList[e](randPos, self.dieEvent, self.fireEvent)
                group.add(newEnemy)
                self.entityCount[e] += 1
        return group