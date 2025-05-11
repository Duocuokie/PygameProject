import pygame
from enemy import Enemy

enemyList = [Enemy]

class EnemySpawner():
    def __init__(self, event):
        self.time = 0
        self.entityCap = [10]
        self.entityCount = [0]
        self.event = event

    def spawn(self, pos, group):
        for e in range(len(self.entityCap)):
            if self.entityCount[e] < self.entityCap[e]:
                newEnemy = enemyList[e](pos, self.event)
                group.add(newEnemy)
                self.entityCount[e] += 1
        return group