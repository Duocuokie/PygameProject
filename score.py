import pygame
from pygame.locals import *
from pygame.math import *

#scoring object

class Score():
    def __init__(self, font, highscore):
        self.score = 0
        self.highscore = highscore
        self.combo = 0
        #float combo for more consistance calcuations
        self.fcombo = 0

        self.comboTime = 5000
        self.lastHit = 0

        self.font = font
        self.image = pygame.Surface((512, 128), SRCALPHA)
    
    #increases score based on combo
    def updateScore(self, newScore):
        self.score += int(newScore * (self.combo / 10 + 1))
        if self.score > self.highscore:
            self.highscore = self.score
        return self.highscore
    #increasaes combo
    def updateCombo(self):
        self.combo += 1
        self.fcombo = self.combo
        self.lastHit = pygame.time.get_ticks()

    def update(self, delta):
        #slowly lose combo
        if self.lastHit + self.comboTime <  pygame.time.get_ticks():
            self.fcombo = clamp(self.fcombo - (5 * delta), 0, 99999)
            self.combo = int(self.fcombo)

        #text
        self.image.fill((0, 0, 0, 0))

        highText = self.font.render(f"{self.highscore}", (255, 255, 255), size = 32)
        self.image.blit(highText[0], (496 - highText[1].width, 16))
        
        scoreText = self.font.render(f"{self.score}", (255, 255, 255), size = 48)
        self.image.blit(scoreText[0], (496 - scoreText[1].width, 44))
        
        comboText = self.font.render(f"x{self.combo}", (255, 255, 255), size = 32)
        self.image.blit(comboText[0], (496 - comboText[1].width, 96))
