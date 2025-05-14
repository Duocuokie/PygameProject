import pygame
from pygame.locals import *
from pygame.math import *



class Score():
    def __init__(self, font):
        self.score = 0
        self.combo = 0
        self.fcombo = 0

        self.comboTime = 5000
        self.lastHit = 0

        self.font = font
        self.image = pygame.Surface((512, 128), SRCALPHA)

    def updateScore(self, newScore):
        self.score += int(newScore * (self.combo / 10 + 1))

    def updateCombo(self):
        self.combo += 1
        self.fcombo = self.combo
        self.lastHit = pygame.time.get_ticks()

    def update(self, delta):
        if self.lastHit + self.comboTime <  pygame.time.get_ticks():
            self.fcombo = clamp(self.fcombo - (5 * delta), 0, 99999)
            print(self.fcombo)
            self.combo = int(self.fcombo)
        self.image.fill((0, 0, 0, 0))
        scoreText = self.font.render(f"Score : {self.score}", (255, 255, 255), size = 48)
        self.image.blit(scoreText[0], (496 - scoreText[1].width, 16))

        comboText = self.font.render(f"Combo : {self.combo}", (255, 255, 255), size = 32)
        self.image.blit(comboText[0], (496 - comboText[1].width, 64))
