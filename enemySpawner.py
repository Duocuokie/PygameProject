import pygame
from enemy import Enemy


class EnemySpawner():
    def __init__(self):
        self.time = 0
        self.entityCap = [10]
        self.entityCount = [0]

    def spawn(self, enemyId, pos, group):
        return group